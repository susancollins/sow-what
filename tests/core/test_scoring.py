from sow_what.core.scoring import Weights, score_layout


class TestScoring:
    def test_score_layout_returns_zero_for_empty_grid(self):
        grid = [[]]
        catalog = {}
        score, breakdown = score_layout(grid, catalog)
        assert score == 0
        assert all(v == 0 for v in breakdown.values())

    def test_score_layout_handles_single_plant(self):
        grid = [[1]]
        catalog = {"1": {"family": "A", "companions": [], "antagonists": []}}
        score, breakdown = score_layout(grid, catalog)
        assert score == 0
        assert all(v == 0 for v in breakdown.values())

    def test_score_layout_applies_companion_bonus_for_adjacent_cells(self):
        grid = [[1, 2], [None, 3]]
        catalog = {
            "1": {"family": "A", "companions": [2], "antagonists": []},
            "2": {"family": "A", "companions": [1], "antagonists": []},
            "3": {"family": "B", "companions": [], "antagonists": [1]},
        }
        score, breakdown = score_layout(grid, catalog)
        assert score > 0
        assert breakdown["companions"] > 0
        assert breakdown["antagonists"] == 0
        assert breakdown["rotation_overlap"] == 0

    def test_score_layout_applies_antagonist_penalty_for_adjacent_cells(self):
        grid = [[1, 3], [None, None]]
        catalog = {
            "1": {"family": "A", "companions": [], "antagonists": [3]},
            "3": {"family": "B", "companions": [], "antagonists": [1]},
        }
        score, breakdown = score_layout(grid, catalog)
        assert score < 0
        assert breakdown["companions"] == 0
        assert breakdown["antagonists"] < 0
        assert breakdown["rotation_overlap"] == 0

    def test_score_layout_applies_rotation_penalty_for_same_family_overlap(self):
        grid = [[1, None], [None, None]]
        last = [[2, None], [None, None]]
        catalog = {
            "1": {"family": "A", "companions": [], "antagonists": []},
            "2": {"family": "A", "companions": [], "antagonists": []},
        }
        score, breakdown = score_layout(grid, catalog, last=last)
        assert score < 0
        assert breakdown["companions"] == 0
        assert breakdown["antagonists"] == 0
        assert breakdown["rotation_overlap"] < 0

    def test_score_layout_higher_weights_increase_score(self):
        grid = [[1, 2], [None, 3]]
        last = [[2, None], [None, None]]
        catalog = {
            "1": {"family": "A", "companions": [2], "antagonists": []},
            "2": {"family": "A", "companions": [1], "antagonists": []},
            "3": {"family": "B", "companions": [], "antagonists": [1]},
        }
        weights = Weights()
        weights.w_companion = 3.0
        weights.w_antagonist = 4.0
        weights.w_rotation_overlap = 2.0
        score, breakdown = score_layout(grid, catalog, last=last, weights=weights)
        assert score > 0
        assert breakdown["companions"] > 0
        assert breakdown["antagonists"] == 0
        assert breakdown["rotation_overlap"] == 0

    def test_score_layout_handles_rectangular_grids_without_error(self):
        grid = [[1, 2, 3], [None, None, None]]
        catalog = {
            "1": {"family": "A", "companions": [2], "antagonists": []},
            "2": {"family": "A", "companions": [1], "antagonists": []},
            "3": {"family": "B", "companions": [], "antagonists": [1]},
        }
        score, breakdown = score_layout(grid, catalog)
        assert score > 0
        assert breakdown["companions"] > 0
        assert breakdown["antagonists"] == 0
        assert breakdown["rotation_overlap"] == 0

    def test_score_layout_is_orientation_invariant_for_companion_pair():
        base_grid = [[1, 2], [None, None]]
        rotated_grid = [[None, 1], [None, 2]]
        flipped_grid = [[2, 1], [None, None]]

        catalog = {
            "1": {"family": "A", "companions": [2], "antagonists": []},
            "2": {"family": "A", "companions": [1], "antagonists": []},
        }
        base_score, _ = score_layout(base_grid, catalog)
        rotated_score, _ = score_layout(rotated_grid, catalog)
        flipped_score, _ = score_layout(flipped_grid, catalog)
        assert base_score == rotated_score == flipped_score

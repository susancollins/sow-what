from typing import Optional

from .types import Catalog, Grid, Score


class Weights:
    w_companion = 2.0
    w_antagonist = 3.0
    w_rotation_overlap = 5.0
    w_rotation_proximity = 1.5
    radius = 1  # num of cells


def score_layout(
    grid: Grid, catalog: Catalog, last: Optional[Grid] = None, weights: Weights = Weights()
) -> Score:
    """
    Compute the total score of a garden layout and return a breakdown.

    The scoring function evaluates:
      * companion bonuses for adjacent plants,
      * antagonist penalties for adjacent plants, and
      * rotation penalties when the same family occupies the same cell as last season.

    Parameters
    ----------
    grid : list[list[int | None]]
        Current-season layout as a 2D grid of plant IDs (or ``None`` for empty cells).
    catalog : dict[str, dict]
        Plant metadata keyed by plant ID (as string). Each entry should define:
        ``family`` (str), ``companions`` (list[int]), and ``antagonists`` (list[int]).
    last : list[list[int | None]], optional
        Previous-season layout, same shape as ``grid``. Used for crop-rotation penalties.
    w : Weights, optional
        Scoring weights container. If ``None``, default weights are used.

    Returns
    -------
    total_score : float
        Overall score for the layout.
    breakdown : dict[str, float]
        Score contributions by category. Possible keys include:
        ``"companions"``, ``"antagonists"``, ``"rotation_overlap"``.
    """
    raise NotImplementedError

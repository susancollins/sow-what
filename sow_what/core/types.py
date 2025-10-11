from typing import Dict, List, Optional, Tuple, TypedDict


class CatalogEntry(TypedDict):
    family: str
    companions: List[int]
    antagonists: List[int]


Catalog = Dict[str, CatalogEntry]
Grid = List[List[Optional[int]]]
Breakdown = Dict[str, float]
Score = Tuple[float, Breakdown]

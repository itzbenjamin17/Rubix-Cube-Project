from Cubie import Cubie
from typing import Dict


class Edge(Cubie):
    def __init__(self, x: int, y: int, z: int, colours: Dict[str, tuple]) -> None:
        super().__init__(x, y, z, colours)

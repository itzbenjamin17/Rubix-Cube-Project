from typing import Tuple


class Face:
    def __init__(self, colour: Tuple[float, float, float], name: str) -> None:
        self.colour = colour
        self.name = name

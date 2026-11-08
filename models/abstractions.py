from abc import ABC
from dataclasses import dataclass
from enum import Enum


class TileType(Enum):
    Quad = "quad"
    Hex = "hex"


class GroundType(Enum):
    Plain = "plain"
    Wall = "wall"
    Water = "water"
    Home = "home"


class ResourcesType(Enum):
    Food = "food"
    Stuff = "stuff"
    Poison = "poison"


class PlayerType(Enum):
    Scrapper = "scrapper"
    Beast = "beast"


class Resource(ABC): ...


class Player(ABC): ...


class Ground(ABC):
    type: GroundType
    resources: list[Resource]
    occupants: list[Player]
    neighbors: list[Ground]


@dataclass
class WorldConfig:
    tile_type: TileType
    columns: int
    rows: int
    player_count: int
    speed: float  # frames per second



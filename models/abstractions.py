from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
import random


class GroundType(Enum):
    Plain = "plain"
    Wall = "wall"
    Water = "water"
    Home = "home"


class Direction(Enum):
    North = "north"
    North_East = "north_east"
    East = "east"
    South_East = "south_east"
    South = "south"
    South_West = "south_west"
    West = "west"
    North_West = "north_west"


class ResourcesType(Enum):
    Food = "food"
    Stuff = "stuff"
    Poison = "poison"


class Clamped:
    def __init__(self, default: float = 1.0) -> None:
        self.default = default

    def __set_name__(self, owner: type, name: str) -> None:
        self.attr = f"_{name}"

    def __get__(self, obj: object, owner: type | None = None) -> float:
        if obj is None:
            return self.default
        return getattr(obj, self.attr, self.default)

    def __set__(self, obj: object, value: float) -> None:
        setattr(obj, self.attr, min(1.0, max(0.0, value)))


class PlayerDecision(Enum):

    Rest = "rest"
    Attack = "attack"
    Collect_Resource = "collect_resource"

    Go_North = "go_north"
    Go_North_East = "go_north_east"
    Go_East = "go_east"
    Go_South_East = "go_south_east"
    Go_South = "go_south"
    Go_South_West = "go_south_west"
    Go_West = "go_west"
    Go_North_West = "go_north_west"


class PlayerType(Enum):
    Scrapper = "scrapper"
    Beast = "beast"


class PlayerState(Enum):
    Normal = "normal"
    Sleeping = "sleeping"
    Dead = "dead"


class Resource(ABC): ...


class Player(ABC):

    stamina: Clamped
    health: Clamped
    happiness: Clamped
    fullness: Clamped

    @abstractmethod
    def make_decision(
        self, current_ground: Ground, surroundings: dict[Direction, Ground]
    ) -> PlayerDecision: ...


class Ground(ABC):
    resources: list[Resource]

    def add_resource(self, resource: Resource) -> None:
        self.resources.append(resource)

    def get_resource(self) -> Resource | None:
        if not self.resources:
            return None
        return self.resources.pop(random.randrange(len(self.resources)))


@dataclass
class WorldConfig:
    columns: int
    rows: int
    player_count: int
    speed: float  # frames per second

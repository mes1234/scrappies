import random

from models.abstractions import Ground, GroundType


def generate_ground_item(row: int, column: int, existing: list[Ground]) -> Ground:
    picked = random.choice(list(GroundType))

    if picked == GroundType.Water:
        return WaterGround()
    if picked == GroundType.Wall:
        return WallGround()
    if picked == GroundType.Home:
        return HomeGround()
    if picked == GroundType.Plain:
        return PlainGround()


def arrange_in_pattern(
    grounds: list[Ground],
    rows: int,
    columns: int,
) -> list[Ground]:
    if len(grounds) != rows * columns:
        raise ValueError("grounds must contain exactly rows * columns items")

    for row in range(rows):
        for column in range(columns):
            neighbors: list[Ground] = []
            offsets = ((-1, 0), (0, 1), (1, 0), (0, -1))

            for row_offset, column_offset in offsets:
                neighbor_row = (row + row_offset) % rows
                neighbor_column = (column + column_offset) % columns
                neighbor = grounds[neighbor_row * columns + neighbor_column]
                if (
                    neighbor is not grounds[row * columns + column]
                    and neighbor not in neighbors
                ):
                    neighbors.append(neighbor)

            grounds[row * columns + column].neighbors = neighbors

    return grounds


class PlainGround(Ground):
    def __init__(self) -> None:
        super().__init__()
        self.type = GroundType.Plain


class WallGround(Ground):
    def __init__(self) -> None:
        super().__init__()
        self.type = GroundType.Wall


class WaterGround(Ground):
    def __init__(self) -> None:
        super().__init__()
        self.type = GroundType.Water


class HomeGround(Ground):
    def __init__(self) -> None:
        super().__init__()
        self.type = GroundType.Home

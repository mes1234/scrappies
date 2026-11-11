import random

from models.abstractions import Ground, GroundType

HOME_COLUMN_RATIO = 0.2
WALL_CLUSTER_COUNT = 12
WALL_MIN_LENGTH = 3
WALL_MAX_LENGTH = 5


def _home_columns(columns: int) -> tuple[int, int]:
    offset = int(columns * HOME_COLUMN_RATIO)
    return offset, columns - 1 - offset


def _river_columns(columns: int) -> range:
    width = max(1, columns // 10)
    start = (columns - width) // 2
    return range(start, start + width)


def _is_free_for_wall(row: int, column: int, rows: int, columns: int) -> bool:
    if column in _river_columns(columns):
        return False
    return not (
        row == rows // 2 and any(abs(column - c) <= 1 for c in _home_columns(columns))
    )


def generate_wall_cells(rows: int, columns: int) -> set[tuple[int, int]]:
    """Place straight wall segments, each at least WALL_MIN_LENGTH tiles long."""
    walls: set[tuple[int, int]] = set()

    for _ in range(WALL_CLUSTER_COUNT):
        for _attempt in range(50):
            length = random.randint(WALL_MIN_LENGTH, WALL_MAX_LENGTH)
            d_row, d_column = random.choice(((0, 1), (1, 0)))
            row = random.randrange(rows)
            column = random.randrange(columns)
            cells = [(row + i * d_row, column + i * d_column) for i in range(length)]
            if all(
                r < rows
                and c < columns
                and (r, c) not in walls
                and _is_free_for_wall(r, c, rows, columns)
                for r, c in cells
            ):
                walls.update(cells)
                break

    return walls


def generate_ground_item(
    row: int,
    column: int,
    existing: list[Ground],
    rows: int,
    columns: int,
    walls: set[tuple[int, int]],
) -> Ground:
    home_row = rows // 2

    if row == home_row and column in _home_columns(columns):
        return HomeGround()

    if column in _river_columns(columns):
        # Leave a ford at home row so both sides stay connected.
        return PlainGround() if row == home_row else WaterGround()

    if (row, column) in walls:
        return WallGround()

    return PlainGround()


class PlainGround(Ground):

    MAX_RESOURCE = 10

    def __init__(self) -> None:
        super().__init__()
        self.type = GroundType.Plain
        self._wilderness = 0.5

    @property
    def wealth(self) -> float:
        w = len(self.resources) / self.MAX_RESOURCE + random.uniform(-0.1, 0.1)

        if w > 1.0:
            return 1.0
        if w < 0.0:
            return 0.0
        return w


class WallGround(Ground):
    def __init__(self) -> None:
        super().__init__()
        self.type = GroundType.Wall
        self._wilderness = 1.0

    @property
    def wealth(self) -> float:
        return 0.0


class WaterGround(Ground):

    MAX_RESOURCE = 10

    def __init__(self) -> None:
        super().__init__()
        self.type = GroundType.Water

    @property
    def wealth(self) -> float:
        w = len(self.resources) / self.MAX_RESOURCE + random.uniform(-0.1, 0.1)

        if w > 1.0:
            return 1.0
        if w < 0.0:
            return 0.0
        return w


class HomeGround(Ground):

    MAX_RESOURCE = 100

    def __init__(self) -> None:
        super().__init__()
        self.type = GroundType.Home
        self._wilderness = 0.0

    @property
    def wealth(self) -> float:
        w = len(self.resources) / self.MAX_RESOURCE + random.uniform(-0.1, 0.1)

        if w > 1.0:
            return 1.0
        if w < 0.0:
            return 0.0
        return w

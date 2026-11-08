from models.abstractions import Ground, GroundType, TileType


def generate_ground_item(row: int, column: int, existing: list[Ground]) -> Ground:
    return PlainGround()


def arrange_in_pattern(
    tile_type: TileType,
    grounds: list[Ground],
    rows: int,
    columns: int,
) -> list[Ground]:
    if len(grounds) != rows * columns:
        raise ValueError("grounds must contain exactly rows * columns items")

    for row in range(rows):
        for column in range(columns):
            neighbors: list[Ground] = []
            if tile_type is TileType.Quad:
                offsets = ((-1, 0), (0, 1), (1, 0), (0, -1))
            else:
                if row % 2 == 0:
                    offsets = (
                        (-1, -1),
                        (-1, 0),
                        (0, 1),
                        (1, 0),
                        (1, -1),
                        (0, -1),
                    )
                else:
                    offsets = (
                        (-1, 0),
                        (-1, 1),
                        (0, 1),
                        (1, 1),
                        (1, 0),
                        (0, -1),
                    )

            for row_offset, column_offset in offsets:
                neighbor_row = row + row_offset
                if not 0 <= neighbor_row < rows or columns == 0:
                    continue

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


class HomeGround(Ground):
    def __init__(self) -> None:
        super().__init__()
        self.type = GroundType.Home

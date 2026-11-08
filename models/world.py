from models.abstractions import Ground, Player, WorldConfig
from models.grounds import arrange_in_pattern, generate_ground_item


class World:
    grounds: list[Ground]
    players: list[Player]
    time: int

    def __init__(self, config: WorldConfig) -> None:
        self.config = config

    def _bootstrap_ground(self) -> list[Ground]:
        grounds: list[Ground] = []

        for row in range(self.config.rows):
            for column in range(self.config.columns):
                ground_item = generate_ground_item(
                    row=row, column=column, existing=grounds
                )
                grounds.append(ground_item)

        return arrange_in_pattern(
            tile_type=self.config.tile_type,
            grounds=grounds,
            rows=self.config.rows,
            columns=self.config.columns,
        )

    def _bootstrap(self) -> None: ...

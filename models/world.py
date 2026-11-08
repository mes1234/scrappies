from models.abstractions import Ground, Player, WorldConfig
from models.grounds import arrange_in_pattern, generate_ground_item


class World:
    __grounds: list[Ground]
    __players: list[Player]
    __time: int

    def __init__(self, config: WorldConfig) -> None:
        self.config = config
        self.__bootstrap()

    @property
    def grounds(self) -> list[Ground]:
        return self.__grounds

    def __bootstrap_ground(self) -> list[Ground]:
        grounds: list[Ground] = []

        for row in range(self.config.rows):
            for column in range(self.config.columns):
                ground_item = generate_ground_item(
                    row=row, column=column, existing=grounds
                )
                grounds.append(ground_item)

        return arrange_in_pattern(
            grounds=grounds,
            rows=self.config.rows,
            columns=self.config.columns,
        )

    def __bootstrap(self) -> None:
        self.__grounds = self.__bootstrap_ground()

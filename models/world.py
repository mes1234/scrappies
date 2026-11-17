from models.abstractions import Ground, Player, Position, WorldConfig
from models.grounds import (
    generate_ground_item,
    generate_wall_cells,
)
from models.players import Scrapper


class World:
    __grounds: list[Ground]
    __players: list[tuple[Player, Position]]  # player row col
    __time: int

    def __init__(self, config: WorldConfig) -> None:
        self.config = config
        self.__bootstrap()

    @property
    def grounds(self) -> list[Ground]:
        return self.__grounds

    @property
    def players(self) -> list[tuple[Player, Position]]:
        return self.__players

    def __bootstrap_ground(self) -> list[Ground]:
        grounds: list[Ground] = []
        walls = generate_wall_cells(self.config.rows, self.config.columns)

        for row in range(self.config.rows):
            for column in range(self.config.columns):
                ground_item = generate_ground_item(
                    row=row,
                    column=column,
                    existing=grounds,
                    rows=self.config.rows,
                    columns=self.config.columns,
                    walls=walls,
                )
                grounds.append(ground_item)

        return grounds

    def __bootstrap_players(self) -> list[tuple[Player, Position]]:
        player_1 = Scrapper()
        player_2 = Scrapper()
        return [(player_1, Position(0, 1)), (player_2, Position(0, 2))]

    def __bootstrap(self) -> None:
        self.__grounds = self.__bootstrap_ground()
        self.__players = self.__bootstrap_players()

import random
from time import monotonic

from models.abstractions import (
    Direction,
    Ground,
    Player,
    PlayerDecision,
    Position,
    WorldConfig,
)
from models.grounds import (
    WallGround,
    WaterGround,
    generate_ground_item,
    generate_wall_cells,
)
from models.players import Beast, Scrapper


class World:
    BEAST_SPAWN_INTERVAL = 10.0

    __grounds: list[Ground]
    __players: list[tuple[Player, Position]]  # player row col
    __time: int

    def __init__(self, config: WorldConfig) -> None:
        self.config = config
        self.__bootstrap()
        self.__decisions: dict[Player, list[PlayerDecision]] = {
            player: [] for player, _ in self.__players
        }
        self.__next_beast_spawn = monotonic() + self.BEAST_SPAWN_INTERVAL

    def step(self) -> None:
        for index, (player, position) in enumerate(self.__players):
            surroundings = self.__get_player_context(position)
            player_decision = player.make_decision(surroundings)
            history = self.__decisions.setdefault(player, [])
            history.append(player_decision)
            del history[:-10]
            new_position = self.__evaluate_player_decision(position, player_decision)
            self.__players[index] = (player, new_position)

        if monotonic() >= self.__next_beast_spawn:
            positions = [
                Position(*divmod(index, self.config.columns))
                for index, ground in enumerate(self.__grounds)
                if not isinstance(ground, (WallGround, WaterGround))
            ]
            if not positions:
                raise RuntimeError("Cannot spawn a beast: map has no passable tiles")
            beast = Beast()
            self.__players.append((beast, random.choice(positions)))
            self.__decisions[beast] = []
            self.__next_beast_spawn += self.BEAST_SPAWN_INTERVAL

    @property
    def grounds(self) -> list[Ground]:
        return self.__grounds

    @property
    def players(self) -> list[tuple[Player, Position]]:
        return self.__players

    @property
    def decision(self) -> dict[Player, list[PlayerDecision]]:
        return self.__decisions

    def __evaluate_player_decision(
        self, current_position: Position, player_decision: PlayerDecision
    ) -> Position:
        """
        based on current position and player decision return new player position
        NOTICE: currently only movement is implemented
        Player cannot move through wall or water
        """
        offsets = {
            PlayerDecision.Go_North: (-1, 0),
            PlayerDecision.Go_North_East: (-1, 1),
            PlayerDecision.Go_East: (0, 1),
            PlayerDecision.Go_South_East: (1, 1),
            PlayerDecision.Go_South: (1, 0),
            PlayerDecision.Go_South_West: (1, -1),
            PlayerDecision.Go_West: (0, -1),
            PlayerDecision.Go_North_West: (-1, -1),
        }
        offset = offsets.get(player_decision)
        if offset is None:
            return current_position

        row = (current_position.row + offset[0]) % self.config.rows
        column = (current_position.col + offset[1]) % self.config.columns
        destination = self.__grounds[row * self.config.columns + column]
        if isinstance(destination, (WallGround, WaterGround)):
            return current_position

        return Position(row, column)

    def __get_player_context(
        self, position: Position
    ) -> dict[Direction, tuple[Ground, list[Player]]]:
        rows = self.config.rows
        columns = self.config.columns
        row = position.row % rows
        column = position.col % columns

        offsets = {
            Direction.Here: (0, 0),
            Direction.North: (-1, 0),
            Direction.North_East: (-1, 1),
            Direction.East: (0, 1),
            Direction.South_East: (1, 1),
            Direction.South: (1, 0),
            Direction.South_West: (1, -1),
            Direction.West: (0, -1),
            Direction.North_West: (-1, -1),
        }
        surroundings: dict[Direction, tuple[Ground, list[Player]]] = {}
        for direction, (row_offset, column_offset) in offsets.items():
            neighbor_row = (row + row_offset) % rows
            neighbor_column = (column + column_offset) % columns
            ground = self.__grounds[neighbor_row * columns + neighbor_column]
            players = [
                player
                for player, player_position in self.__players
                if player_position.row % rows == neighbor_row
                and player_position.col % columns == neighbor_column
            ]
            surroundings[direction] = (ground, players)
        return surroundings

    def __bootstrap_ground(self) -> list[Ground]:
        grounds: list[Ground] = []
        walls = generate_wall_cells(self.config.rows, self.config.columns)

        for row in range(self.config.rows):
            for column in range(self.config.columns):
                if row in (0, self.config.rows - 1) or column in (
                    0,
                    self.config.columns - 1,
                ):
                    grounds.append(WallGround())
                    continue
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
        positions = [
            Position(row, column)
            for row in range(1, self.config.rows - 1)
            for column in range(1, self.config.columns - 1)
            if not isinstance(
                self.__grounds[row * self.config.columns + column],
                (WallGround, WaterGround),
            )
        ]
        if not positions:
            raise ValueError("Cannot place players: map has no passable interior tiles")

        player_1 = Scrapper("A")
        player_2 = Scrapper("B")
        second = positions[1 % len(positions)]
        return [
            (player_1, positions[0]),
            (player_2, Position(second.row, second.col)),
        ]

    def __bootstrap(self) -> None:
        self.__grounds = self.__bootstrap_ground()
        self.__players = self.__bootstrap_players()

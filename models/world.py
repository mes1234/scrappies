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
from models.game_rules import GameRules
from models.grounds import (
    HomeGround,
    WallGround,
    WaterGround,
    generate_ground_item,
    generate_wall_cells,
)
from models.players import Beast, Scrapper
from models.resources import FoodResource


class World:
    BEAST_SPAWN_INTERVAL = 10.0
    MAX_BEASTS = 5
    RESOURCE_CHANCE = 0.1

    __grounds: list[Ground]
    __players: list[Player]
    __time: int

    def __init__(self, config: WorldConfig) -> None:
        self.config = config
        self.__grounds = self.__bootstrap_ground()
        self.__players = self.__bootstrap_players()
        self.__decisions: dict[Player, list[PlayerDecision]] = {
            player: [] for player in self.__players
        }
        self.__next_beast_spawn = monotonic() + self.BEAST_SPAWN_INTERVAL

    def step(self) -> None:
        for player in self.__players:
            surroundings = self.__get_player_context(player.position)
            player_decision = player.make_decision(surroundings)
            history = self.__decisions.setdefault(player, [])
            history.append(player_decision)
            del history[:-10]
            self.__evaluate_player_decision(
                player, player_decision
            )

        if monotonic() >= self.__next_beast_spawn:
            beast_count = sum(
                isinstance(player, Beast) for player in self.__players
            )
            if beast_count < self.MAX_BEASTS:
                positions = [
                    Position(*divmod(index, self.config.columns))
                    for index, ground in enumerate(self.__grounds)
                    if not isinstance(ground, (WallGround, WaterGround))
                ]
                if not positions:
                    raise RuntimeError("Cannot spawn a beast: map has no passable tiles")
                beast = Beast()
                beast.position = random.choice(positions)
                self.__players.append(beast)
                self.__decisions[beast] = []
            self.__next_beast_spawn += self.BEAST_SPAWN_INTERVAL

    @property
    def grounds(self) -> list[Ground]:
        return self.__grounds

    @property
    def players(self) -> list[Player]:
        return self.__players

    @property
    def decision(self) -> dict[Player, list[PlayerDecision]]:
        return self.__decisions

    def __evaluate_player_decision(
        self,
        player: Player,
        player_decision: PlayerDecision,
    ) -> None:
        """
        Evaluate a player decision using the player's position.
        Player cannot move through wall or water
        """
        game_rules = GameRules()
        other_players_in_position = self.__get_other_players_in_position(
            player
        )
        return game_rules.evaluate_player_decision(
            self.grounds,
            self.config,
            player,
            player_decision,
            other_players_in_position,
        )

    def __get_other_players_in_position(
        self, player: Player
    ) -> list[Player]:
        rows = self.config.rows
        columns = self.config.columns
        row = player.position.row % rows
        column = player.position.col % columns
        return [
            other_player
            for other_player in self.__players
            if other_player is not player
            and other_player.position.row % rows == row
            and other_player.position.col % columns == column
        ]

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
                for player in self.__players
                if player.position.row % rows == neighbor_row
                and player.position.col % columns == neighbor_column
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
                if not isinstance(ground_item, (WallGround, WaterGround)):
                    if random.random() < self.RESOURCE_CHANCE:
                        ground_item.add_resource(FoodResource(random.random()))
                grounds.append(ground_item)

        return grounds

    def __bootstrap_players(self) -> list[Player]:
        home_positions = [
            Position(row, column)
            for row in range(self.config.rows)
            for column in range(self.config.columns)
            if isinstance(
                self.__grounds[row * self.config.columns + column], HomeGround
            )
        ]
        if len(home_positions) < 2:
            raise ValueError("Cannot place players: map must have two home tiles")

        player_1 = Scrapper("A")
        player_2 = Scrapper("B")
        player_1.position = home_positions[0]
        player_2.position = home_positions[1]
        return [player_1, player_2]

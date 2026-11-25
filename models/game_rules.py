from models.abstractions import Ground, Player, PlayerDecision, Position, WorldConfig
from models.grounds import WallGround, WaterGround


class GameRules:
    def evaluate_player_decision(
        self,
        grounds: list[Ground],
        config: WorldConfig,
        player: Player,
        player_decision: PlayerDecision,
        player_in_position: list[Player],
    ) -> None:
        match player_decision:
            case PlayerDecision.Rest:
                self.__evaluate_rest(player)
            case PlayerDecision.Attack:
                self.__evaluate_attack(player, player_in_position)
            case PlayerDecision.Collect_Resource:
                row = player.position.row % config.rows
                column = player.position.col % config.columns
                current_ground = grounds[row * config.columns + column]
                self.__evaluate_collect_resource(player, current_ground)
            case (
                PlayerDecision.Go_North
                | PlayerDecision.Go_North_East
                | PlayerDecision.Go_East
                | PlayerDecision.Go_South_East
                | PlayerDecision.Go_South
                | PlayerDecision.Go_South_West
                | PlayerDecision.Go_West
                | PlayerDecision.Go_North_West
            ):
                self.__evaluate_movement(
                    grounds,
                    config,
                    player,
                    player_decision,
                )
            case _:
                raise ValueError(f"Unsupported player decision: {player_decision}")

    def __evaluate_rest(self, player: Player) -> None:
        # Placeholder for future rest implementation.
        return

    def __evaluate_attack(
        self,
        player: Player,
        other_players_in_position: list[Player],
    ) -> None:
        # Placeholder for future attack implementation.
        return

    def __evaluate_collect_resource(
        self,
        player: Player,
        ground: Ground,
    ) -> None:
        # Placeholder for future resource collection implementation.
        return

    def __evaluate_movement(
        self,
        grounds: list[Ground],
        config: WorldConfig,
        player: Player,
        player_decision: PlayerDecision,
    ) -> None:
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
        row_offset, column_offset = offsets[player_decision]
        row = (player.position.row + row_offset) % config.rows
        column = (player.position.col + column_offset) % config.columns
        destination = grounds[row * config.columns + column]
        if isinstance(destination, (WallGround, WaterGround)):
            return

        player.position = Position(row, column)
        return

from models.abstractions import Ground, Player, PlayerDecision, Position, WorldConfig
from models.grounds import WallGround, WaterGround


class GameRules:
    def evaluate_player_decision(
        self,
        grounds: list[Ground],
        config: WorldConfig,
        player: Player,
        current_position: Position,
        player_decision: PlayerDecision,
        player_in_position: list[Player],
    ) -> tuple[Player, Position]:
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
            return (player, current_position)

        row = (current_position.row + offset[0]) % config.rows
        column = (current_position.col + offset[1]) % config.columns
        destination = grounds[row * config.columns + column]
        if isinstance(destination, (WallGround, WaterGround)):
            return (player, current_position)

        return (player, Position(row, column))

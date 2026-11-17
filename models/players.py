import random

from models.abstractions import Direction, Ground, Player, PlayerDecision


class Scrapper(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_decision(
        self, current_ground: Ground, surroundings: dict[Direction, Ground]
    ) -> PlayerDecision:
        return random.choice(list(PlayerDecision))

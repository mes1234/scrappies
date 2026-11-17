import random

from models.abstractions import Direction, Ground, Player, PlayerDecision


class Scrapper(Player):
    def __init__(self, name: str = "Scrapper") -> None:
        super().__init__()
        self.name = name

    def make_decision(
        self, surroundings: dict[Direction, tuple[Ground, list[Player]]]
    ) -> PlayerDecision:
        return random.choice(list(PlayerDecision))


class Beast(Player):
    def __init__(self, name: str = "Beast") -> None:
        super().__init__()
        self.name = name

    def make_decision(
        self, surroundings: dict[Direction, tuple[Ground, list[Player]]]
    ) -> PlayerDecision:
        return random.choice(list(PlayerDecision))

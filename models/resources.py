from models.abstractions import Resource


class FoodResource(Resource):
    def __init__(self, amount: float) -> None:
        super().__init__()
        self.amount = amount

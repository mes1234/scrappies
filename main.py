import arcade

from models.abstractions import GroundType, WorldConfig
from models.world import World


class WorldWindow(arcade.Window):
    COLUMNS = 40
    ROWS = 30
    TILE_SIZE = 20
    MAP_LEFT = 20
    MAP_BOTTOM = 80
    WINDOW_WIDTH = COLUMNS * TILE_SIZE + 2 * MAP_LEFT
    WINDOW_HEIGHT = MAP_BOTTOM + ROWS * TILE_SIZE + 60

    GROUND_COLORS = {
        GroundType.Plain: (111, 139, 91),
        GroundType.Wall: (92, 96, 104),
        GroundType.Water: (62, 126, 171),
        GroundType.Home: (202, 151, 78),
    }

    LEGEND_ITEMS = (
        (GroundType.Plain, "Plain"),
        (GroundType.Wall, "Wall"),
        (GroundType.Water, "Water"),
        (GroundType.Home, "Home"),
    )

    def __init__(self) -> None:
        self.world = World(
            WorldConfig(columns=self.COLUMNS, rows=self.ROWS, player_count=0, speed=30)
        )
        super().__init__(
            self.WINDOW_WIDTH,
            self.WINDOW_HEIGHT,
            "Scrappies world demo",
            draw_rate=1 / self.world.config.speed,
        )

        self.title_text = arcade.Text(
            "Scrappies - wrapped world",
            self.MAP_LEFT,
            self.WINDOW_HEIGHT - 32,
            (235, 238, 242),
            font_size=20,
        )
        self.legend_texts = [
            arcade.Text(
                label, self.MAP_LEFT + 22 + index * 100, 34, (220, 224, 230), 14
            )
            for index, (_, label) in enumerate(self.LEGEND_ITEMS)
        ]
        self.quit_text = arcade.Text(
            "Esc or Q to quit", self.MAP_LEFT + 600, 34, (170, 176, 185), 14
        )

    def on_draw(self) -> None:
        self.clear((28, 31, 38))
        self.title_text.draw()

        self.show_grounds()
        self.show_legend()

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        _ = modifiers
        if symbol in (arcade.key.ESCAPE, arcade.key.Q):
            self.close()

    def show_legend(self) -> None:
        for index, (ground_type, _) in enumerate(self.LEGEND_ITEMS):
            arcade.draw_lbwh_rectangle_filled(
                self.MAP_LEFT + index * 100, 32, 16, 16, self.GROUND_COLORS[ground_type]
            )
            self.legend_texts[index].draw()
        self.quit_text.draw()

    def show_grounds(self) -> None:
        for index, ground in enumerate(self.world.grounds):
            row, column = divmod(index, self.COLUMNS)
            left = self.MAP_LEFT + column * self.TILE_SIZE
            bottom = self.MAP_BOTTOM + (self.ROWS - 1 - row) * self.TILE_SIZE
            arcade.draw_lbwh_rectangle_filled(
                left,
                bottom,
                self.TILE_SIZE,
                self.TILE_SIZE,
                self.GROUND_COLORS[ground.type],
            )
            arcade.draw_lbwh_rectangle_outline(
                left,
                bottom,
                self.TILE_SIZE,
                self.TILE_SIZE,
                (37, 43, 48),
                border_width=1,
            )


def run() -> None:
    WorldWindow()
    arcade.run()


if __name__ == "__main__":
    run()

from collections.abc import Sequence
from math import pi, sin
from time import monotonic

import arcade

from models.abstractions import Ground, GroundType, Player, PlayerDecision, WorldConfig
from models.world import World


def get_ground_type(ground: Ground) -> GroundType:
    ground_type = getattr(ground, "type", None)
    if not isinstance(ground_type, GroundType):
        raise TypeError(f"{type(ground).__name__} must define a valid GroundType")
    return ground_type


def get_player_name(player: Player) -> str:
    name = getattr(player, "name", None)
    if not isinstance(name, str):
        raise TypeError(f"{type(player).__name__} must define a player name")
    return name


class WorldWindow(arcade.Window):
    COLUMNS = 40
    ROWS = 30
    TILE_SIZE = 20
    MAP_LEFT = 20
    MAP_BOTTOM = 80
    WINDOW_WIDTH = COLUMNS * TILE_SIZE + 2 * MAP_LEFT
    WINDOW_HEIGHT = MAP_BOTTOM + ROWS * TILE_SIZE + 60
    MOVE_DURATION = 1.0

    GROUND_COLORS = {
        GroundType.Plain: (111, 139, 91),
        GroundType.Wall: (92, 96, 104),
        GroundType.Water: (62, 126, 171),
        GroundType.Home: (202, 151, 78),
    }
    RESOURCE_COLOR = (232, 196, 86)
    RESOURCE_RADIUS = 2.5
    PLAYER_COLORS = {
        "A": (245, 214, 96),
        "B": (245, 125, 190),
        "Beast": (234, 98, 83),
    }

    LEGEND_ITEMS = (
        (GroundType.Plain, "Plain"),
        (GroundType.Wall, "Wall"),
        (GroundType.Water, "Water"),
        (GroundType.Home, "Home"),
    )

    def __init__(self) -> None:
        self.world = World(
            WorldConfig(columns=self.COLUMNS, rows=self.ROWS, player_count=0, speed=1)
        )
        self.world_update_elapsed = 0.0
        self.player_transitions = [
            (
                get_player_name(player),
                (player.position.row, player.position.col),
                (player.position.row, player.position.col),
                None,
            )
            for player in self.world.players
        ]
        self.transition_started = monotonic()
        super().__init__(
            self.WINDOW_WIDTH,
            self.WINDOW_HEIGHT,
            "Scrappies world demo",
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
        self.player_legend_texts = [
            arcade.Text(
                name,
                self.MAP_LEFT + 22 + (len(self.LEGEND_ITEMS) + index) * 100,
                34,
                (220, 224, 230),
                14,
            )
            for index, name in enumerate(self.PLAYER_COLORS)
        ]
        self.player_texts = {
            name: arcade.Text(
                "!" if name == "Beast" else name,
                0,
                0,
                (28, 31, 38),
                9,
                anchor_x="center",
                anchor_y="center",
            )
            for name in self.PLAYER_COLORS
        }
        self.rest_text = arcade.Text("Zzzz", 0, 0, (245, 245, 255), 10)
        self.quit_text = arcade.Text(
            "Esc or Q to quit",
            self.WINDOW_WIDTH - 135,
            self.WINDOW_HEIGHT - 32,
            (170, 176, 185),
            14,
        )

    def on_draw(self) -> None:
        ground_types = [get_ground_type(ground) for ground in self.world.grounds]
        resource_coverages = [
            self.get_resource_coverage(ground) for ground in self.world.grounds
        ]
        player_transitions = self.player_transitions
        transition_started = self.transition_started

        self.clear((28, 31, 38))
        self.title_text.draw()

        self.show_grounds(ground_types, resource_coverages)
        self.show_players(player_transitions, monotonic() - transition_started)
        self.show_legend()

    @staticmethod
    def get_resource_coverage(ground: Ground) -> float:
        total_amount = sum(resource.amount for resource in ground.resources)
        if total_amount <= 0.0:
            return 0.0
        if total_amount <= 0.25:
            return 0.25
        if total_amount <= 0.5:
            return 0.5
        if total_amount <= 0.75:
            return 0.75
        return 1.0

    def on_update(self, delta_time: float) -> None:
        if self.world.config.speed <= 0:
            return

        self.world_update_elapsed += delta_time
        update_interval = 1.0 / self.world.config.speed
        if self.world_update_elapsed < update_interval:
            return

        self.world_update_elapsed %= update_interval
        old_positions = {
            player: (player.position.row, player.position.col)
            for player in self.world.players
        }
        self.world.step()
        self.player_transitions = [
            (
                get_player_name(player),
                old_positions.get(
                    player,
                    (player.position.row, player.position.col),
                ),
                (player.position.row, player.position.col),
                self.world.decision[player][-1]
                if self.world.decision[player]
                else None,
            )
            for player in self.world.players
        ]
        self.transition_started = monotonic()

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
        for index, color in enumerate(self.PLAYER_COLORS.values()):
            arcade.draw_circle_filled(
                self.MAP_LEFT + (len(self.LEGEND_ITEMS) + index) * 100 + 8,
                40,
                7,
                color,
            )
            self.player_legend_texts[index].draw()
        self.quit_text.draw()

    def show_players(
        self,
        transitions: Sequence[
            tuple[str, tuple[int, int], tuple[int, int], PlayerDecision | None]
        ],
        elapsed: float,
    ) -> None:
        progress = min(1.0, max(0.0, elapsed / self.MOVE_DURATION))
        tail = progress * progress
        head = 1.0 - (1.0 - progress) ** 2
        previous_scissor = self.ctx.scissor
        self.ctx.scissor = (
            self.MAP_LEFT,
            self.MAP_BOTTOM,
            self.COLUMNS * self.TILE_SIZE,
            self.ROWS * self.TILE_SIZE,
        )
        try:
            for name, (old_row, old_column), (row, column), decision in transitions:
                color = self.PLAYER_COLORS[name]
                label = self.player_texts[name]
                row_delta = row - old_row
                column_delta = column - old_column
                if abs(row_delta) > self.ROWS / 2:
                    row_delta -= self.ROWS if row_delta > 0 else -self.ROWS
                if abs(column_delta) > self.COLUMNS / 2:
                    column_delta -= self.COLUMNS if column_delta > 0 else -self.COLUMNS

                for index in range(5):
                    fraction = tail + (head - tail) * index / 4
                    current_row = (old_row + row_delta * fraction + 0.5) % self.ROWS
                    current_column = (
                        old_column + column_delta * fraction + 0.5
                    ) % self.COLUMNS
                    x = self.MAP_LEFT + current_column * self.TILE_SIZE
                    y = self.MAP_BOTTOM + (self.ROWS - current_row) * self.TILE_SIZE
                    radius = 4.5 + 1.5 * index / 4
                    width = self.COLUMNS * self.TILE_SIZE
                    height = self.ROWS * self.TILE_SIZE
                    x_offsets = [0]
                    y_offsets = [0]
                    if x - radius < self.MAP_LEFT:
                        x_offsets.append(width)
                    if x + radius > self.MAP_LEFT + width:
                        x_offsets.append(-width)
                    if y - radius < self.MAP_BOTTOM:
                        y_offsets.append(height)
                    if y + radius > self.MAP_BOTTOM + height:
                        y_offsets.append(-height)
                    for x_offset in x_offsets:
                        for y_offset in y_offsets:
                            arcade.draw_circle_filled(
                                x + x_offset, y + y_offset, radius, color
                            )
                            if index == 4:
                                label.x = x + x_offset
                                label.y = y + y_offset
                                label.draw()
                                if decision == PlayerDecision.Rest:
                                    self.rest_text.x = min(
                                        x + x_offset + 8,
                                        self.MAP_LEFT + width - self.rest_text.content_width,
                                    )
                                    self.rest_text.y = min(
                                        y + y_offset + 8 + 2 * sin(2 * pi * elapsed),
                                        self.MAP_BOTTOM + height - self.rest_text.content_height,
                                    )
                                    self.rest_text.draw()
        finally:
            self.ctx.scissor = previous_scissor

    def show_grounds(
        self,
        ground_types: list[GroundType],
        resource_coverages: list[float],
    ) -> None:
        for index, (ground_type, resource_coverage) in enumerate(
            zip(ground_types, resource_coverages)
        ):
            row, column = divmod(index, self.COLUMNS)
            left = self.MAP_LEFT + column * self.TILE_SIZE
            bottom = self.MAP_BOTTOM + (self.ROWS - 1 - row) * self.TILE_SIZE
            arcade.draw_lbwh_rectangle_filled(
                left,
                bottom,
                self.TILE_SIZE,
                self.TILE_SIZE,
                self.GROUND_COLORS[ground_type],
            )
            arcade.draw_lbwh_rectangle_outline(
                left,
                bottom,
                self.TILE_SIZE,
                self.TILE_SIZE,
                (37, 43, 48),
                border_width=1,
            )
            if resource_coverage > 0.0:
                covered_height = self.TILE_SIZE * resource_coverage
                radius = min(
                    self.RESOURCE_RADIUS,
                    self.TILE_SIZE / 2,
                    covered_height / 2,
                )
                arcade.draw_lbwh_rectangle_filled(
                    left + radius,
                    bottom,
                    self.TILE_SIZE - 2 * radius,
                    covered_height,
                    self.RESOURCE_COLOR,
                )
                arcade.draw_lbwh_rectangle_filled(
                    left,
                    bottom + radius,
                    self.TILE_SIZE,
                    covered_height - 2 * radius,
                    self.RESOURCE_COLOR,
                )
                arcade.draw_circle_filled(
                    left + radius,
                    bottom + radius,
                    radius,
                    self.RESOURCE_COLOR,
                )
                arcade.draw_circle_filled(
                    left + self.TILE_SIZE - radius,
                    bottom + radius,
                    radius,
                    self.RESOURCE_COLOR,
                )
                arcade.draw_circle_filled(
                    left + radius,
                    bottom + covered_height - radius,
                    radius,
                    self.RESOURCE_COLOR,
                )
                arcade.draw_circle_filled(
                    left + self.TILE_SIZE - radius,
                    bottom + covered_height - radius,
                    radius,
                    self.RESOURCE_COLOR,
                )


def run() -> None:
    window = WorldWindow()
    arcade.run()


if __name__ == "__main__":
    run()

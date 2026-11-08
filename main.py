import pygame

from models.abstractions import GroundType, WorldConfig
from models.world import World

COLUMNS = 40
ROWS = 30
TILE_SIZE = 20
MAP_LEFT = 20
MAP_TOP = 60
WINDOW_WIDTH = COLUMNS * TILE_SIZE + 2 * MAP_LEFT
WINDOW_HEIGHT = MAP_TOP + ROWS * TILE_SIZE + 80

GROUND_COLORS = {
    GroundType.Plain: (111, 139, 91),
    GroundType.Wall: (92, 96, 104),
    GroundType.Water: (62, 126, 171),
    GroundType.Home: (202, 151, 78),
}


def run() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Scrappies world demo")
    clock = pygame.time.Clock()
    title_font = pygame.font.Font(None, 30)
    legend_font = pygame.font.Font(None, 22)

    world = World(
        WorldConfig(columns=COLUMNS, rows=ROWS, player_count=0, speed=30)
    )
    legend_items = (
        (GroundType.Plain, "Plain"),
        (GroundType.Wall, "Wall"),
        (GroundType.Water, "Water"),
        (GroundType.Home, "Home"),
    )

    running = True
    try:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN
                    and event.key in (pygame.K_ESCAPE, pygame.K_q)
                ):
                    running = False

            screen.fill((28, 31, 38))
            title = title_font.render("Scrappies - wrapped world", True, (235, 238, 242))
            screen.blit(title, (MAP_LEFT, 18))

            for index, ground in enumerate(world.grounds):
                row, column = divmod(index, COLUMNS)
                tile = pygame.Rect(
                    MAP_LEFT + column * TILE_SIZE,
                    MAP_TOP + row * TILE_SIZE,
                    TILE_SIZE,
                    TILE_SIZE,
                )
                pygame.draw.rect(screen, GROUND_COLORS[ground.type], tile)
                pygame.draw.rect(screen, (37, 43, 48), tile, width=1)

            legend_x = MAP_LEFT
            legend_y = MAP_TOP + ROWS * TILE_SIZE + 22
            for ground_type, label in legend_items:
                pygame.draw.rect(
                    screen,
                    GROUND_COLORS[ground_type],
                    pygame.Rect(legend_x, legend_y, 16, 16),
                )
                screen.blit(
                    legend_font.render(label, True, (220, 224, 230)),
                    (legend_x + 22, legend_y - 2),
                )
                legend_x += 100

            screen.blit(
                legend_font.render("Esc or Q to quit", True, (170, 176, 185)),
                (MAP_LEFT + 300, legend_y - 2),
            )
            pygame.display.flip()
            clock.tick(int(world.config.speed))
    finally:
        pygame.quit()


if __name__ == "__main__":
    run()

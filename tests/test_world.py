from models.abstractions import WorldConfig
from models.world import World


def test_bootstrap_6_by_6_quad_world() -> None:
    config = WorldConfig(
        columns=6,
        rows=6,
        player_count=0,
        speed=1.0,
    )
    world = World(config)

    grounds = world.grounds

    assert len(grounds) == 36
    assert len(grounds[2 * config.columns + 2].neighbors) == 4

    left_edge = grounds[0]
    right_edge = grounds[config.columns - 1]
    top_edge = grounds[0]
    bottom_edge = grounds[(config.rows - 1) * config.columns]
    assert left_edge in right_edge.neighbors
    assert right_edge in left_edge.neighbors
    assert top_edge in bottom_edge.neighbors
    assert bottom_edge in top_edge.neighbors
    assert all(len(ground.neighbors) == 4 for ground in grounds)

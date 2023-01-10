import pygame

from src.common import HEIGHT, WIDTH
from src.world import World


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
    clock = pygame.time.Clock()

    world = World()

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                world.save()
                pygame.quit()
                raise SystemExit

        dt = clock.tick(60) / 100

        event_info = {
            "events": events,
            "dt": dt,
            "keys": pygame.key.get_pressed(),
            "mouse": pygame.mouse.get_pos(),
        }

        world.update(event_info)
        world.draw(screen, event_info)

        pygame.display.flip()
        pygame.display.set_caption(f"{clock.get_fps():.0f}")


if __name__ == "__main__":
    main()

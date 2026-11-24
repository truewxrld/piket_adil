import pygame
from game_logic import Game
from game_render import SIZE, draw, make_fonts
from solver import ALGORITHMS


def handle_action(game, action):
    kind, value = action
    if kind == "level":
        game.set_level(value)
    elif kind == "algorithm":
        game.set_algorithm(value)
    elif kind == "day":
        game.select_day(value)
    elif kind == "person":
        game.assign(value)
    elif kind == "clear":
        game.assign(None)
    elif kind == "solve":
        game.start_solver()
    elif kind == "reset":
        game.reset()
    elif kind == "pause":
        game.toggle_pause()
    elif kind == "speed":
        game.cycle_speed()


def main():
    pygame.init()
    try:
        screen = pygame.display.set_mode(SIZE)
        pygame.display.set_caption("Piket Adil | Kelompok 11")
        clock = pygame.time.Clock()
        fonts = make_fonts()
        game = Game()
        buttons = draw(screen, game, fonts)
        alive = True
        while alive:
            dt_ms = clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    alive = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for action, rect in buttons.items():
                        if rect.collidepoint(event.pos):
                            handle_action(game, action)
                            buttons = draw(screen, game, fonts)
                            break
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        alive = False
                    elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                        game.set_level(event.key - pygame.K_1)
                    elif event.key == pygame.K_TAB:
                        keys = list(ALGORITHMS)
                        game.set_algorithm(keys[(keys.index(game.algorithm) + 1) % len(keys)])
                    elif event.key == pygame.K_s:
                        game.start_solver()
                    elif event.key == pygame.K_SPACE:
                        game.toggle_pause()
                    elif event.key == pygame.K_r:
                        game.reset()
                    elif event.key == pygame.K_f:
                        game.cycle_speed()
                    elif event.key in (pygame.K_DELETE, pygame.K_BACKSPACE):
                        game.assign(None)
                    buttons = draw(screen, game, fonts)
            game.update(dt_ms)
            buttons = draw(screen, game, fonts)
            pygame.display.flip()
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()

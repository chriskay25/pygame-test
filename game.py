import pygame as pg
# Import pygame.locals for easier access to key coordinates
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

def run_game():
    # Initialize and set up screen
    pg.init()
    screen = pg.display.set_mode([800, 500])

    running = True

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        screen.fill((255,255,255))

        pg.draw.circle(screen, (0,0,255), (250,250), 75)
        # Screen refresh
        pg.display.flip()

    pg.quit()
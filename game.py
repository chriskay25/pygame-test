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
    screen_width = 800
    screen_height = 500
    screen = pg.display.set_mode([screen_width, screen_height])

    running = True

    while running:
        for event in pg.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == pg.QUIT:
                running = False
            
        screen.fill((255,255,255))

        surf = pg.Surface((50,50))
        surf.fill((0,0,0))
        rect = surf.get_rect()
        surf_center = (
            (screen_width - surf.get_width()) / 2,
            (screen_height - surf.get_height()) / 2
        )
        # Use blit to copy surf Surface onto screen Surface
        screen.blit(surf, surf_center)

        # Screen refresh
        pg.display.flip()

    pg.quit()

run_game()
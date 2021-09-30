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
    # Set up screen.
    screen_width = 800
    screen_height = 500

    # Create Player object.
    class Player(pg.sprite.Sprite):
        def __init__(self):
            super(Player, self).__init__()
            self.surf = pg.Surface((75,25))
            self.surf.fill((150,150,255))
            self.rect = self.surf.get_rect()

    pg.init()

    screen = pg.display.set_mode([screen_width, screen_height])
    
    # Instantiate player.
    player = Player()

    running = True

    while running:
        for event in pg.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == pg.QUIT:
                running = False
            
        screen.fill((255,255,255))

        player_center = (
            (screen_width - player.surf.get_width()) / 2,
            (screen_height - player.surf.get_height()) / 2
        )
        # Use blit to copy player Surface onto screen Surface.
        screen.blit(player.surf, player_center)

        # Screen refresh.
        pg.display.flip()

    pg.quit()

run_game()
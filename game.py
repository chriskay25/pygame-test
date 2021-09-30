import pygame as pg
import random
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

        # Move sprite on keypresses.
        def update(self, pressed_keys):
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -5)
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0, 5)
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)
            
            # Keep player from going off screen.
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > screen_width:
                self.rect.right = screen_width
            if self.rect.top <= 0:
                self.rect.top = 0
            if self.rect.bottom >= screen_height:
                self.rect.bottom = screen_height
    
    # Create enemy object
    class Enemy(pg.sprite.Sprite):
        def __init__(self):
            super(Enemy, self).__init__()
            self.surf = pg.Surface((20,10))
            self.surf.fill((90,90,150))
            self.rect = self.surf.get_rect(
                center = (
                    random.randint(screen_width + 20, screen_width + 100),
                    random.randint(0, screen_height)
                )
            )
            self.speed = random.randint(5,20)

        def update(self):
            self.rect.move_ip(-self.speed, 0)
            if self.rect.right < 0:
                self.kill()

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

        # Get all currently pressed keys.
        pressed_keys = pg.key.get_pressed()

        player.update(pressed_keys)
            
        screen.fill((255,255,255))

        # Use blit to copy player Surface onto screen Surface.
        screen.blit(player.surf, player.rect)

        # Screen refresh.
        pg.display.flip()

    pg.quit()

run_game()
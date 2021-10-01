import pygame as pg
import random
# Import pygame.locals for easier access to key coordinates
from pygame.locals import (
    RLEACCEL,
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
    screen_width = 1200
    screen_height = 900

    # Create Player object.
    class Player(pg.sprite.Sprite):
        def __init__(self):
            super(Player, self).__init__()
            self.surf = pg.image.load('./images/playerShip3_red.png').convert()
            self.surf.set_colorkey((0,0,0), RLEACCEL)
            self.rect = self.surf.get_rect()
            self.rect.bottom = screen_height
            self.rect.right = screen_width/2

        # Move sprite on keypresses.
        def update(self, pressed_keys):
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -10)
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0, 10)
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-10, 0)
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(10, 0)
            
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
            self.surf = pg.image.load('./images/ufoGreen.png').convert()
            self.surf.set_colorkey((0,0,0), RLEACCEL)
            self.rect = self.surf.get_rect(
                center = (
                    random.randint(0, screen_width),
                    random.randint(0, 1)
                )
            )
            self.speed = random.randint(1,4)

        def update(self):
            self.rect.move_ip(0, self.speed)
            if self.rect.bottom > screen_height:
                self.kill()

    pg.init()

    screen = pg.display.set_mode([screen_width, screen_height])
    
    # Custom event for adding a new enemy
    ADDENEMY = pg.USEREVENT + 1
    pg.time.set_timer(ADDENEMY, 1000)

    # Instantiate player.
    player = Player()

    # Groups to hold sprites
    enemies = pg.sprite.Group()  # for collision detection & updates
    all_sprites = pg.sprite.Group()  # for rendering
    all_sprites.add(player)

    running = True

    while running:
        for event in pg.event.get():
            # Did the user press a key?
            if event.type == KEYDOWN:
                # If user pressed Escape key, stop loop.
                if event.key == K_ESCAPE:
                    running = False

            # If the user clicked the window close bttn, stop loop.
            elif event.type == pg.QUIT:
                running = False
            
            # Add new enemy
            elif event.type == ADDENEMY:
                # Create new enemy and add it to sprite groups.
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)
            
        # Use clock to set framerate.
        clock = pg.time.Clock()

        # Get all currently pressed keys.
        pressed_keys = pg.key.get_pressed()
        player.update(pressed_keys)

        # Update enemy position.
        enemies.update()
            
        screen.fill((255,255,255))

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        # Check if any enemies have collided with the player.
        if pg.sprite.spritecollideany(player, enemies):
            # If so, then remove the player and stop loop.
            player.kill()
            running = False

        # Screen refresh.
        pg.display.flip()

        # Set a framerate of 30 frames per second.
        clock.tick(30)

    pg.quit()

run_game()
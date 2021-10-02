import os, sys
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
    K_SPACE,
    KEYDOWN,
    QUIT,
)

def load_image(name, colorkey=None):
    fullname = os.path.join('images', name)
    try:
        image = pg.image.load(fullname)
    except pg.error as message:
        print("Can't load image: ", name)
        raise SystemExit(message)
    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def run_game():
    # Set up screen.
    screen_width = 1200
    screen_height = 900

    # Create Player object.
    class Player(pg.sprite.Sprite):
        def __init__(self):
            super(Player, self).__init__()
            self.image, self.rect = load_image('playerShip3_red.png', -1)
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

    class Laser(pg.sprite.Sprite):
        def __init__(self, pos):
            super(Laser, self).__init__()
            self.image, self.rect = load_image('laserBlue14.png', -1)
            self.rect.center = pos.center
            self.rect.bottom = pos.top

        def update(self):
            self.rect.move_ip(0, -10)
            if self.rect.bottom <= 10:
                self.kill()
    
    # Create enemy object
    class Enemy(pg.sprite.Sprite):
        def __init__(self):
            super(Enemy, self).__init__()
            self.image, self.rect = load_image('ufoGreen.png', -1)
            self.rect = self.image.get_rect(
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
    pg.time.set_timer(ADDENEMY, 3000)

    # Instantiate player.
    player = Player()

    # Groups to hold sprites
    enemies = pg.sprite.Group()  # for collision detection & updates
    lasers = pg.sprite.Group()
    all_sprites = pg.sprite.Group()  # for rendering
    all_sprites.add(player)
    all_sprites.add(lasers)

    running = True

    while running:
        for event in pg.event.get():
            # Did the user press a key?
            if event.type == KEYDOWN:
                # If user pressed Escape key, stop loop.
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_SPACE:
                    pos = player.rect
                    laser = Laser(pos)
                    lasers.add(laser)
                    all_sprites.add(laser)

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

        lasers.update()
            
        screen.fill((255,255,255))

        for entity in all_sprites:
            screen.blit(entity.image, entity.rect)

        # Check if any enemies have collided with the player.
        if pg.sprite.spritecollideany(player, enemies):
            # If so, then remove the player and stop loop.
            player.kill()
            running = False

        # Screen refresh.
        pg.display.flip()

        # Set a framerate of 30 frames per second.
        clock.tick(40)

    pg.quit()

run_game()
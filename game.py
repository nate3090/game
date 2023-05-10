# a simple game to connect with arduino one
# import and init game
import pygame
import random

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

pygame.mixer.init()
pygame.mixer.music.load("Apoxode_-_Electric_1.mp3")
pygame.mixer.music.play(loops=-1)

# Load all sound files
# Sound sources: Jon Fincher
move_up_sound = pygame.mixer.Sound("Rising_putter.ogg")
move_down_sound = pygame.mixer.Sound("Falling_putter.ogg")
collision_sound = pygame.mixer.Sound("Collision.ogg")



SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400


# Initialize pygame
pygame.init()

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
# Create custom events for adding a new enemy and cloud
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# define class mario

class Mario(pygame.sprite.Sprite):
    def __init__(self):
        super(Mario, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf = pygame.image.load("mario.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.rect.bottom = 300
        self.onGround = True
        self.falling = False

    # Move the sprite based on keypresses
    def update(self, pressed_keys):
        # if pressed_keys[K_DOWN]:
        #    self.rect.move_ip(0, 5)
        #            move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
        if pressed_keys[K_SPACE]:
            # self.rect.move_ip(0, -5)            
            # move_up_sound.play()
            self.jump()
        if self.falling == True:
            if self.rect.bottom >= 300:
                self.rect.bottom = 300
                self.falling = False
                self.onGround = True
            else:
                self.rect.move_ip(0, 3)
    def jump(self):
        if self.onGround == False:
            return
        self.rect.move_ip(0, -50)
        move_up_sound.play()
        self.velocity = 8
        self.onGround = False
        self.falling = True

class Block(pygame.sprite.Sprite):
    def __init__(self):
        super(Block, self).__init__()
        self.surf = pygame.image.load("rocket.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)

# Define the enemy object extending pygame.sprite.Sprite
# Instead of a surface, we use an image for a better looking sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("rocket.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        # The starting position is randomly generated, as is the speed
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, 300),
            )
        )
        self.speed = random.randint(5, 20)

    # Move the enemy based on speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

# set up screen and all stuff
# Create our 'player'
player = Mario()

# Create groups to hold enemy sprites, cloud sprites, and all sprites
# - enemies is used for collision detection and position updates
# - clouds is used for position updates
# - all_sprites isused for rendering
enemies = pygame.sprite.Group()
# clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == ADDENEMY:
            # Create the new enemy, and add it to our sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
     # Get all the keys currently pressed
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    # Update the position of our enemies and clouds
    enemies.update()
    # Fill the screen with sky blue
    screen.fill((135, 206, 250))

    # Draw all our sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    
    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
        # If so, remove the player and stop the loop
        player.kill()
        running = False


    pygame.display.flip()
    # Ensure we maintain a 30 frames per second rate
    clock.tick(30)

pygame.mixer.music.stop()
pygame.quit()

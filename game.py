# Import packages
import pygame
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
# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
clock = pygame.time.Clock()
bg = pygame.image.load("bg1.png")

# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load('player.png').convert_alpha()
        self.rect = self.surf.get_rect()
#Player update function        
def update(player, pressed_keys):
    if pressed_keys[K_UP]:
        player.rect.move_ip(0, -5)
    if pressed_keys[K_DOWN]:
        player.rect.move_ip(0, 5)
    if pressed_keys[K_LEFT]:
        player.rect.move_ip(-5, 0)
    if pressed_keys[K_RIGHT]:
        player.rect.move_ip(5, 0)
        # Keep player on the screen
    if player.rect.left < 0:
        player.rect.left = 0
    if player.rect.right > SCREEN_WIDTH:
        player.rect.right = SCREEN_WIDTH
    if player.rect.top <= 0:
        player.rect.top = 0
    if player.rect.bottom >= SCREEN_HEIGHT:
        player.rect.bottom = SCREEN_HEIGHT
# Define the enemy function
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load('enemy-icon.png').convert_alpha()
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

# Initialize pygame
pygame.init()
# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# Create a custom event for adding a new enemy
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)

# Instantiate player. Right now, this is just a rectangle.
player = Player()
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
# Variable to keep the main loop running
running = True

# Main loop
while running:
    # for loop through the event queue
    for event in pygame.event.get():
        # Check for KEYDOWN event
        if event.type == pygame.KEYDOWN:
            #print('KEY pressed is ' + str(event.key) + '.') # Just for testing the key pressed
            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
                pauseGame()
                running = False
        # Check for QUIT event. If QUIT, then set running to false.
        elif event.type == QUIT:
            running = False  
        # Add a new enemy?
        elif event.type == ADDENEMY:
            # Create the new enemy and add it to sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
       
            
    pressed_keys = pygame.key.get_pressed()

    # Update the player sprite based on user keypresses
    update(player,pressed_keys)
    # Update enemy and background positions
    enemies.update()
    # Fill the screen with black
    screen.fill((135, 206, 250))
    screen.blit(bg, (0, 0))
    # Draw all sprites
    for entity in all_sprites:

        screen.blit(entity.surf, entity.rect)
        # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
    # If so, then remove the player and stop the loop
        player.kill()
        running = False
    # Update the display
    pygame.display.flip()
    # Ensure program maintains a rate of 30 frames per second
    clock.tick(30)  
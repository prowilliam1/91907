import pygame
import random

pygame.init()

# Screen setup
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Move Example 1")

# Load image
character_image = pygame.image.load("Graphics\\Characters\\Example 1.png")
character_x, character_y = 100, 100  # Initial position
character_speed = 5  # Movement speed

# Clock setup for 60 FPS
clock = pygame.time.Clock()

def align_to_facing_grid(value, grid_size, direction):
    """Align a value to the grid in the direction the player is facing."""
    if direction > 0:  # Moving right or down
        return ((value + grid_size - 1) // grid_size) * grid_size
    elif direction < 0:  # Moving left or up
        return (value // grid_size) * grid_size
    return value  # No movement

def check_for_battle():
    """Check if a battle should occur with a 5% chance."""
    if random.randint(1, 100) <= 5:  # 5% chance
        print("A wild battle has started!")
        # Add logic to transition to the battle screen here

# Main loop
running = True
facing_x, facing_y = 0, 0  # Direction the player is facing
last_grid_x, last_grid_y = character_x // 64, character_y // 64  # Track the last grid position
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get keys pressed
    keys = pygame.key.get_pressed()
    moving = False
    if keys[pygame.K_w]:  # Move up
        character_y -= 4
        facing_x, facing_y = 0, -1
        moving = True
    if keys[pygame.K_s]:  # Move down
        character_y += 4
        facing_x, facing_y = 0, 1
        moving = True
    if keys[pygame.K_a]:  # Move left
        character_x -= 4
        facing_x, facing_y = -1, 0
        moving = True
    if keys[pygame.K_d]:  # Move right
        character_x += 4
        facing_x, facing_y = 1, 0
        moving = True

    # Push character to the grid they are facing when not moving
    if not moving:
        character_x = align_to_facing_grid(character_x, 64, facing_x)
        character_y = align_to_facing_grid(character_y, 64, facing_y)

    # Check for battle when moving to a new grid tile
    current_grid_x, current_grid_y = character_x // 64, character_y // 64
    if (current_grid_x, current_grid_y) != (last_grid_x, last_grid_y):
        check_for_battle()
        last_grid_x, last_grid_y = current_grid_x, current_grid_y

    # Draw background and character
    screen.fill((0, 0, 0))  # Black background
    screen.blit(character_image, (character_x, character_y))

    pygame.display.flip()

    # Limit the frame rate to 60 FPS
    clock.tick(60)

pygame.quit()

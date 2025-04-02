import pygame
import tkinter

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Character Movement")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Load background image
background_image = pygame.image.load("C:\\Users\\21020\\OneDrive - Lynfield College\\Documents\\3PAD\\Assessment 91906 and 91907\\Game\\Assets\\Backgrounds\\background.png")

# Character properties
character_size = 50
character_x = WIDTH // 2
character_y = HEIGHT // 2
character_speed = 5

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get keys pressed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:  # Move up
        character_y -= character_speed
    if keys[pygame.K_s]:  # Move down
        character_y += character_speed
    if keys[pygame.K_a]:  # Move left
        character_x -= character_speed
    if keys[pygame.K_d]:  # Move right
        character_x += character_speed

    # Prevent the character from going out of bounds
    character_x = max(0, min(WIDTH - character_size, character_x))
    character_y = max(0, min(HEIGHT - character_size, character_y))

    # Drawing everything
    screen.blit(background_image, (0, 0))  # Draw background image
    pygame.draw.rect(screen, BLUE, (character_x, character_y, character_size, character_size))  # Draw character
    pygame.display.flip()  # Update the display

    # Limit the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()

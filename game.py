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
background_image = pygame.image.load("C:\\Users\\21020\\OneDrive - Lynfield College\\Documents\\3PAD\\Assessment 91906 and 91907\\Game\\Assets\\Backgrounds\\Room 1\\background.png")

# Load table image
table_image = pygame.image.load("C:\\Users\\21020\\OneDrive - Lynfield College\\Documents\\3PAD\\Assessment 91906 and 91907\\Game\\Assets\\Backgrounds\\Room 1\\Table.png")
table_width, table_height = table_image.get_width(), table_image.get_height()

# Table properties
table_x = 410  # Set the specific x-coordinate for the table
table_y = 255  # Set the specific y-coordinate for the table

I1_image = pygame.image.load("C:\\Users\\21020\\OneDrive - Lynfield College\\Documents\\3PAD\\Assessment 91906 and 91907\\Game\\Assets\\Backgrounds\\Room 1\\A.png")
I1_width, I1_height = I1_image.get_width(), I1_image.get_height()

# interactable properties
I1_x = 420  # Set the specific x-coordinate for the interactable
I1_y = 295  # Set the specific y-coordinate for the interactable

bed_image = pygame.image.load("C:\\Users\\21020\\OneDrive - Lynfield College\\Documents\\3PAD\\Assessment 91906 and 91907\\Game\\Assets\\Backgrounds\\Room 1\\Bed.png")
bed_width, bed_height = bed_image.get_width(), bed_image.get_height()

# Bed properties
bed_x = 245  # Set the specific x-coordinate for the bed
bed_y = 240  # Set the specific y-coordinate for the bed

# Character properties
character_size = 50
character_x = 100  # Set the specific starting x-coordinate for the character
character_y = 100  # Set the specific starting y-coordinate for the character
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

    # Check for collision with the table
    character_rect = pygame.Rect(character_x, character_y, character_size, character_size)
    table_rect = pygame.Rect(table_x, table_y, table_width, table_height)
    bed_rect = pygame.Rect(bed_x, bed_y, bed_width, bed_height)
    if character_rect.colliderect(table_rect):
        # Undo movement if collision occurss
        if keys[pygame.K_w]:  # Undo upward movement
            character_y += character_speed
        if keys[pygame.K_s]:  # Undo downward movement
            character_y -= character_speed
        if keys[pygame.K_a]:  # Undo leftward movement
            character_x += character_speed
        if keys[pygame.K_d]:  # Undo rightward movement
            character_x -= character_speed
    elif character_rect.colliderect(bed_rect):
        # Undo movement if collision occurss
        if keys[pygame.K_w]:  # Undo upward movement
            character_y += character_speed
        if keys[pygame.K_s]:  # Undo downward movement
            character_y -= character_speed
        if keys[pygame.K_a]:  # Undo leftward movement
            character_x += character_speed
        if keys[pygame.K_d]:  # Undo rightward movement
            character_x -= character_speed

    # Drawing everything
    screen.blit(background_image, (0, 0))  # Draw background image
    screen.blit(table_image, (table_x, table_y))  # Draw table image
    screen.blit(bed_image, (bed_x, bed_y))  # Draw bed image
    screen.blit(I1_image, (I1_x, I1_y))  # Draw I1 image on top of the table
    pygame.draw.rect(screen, BLUE, (character_x, character_y, character_size, character_size))  # Draw character
    pygame.display.flip()  # Update the display

    # Limit the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()

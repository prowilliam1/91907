import pygame as pg
import tkinter as tk

screen = pg.display.set_mode((1280, 720))

# Initialize player position
player_x, player_y = screen.get_width() // 2, screen.get_height() // 2  # Player starts at the center of the screen
player_speed = 5  # Speed of movement

clock = pg.time.Clock()  # Create a clock object to manage frame rate

# Load player image
player_image = pg.image.load("Assets\\Characters\\Player\\Player.png")

# Load background image
background_image = pg.image.load("Assets\\Backgrounds\\Room 1\\Room 1.png")

# Load table image
table_image = pg.image.load("Assets\\Backgrounds\\Room 1\\Table.png")
table_rect = table_image.get_rect(topleft=(50, 300))  # Set table position

# Game loop
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # Get key states
    keys = pg.key.get_pressed()
    move_x, move_y = 0, 0
    if keys[pg.K_w]:  # Move up
        move_y -= 1
    if keys[pg.K_s]:  # Move down
        move_y += 1
    if keys[pg.K_a]:  # Move left
        move_x -= 1
    if keys[pg.K_d]:  # Move right
        move_x += 1

    # Normalize diagonal movement
    if move_x != 0 and move_y != 0:
        move_x /= (move_x ** 2 + move_y ** 2) ** 0.5  # Normalize x
        move_y /= (move_x ** 2 + move_y ** 2) ** 0.5  # Normalize y

    # Calculate new player position
    new_player_x = player_x + move_x * player_speed
    new_player_y = player_y + move_y * player_speed

    # Create a temporary rect for collision detection
    player_rect = pg.Rect(
        new_player_x - player_image.get_width() // 2,
        new_player_y - player_image.get_height() // 2,
        player_image.get_width(),
        player_image.get_height(),
    )

    # Check for collision with the table
    if not table_rect.colliderect(player_rect):
        player_x = new_player_x
        player_y = new_player_y

    # Update screen
    screen.fill((0, 0, 0))  # Clear screen with black
    screen.blit(background_image, (0, 0))  # Draw background image
    screen.blit(table_image, table_rect.topleft)  # Draw table
    screen.blit(player_image, (player_x - player_image.get_width() // 2, 
                               player_y - player_image.get_height() // 2))  # Draw player
    pg.display.flip()
    clock.tick(60)  # Limit the game to 60 frames per second

pg.quit()
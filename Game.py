import pygame as pg
import tkinter as tk

screen = pg.display.set_mode((1280, 720))

# Load the custom room image
room_image = pg.image.load("path/to/your/room_image.png")  # Replace with the actual path to your image
room_image = pg.transform.scale(room_image, (1280, 720))  # Scale the image to fit the screen

# Initialize player position
player_x, player_y = 100, 100  # Example starting position
player_speed = 5  # Speed of movement

clock = pg.time.Clock()  # Create a clock object to manage frame rate

# Game loop
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # Get key states
    keys = pg.key.get_pressed()
    if keys[pg.K_w]:  # Move up
        player_y -= player_speed
    if keys[pg.K_s]:  # Move down
        player_y += player_speed
    if keys[pg.K_a]:  # Move left
        player_x -= player_speed
    if keys[pg.K_d]:  # Move right
        player_x += player_speed

    # Update screen (example placeholder)
    screen.fill((0, 0, 0))  # Clear screen with black
    screen.blit(room_image, (0, 0))  # Draw the room image at the top-left corner
    pg.draw.rect(screen, (255, 0, 0), (player_x, player_y, 50, 50))  # Draw player as a red square
    pg.display.flip()
    clock.tick(60)  # Limit the game to 60 frames per second

pg.quit()
import pygame as pg
import tkinter as tk

screen = pg.display.set_mode((1280, 720))

# Initialize player position
player_x, player_y = 100, 100  # Example starting position
player_speed = 5  # Speed of movement

clock = pg.time.Clock()  # Create a clock object to manage frame rate

# Load player image
player_image = pg.image.load("Assets\\Characters\\Player\\Player.png")

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
        move_x *= 0.7071  # 1/sqrt(2)
        move_y *= 0.7071  # 1/sqrt(2)

    # Update player position
    player_x += move_x * player_speed
    player_y += move_y * player_speed

    # Update screen
    screen.fill((0, 0, 0))  # Clear screen with black
    screen.blit(player_image, (player_x, player_y))  # Draw player image at updated position
    pg.display.flip()
    clock.tick(60)  # Limit the game to 60 frames per second

pg.quit()
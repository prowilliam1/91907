import pygame as pg
import tkinter as tk

pg.init()  # Initialize all pygame modules

screen = pg.display.set_mode((1280, 720))

# Initialize player position
player_x, player_y = 100, 100  # Example starting position
player_speed = 5  # Speed of movement

# Initialize player direction
player_direction = "down"  # Default direction

clock = pg.time.Clock()  # Create a clock object to manage frame rate

# Load player images for different directions
player_images = {
    "up": pg.image.load("Assets\\Characters\\Player\\Player_Up.png"),
    "down": pg.image.load("Assets\\Characters\\Player\\Player_Down.png"),
    "left": pg.image.load("Assets\\Characters\\Player\\Player_Left.png"),
    "right": pg.image.load("Assets\\Characters\\Player\\Player_Right.png"),
}

# Load background image
background_image = pg.image.load("Assets\\Backgrounds\\Room 1\\Room 1.png")

# Load table image
table_image = pg.image.load("Assets\\Backgrounds\\Room 1\\Table.png")
table_rect = table_image.get_rect(topleft=(656, 288))  # Set table position

# Load new image
new_image = pg.image.load("Assets\\Backgrounds\\Room 1\\Table Interaction.png")
new_image_rect = new_image.get_rect(topleft=(672, 352))  # Set position for the new image

# Load exclamation mark image
exclamation_image = pg.image.load("Assets\\Characters\\Player\\Interaction.png")

# Load text box image
text_box_image = pg.image.load("Assets\\UI\\Text Box.png")

# Load custom font
custom_font = pg.font.Font("Assets\\Fonts\\Font.TTF", 40)  # Replace with your custom font file and size

# Variable to track if text box is visible
text_box_visible = False

# Variable to store the message for the text box
text_box_message = ""

# Define interaction distance

# Game loop
running = True
while running:
    can_interact = False  # Reset interaction flag

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN and event.key == pg.K_e:  # Check for 'E' key press
            # Check if player is within interaction distance below "Table Interaction" and facing up
            if (
                player_direction == "up" and 
                abs(player_x - new_image_rect.x) < 120 and 
                abs(player_y + player_images[player_direction].get_height() - new_image_rect.y) < 120
            ):
                print("Interacted with Table Interaction!")
                text_box_visible = True  # Show text box
                text_box_message = "X = 2"  # Set the message

    # Check if player can interact
    if (
        player_direction == "up" and 
        abs(player_x - new_image_rect.x) < 120 and 
        abs(player_y + player_images[player_direction].get_height() - new_image_rect.y) < 120
    ):
        can_interact = True

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

    # Calculate new player position
    new_player_x = player_x + move_x * player_speed
    new_player_y = player_y + move_y * player_speed
    player_rect_x = pg.Rect(new_player_x, player_y, player_images[player_direction].get_width(), player_images[player_direction].get_height())
    player_rect_y = pg.Rect(player_x, new_player_y, player_images[player_direction].get_width(), player_images[player_direction].get_height())

    # Check for collision with the table
    if not player_rect_x.colliderect(table_rect):
        player_x = new_player_x  # Update X position if no collision
    if not player_rect_y.colliderect(table_rect):
        player_y = new_player_y  # Update Y position if no collision

    # Determine movement direction and update player direction
    if move_y < 0:  # Moving up
        player_direction = "up"
    elif move_y > 0:  # Moving down
        player_direction = "down"
    elif move_x < 0:  # Moving left
        player_direction = "left"
    elif move_x > 0:  # Moving right
        player_direction = "right"

    # Get the current player image based on direction
    current_player_image = player_images[player_direction]

    # Update screen
    screen.fill((0, 0, 0))  # Clear screen with black
    screen.blit(background_image, (0, 0))  # Draw background image
    screen.blit(new_image, new_image_rect.topleft)  # Draw new image
    screen.blit(table_image, table_rect.topleft)  # Draw table
    screen.blit(current_player_image, (player_x, player_y))  # Draw player image at updated position

    # Draw exclamation mark if player can interact
    if can_interact:
        exclamation_x = player_x + (current_player_image.get_width() // 2) - (exclamation_image.get_width() // 2)
        exclamation_y = player_y - exclamation_image.get_height()
        screen.blit(exclamation_image, (exclamation_x, exclamation_y))

    # Draw text box if visible
    if text_box_visible:
        text_box_x = 8
        text_box_y = 496
        screen.blit(text_box_image, (text_box_x, text_box_y))

        # Render and display text in the text box
        text_surface = custom_font.render(text_box_message, True, (255, 255, 255))  # White text
        text_surface_x = text_box_x + 20  # Padding inside the text box
        text_surface_y = text_box_y + 20  # Padding inside the text box
        screen.blit(text_surface, (text_surface_x, text_surface_y))

    pg.display.flip()
    clock.tick(60)  # Limit the game to 60 frames per second

pg.quit()
import pygame as pg
import tkinter as tk

pg.init()  # Initialize all pygame modules

Width = 1280  # Set the width of the window
Height = 720  # Set the height of the window
screen = pg.display.set_mode((Width, Height))  # Create a window with the specified dimensions

# Initialize player position
player_x, player_y = 520, 280  # Example starting position
player_speed = 4  # Speed of movement

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

# Load table image and interaction image
table_image = pg.image.load("Assets\\Backgrounds\\Room 1\\Table.png")
table_rect = table_image.get_rect(topleft=(656, 288))  # Set table position

table_interaction_image = pg.image.load("Assets\\Backgrounds\\Room 1\\Table Interaction.png")
table_interaction_image_rect = table_interaction_image.get_rect(topleft=(672, 352))  # Set position for the new image

# Load bed image and interaction image
bed_image = pg.image.load("Assets\\Backgrounds\\Room 1\\Bed.png")
bed_image_rect = bed_image.get_rect(topleft=(392, 264))  # Set position for the new image

bed_interaction_image = pg.image.load("Assets\\Backgrounds\\Room 1\\Bed Interaction.png")
bed_interaction_image_rect = bed_interaction_image.get_rect(topleft=(392, 440))  # Set position for the new image

# Load wall image and interaction image
wall_image = pg.image.load("Assets\\Backgrounds\\Room 1\\Wall.png")
wall_image_rect = wall_image.get_rect(topleft=(384, 192))  # Set position for the wall image

wall_interaction_image = pg.image.load("Assets\\Backgrounds\\Room 1\\Wall Interaction.png")
wall_interaction_image_rect = wall_interaction_image.get_rect(topleft=(544, 144))  # Set position for the wall image

exit_image = pg.image.load("Assets\\Backgrounds\\Room 1\\Exit.png")
exit_image_rect = exit_image.get_rect(topleft=(576, 704))  # Set position for the exit image

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

# Variable to track if input box is visible
input_box_visible = False
input_text = ""  # Text entered by the player

# Define input box dimensions and position
input_box_rect = pg.Rect(880, 480, 360, 40)  # Position and size of the input box
input_box_color = (255, 255, 255)  # White color for the input box
input_text_color = (0, 0, 0)  # Black color for the input text

# Load border images
border_top = pg.Rect(0, 0, Width, 8)
border_bottom_1 = pg.Rect(0, 712, Width, 720)
border_bottom_2 = pg.Rect(0, 648, 574, Height)
border_bottom_3 = pg.Rect(704, 648, Width, Height)
border_left = pg.Rect(0, 0, 376, Height)
border_right = pg.Rect(896, 0, Width, Height)
border_rects = [border_top, border_bottom_1, border_bottom_2, border_bottom_3, border_left, border_right]

# Variable to track if the door is open
door_open = False

# Variable to track if the table has been interacted with
table_interacted = False

# Game loop
running = True
while running:
    can_interact = False  # Reset interaction flag

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_e:  # Check for 'E' key press
                # Check if player is within interaction distance below "Table Interaction" and facing up
                if (
                    player_direction == "up" and 
                    abs(player_x - table_interaction_image_rect.x) < 24 and 
                    abs(player_y + player_images[player_direction].get_height() - table_interaction_image_rect.y) < 120
                ):
                    text_box_visible = True  # Show text box
                    text_box_message = "There is a message on the table\nX = 2\n\n\n... Space to close"  # Set the message with a newline
                    table_interacted = True  # Mark table as interacted
                # Add bed interaction logic
                if (
                    player_direction == "up" and 
                    abs(player_x - bed_interaction_image_rect.x) < 24 and 
                    abs(player_y + player_images[player_direction].get_height() - bed_interaction_image_rect.y) < 120
                ):
                    text_box_visible = True  # Show text box
                    text_box_message = "There's nothing under the bed\n\n\n\n... Space to close"  # Set the message with a newline

                # Add wall interaction logic
                if (
                    player_direction == "up" and 
                    abs(player_x - wall_interaction_image_rect.x) < 40 and 
                    abs(player_y + player_images[player_direction].get_height() - wall_interaction_image_rect.y) < 200 and
                    544 <= player_x <= 600  # Ensure player_x is between 500 and 600
                ):
                    text_box_visible = True
                    text_box_message = "The Window has been boarded up\n\n\n\n... Space to close"  # Set the message with a newline

                # Add exit interaction logic
                if (
                    not door_open and  # Ensure the door is not already open
                    player_direction == "down" and 
                    abs(player_x - exit_image_rect.x) < 64 and 
                    abs(player_y + player_images[player_direction].get_height() - exit_image_rect.y) < 8
                ):
                    if not table_interacted:
                        text_box_visible = True
                        text_box_message = "The door is locked...\nMaybe there's a clue in this room\n\n\n... Space to close"
                    else:
                        text_box_visible = True
                        input_box_visible = True  # Show input box
                        text_box_message = "7 + (12/x)^2 * 5 \n\n\n... Press Enter to confirm"
            if event.key == pg.K_SPACE:  # Check for 'Spacebar' key press
                if text_box_visible:
                    text_box_visible = False  # Close the text box
                    input_box_visible = False  # Close the input box
                    input_text = ""  # Clear the input text
            if input_box_visible:  # Handle input box text
                if event.key == pg.K_BACKSPACE:
                    input_text = input_text[:-1]  # Remove the last character
                elif event.key == pg.K_RETURN:  # Confirm input
                    if input_text == "187":  # Check if the correct code is entered
                        door_open = True
                        input_box_visible = False  # Show text box
                        text_box_message = "The door has opened\nWalk past the door to proceed\n\n... Space to Close"
                        print("The door has opened")  # Debug message
                        border_rects.remove(border_bottom_1)  # Remove border_bottom_1
                    else:
                        text_box_message = "Incorrect code. Try again."
                    input_text = ""  # Clear the input text
                elif event.unicode.isdigit():  # Allow only numeric input
                    input_text += event.unicode  # Add the typed character

    # Check if player can interact
    if (
        player_direction == "up" and 
        abs(player_x - table_interaction_image_rect.x) < 24 and 
        abs(player_y + player_images[player_direction].get_height() - table_interaction_image_rect.y) < 120
    ):
        can_interact = True
    # Check if player can interact with bed
    if (
        player_direction == "up" and 
        abs(player_x - bed_interaction_image_rect.x) < 24 and 
        abs(player_y + player_images[player_direction].get_height() - bed_interaction_image_rect.y) < 120
    ):
        can_interact = True

    # Check if player can interact with wall
    if (
        player_direction == "up" and 
        abs(player_x - wall_interaction_image_rect.x) < 40 and 
        abs(player_y + player_images[player_direction].get_height() - wall_interaction_image_rect.y) < 200 and
        544 <= player_x <= 600
    ):
        can_interact = True

    # Check if player can interact with exit
    if (
        not door_open and  # Ensure the door is not already open
        player_direction == "down" and 
        abs(player_x - exit_image_rect.x) < 64 and 
        abs(player_y + player_images[player_direction].get_height() - exit_image_rect.y) < 8
    ):
        can_interact = True

    # Check if the player walks past the exit when the door is open
    if door_open and player_x >= 576 and player_x <= 704 and player_y >= 600 and player_y <= 704:
        print("Entering a new room...")  # Debug message
        # Logic to transition to a new room can be added here
        running = False  # End the current game loop for now

    # Disable movement when the text box is visible
    if not text_box_visible:
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

        # Check for collision
        for border in border_rects:  # Iterate through remaining borders
            if player_rect_x.colliderect(border):
                new_player_x = player_x  # Reset X position if collision occurs
            if player_rect_y.colliderect(border):
                new_player_y = player_y  # Reset Y position if collision occurs

        if not player_rect_x.colliderect(table_rect) and not player_rect_x.colliderect(bed_image_rect) and not player_rect_x.colliderect(wall_image_rect):
            player_x = new_player_x  # Update X position if no collision
        if not player_rect_y.colliderect(table_rect) and not player_rect_y.colliderect(bed_image_rect) and not player_rect_y.colliderect(wall_image_rect):
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
    screen.blit(table_interaction_image, table_interaction_image_rect.topleft)  # Draw new image
    screen.blit(table_image, table_rect.topleft)  # Draw table
    screen.blit(bed_image, bed_image_rect.topleft)  # Draw bed image
    screen.blit(bed_interaction_image, bed_interaction_image_rect.topleft)  # Draw new image
    screen.blit(wall_image, wall_image_rect.topleft)  # Draw wall image
    screen.blit(wall_interaction_image, wall_interaction_image_rect.topleft)  # Draw new image
    screen.blit(exit_image, exit_image_rect.topleft)  # Draw exit image
    screen.blit(current_player_image, (player_x, player_y))  # Draw player image at updated position

    # Draw exclamation mark if player can interact and text box is not visible
    if can_interact and not text_box_visible:
        exclamation_x = player_x + (current_player_image.get_width() // 2) - (exclamation_image.get_width() //2)
        exclamation_y = player_y - exclamation_image.get_height()
        screen.blit(exclamation_image, (exclamation_x, exclamation_y))

    # Display interaction prompt
    if can_interact and not text_box_visible:
        interaction_prompt = pg.font.Font("Assets\\Fonts\\Font.TTF", 32).render("Press E to Interact", True, (255, 255, 255))
        screen.blit(interaction_prompt, (10, 10))  # Top-left corner of the screen

    # Draw text box if visible
    if text_box_visible:
        text_box_x = 8
        text_box_y = 456
        screen.blit(text_box_image, (text_box_x, text_box_y))

        # Render and display text in the text box
        lines = text_box_message.split("\n")  # Split the message into lines
        for i, line in enumerate(lines):
            text_surface = custom_font.render(line, True, (255, 255, 255))  # Render each line
            text_surface_x = text_box_x + 20  # Padding inside the text box
            text_surface_y = text_box_y + 20 + i * 40  # Adjust Y position for each line
            screen.blit(text_surface, (text_surface_x, text_surface_y))

    # Draw input box if visible
    if input_box_visible:
        pg.draw.rect(screen, input_box_color, input_box_rect)  # Draw input box
        input_text_surface = custom_font.render(input_text, True, input_text_color)  # Render input text
        screen.blit(input_text_surface, (input_box_rect.x + 10, input_box_rect.y + 5))  # Display input text

    pg.display.flip()
    clock.tick(60)  # Limit the game to 60 frames per second

pg.quit()
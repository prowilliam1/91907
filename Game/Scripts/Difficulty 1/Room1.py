import pygame
import sys

pygame.init()

pygame.mixer.init()
pygame.mixer.music.load("Audio\\1.mp3")
pygame.mixer.music.set_volume(0.5)

screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Room 1")

white = (255, 255, 255)
black = (0, 0, 0)

walk_right = [pygame.transform.scale(pygame.image.load(f"Graphics\\Characters\\Player\\Player_Right{i}.png"), (64, 96)) for i in range(1, 5)]
walk_left = [pygame.transform.scale(pygame.image.load(f"Graphics\\Characters\\Player\\Player_Left{i}.png"), (64, 96)) for i in range(1, 5)]
walk_up = [pygame.transform.scale(pygame.image.load(f"Graphics\\Characters\\Player\\Player_Up{i}.png"), (64, 96)) for i in range(1, 5)]
walk_down = [pygame.transform.scale(pygame.image.load(f"Graphics\\Characters\\Player\\Player_Down{i}.png"), (64, 96)) for i in range(1, 5)]

tileset = pygame.transform.scale(pygame.image.load("Graphics\\Tilesets\\Example.png"), (pygame.image.load("Graphics\\Tilesets\\Example.png").get_width() * 2, pygame.image.load("Graphics\\Tilesets\\Example.png").get_height() * 2))
tile_size = 64

overlay_tileset = pygame.transform.scale(
    pygame.image.load("Graphics\\Tilesets\\Example.png"),
    (pygame.image.load("Graphics\\Tilesets\\Example.png").get_width() * 2,
     pygame.image.load("Graphics\\Tilesets\\Example.png").get_height() * 2)
)

map_layout = [
    [18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18],
    [18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18],
    [18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18],
    [18, 18, 18, 18, 18, 18, 18, 15, 15, 15, 15, 15, 15],
    [18, 18, 18, 18, 18, 18, 18, 20, 20, 20, 20, 20, 20],
    [18, 18, 18, 18, 18, 18, 18, 0, 1, 1, 1, 1, 2],
    [18, 18, 18, 18, 18, 18, 18, 5, 6, 6, 6, 6, 7],
    [18, 18, 18, 18, 18, 18, 18, 10, 11, 11, 11, 11, 12]
]

overlay_map_layout = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 16, 0, 0, 0, 0, 0],    
    [0, 0, 0, 0, 0, 0, 0, 21, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 17, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

collision_map_layout = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
]

def draw_map():
    for row_index, row in enumerate(map_layout):
        for col_index, tile_index in enumerate(row):

            tile_x = (tile_index % (tileset.get_width() // tile_size)) * tile_size
            tile_y = (tile_index // (tileset.get_width() // tile_size)) * tile_size
            tile_rect = pygame.Rect(tile_x, tile_y, tile_size, tile_size)
            screen.blit(tileset, (col_index * tile_size, row_index * tile_size), tile_rect)

            overlay_tile_index = overlay_map_layout[row_index][col_index]
            if overlay_tile_index != 0:
                overlay_tile_x = (overlay_tile_index % (overlay_tileset.get_width() // tile_size)) * tile_size
                overlay_tile_y = (overlay_tile_index // (overlay_tileset.get_width() // tile_size)) * tile_size
                overlay_tile_rect = pygame.Rect(overlay_tile_x, overlay_tile_y, tile_size, tile_size)
                screen.blit(overlay_tileset, (col_index * tile_size, row_index * tile_size), overlay_tile_rect)

def is_walkable(target_x, target_y):
    col = int(target_x // tile_size)
    row = int(target_y // tile_size)
    if 0 <= row < len(collision_map_layout) and 0 <= col < len(collision_map_layout[0]):
        return collision_map_layout[row][col] == 0
    return False

char_x, char_y = 512, 288
char_speed = 4
current_frame = 0
direction = "down"

animation_speed = 10

movement_cooldown = 150
last_move_time = 0

snap_speed = 4

def main():
    global char_x, char_y, current_frame, direction, last_move_time
    clock = pygame.time.Clock()
    running = True
    frame_counter = 0
    target_x, target_y = char_x, char_y

    pygame.mixer.music.play(-1)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        if current_time - last_move_time >= movement_cooldown:
            if keys[pygame.K_w]:
                direction = "up"
                if char_y > 0 and is_walkable(char_x, target_y - tile_size):
                    target_y -= tile_size
                    last_move_time = current_time
            elif keys[pygame.K_s]:
                direction = "down"
                if is_walkable(char_x, target_y + tile_size):
                    target_y += tile_size
                    last_move_time = current_time
            elif keys[pygame.K_a]:
                direction = "left"
                if char_x > 0 and is_walkable(target_x - tile_size, char_y):
                    target_x -= tile_size
                    last_move_time = current_time
            elif keys[pygame.K_d]:
                direction = "right"
                if is_walkable(target_x + tile_size, char_y):
                    target_x += tile_size
                    last_move_time = current_time

        char_x += (target_x - char_x) / snap_speed
        char_y += (target_y - char_y) / snap_speed

        if keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]:
            frame_counter += 1
            if frame_counter >= animation_speed:
                current_frame = (current_frame + 1) % len(walk_right)
                frame_counter = 0
        else:
            current_frame = 0

        screen.fill(black)

        draw_map()

        if direction == "up":
            screen.blit(walk_up[current_frame], (char_x, char_y))
        elif direction == "down":
            screen.blit(walk_down[current_frame], (char_x, char_y))
        elif direction == "left":
            screen.blit(walk_left[current_frame], (char_x, char_y))
        elif direction == "right":
            screen.blit(walk_right[current_frame], (char_x, char_y))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

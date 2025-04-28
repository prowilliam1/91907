import pygame
import sys

pygame.init()

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

map_layout = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

def draw_map():
    for row_index, row in enumerate(map_layout):
        for col_index, tile_index in enumerate(row):
            tile_x = (tile_index % (tileset.get_width() // tile_size)) * tile_size
            tile_y = (tile_index // (tileset.get_width() // tile_size)) * tile_size
            tile_rect = pygame.Rect(tile_x, tile_y, tile_size, tile_size)
            screen.blit(tileset, (col_index * tile_size, row_index * tile_size), tile_rect)

char_x, char_y = 0, -32
char_speed = 4
current_frame = 0
direction = "down"

animation_speed = 10

movement_cooldown = 150
last_move_time = 0

snap_speed = 6

def main():
    global char_x, char_y, current_frame, direction, last_move_time
    clock = pygame.time.Clock()
    running = True
    frame_counter = 0
    target_x, target_y = char_x, char_y

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        if current_time - last_move_time >= movement_cooldown:
            if keys[pygame.K_w] and char_y > 0:
                target_y -= tile_size
                direction = "up"
                last_move_time = current_time
            elif keys[pygame.K_s] and char_y < (len(map_layout) - 1) * tile_size:
                target_y += tile_size
                direction = "down"
                last_move_time = current_time
            elif keys[pygame.K_a] and char_x > 0:
                target_x -= tile_size
                direction = "left"
                last_move_time = current_time
            elif keys[pygame.K_d] and char_x < (len(map_layout[0]) - 1) * tile_size:
                target_x += tile_size
                direction = "right"
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

        screen.fill(white)

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

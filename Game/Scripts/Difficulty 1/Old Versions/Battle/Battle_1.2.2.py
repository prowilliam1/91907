import pygame
import random
import time
from Character_Stats import *
from Weapon_Stats import *
from Enemy_Stats import *

pygame.init()

screen_width, screen_height = 1920, 1080
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Battle Screen")

background_image = pygame.image.load("Graphics\\Backgrounds\\Battle Sequence.png")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

character1_image = pygame.image.load("Graphics\\Characters\\Example 2.png")
character2_image = pygame.image.load("Graphics\\Characters\\Example 3.png")
character3_image = pygame.image.load("Graphics\\Characters\\Example 4.png")
character4_image = pygame.image.load("Graphics\\Characters\\Example 1.png")

character_positions = [
    (60, 240),
    (60, 450),
    (270, 240),
    (270, 450),
]

seperator1_image = pygame.image.load("Graphics\\UI\\Battle\\Seperator\\1.png")
seperator2_image = pygame.image.load("Graphics\\UI\\Battle\\Seperator\\2.png")

seperator1_x = 0
seperator1_y = 666

current_level = 1

player1_stats = get_player1_stats(current_level)
player2_stats = get_player2_stats(current_level)
player3_stats = get_player3_stats(current_level)
player4_stats = get_player4_stats(current_level)

equipped_weapon = "Sword"
weapon_stats = get_weapon_stats(equipped_weapon)

player1_stats["attack"] += weapon_stats["attack"]
player1_stats["special_attack"] += weapon_stats["special_attack"]
player2_stats["attack"] += weapon_stats["attack"]
player2_stats["special_attack"] += weapon_stats["special_attack"]
player3_stats["attack"] += weapon_stats["attack"]
player3_stats["special_attack"] += weapon_stats["special_attack"]
player4_stats["attack"] += weapon_stats["attack"]
player4_stats["special_attack"] += weapon_stats["special_attack"]

player_stats_list = [player1_stats, player2_stats, player3_stats, player4_stats]

player_hp_list = [player1_stats["hp"], player2_stats["hp"], player3_stats["hp"], player4_stats["hp"]]

enemy_names = ["Enemy Dumm", "Goblin", "Orc"]
enemy_positions = [
    (1000, 300),
    (1200, 350),
    (1400, 250),
]
enemy_images = [
    pygame.image.load("Graphics\\Characters\\Enemy Dumm.png"),
    pygame.image.load("Graphics\\Characters\\Enemy Dumm.png"),
    pygame.image.load("Graphics\\Characters\\Enemy Dumm.png"),
]
enemies = []
for i, name in enumerate(enemy_names):
    stats = get_enemy_stats(name)
    enemies.append({
        "name": name,
        "stats": stats,
        "hp": stats["hp"],
        "max_hp": stats["hp"],
        "defense": stats["defense"],
        "resistance": stats["resistance"],
        "image": enemy_images[i],
        "pos": enemy_positions[i],
    })

def get_health_bar_image_for_enemy(enemy):
    hp_percentage = (enemy["hp"] / enemy["max_hp"]) * 100
    if hp_percentage <= 0:
        return pygame.image.load("Graphics\\UI\\Battle\\Bars\\Health\\Health Bar 0%.png")
    health_bar_number = (hp_percentage // 10) * 10
    return pygame.image.load(f"Graphics\\UI\\Battle\\Bars\\Health\\Health Bar {health_bar_number}%.png")

custom_font_path = "Fonts\\Font.ttf"
font = pygame.font.Font(custom_font_path, 36)
font_large = pygame.font.Font(custom_font_path, 96)
font_medium = pygame.font.Font(custom_font_path, 64)

attack_button_width, attack_button_height = 200, 40
attack_button_x, attack_button_y = 24, 690

special_button_width, special_button_height = 200, 40
special_button_x, special_button_y = 594, 690

items_button_width, items_button_height = 200, 40
items_button_x, items_button_y = 24, 894

run_button_width, run_button_height = 200, 40
run_button_x, run_button_y = 594, 894

attack_button_image = pygame.image.load("Graphics\\UI\\Battle\\Buttons\\ATK BTN.png")
special_button_image = pygame.image.load("Graphics\\UI\\Battle\\Buttons\\SPC BTN.png")
items_button_image = pygame.image.load("Graphics\\UI\\Battle\\Buttons\\ITM BTN.png")
run_button_image = pygame.image.load("Graphics\\UI\\Battle\\Buttons\\RUN BTN.png")
highlight_button_image = pygame.image.load("Graphics\\UI\\Battle\\Buttons\\BTN OTL.png")
arrow_image = pygame.image.load("Graphics\\UI\\Battle\\arrow.png")

def draw_attack_button():
    screen.blit(attack_button_image, (attack_button_x, attack_button_y))
    text_surface = font_medium.render("Attack", True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=((attack_button_x + attack_button_width // 2) + 162, (attack_button_y + attack_button_height // 2) + 60))
    screen.blit(text_surface, text_rect)

def draw_special_button():
    screen.blit(special_button_image, (special_button_x, special_button_y))
    text_surface = font_medium.render("Special", True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=((special_button_x + special_button_width // 2) + 162, (special_button_y + special_button_height // 2) + 60))
    screen.blit(text_surface, text_rect)

def draw_items_button():
    screen.blit(items_button_image, (items_button_x, items_button_y))
    text_surface = font_medium.render("Items", True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=((items_button_x + items_button_width // 2) + 162, (items_button_y + items_button_height // 2) + 60))
    screen.blit(text_surface, text_rect)

def draw_run_button():
    screen.blit(run_button_image, (run_button_x, run_button_y))
    text_surface = font_medium.render("Run", True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=((run_button_x + run_button_width // 2) + 162, (run_button_y + run_button_height // 2) + 60))
    screen.blit(text_surface, text_rect)

selected_button = 0
button_positions = [(24, 690), (594, 690), (24, 894), (594, 894)]
selected_enemy_index = 0

target_select_mode = False
target_action = None

special_select_mode = False
selected_special_index = 0
special_attack_names = ["1", "2", "3", "4", "5"]

def draw_button_highlight():
    if not target_select_mode and not special_select_mode:
        screen.blit(highlight_button_image, (button_positions[selected_button][0] - 6, button_positions[selected_button][1] - 6))

def draw_special_select_menu():
    for i, name in enumerate(special_attack_names):
        color = (255, 255, 0) if i == selected_special_index else (255, 255, 255)
        attack_surface = font_medium.render(f"{i+1}. Special {name}", True, color)
        screen.blit(attack_surface, (42, 690 + i * 60))
    instr_surface = font.render("Use W/S to move, ENTER to select, ESC to cancel", True, (200, 200, 200))
    screen.blit(instr_surface, (40, 60))
    screen.blit(seperator2_image, (seperator1_x, seperator1_y))


def draw_enemies():
    for i, enemy in enumerate(enemies):
        x, y = enemy["pos"]
        screen.blit(enemy["image"], (x, y))
        if target_select_mode and i == selected_enemy_index:
            arrow_rect = arrow_image.get_rect(midbottom=(x + enemy["image"].get_width() // 2, y - 10))
            screen.blit(arrow_image, arrow_rect)

def draw_enemy_hp():
    enemy = enemies[selected_enemy_index]
    health_bar_img = get_health_bar_image_for_enemy(enemy)
    bar_width = health_bar_img.get_width()
    bar_height = health_bar_img.get_height()
    bar_x = screen_width - bar_width - 24
    bar_y = 24
    enemy_hp_text = font.render(
        f"{enemy['hp']} / {enemy['max_hp']}", True, (255, 255, 255)
    )
    text_x = bar_x - enemy_hp_text.get_width() - 20
    text_y = bar_y + (bar_height // 2) - (enemy_hp_text.get_height() // 2)
    screen.blit(enemy_hp_text, (text_x, text_y))
    screen.blit(health_bar_img, (bar_x, bar_y))

def draw_player_hp():
    idx = current_character_turn
    stats = player_stats_list[idx]
    hp = player_hp_list[idx]
    bar_img = get_health_bar_image_for_enemy({"hp": hp, "max_hp": stats["hp"]})
    bar_x = 24
    bar_y = 24
    screen.blit(bar_img, (bar_x, bar_y))
    hp_text = font.render(f"{hp} / {stats['hp']}", True, (255, 255, 255))
    text_x = bar_x + bar_img.get_width() + 20
    text_y = bar_y + (bar_img.get_height() // 2) - (hp_text.get_height() // 2)
    screen.blit(hp_text, (text_x, text_y))

timer_active = False
timer_start_time = 0
timer_duration = 15
questions = []
current_question_index = 0
player_answer = ""
correct_answers = 0

def generate_question():
    operator = random.choice(["+", "-", "*", "/"])
    if operator == "/":
        num2 = random.randint(1, 15)
        num1 = num2 * random.randint(1, 15)
    else:
        num1 = random.randint(1, 15)
        num2 = random.randint(1, 15)
    question = f"{num1} {operator} {num2}"
    correct_answer = eval(question.replace("/", "//"))
    return question, correct_answer

def generate_special_question():
    special_logic = get_special_question(equipped_weapon)
    x = random.randint(1, 15)
    y = random.randint(1, 15)
    v = random.randint(2, 4)
    w = random.randint(1, 5)
    z = special_logic["adjust_z"](x, y, v, w)
    question = special_logic["question"](x, y, v, w, z)
    correct_answer = special_logic["answer"](x, y, v, w, z)
    return question, correct_answer

def evaluate_question(question, answer):
    if isinstance(question, tuple):
        correct_answer = question[1]
        return int(answer) == correct_answer
    else:
        num1, num2, operator = question
        if operator == "+":
            correct_answer = num1 + num2
        elif operator == "-":
            correct_answer = num1 - num2
        elif operator == "*":
            correct_answer = num1 * num2
        elif operator == "/":
            correct_answer = num1 // num2
        return int(answer) == correct_answer

def draw_timer_and_question():
    global timer_start_time, questions, current_question_index, player_answer
    elapsed_time = time.time() - timer_start_time
    remaining_time = max(0, timer_duration - elapsed_time)
    if remaining_time <= 5:
        blink_on = int((elapsed_time * 2) % 2) == 0
        timer_color = (255, 0, 0) if blink_on else (255, 255, 255)
    else:
        timer_color = (255, 255, 255)
    if current_question_index < len(questions):
        question = questions[current_question_index]
        if isinstance(question, tuple):
            question_text = str(question[0])
        else:
            question_text = "Invalid question format"
        question_surface = font_large.render(question_text, True, (255, 255, 255))
        answer_surface = font_large.render(player_answer, True, (255, 255, 255))
        timer_text = font_large.render(f"Time Left: {int(remaining_time)}s", True, timer_color)
        question_x = (screen_width - question_surface.get_width()) // 2
        question_y = screen_height - 378
        answer_x = (screen_width - answer_surface.get_width()) // 2
        answer_y = question_y + question_surface.get_height() + 10
        timer_x = (screen_width - timer_text.get_width()) // 2
        timer_y = answer_y + answer_surface.get_height() + 10
        screen.blit(question_surface, (question_x, question_y))
        screen.blit(answer_surface, (answer_x, answer_y))
        screen.blit(timer_text, (timer_x, timer_y))

current_character_turn = 0
total_characters = 4

player_characters = [
    {"name": "Char1", "stats": player1_stats, "hp": player_hp_list[0]},
    {"name": "Char2", "stats": player2_stats, "hp": player_hp_list[1]},
    {"name": "Char3", "stats": player3_stats, "hp": player_hp_list[2]},
    {"name": "Char4", "stats": player4_stats, "hp": player_hp_list[3]},
]

def draw_player_stats():
    idx = current_character_turn
    stats = player_stats_list[idx]
    stat_lines = [
        f"ATK: {stats['attack']}",
        f"DEF: {stats['defense']}",
        f"SPC ATK: {stats['special_attack']}",
        f"RES: {stats['resistance']}"
    ]
    x = screen_width - 744
    y = screen_height - 378
    for i, stat in enumerate(stat_lines):
        stat_surface = font_medium.render(stat, True, (255, 255, 255))
        screen.blit(stat_surface, (x, y + i * 72))

def draw_ui():
    if not target_select_mode and not timer_active and not special_select_mode:
        screen.blit(seperator1_image, (seperator1_x, seperator1_y))
        draw_attack_button()
        draw_special_button()
        draw_items_button()
        draw_run_button()
        draw_button_highlight()
        draw_player_stats()
    elif special_select_mode:
        draw_special_select_menu()
    elif target_select_mode:
        screen.blit(seperator1_image, (seperator1_x, seperator1_y))
        instructions = [
            "Press ESC to go back",
            "Press A or D to switch",
            "Press ENTER to attack"
        ]
        for i, text in enumerate(instructions):
            instr_surface = font_large.render(text, True, (255, 255, 255))
            instr_x = 24
            instr_y = screen_height - 378 + i * 120
            screen.blit(instr_surface, (instr_x, instr_y))
    elif timer_active:
        screen.blit(seperator2_image, (seperator1_x, seperator1_y))

def draw_player_characters():
    screen.blit(character1_image, character_positions[0])
    screen.blit(character2_image, character_positions[1])
    screen.blit(character3_image, character_positions[2])
    screen.blit(character4_image, character_positions[3])
    char_x, char_y = character_positions[current_character_turn]
    char_images = [character1_image, character2_image, character3_image, character4_image]
    char_img = char_images[current_character_turn]
    arrow_rect = arrow_image.get_rect(midbottom=(char_x + char_img.get_width() // 2, char_y - 10))
    screen.blit(arrow_image, arrow_rect)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if special_select_mode:
                if event.key == pygame.K_w:
                    selected_special_index = (selected_special_index - 1) % len(special_attack_names)
                elif event.key == pygame.K_s:
                    selected_special_index = (selected_special_index + 1) % len(special_attack_names)
                elif event.key == pygame.K_RETURN:
                    special_select_mode = False
                    target_select_mode = True
                    target_action = "special"
                elif event.key == pygame.K_ESCAPE:
                    special_select_mode = False
            elif not timer_active:
                if target_select_mode:
                    if event.key == pygame.K_a:
                        selected_enemy_index = (selected_enemy_index - 1) % len(enemies)
                    elif event.key == pygame.K_d:
                        selected_enemy_index = (selected_enemy_index + 1) % len(enemies)
                    elif event.key == pygame.K_RETURN:
                        timer_active = True
                        timer_start_time = time.time()
                        if target_action == "attack":
                            timer_duration = 10
                            questions = [generate_question()]
                        elif target_action == "special":
                            timer_duration = 45
                            questions = [generate_special_question()]
                        current_question_index = 0
                        player_answer = ""
                        correct_answers = 0
                        target_select_mode = False
                        target_action = None
                    elif event.key == pygame.K_ESCAPE:
                        target_select_mode = False
                        target_action = None
                else:
                    if event.key == pygame.K_w:
                        if selected_button > 1:
                            selected_button -= 2
                    elif event.key == pygame.K_s:
                        if selected_button < 2:
                            selected_button += 2
                    elif event.key == pygame.K_a:
                        if selected_button % 2 == 1:
                            selected_button -= 1
                    elif event.key == pygame.K_d:
                        if selected_button % 2 == 0:
                            selected_button += 1
                    elif event.key == pygame.K_RETURN:
                        if selected_button == 0:
                            target_select_mode = True
                            target_action = "attack"
                        elif selected_button == 1:
                            special_select_mode = True
                            selected_special_index = 0
                        elif selected_button == 2:
                            print("Items button selected!")
                        elif selected_button == 3:
                            print("Run button selected!")
                            running = False
            else:
                if event.key == pygame.K_RETURN:
                    if current_question_index < len(questions):
                        if player_answer.strip() == "":
                            print("Incorrect! (Blank answer)")
                            if target_action == "attack" or selected_button == 0:
                                correct_answers = max(0, correct_answers - 1)
                                print(f"Damage reduced! Total correct answers: {correct_answers}")
                        elif evaluate_question(questions[current_question_index], player_answer):
                            print("Correct!")
                            correct_answers += 1
                        else:
                            print("Incorrect!")
                            if target_action == "attack" or selected_button == 0:
                                correct_answers = max(0, correct_answers - 1)
                                print(f"Damage reduced! Total correct answers: {correct_answers}")
                            elif target_action == "special" or selected_button == 1:
                                print("No damage dealt for incorrect special answer.")
                        current_question_index += 1
                        player_answer = ""
                        if (target_action == "special" or selected_button == 1):
                            timer_active = False
                            enemy = enemies[selected_enemy_index]
                            idx = current_character_turn
                            stats = player_stats_list[idx]
                            special_damage = max(0, stats["special_attack"] - enemy["resistance"])
                            enemy["hp"] -= special_damage
                            if enemy["hp"] < 0:
                                enemy["hp"] = 0
                            print(f"Special attack dealt {special_damage} damage to {enemy['name']}! {enemy['name']} HP: {enemy['hp']}")
                            current_character_turn = (current_character_turn + 1) % total_characters
                        elif (target_action == "attack" or selected_button == 0) and timer_active:
                            questions.append(generate_question())
                elif event.key == pygame.K_BACKSPACE:
                    player_answer = player_answer[:-1]
                elif event.unicode.isdigit() or (event.unicode == "-" and len(player_answer) == 0):
                    player_answer += event.unicode
                elif event.key == pygame.K_ESCAPE:
                    timer_active = False
                    print("Attack ended early!")
                    enemy = enemies[selected_enemy_index]
                    idx = current_character_turn
                    stats = player_stats_list[idx]
                    if target_action == "attack" or selected_button == 0:
                        if enemy["hp"] > 0:
                            per_hit_damage = max(0, stats["attack"] - enemy["defense"])
                            total_damage = per_hit_damage * correct_answers
                            enemy["hp"] -= total_damage
                            if enemy["hp"] < 0:
                                enemy["hp"] = 0
                            print(f"Player dealt {total_damage} damage to {enemy['name']}! {enemy['name']} HP: {enemy['hp']}")
                    elif target_action == "special" or selected_button == 1:
                        if enemy["hp"] > 0 and correct_answers > 0:
                            special_damage = max(0, stats["special_attack"] - enemy["resistance"])
                            enemy["hp"] -= special_damage
                            if enemy["hp"] < 0:
                                enemy["hp"] = 0
                            print(f"Special attack dealt {special_damage} damage to {enemy['name']}! {enemy['name']} HP: {enemy['hp']}")
                    current_character_turn = (current_character_turn + 1) % total_characters

    if timer_active:
        elapsed_time = time.time() - timer_start_time
        if elapsed_time >= timer_duration:
            timer_active = False
            print("Timer ended!")
            if target_action == "attack" or selected_button == 0:
                enemy = enemies[selected_enemy_index]
                idx = current_character_turn
                stats = player_stats_list[idx]
                if enemy["hp"] > 0:
                    per_hit_damage = max(0, stats["attack"] - enemy["defense"])
                    total_damage = per_hit_damage * correct_answers
                    enemy["hp"] -= total_damage
                    if enemy["hp"] < 0:
                        enemy["hp"] = 0
                    print(f"Player dealt {total_damage} damage to {enemy['name']}! {enemy['name']} HP: {enemy['hp']}")
                current_character_turn = (current_character_turn + 1) % total_characters
            elif target_action == "special" or selected_button == 1:
                enemy = enemies[selected_enemy_index]
                idx = current_character_turn
                stats = player_stats_list[idx]
                if enemy["hp"] > 0:
                    special_damage = max(0, stats["special_attack"] - enemy["resistance"])
                    enemy["hp"] -= special_damage
                    if enemy["hp"] < 0:
                        enemy["hp"] = 0
                    print(f"Special attack dealt {special_damage} damage to {enemy['name']}! {enemy['name']} HP: {enemy['hp']}")
                current_character_turn = (current_character_turn + 1) % total_characters

    screen.blit(background_image, (0, 0))
    draw_player_characters()
    draw_enemies()
    draw_player_hp()
    draw_enemy_hp()
    draw_ui()
    if timer_active:
        draw_timer_and_question()
    pygame.display.flip()

pygame.quit()
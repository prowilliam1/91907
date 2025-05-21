import pygame
import random
import time
from Stats.Character_Stats import get_player_stats
from Stats.Weapon_Stats import get_weapon_stats, get_special_question

pygame.init()

screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Battle Screen")

background_image = pygame.image.load("Graphics\\Backgrounds\\Battle Sequence.png")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

character1_image = pygame.image.load("Graphics\\Characters\\Example 1.png")

character1_x = 100
character1_y = 300

enemy1_image = pygame.image.load("Graphics\\Characters\\Enemy Dummy.png")

enemy1_x = 1000
enemy1_y = 300

current_level = 1
player_stats = get_player_stats(current_level)
player_hp = player_stats["hp"]
player_attack = player_stats["attack"]
player_special_attack = player_stats["special_attack"]
enemy_max_hp = 100
enemy_hp = enemy_max_hp

equipped_weapon = "Sword"
weapon_stats = get_weapon_stats(equipped_weapon)
player_attack += weapon_stats["attack"]
player_special_attack += weapon_stats["special_attack"]

def get_health_bar_image():
    hp_percentage = (enemy_hp / enemy_max_hp) * 100
    if hp_percentage <= 0:
        return pygame.image.load("Graphics\\UI\\Health\\Health Bar 0%.png")
    health_bar_number = (hp_percentage // 10) * 10
    return pygame.image.load(f"Graphics\\UI\\Health\\Health Bar {health_bar_number}%.png")

custom_font_path = "Fonts\\Font.otf"
font = pygame.font.Font(custom_font_path, 36)
font_large = pygame.font.Font(custom_font_path, 48)

attack_button_width, attack_button_height = 200, 40
attack_button_x, attack_button_y = 40, 580

special_button_width, special_button_height = 200, 40
special_button_x, special_button_y = 260, 580

items_button_width, items_button_height = 200, 40
items_button_x, items_button_y = 40, 640

run_button_width, run_button_height = 200, 40
run_button_x, run_button_y = 260, 640

attack_button_image = pygame.image.load("Graphics\\UI\\Buttons\\ATK BTN.png")
special_button_image = pygame.image.load("Graphics\\UI\\Buttons\\SPC BTN.png")
items_button_image = pygame.image.load("Graphics\\UI\\Buttons\\ITM BTN.png")
run_button_image = pygame.image.load("Graphics\\UI\\Buttons\\RUN BTN.png")
highlight_button_image = pygame.image.load("Graphics\\UI\\Buttons\\BTN OTL.png")

def draw_attack_button():
    screen.blit(attack_button_image, (attack_button_x, attack_button_y))
    text_surface = font.render("Attack", True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(attack_button_x + attack_button_width // 2, (attack_button_y + attack_button_height // 2) - 8))
    screen.blit(text_surface, text_rect)

def draw_special_button():
    screen.blit(special_button_image, (special_button_x, special_button_y))
    text_surface = font.render("Special", True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(special_button_x + special_button_width // 2, (special_button_y + special_button_height // 2) - 8))
    screen.blit(text_surface, text_rect)

def draw_items_button():
    screen.blit(items_button_image, (items_button_x, items_button_y))
    text_surface = font.render("Items", True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(items_button_x + items_button_width // 2, (items_button_y + items_button_height // 2) - 8))
    screen.blit(text_surface, text_rect)

def draw_run_button():
    screen.blit(run_button_image, (run_button_x, run_button_y))
    text_surface = font.render("Run", True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(run_button_x + run_button_width // 2, (run_button_y + run_button_height // 2) - 8))
    screen.blit(text_surface, text_rect)

selected_button = 0
button_positions = [(40, 580), (260, 580), (40, 640), (260, 640)]

def draw_button_highlight():
    screen.blit(highlight_button_image, (button_positions[selected_button][0] - 5, button_positions[selected_button][1] - 5))

def draw_hp():
    player_hp_text = font.render(f"Player HP: {player_hp} (Level {current_level})", True, (255, 255, 255))
    weapon_text = font.render(f"Weapon: {equipped_weapon}", True, (255, 255, 255))
    enemy_hp_text = font.render(f"Enemy HP: {enemy_hp}", True, (255, 255, 255))
    screen.blit(player_hp_text, (50, 50))
    screen.blit(weapon_text, (50, 90))
    screen.blit(enemy_hp_text, (screen_width - 250, 50))

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
    timer_text = font_large.render(f"Time Left: {int(remaining_time)}s", True, timer_color)
    screen.blit(timer_text, (screen_width // 2 - 100, 50))
    if current_question_index < len(questions):
        question = questions[current_question_index]
        if isinstance(question, tuple):
            question_text = str(question[0])
        else:
            question_text = "Invalid question format"
        question_surface = font_large.render(question_text, True, (255, 255, 255))
        screen.blit(question_surface, (screen_width // 2 - 100, 150))
        answer_text = font_large.render(player_answer, True, (255, 255, 255))
        screen.blit(answer_text, (screen_width // 2 - 100, 200))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if not timer_active:
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
                        if enemy_hp > 0:
                            timer_active = True
                            timer_start_time = time.time()
                            timer_duration = 15
                            questions = [generate_question()]
                            current_question_index = 0
                            player_answer = ""
                            correct_answers = 0
                    elif selected_button == 1:
                        if enemy_hp > 0:
                            timer_active = True
                            timer_start_time = time.time()
                            timer_duration = 45
                            questions = [generate_special_question()]
                            current_question_index = 0
                            player_answer = ""
                            correct_answers = 0
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
                            if selected_button == 0:
                                correct_answers = max(0, correct_answers - 1)
                                print(f"Damage reduced! Total correct answers: {correct_answers}")
                            elif selected_button == 1:
                                print("No damage dealt for incorrect special answer.")
                        elif evaluate_question(questions[current_question_index], player_answer):
                            print("Correct!")
                            correct_answers += 1
                        else:
                            print("Incorrect!")
                            if selected_button == 0:
                                correct_answers = max(0, correct_answers - 1)
                                print(f"Damage reduced! Total correct answers: {correct_answers}")
                            elif selected_button == 1:
                                print("No damage dealt for incorrect special answer.")
                        current_question_index += 1
                        player_answer = ""
                        if selected_button == 1:
                            timer_active = False
                            if correct_answers > 0:
                                enemy_hp -= player_special_attack
                                if enemy_hp < 0:
                                    enemy_hp = 0
                                print(f"Special attack dealt {player_special_attack} damage! Enemy HP: {enemy_hp}")
                        elif selected_button == 0 and timer_active:
                            questions.append(generate_question())
                elif event.key == pygame.K_BACKSPACE:
                    player_answer = player_answer[:-1]
                elif event.unicode.isdigit() or (event.unicode == "-" and len(player_answer) == 0):
                    player_answer += event.unicode

    if timer_active:
        elapsed_time = time.time() - timer_start_time
        if elapsed_time >= timer_duration:
            timer_active = False
            print("Timer ended!")
            if enemy_hp > 0:
                if selected_button == 1:
                    if current_question_index < len(questions):
                        print("No answer provided for special question.")
                        print("No damage dealt for unanswered special question.")
                else:
                    if current_question_index < len(questions):
                        print("No answer provided for attack question.")
                        print(f"Total correct answers: {correct_answers}")
                    total_damage = player_attack * correct_answers
                    enemy_hp -= total_damage
                    if enemy_hp < 0:
                        enemy_hp = 0
                    print(f"Player dealt {total_damage} damage! Enemy HP: {enemy_hp}")

    screen.blit(background_image, (0, 0))
    screen.blit(character1_image, (character1_x, character1_y))
    screen.blit(enemy1_image, (enemy1_x, enemy1_y))
    screen.blit(get_health_bar_image(), (enemy1_x - 12, enemy1_y - 28))
    draw_hp()
    draw_attack_button()
    draw_special_button()
    draw_items_button()
    draw_run_button()
    draw_button_highlight()
    if timer_active:
        draw_timer_and_question()
    pygame.display.flip()

pygame.quit()
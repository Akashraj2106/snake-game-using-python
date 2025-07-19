gitimport pygame
import time
import random
import os

pygame.init()
pygame.mixer.init()

# Colors
cream_white = (255, 253, 208)
gold_yellow = (218, 165, 32)
earthy_orange = (255, 140, 0)
pastel_green = (143, 188, 143)
soft_red = (220, 20, 60)
black = (0, 0, 0)
blue = (50, 153, 213)
green = (0, 255, 0)

# Display
dis_width = 800
dis_height = 600
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game by AkashRAj')
clock = pygame.time.Clock()
snake_block = 20

# Fonts
font_style = pygame.font.SysFont("Segoe Print", 28)
score_font = pygame.font.SysFont("Segoe Print", 32, bold=True)
title_font = pygame.font.SysFont("Garamond", 60, bold=True)
small_font = pygame.font.SysFont("Segoe Print", 20)

# Music
music_path = ""
pygame.mixer.music.set_volume(0.5)
if os.path.isfile(music_path):
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(-1)

# Background
bg_image_path = "background_image.jpg"
if os.path.isfile(bg_image_path):
    background = pygame.image.load(bg_image_path)
    background = pygame.transform.scale(background, (dis_width, dis_height))
else:
    background = None

# Eating sound
eat_sound_path = "eat_sound.mp3"
eat_sound = pygame.mixer.Sound(eat_sound_path) if os.path.isfile(eat_sound_path) else None

def your_score(score):
    value = small_font.render("Score: " + str(score), True, earthy_orange)
    dis.blit(value, [10, 10])

# Draw snake with white border
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, (255, 255, 255), [x[0] - 2, x[1] - 2, snake_block + 4, snake_block + 4])
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

# Message display
def message(msg, color, y_offset=0, font=None, shadow=True):
    if font is None:
        font = font_style
    mesg = font.render(msg, True, color)
    mesg_rect = mesg.get_rect(center=(dis_width / 2, dis_height / 3 + y_offset))
    if shadow:
        shadow_text = font.render(msg, True, (0, 0, 0))
        shadow_rect = shadow_text.get_rect(center=(dis_width / 2 + 2, dis_height / 3 + y_offset + 2))
        dis.blit(shadow_text, shadow_rect)
    dis.blit(mesg, mesg_rect)

# Head aura
def draw_visualization(snake_list):
    if len(snake_list) > 0:
        head_x, head_y = snake_list[-1]
        for i in range(5, 0, -1):
            radius = i * 8
            alpha = max(20, 50 - i*10)
            surface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
            pygame.draw.circle(surface, (255, 255, 255, alpha), (radius, radius), radius)
            dis.blit(surface, (head_x - radius + snake_block//2, head_y - radius + snake_block//2))

# Main Game Loop
def game_loop(snake_speed):
    game_over = False
    game_close = False
    x1 = dis_width / 2
    y1 = dis_height / 2
    x1_change = 0
    y1_change = 0
    snake_list = []
    length_of_snake = 1
    foodx = round(random.randrange(0, dis_width - snake_block) / 20.0) * 20.0
    foody = round(random.randrange(0, dis_height - snake_block) / 20.0) * 20.0

    while not game_over:
        while game_close:
            dis.blit(background, (0, 0)) if background else dis.fill(blue)
            message("You Lost! \U0001F622 Press C-Play Again or Q-Quit", soft_red)
            your_score(length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        return
                    if event.key == pygame.K_c:
                        game_loop(snake_speed)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change

        dis.blit(background, (0, 0)) if background else dis.fill(blue)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])

        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        draw_visualization(snake_list)
        our_snake(snake_block, snake_list)
        your_score(length_of_snake - 1)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            if eat_sound:
                eat_sound.play()
            foodx = round(random.randrange(0, dis_width - snake_block) / 20.0) * 20.0
            foody = round(random.randrange(0, dis_height - snake_block) / 20.0) * 20.0
            length_of_snake += 1

        clock.tick(snake_speed)

# Difficulty Menu
def difficulty_selection_menu():
    selecting = True
    selected_speed = None
    dis.blit(background, (0, 0)) if background else dis.fill(blue)
    message("Select Difficulty Level", gold_yellow, y_offset=-100, font=title_font)
    message("1. Easy (Speed: 10)", cream_white, y_offset=-30)
    message("2. Medium (Speed: 15)", cream_white, y_offset=10)
    message("3. Hard (Speed: 22)", cream_white, y_offset=50)
    message("Press 1, 2, or 3 to choose level", pastel_green, y_offset=130)
    pygame.display.update()

    while selecting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected_speed = 10
                    selecting = False
                elif event.key == pygame.K_2:
                    selected_speed = 15
                    selecting = False
                elif event.key == pygame.K_3:
                    selected_speed = 22
                    selecting = False

    return selected_speed

# Main Menu
def main_menu():
    running = True
    while running:
        dis.blit(background, (0, 0)) if background else dis.fill(blue)
        message("Snake Game", gold_yellow, y_offset=-150, font=title_font)
        message("1. Play Game", cream_white, y_offset=-50)
        message("2. Quit", cream_white, y_offset=0)
        message("Press 1 or 2 to choose", pastel_green, y_offset=150)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    speed = difficulty_selection_menu()
                    game_loop(speed)
                elif event.key == pygame.K_2:
                    pygame.quit()
                    quit()

if __name__ == "__main__":
    main_menu()

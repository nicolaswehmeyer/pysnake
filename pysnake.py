#!/usr/bin/env python
import pygame
import time
import random

pygame.init()

# Define colors
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
BLINKING_COLOR = (255, 255, 255)

# Set up the game window
DIS_WIDTH = 600
DIS_HEIGHT = 400
DIS = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
pygame.display.set_caption('Snake Game')

# Set up the snake and food
SNAKE_BLOCK = 10
SNAKE_SPEED = 15

FONT_STYLE = pygame.font.SysFont(None, 50)

# Function to draw the snake
def draw_snake(snake_block, snake_list, snake_color=GREEN):
    for segment in snake_list:
        pygame.draw.rect(DIS, snake_color, [segment[0], segment[1], snake_block, snake_block])

# Function to display the score
def display_score(score):
    score_text = FONT_STYLE.render("Score: " + str(score), True, BLUE)
    DIS.blit(score_text, [0, 0])

# Function for the game over screen
def game_over_screen(length_of_snake):
    over_font = pygame.font.SysFont(None, 75)
    over_text = over_font.render("GAME OVER", True, RED)
    DIS.blit(over_text, [DIS_WIDTH / 5, DIS_HEIGHT / 3])

    message = FONT_STYLE.render("'Q' to quit or 'R' to retry", True, RED)
    DIS.blit(message, [DIS_WIDTH / 6, DIS_HEIGHT / 2])

    display_score(length_of_snake - 1)
    pygame.display.update()

    pygame.time.wait(2000)  # Wait for 2 seconds

# Function to run the game
def game_loop():
    global SNAKE_SPEED  # Use global variable for SNAKE_SPEED

    game_over = False
    game_close = False

    x1 = DIS_WIDTH / 2
    y1 = DIS_HEIGHT / 2

    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1

    foodx = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
    foody = round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0

    blinking_duration = 500  # milliseconds
    blinking_timer = 0
    blinking_color_flag = False

    while not game_over:

        while game_close:
            DIS.fill(BLACK)
            game_over_screen(length_of_snake)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_r:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:  # Ignore opposite direction
                    x1_change = -SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -SNAKE_BLOCK
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = SNAKE_BLOCK
                    x1_change = 0

        if x1 >= DIS_WIDTH or x1 < 0 or y1 >= DIS_HEIGHT or y1 < 0:
            game_close = True
            game_over_screen(length_of_snake)  # Display game over screen

        x1 += x1_change
        y1 += y1_change
        DIS.fill(BLACK)

        # Blinking logic
        if blinking_timer > 0:
            blinking_timer -= pygame.time.Clock().get_rawtime()
            if blinking_timer <= 0:
                blinking_color_flag = not blinking_color_flag
                blinking_timer = blinking_duration
        else:
            blinking_color_flag = False

        # Change color based on blinking flag
        snake_color = BLINKING_COLOR if blinking_color_flag else GREEN

        pygame.draw.rect(DIS, RED, [foodx, foody, SNAKE_BLOCK, SNAKE_BLOCK])
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        draw_snake(SNAKE_BLOCK, snake_list, snake_color)
        display_score(length_of_snake - 1)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
            foody = round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
            length_of_snake += 1
            SNAKE_SPEED += 1  # Increase snake speed

            # Reset blinking timer
            blinking_timer = blinking_duration
            blinking_color_flag = True

        pygame.time.Clock().tick(SNAKE_SPEED)

    pygame.quit()
    quit()

if __name__ == '__main__':
    game_loop()

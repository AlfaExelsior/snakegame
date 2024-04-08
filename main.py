import pygame
import random
import csv

WIDTH = 400
HEIGHT = 400
CELL_SIZE = 20
SPEED = 5       

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Exelsior's Snake Game")

snake_body = [(WIDTH//2, HEIGHT//2)]  
snake_direction = (0, -1)          

with open('scores.csv', 'w', newline='') as csvfile:
    fields = ['Name', 'Score']
    writer = csv.writer(csvfile)
    writer.writerow(fields)  

def generate_food():
    while True:
        food_x = random.randint(0, WIDTH // CELL_SIZE - 1) * CELL_SIZE
        food_y = random.randint(0, HEIGHT // CELL_SIZE - 1) * CELL_SIZE
        if (food_x, food_y) not in snake_body:
            return food_x, food_y

food = generate_food()

def game_over_screen():
    game_over_surface = pygame.Surface((WIDTH, HEIGHT))
    game_over_surface.fill(BLACK)

    font = pygame.font.SysFont("Arial", 32)
    message = font.render("Game Over! We'll see you soon!", True, WHITE)

    game_over_surface.blit(message, (WIDTH // 2 - message.get_width() // 2,
                                   HEIGHT // 2 - message.get_height() // 2))

    screen.blit(game_over_surface, (0, 0))
    pygame.display.update()

    pygame.time.wait(3000)


game_running = True
clock = pygame.time.Clock()
while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_direction != (0, 1):
                snake_direction = (0, -1)
            elif event.key == pygame.K_DOWN and snake_direction != (0, -1):
                snake_direction = (0, 1)
            elif event.key == pygame.K_LEFT and snake_direction != (1, 0):
                snake_direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and snake_direction != (-1, 0):
                snake_direction = (1, 0)

    new_head = (snake_body[0][0] + snake_direction[0] * CELL_SIZE,
                snake_body[0][1] + snake_direction[1] * CELL_SIZE)

    if (new_head[0] < 0 or new_head[0] >= WIDTH or
        new_head[1] < 0 or new_head[1] >= HEIGHT or
        new_head in snake_body[1:]):
        game_running = False
        game_over_screen()

    if new_head == food:
        food = generate_food()
        if len(snake_body) % 5 == 0:
            SPEED += 1
    else:
        snake_body.pop()

    snake_body.insert(0, new_head)

    if not game_running:
        name = input("Enter your name: ")
        score = len(snake_body) - 1 

        with open('scores.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([name, score])

    screen.fill(WHITE)
    for cell in snake_body:
        pygame.draw.rect(screen, GREEN, (cell[0], cell[1], CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, RED, (food[0], food[1], CELL_SIZE, CELL_SIZE))
    pygame.display.update()

    clock.tick(SPEED)  

pygame.quit()

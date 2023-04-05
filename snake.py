import pygame
import sys
import random

import pygame.freetype


pygame.init()

# Screen dimensions
WIDTH = 640
HEIGHT = 480
CELL_SIZE = 20

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.body = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = (CELL_SIZE, 0)
    
    def move(self):
        new_head = (self.body[0][0] + self.direction[0], self.body[0][1] + self.direction[1])
        self.body.insert(0, new_head)
        self.body.pop()

    def grow(self):
        new_head = (self.body[0][0] + self.direction[0], self.body[0][1] + self.direction[1])
        self.body.insert(0, new_head)

    def change_direction(self, new_direction):
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction

    def draw(self, surface):
        for part in self.body:
            pygame.draw.rect(surface, GREEN, pygame.Rect(part[0], part[1], CELL_SIZE, CELL_SIZE))

class Food:
    def __init__(self):
        self.position = self.generate_random_position()

    def generate_random_position(self):
        x = random.randrange(0, WIDTH, CELL_SIZE)
        y = random.randrange(0, HEIGHT, CELL_SIZE)
        return (x, y)

    def draw(self, surface):
        pygame.draw.rect(surface, RED, pygame.Rect(self.position[0], self.position[1], CELL_SIZE, CELL_SIZE))

def check_collision(snake, food):
    if snake.body[0] == food.position:
        snake.grow()
        food.position = food.generate_random_position()

def check_game_over(snake):
    head = snake.body[0]
    if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT or head in snake.body[1:]:
        return True
    return False

def main():
    snake = Snake()
    food = Food()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction((0, -CELL_SIZE))
                elif event.key == pygame.K_DOWN:
                    snake.change_direction((0, CELL_SIZE))
                elif event.key == pygame.K_LEFT:
                    snake.change_direction((-CELL_SIZE, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction((CELL_SIZE, 0))

        snake.move()
        check_collision(snake, food)

        if check_game_over(snake):
            break

        screen.fill(WHITE)
        snake.draw(screen)
        food.draw(screen)
        pygame.display.flip()

        clock.tick(10)

def menu():
    font = pygame.freetype.SysFont('Arial', 36)
    start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 100)

    while True:
        screen.fill(WHITE)
        font.render_to(screen, (WIDTH // 2 - 60, HEIGHT // 2 - 25), "START", RED)
        pygame.draw.rect(screen, RED, start_button, 3)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    return

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    while True:
        menu()
        main()

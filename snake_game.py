import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 800
GRID_SIZE = 20
GRID_WIDTH = WINDOW_SIZE // GRID_SIZE
GRID_HEIGHT = WINDOW_SIZE // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Initialize screen
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH//2, GRID_HEIGHT//2)]
        self.direction = (1, 0)
        self.grow = False

    def move(self):
        current = self.positions[0]
        x = current[0] + self.direction[0]
        y = current[1] + self.direction[1]
        
        # Check for wrap-around
        x = x % GRID_WIDTH
        y = y % GRID_HEIGHT
        
        self.positions.insert(0, (x, y))
        if not self.grow:
            self.positions.pop()
        self.grow = False

    def change_direction(self, new_direction):
        # Prevent 180-degree turns
        opposite = (-self.direction[0], -self.direction[1])
        if new_direction != opposite:
            self.direction = new_direction

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = self.generate_food()
        self.score = 0

    def generate_food(self):
        while True:
            food = (random.randint(0, GRID_WIDTH-1), 
                   random.randint(0, GRID_HEIGHT-1))
            if food not in self.snake.positions:
                return food

    def check_collision(self):
        head = self.snake.positions[0]
        return head in self.snake.positions[1:]

    def update(self):
        self.snake.move()
        
        # Check if snake ate food
        if self.snake.positions[0] == self.food:
            self.snake.grow = True
            self.food = self.generate_food()
            self.score += 1

        # Check for collision
        if self.check_collision():
            return False
        return True

    def draw(self):
        screen.fill(BLACK)
        
        # Draw snake
        for position in self.snake.positions:
            rect = (position[0] * GRID_SIZE, position[1] * GRID_SIZE,
                   GRID_SIZE-2, GRID_SIZE-2)
            pygame.draw.rect(screen, GREEN, rect)
        
        # Draw food
        rect = (self.food[0] * GRID_SIZE, self.food[1] * GRID_SIZE,
               GRID_SIZE-2, GRID_SIZE-2)
        pygame.draw.rect(screen, RED, rect)
        
        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        screen.blit(score_text, (10, 10))
        
        pygame.display.flip()

def main():
    game = Game()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.snake.change_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    game.snake.change_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    game.snake.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    game.snake.change_direction((1, 0))
        
        if not game.update():
            running = False
        
        game.draw()
        clock.tick(10)  # Control game speed

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()

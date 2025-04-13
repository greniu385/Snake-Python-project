import pygame
import random
import sys

pygame.init()

#dimensions
WINDOW_SIZE = 400  
GRID_SIZE = 20
GRID_COUNT = WINDOW_SIZE // GRID_SIZE
FPS = 10

#colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

#setting up the screen
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [(WINDOW_SIZE // 2, WINDOW_SIZE // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN
        self.score = 0
        self.game_over = False

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = ((cur[0] + (x * GRID_SIZE)), (cur[1] + (y * GRID_SIZE)))
        
        #checking for wall collision
        if (new[0] < 0 or new[0] >= WINDOW_SIZE or 
            new[1] < 0 or new[1] >= WINDOW_SIZE):
            self.game_over = True
            return False
            
        if new in self.positions[3:]:
            self.game_over = True
            return False
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
            return True

    def reset(self):
        self.length = 1
        self.positions = [(WINDOW_SIZE // 2, WINDOW_SIZE // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0
        self.game_over = False

    def render(self, surface):
        for p in self.positions:
            pygame.draw.rect(surface, self.color, (p[0], p[1], GRID_SIZE, GRID_SIZE))

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_COUNT - 1) * GRID_SIZE,
                        random.randint(0, GRID_COUNT - 1) * GRID_SIZE)

    def render(self, surface):
        pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], GRID_SIZE, GRID_SIZE))

#directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

def show_game_over(screen, score):
    font = pygame.font.Font(None, 50)
    game_over_text = font.render('GAME OVER', True, RED)
    score_text = font.render(f'Score: {score}', True, WHITE)
    restart_text = font.render('Press R to restart', True, WHITE)
    
    screen.blit(game_over_text, (WINDOW_SIZE//2 - game_over_text.get_width()//2, WINDOW_SIZE//2 - 80))
    screen.blit(score_text, (WINDOW_SIZE//2 - score_text.get_width()//2, WINDOW_SIZE//2))
    screen.blit(restart_text, (WINDOW_SIZE//2 - restart_text.get_width()//2, WINDOW_SIZE//2 + 80))
    pygame.display.update()

def main():
    snake = Snake()
    food = Food()
    font = pygame.font.Font(None, 36)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if snake.game_over:
                    if event.key == pygame.K_r:
                        snake.reset()
                        food.randomize_position()
                else:
                    if event.key == pygame.K_UP and snake.direction != DOWN:
                        snake.direction = UP
                    elif event.key == pygame.K_DOWN and snake.direction != UP:
                        snake.direction = DOWN
                    elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                        snake.direction = LEFT
                    elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                        snake.direction = RIGHT

        if not snake.game_over:
            if not snake.update():
                show_game_over(screen, snake.score)
                continue

            if snake.get_head_position() == food.position:
                snake.length += 1
                snake.score += 1
                food.randomize_position()

            screen.fill(BLACK)
            snake.render(screen)
            food.render(screen)
            
            #displaying points
            score_text = font.render(f'Score: {snake.score}', True, WHITE)
            screen.blit(score_text, (10, 10))
            
            pygame.display.update()
            clock.tick(FPS)
        else:
            show_game_over(screen, snake.score)
            clock.tick(FPS)

if __name__ == '__main__':
    main()

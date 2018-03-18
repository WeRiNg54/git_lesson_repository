import pygame
import sys
import random
import time

pygame.font.init()

width = 720
height = 460


class Menu:
    def __init__(self, punkts=None):
        if punkts is None:
            punkts = [300, 250, u'Punkt', (150, 75, 0), (0, 0, 0), 1]
        self.surface = pygame.display.set_mode((width, height), 0, 32)
        self.punkts = punkts

    def render(self, surface, font, num_punkt):
        for i in self.punkts:
            if num_punkt == i[5]:
                surface.blit(font.render(i[2], 1, i[4]), (i[0], i[1]))
            else:
                surface.blit(font.render(i[2], 1, i[3]), (i[0], i[1]))

    def menu(self):
        done = True
        font_menu = pygame.font.SysFont('monaco', 50)
        pygame.key.set_repeat(0, 0)
        pygame.mouse.set_visible(True)
        punkt = 0
        while done:
            self.surface.fill((0, 255, 0))

            mp = pygame.mouse.get_pos()
            for i in self.punkts:
                if mp[0] > i[0] and mp[0] < i[0] + 155 and mp[1] > i[1] and mp[1] > i[1]:
                    punkt = i[5]
                self.render(self.surface, font_menu, punkt)

                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        sys.exit()
                    if e.type == pygame.KEYDOWN:
                        if e.type == pygame.K_ESCAPE:
                            sys.exit()
                        if e.key == pygame.K_UP or e.key == ord('w'):
                            if punkt > 0:
                                punkt -= 1
                        if e.key == pygame.K_DOWN or e.key == ord('s'):
                            if punkt < len(self.punkts) - 1:
                                punkt += 1
                    if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                        if punkt == 0:
                            done = False
                        if punkt == 1:
                            sys.exit()

            self.surface.blit(self.surface, (0, 0))
            pygame.display.flip()


punkts = [(300, 150, u'Game', (150, 75, 0), (0, 0, 0), 0),
          (300, 250, u'Quit', (150, 75, 0), (0, 0, 0), 1)]

play = Menu(punkts)
play.menu()


class Game:
    def __init__(self):

        self.black = pygame.Color(0, 0, 0)
        self.red = pygame.Color(255, 0, 0)
        self.green = pygame.Color(0, 255, 0)
        self.blue = pygame.Color(0, 0, 255)

        self.fps_controller = pygame.time.Clock()

        self.score = 0

    def set_surface(self):
        self.surface = pygame.display.set_mode((
            width, height))
        pygame.display.set_caption('Snake Game')

    def checker(self):
        check_errors = pygame.init()
        if check_errors[1] > 0:
            sys.exit()
        else:
            print('Ok')

    def event(self, change):

        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RIGHT or e.key == ord('d'):
                    change = "RIGHT"
                elif e.key == pygame.K_LEFT or e.key == ord('a'):
                    change = "LEFT"
                elif e.key == pygame.K_UP or e.key == ord('w'):
                    change = "UP"
                elif e.key == pygame.K_DOWN or e.key == ord('s'):
                    change = "DOWN"
                elif e.key == pygame.K_ESCAPE or e.key == pygame.K_DELETE:
                    play.menu()
        return change

    def screen(self):
        pygame.display.flip()
        game.fps_controller.tick(23)

    def show_score(self, choice=1):
        score_font = pygame.font.SysFont('monaco', 24)
        score_surf = score_font.render(
            'Score: {0}'.format(self.score), True, self.black)
        score_rect = score_surf.get_rect()
        if choice == 1:
            score_rect.midtop = (80, 10)
        else:
            score_rect.midtop = (360, 120)
        self.surface.blit(score_surf, score_rect)

    def game_over(self):
        game_font = pygame.font.SysFont('monaco', 72)
        game_surf = game_font.render('Game over', True, self.red)
        game_rect = game_surf.get_rect()
        game_rect.midtop = (360, 15)
        self.surface.blit(game_surf, game_rect)
        self.show_score(0)
        pygame.display.flip()
        pygame.mixer.music.load("sounds\lose.ogg")
        pygame.mixer.music.play()
        time.sleep(4)
        pygame.quit()
        sys.exit()


class Snake:
    def __init__(self, snake_color):
        self.snake_head_pos = [150, 100]
        self.snake_body = [[150, 100], [140, 100], [130, 100]]
        self.snake_color = snake_color
        self.direction = "RIGHT"
        self.change = self.direction

    def direction_and_change(self):
        if any((self.change == "RIGHT" and not self.direction == "LEFT",
                self.change == "LEFT" and not self.direction == "RIGHT",
                self.change == "UP" and not self.direction == "DOWN",
                self.change == "DOWN" and not self.direction == "UP")):
            self.direction = self.change

    def change_head(self):
        if self.direction == "RIGHT":
            self.snake_head_pos[0] += 10
        elif self.direction == "LEFT":
            self.snake_head_pos[0] -= 10
        elif self.direction == "UP":
            self.snake_head_pos[1] -= 10
        elif self.direction == "DOWN":
            self.snake_head_pos[1] += 10

    def mechanism_snake(
            self, score, food_pos, width, height):
        self.snake_body.insert(0, list(self.snake_head_pos))
        if (self.snake_head_pos[0] == food_pos[0] and
                self.snake_head_pos[1] == food_pos[1]):
            pygame.mixer.music.load("sounds\eat.ogg")
            pygame.mixer.music.play()

            food_pos = [random.randrange(1, width / 10) * 10,
                        random.randrange(1, height / 10) * 10]
            score += 1
        else:
            self.snake_body.pop()
        return score, food_pos

    def draw_snake(self, surface, surface_color):
        surface.fill(surface_color)
        for pos in self.snake_body:
            pygame.draw.rect(
                surface, self.snake_color, pygame.Rect(
                    pos[0], pos[1], 10, 10))

    def boundaries(self, game_over, width, height):
        if any((
                self.snake_head_pos[0] > width - 10
                or self.snake_head_pos[0] < 0,
                self.snake_head_pos[1] > height - 10
                or self.snake_head_pos[1] < 0
        )):
            game_over()
        for block in self.snake_body[1:]:
            if (block[0] == self.snake_head_pos[0] and
                    block[1] == self.snake_head_pos[1]):
                game_over()


class Food:
    def __init__(self, food_color, width, height):
        self.food_color = food_color
        self.food_size_x = 10
        self.food_size_y = 10
        self.food_pos = [random.randrange(1, width / 10) * 10,
                         random.randrange(1, height / 10) * 10]

    def draw_food(self, surface):
        pygame.draw.rect(
            surface, self.food_color, pygame.Rect(
                self.food_pos[0], self.food_pos[1],
                self.food_size_x, self.food_size_y))


game = Game()
snake = Snake(game.blue)
pygame.mouse.set_visible(False)
food = Food(game.red, width, height)

game.checker()
game.set_surface()

while True:
    snake.change = game.event(snake.change)

    snake.direction_and_change()
    snake.change_head()
    game.score, food.food_pos = snake.mechanism_snake(
        game.score, food.food_pos, width, height)
    snake.draw_snake(game.surface, game.green)

    food.draw_food(game.surface)

    snake.boundaries(
        game.game_over, width, height)

    game.show_score()
    game.screen()

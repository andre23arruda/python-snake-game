import pygame, time
from pygame.locals import *
from utils import *

class Wall:
    def __init__(self, surface_game, local_path):
        self.surface_game = surface_game
        self.block = pygame.image.load(f'{ local_path }/assets/wall_block.jpg')
        self.coordinates = \
            [[WIDTH - i*BLOCK_SIZE, ZERO] for i in range(int(WIDTH/BLOCK_SIZE) + 1)] + \
            [[WIDTH - i*BLOCK_SIZE, WIDTH - BLOCK_SIZE] for i in range(int(WIDTH/BLOCK_SIZE) + 1)] + \
            [[ZERO, WIDTH - i*BLOCK_SIZE] for i in range(int(WIDTH/BLOCK_SIZE) + 1)] + \
            [[WIDTH - BLOCK_SIZE, WIDTH - i*BLOCK_SIZE] for i in range(int(WIDTH/BLOCK_SIZE) + 1)]

    def draw(self):
        for xy in self.coordinates:
            self.surface_game.blit(
                self.block,
                xy
            )
        pygame.display.flip()

class Apple:
    def __init__(self, surface_game, local_path):
        self.surface_game = surface_game
        self.block = pygame.image.load(f'{ local_path }/assets/apple.png')
        self.coordinates = [
            get_random_number(BLOCK_SIZE),
            get_random_number(BLOCK_SIZE)
        ]

    def draw(self):
        '''Desenha bloco nas coordenadas'''
        self.surface_game.blit(
            self.block,
            self.coordinates
        )
        pygame.display.flip()

    def new(self):
        self.coordinates = [
            get_random_number(BLOCK_SIZE),
            get_random_number(BLOCK_SIZE)
        ]

class Snake:
    def __init__(self, surface_game, local_path, length=1):
        self.surface_game = surface_game
        self.block = pygame.image.load(f'{ local_path }/assets/block.jpg')
        self.first_block = pygame.image.load(f'{ local_path }/assets/first_block.jpg')
        self.direction = 'right'
        self.length = 0
        self.coordinates = [ [START_POSITION - i*BLOCK_SIZE, START_POSITION] for i in range(length) ]
        pygame.display.set_caption(f'Snake game by andre23arruda. Points: { self.length }')

    def draw(self):
        '''Desenha bloco nas coordenadas'''
        for i, xy in enumerate(self.coordinates):
            block = self.block if i != 0 else self.first_block
            self.surface_game.blit(
                block,
                xy
            )
        pygame.display.flip()

    def walk(self, grow_up=False):
        '''Bloco anda de acordo com a direção'''
        if self.direction == 'right':
            x = BLOCK_SIZE
            y = 0
        elif self.direction == 'left':
            x = -BLOCK_SIZE
            y = 0
        elif self.direction == 'up':
            x = 0
            y = -BLOCK_SIZE
        elif self.direction == 'down':
            x = 0
            y = BLOCK_SIZE

        next_block_coordinates = [
            self.coordinates[0][0] + x,
            self.coordinates[0][1] + y
        ]
        self.coordinates.insert(0, next_block_coordinates)
        if not grow_up:
            self.coordinates.pop()
        else:
            self.grow_up()
        self.draw()

    def revert_direction(self):
        self.coordinates.reverse()

    def move_right(self):
        if self.direction == 'left':
            self.revert_direction()
        self.direction = 'right'
    def move_left(self):
        if self.direction == 'right':
            self.revert_direction()
        self.direction = 'left'
    def move_up(self):
        if self.direction == 'down':
            self.revert_direction()
        self.direction = 'up'
    def move_down(self):
        if self.direction == 'up':
            self.revert_direction()
        self.direction = 'down'

    def grow_up(self):
        self.length += 1
        pygame.display.set_caption(f'Snake game by andre23arruda. Points: { self.length }')

    def is_collision(self, other_object):
        '''Verifica se as coordenadas da cobra estão na lista de coordenadas do objeto comparado'''
        first_block_coordinates = self.coordinates[0]
        other_object_coordinates = other_object.coordinates if isinstance(other_object.coordinates[0], list) else [other_object.coordinates]

        if self == other_object:
            other_object_coordinates = other_object_coordinates[:]
            other_object_coordinates.pop(0)

        if first_block_coordinates in other_object_coordinates:
            return True

        return False


class Game:
    def __init__(self):
        pygame.init()

        self.assets = {
            'icon': pygame.image.load(f'{ local_path }/assets/icon.png'),
            'background': pygame.image.load(f'{ local_path }/assets/background.jpg'),
            'crash': pygame.mixer.Sound(f'{ local_path }/assets/crash.mp3'),
            'ding': pygame.mixer.Sound(f'{ local_path }/assets/ding.mp3'),
            'bg_music': pygame.mixer.music.load(f'{ local_path }/assets/bg_music.mp3'),
        }
        pygame.mixer.music.play(-1)
        # pygame.mixer.Sound.play(self.assets['bg_music'])
        pygame.display.set_icon(self.assets['icon'])

        self.surface = pygame.display.set_mode(WINDOW_SIZE)
        self.snake = Snake(self.surface, local_path)
        self.apple = Apple(self.surface, local_path)
        self.wall = Wall(self.surface, local_path)
        self.pause = False
        self.game_over = False


    def render_background(self):
        self.surface.blit(self.assets['background'], (0, 0))

    def restart(self):
        self.snake = Snake(self.surface, local_path)
        self.apple = Apple(self.surface, local_path)
        self.wall = Wall(self.surface, local_path)

    def game_over_message(self):
        '''Show message'''
        green = (0, 255, 0)
        font = pygame.font.Font('freesansbold.ttf', 60)

        text = font.render('GAME OVER', True, green)
        textRect = text.get_rect()
        textRect.center = (300,280)
        self.surface.blit(text, textRect)

        font = pygame.font.Font('freesansbold.ttf', 40)
        text = font.render(f'Your points: { self.snake.length }', True, green)
        textRect = text.get_rect()
        textRect.center = (300,330)
        self.surface.blit(text, textRect)

        font = pygame.font.Font('freesansbold.ttf', 20)
        text = font.render(f'Enter to restart or ESC to quit', True, green)
        textRect = text.get_rect()
        textRect.center = (300,370)
        self.surface.blit(text, textRect)

        pygame.display.flip()

    def play(self):
        '''Render objects'''
        self.render_background()
        self.apple.draw()
        self.wall.draw()

        # snake eats apple
        if self.snake.is_collision(self.apple):
            self.snake.walk(grow_up=True)
            self.apple.new()
            self.apple.draw()
            pygame.mixer.Sound.play(self.assets['ding'])

        # snake collides with wall or itself
        elif self.snake.is_collision(self.wall) or self.snake.is_collision(self.snake):
            self.snake.draw()
            pygame.mixer.Sound.play(self.assets['crash'])
            self.pause = True
            self.game_over_message()
            self.restart()

        else:
            self.snake.walk()

    def finish(self):
        '''End game'''
        self.game_over = True

    def run(self):
        '''Run game'''
        while not self.game_over:

            for event in pygame.event.get():

                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        self.snake.move_up()
                    elif event.key == K_DOWN:
                        self.snake.move_down()
                    elif event.key == K_LEFT:
                        self.snake.move_left()
                    elif event.key == K_RIGHT:
                        self.snake.move_right()
                    elif event.key == K_RETURN:
                        self.pause = False
                    elif event.key == K_ESCAPE:
                        self.finish()

                elif event.type == QUIT:
                    self.finish()

            if not self.pause:
                self.play()
                time.sleep(0.25)

        pygame.quit()
        quit()


if __name__ == '__main__':
    game = Game()
    game.run()

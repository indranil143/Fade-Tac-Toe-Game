import pygame as pg
import sys
from random import randint

# Game settings
WIN_SIZE = 700
CELL_SIZE = WIN_SIZE // 3
INF = float('inf')
vec2 = pg.math.Vector2
CELL_CENTER = vec2(CELL_SIZE / 2)

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# TicTacToe Class
class TicTacToe:
    def __init__(self, game):
        self.game = game
        self.field_image = self.get_scaled_image('resources/field.png', [WIN_SIZE] * 2)
        self.O_image = self.get_scaled_image('resources/o.png', [CELL_SIZE] * 2)
        self.X_image = self.get_scaled_image('resources/x.png', [CELL_SIZE] * 2)

        # faded versions
        self.O_faded = self.O_image.copy()
        self.O_faded.set_alpha(100)
        self.X_faded = self.X_image.copy()
        self.X_faded.set_alpha(100)

        self.game_array = [[INF, INF, INF],
                           [INF, INF, INF],
                           [INF, INF, INF]]
        self.player = randint(0, 1)

        self.line_indices_array = [
            [(0, 0), (0, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)],
            [(0, 0), (1, 0), (2, 0)],
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],
            [(0, 0), (1, 1), (2, 2)],
            [(0, 2), (1, 1), (2, 0)]
        ]

        self.winner = None
        self.winner_line = None
        self.game_steps = 0
        self.font = pg.font.SysFont('Verdana', CELL_SIZE // 4, True)
        self.game_over_sound = pg.mixer.Sound("resources/game_over.wav")
        self.move_sound = pg.mixer.Sound("resources/move.wav")

        self.move_history = {0: [], 1: []}  # 0 for O, 1 for X

    def check_winner(self):
        for line in self.line_indices_array:
            values = [self.game_array[i][j] for i, j in line]
            if values.count(0) == 3:
                self.winner = 'O'
            elif values.count(1) == 3:
                self.winner = 'X'
            if self.winner:
                self.winner_line = [
                    vec2(line[0][::-1]) * CELL_SIZE + CELL_CENTER,
                    vec2(line[2][::-1]) * CELL_SIZE + CELL_CENTER
                ]
                self.game_over_sound.play()
                break

    def run_game_process(self):
        if self.winner:
            return

        current_cell = vec2(pg.mouse.get_pos()) // CELL_SIZE
        col, row = map(int, current_cell)
        left_click = pg.mouse.get_pressed()[0]

        if left_click and self.game_array[row][col] == INF:
            self.game_array[row][col] = self.player
            self.move_history[self.player].append((row, col))

            if len(self.move_history[self.player]) > 3:
                old_row, old_col = self.move_history[self.player].pop(0)
                self.game_array[old_row][old_col] = INF  # Remove oldest

            self.move_sound.play()
            self.player = not self.player
            self.game_steps += 1
            self.check_winner()

    def draw_objects(self):
        for y, row in enumerate(self.game_array):
            for x, cell in enumerate(row):
                if cell == 0 or cell == 1:
                    img = self.O_image if cell == 0 else self.X_image
                    faded_img = self.O_faded if cell == 0 else self.X_faded
                    pos = vec2(x, y) * CELL_SIZE

                    # Check if faded
                    if (y, x) == self.move_history[cell][0] and len(self.move_history[cell]) == 3:
                        self.game.screen.blit(faded_img, pos)
                    else:
                        self.game.screen.blit(img, pos)

    def draw_winner(self):
        if self.winner:
            pg.draw.line(self.game.screen, RED, *self.winner_line, CELL_SIZE // 8)
            label = self.font.render(f'Player "{self.winner}" wins!', True, WHITE, BLACK)
            self.game.screen.blit(label, (WIN_SIZE // 2 - label.get_width() // 2, WIN_SIZE // 4))

    def draw(self):
        self.game.screen.blit(self.field_image, (0, 0))
        self.draw_objects()
        self.draw_winner()

    @staticmethod
    def get_scaled_image(path, res):
        img = pg.image.load(path).convert_alpha()
        return pg.transform.smoothscale(img, res)

    def print_caption(self):
        pg.display.set_caption(f'Player "{"OX"[self.player]}" turn!')
        if self.winner:
            pg.display.set_caption(f'Player "{self.winner}" wins! Press Space to Restart')
        elif self.game_steps == 9:
            pg.display.set_caption(f'Game Over! Press Space to Restart')

    def run(self):
        self.print_caption()
        self.draw()
        self.run_game_process()


# Game Class
class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode([WIN_SIZE] * 2)
        self.clock = pg.time.Clock()
        self.tic_tac_toe = TicTacToe(self)

    def new_game(self):
        self.tic_tac_toe = TicTacToe(self)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                self.new_game()

    def run(self):
        while True:
            self.tic_tac_toe.run()
            self.check_events()
            pg.display.update()
            self.clock.tick(60)


# Main
if __name__ == '__main__':
    game = Game()
    game.run()

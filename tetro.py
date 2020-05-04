import pygame
from random import randint
from copy import deepcopy












class Menu(object):
    def __init__(self, controller):
        self.controller = controller
        self.menu = pygame.image.load("images/main_menu.png")
        self.pos = (100, 200)
        self.button = Button(self.menu, self.pos, "images/start_button.png", (100, 140), hover_image="images/start_button_hover.png")

    def connect_button(self, func):
        self.button.connect(func)

    def check_event(self, event):
        self.button.check_event(event)

    def update(self):
        self.button.update()

    def draw(self):
        self.button.draw()
        self.controller.window.blit(self.menu, self.pos)







class Button(object):
    def __init__(self, surface, parent_pos, image, pos, hover_image=None):
        self.surface = surface
        self.image = pygame.image.load(image)
        self.hovered_image = pygame.image.load(hover_image) if hover_image else None
        self.rect = self.image.get_rect()
        self.rect.center = (parent_pos[0] + pos[0], parent_pos[1] + pos[1])
        self.pos = (pos[0]-(self.rect.w//2), pos[1]-(self.rect.h//2))
        self.function = None
        self.draw_image = self.image

    def check_event(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.on_click(event)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.on_release(event)

    def on_click(self, event):
        if self.rect.collidepoint(event.pos):
            self.clicked = True
            self.function()

    def on_release(self, event):
        self.clicked = False

    def is_hovered(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def connect(self, func):
        self.function = func

    def update(self):
        self.draw_image = self.image
        if self.is_hovered() and self.hovered_image:
            self.draw_image = self.hovered_image

    def draw(self):
        self.surface.blit(self.draw_image, self.pos)








class TetrisController(object):
    def __init__(self):
        self.WIDTH, self.HEIGHT = 600, 700
        self.GRAY = (70, 70, 70)

        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.background = pygame.image.load("images/background.png")
        self.window.blit(self.background, (0, 0))
        pygame.display.set_caption('Tetro')

        self.font = pygame.font.SysFont("comicsansms", 56)

        self.clock = pygame.time.Clock()
        self.fps = 30

        self.level = 1
        self.score = 0
        self.lines_cleared = 0

        self.tetris_pos = (50, 50)
        self.scale = 30
        self.tetris = TetrisGame(self)
        self.game_done = False

        self.main_menu = Menu(self)
        self.main_menu.connect_button(self.start_game)
        self.display_menu = True

        self.draw_stats()

    def start_game(self):
        self.display_menu = False
        self.game_done = False
        self.draw_next_piece()

    def update_score(self, clear_count):
        if clear_count:
            self.lines_cleared += clear_count
            self.score += ((clear_count**3) + (clear_count * 10)) - 1
            self.level = self.lines_cleared // 10 + 1
            self.tetris.time_segment = 15 - self.level
            if self.tetris.time_segment == 0: self.tetris.time_segment = 1

    def game_over(self):
        self.display_menu = True
        self.game_done = True
        self.tetris.clear_grid()
        self.level = 1
        self.score = 0
        self.lines_cleared = 0
        self.tetris.time_segment = 15
        self.tetris.new_piece()

    def draw_stats(self):
        level_text = self.font.render(str(self.level), True, self.GRAY)
        score_text = self.font.render(str(self.score), True, self.GRAY)
        lines_text = self.font.render(str(self.lines_cleared), True, self.GRAY)
        level_w, level_h = self.font.size(str(self.level))
        score_w, score_h = self.font.size(str(self.score))
        lines_w, lines_h = self.font.size(str(self.lines_cleared))
        self.window.blit(level_text, (475-(level_w//2), 405-(level_h//2)))
        self.window.blit(score_text, (475-(score_w//2), 518-(score_h//2)))
        self.window.blit(lines_text, (475-(lines_w//2), 628-(lines_h//2)))

    def draw_next_piece(self):
        next = self.tetris.next_piece
        if next.id == 5:
            xoff = 445
            yoff = 253
        elif next.id == 6:
            xoff = 445
            yoff = 271
        else:
            xoff = 460
            yoff = 271
        for sq in next.shape:
            x = sq[0] * self.scale + xoff
            y = -sq[1] * self.scale + yoff
            self.window.blit(next.piece_img, (x, y))

    def run(self):
        running = True
        while running:

            self.clock.tick(self.fps)

            if self.display_menu:
                self.main_menu.update()
                self.main_menu.draw()
            else:
                self.tetris.update()
                if not self.game_done:
                    if self.tetris.stats_updated:
                        self.window.blit(self.background, (0, 0))
                        self.draw_stats()
                        self.draw_next_piece()
                    self.tetris.draw_grid()
                    self.window.blit(self.tetris.grid_surface, self.tetris_pos)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    self.tetris.key_down(event.key)
                elif event.type == pygame.KEYUP:
                    self.tetris.key_up(event.key)
                else:
                    self.main_menu.check_event(event)







class TetrisGame(object):
    def __init__(self, controller):
        self.GRID_BG = (50, 50, 50)
        self.controller = controller
        self.gw, self.gh = 300, 600
        self.grid_surface = pygame.Surface((self.gw, self.gh))
        self.grid_surface.fill(self.GRID_BG)
        self.grid_pos = (50, 50)
        self.scale = 30
        self.rows = 20
        self.cols = 10
        self.grid = []
        self.grid.append([1] * (self.cols+2))
        for _ in range(self.rows+1):
            self.grid.append([1] + ([0] * self.cols) + [1])

        self.shapes = []
        self.colors = []
        self.offsets = []
        self.init_pieces()
        self.init_offsets()
        rand1 = randint(0, len(self.shapes)-1)
        rand2 = randint(0, len(self.shapes)-1)
        self.piece = Piece(self, deepcopy(self.shapes[rand1]), self.piece_imgs[rand1], rand1, self.offset_indexs[rand1])
        self.next_piece = Piece(self, deepcopy(self.shapes[rand2]), self.piece_imgs[rand2], rand2, self.offset_indexs[rand2])

        self.time = 0
        self.time_segment = 15
        self.time_step = 1
        self.stats_updated = False

        self.down_down = False

        self.lines_cleared = 0

    def key_down(self, key):
        if key == 273 or key == 105:
            self.rotate_clock()
        elif key == 122:
            self.rotate_count()
        elif key == 274 or key == 107:
            self.down_down = True
        elif key == 275 or key == 108:
            self.piece_right()
        elif key == 276 or key == 106:
            self.piece_left()

    def key_up(self, key):
        if key == 274 or key == 107:
            self.down_down = False

    def new_piece(self):
        self.piece = self.next_piece
        randi = randint(0, len(self.shapes)-1)
        self.next_piece = Piece(self, deepcopy(self.shapes[randi]), self.piece_imgs[randi], randi, self.offset_indexs[randi])

    def grid_intersect(self):
        for sq in self.piece.shape:
            gj = self.piece.j + sq[0] + 1
            gi = self.piece.i + sq[1]
            if self.grid[gi][gj]:
                return True
        return False

    def piece_down(self):
        self.piece.i -= 1
        if self.grid_intersect():
            self.piece.i += 1

    def piece_right(self):
        self.piece.j += 1
        if self.grid_intersect():
            self.piece.j -= 1

    def piece_left(self):
        self.piece.j -= 1
        if self.grid_intersect():
            self.piece.j += 1

    def rotate_clock(self):
        old_rot_pos = self.piece.rotation
        self.piece.rotate_clock()
        new_rot_pos = self.piece.rotation
        vaid = self.check_offsets(old_rot_pos, new_rot_pos)
        if not vaid:
            self.piece.rotate_count()

    def rotate_count(self):
        old_rot_pos = self.piece.rotation
        self.piece.rotate_count()
        new_rot_pos = self.piece.rotation
        vaid = self.check_offsets(old_rot_pos, new_rot_pos)
        if not vaid:
            self.piece.rotate_clock()

    def check_offsets(self, old, new):
        for offset in self.offsets[self.piece.offset_index]:
            x1, y1 = offset[old]
            x2, y2 = offset[new]
            ox, oy = (x1-x2, y1-y2)
            self.piece.j += ox
            self.piece.i += oy
            if not self.grid_intersect():
                return True
            else:
                self.piece.j -= ox
                self.piece.i -= oy
        return False

    def clear_lines(self):
        clear_count = 0
        for i in range(self.rows-1, 0, -1):
            full = True
            for j in range(1, self.cols+1):
                if not self.grid[i][j]:
                    full = False
                    break
            if full:
                self.grid.pop(i)
                clear_count += 1
        for i in range(clear_count):
            self.grid.append([1] + [0] * self.cols + [1])
        return clear_count

    def finish_piece(self):
        self.place_piece()
        clear_count = self.clear_lines()
        self.controller.update_score(clear_count)
        self.new_piece()

    def place_piece(self):
        for sq in self.piece.shape:
            gj = self.piece.j + sq[0] + 1
            gi = self.piece.i + sq[1]
            self.grid[gi][gj] = self.piece.piece_img

    def next_down_inter(self):
        self.piece.i -= 1
        if self.grid_intersect():
            self.piece.i += 1
            return True
        self.piece.i += 1
        return False

    def clear_grid(self):
        for i in range(1, self.rows+2):
            for j in range(1, self.cols + 1):
                self.grid[i][j] = 0

    def update(self):
        self.time += self.time_step
        if self.time >= self.time_segment or self.down_down:
            self.time = 0
            if self.next_down_inter():
                self.finish_piece()
                self.stats_updated = True
                self.down_down = False
                if self.grid_intersect():
                    self.controller.game_over()
            else:
                self.piece.i -= 1

    def draw_grid(self):
        self.grid_surface.fill(self.GRID_BG)

        for sq in self.piece.shape:
            x = (self.piece.j + sq[0]) * self.scale
            y = self.gh - (self.piece.i + sq[1]) * self.scale
            self.grid_surface.blit(self.piece.piece_img, (x, y))

        for gi in range(1, self.rows+1):
            for gj in range(1, self.cols+1):
                x = (gj-1) * self.scale
                y = self.gh - (gi * self.scale)
                if self.grid[gi][gj]:
                    self.grid_surface.blit(self.grid[gi][gj], (x, y))

    def init_offsets(self):
        self.offsets = [
            [
                [(0, 0), (0, 0), (0, 0), (0, 0)],
                [(0, 0), (1, 0), (0, 0), (-1, 0)],
                [(0, 0), (1, -1), (0, 0), (-1, -1)],
                [(0, 0), (0, 2), (0, 0), (0, 2)],
                [(0, 0), (1, 2), (0, 0), (-1, 2)]
            ],
            [
                [(0, 0), (-1, 0), (-1, 1), (0, 1)],
                [(-1, 0), (0, 0), (1, 1), (0, 1)],
                [(2, 0), (0, 0), (-2, 1), (0, 1)],
                [(-1, 0), (0, 1),  (1, 0), (0, -1)],
                [(2, 0), (0, -2), (-2, 0), (0, 2)]
            ],
            [
                [(0, 0), (0, -1), (-1, -1), (-1, 0)]
            ]
        ]

    def init_pieces(self):
        self.offset_indexs = [0, 0, 0, 0, 0, 1, 2]
        self.piece_imgs = [
            pygame.image.load("pieces/piece_purple.png"),
            pygame.image.load("pieces/piece_blue.png"),
            pygame.image.load("pieces/piece_orange.png"),
            pygame.image.load("pieces/piece_red.png"),
            pygame.image.load("pieces/piece_green.png"),
            pygame.image.load("pieces/piece_lightblue.png"),
            pygame.image.load("pieces/piece_yellow.png"),
        ]
        self.colors = [
            (200, 0, 0),
            (0, 200, 0),
            (50, 50, 200),
            (200, 200, 0),
            (0, 200, 200),
            (200, 200, 200),
            (200, 0, 200)
        ]
        self.shapes.append([
            [0, 0],
            [-1, 0],
            [1, 0],
            [0, 1]
        ])
        self.shapes.append([
            [0, 0],
            [-1, 0],
            [1, 0],
            [-1, 1]
        ])
        self.shapes.append([
            [0, 0],
            [-1, 0],
            [1, 0],
            [1, 1]
        ])
        self.shapes.append([
            [0, 0],
            [-1, 1],
            [0, 1],
            [1, 0]
        ])
        self.shapes.append([
            [0, 0],
            [-1, 0],
            [0, 1],
            [1, 1]
        ])
        self.shapes.append([
            [0, 0],
            [-1, 0],
            [1, 0],
            [2, 0]
        ])
        self.shapes.append([
            [0, 0],
            [0, 1],
            [1, 1],
            [1, 0]
        ])








class Piece(object):
    def __init__(self, tetris, shape, piece_img, id, offset_index):
        self.tetris = tetris
        self.shape = shape
        self.id = id
        self.offset_index = offset_index
        self.piece_img = piece_img
        self.j = 4
        self.i = 20 if self.id == 5 else 19
        self.size = len(self.shape)
        self.rotation = 0

    def rotate_clock(self):
        self.rotation = (self.rotation + 1) % 4
        for i in range(4):
            self.shape[i] = [self.shape[i][1], -self.shape[i][0]]

    def rotate_count(self):
        self.rotation = (self.rotation - 1) % 4
        for i in range(4):
            self.shape[i] = [-self.shape[i][1], self.shape[i][0]]









def main():
    pygame.init()
    tetris = TetrisController()
    tetris.run()
    pygame.quit()



if __name__ == "__main__":
    main()

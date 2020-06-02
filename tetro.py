import pygame
from pygame_textinput import TextInput
import requests
from random import randint
from copy import deepcopy



GRAY = pygame.Color(70, 70, 70)
WHITE = pygame.Color(255, 255, 255)





class SurfaceObject(object):
    def __init__(self, parent, pos):
        self.parent = parent
        if self.parent:
            self.pos = (parent.pos[0] + pos[0], parent.pos[1] + pos[1])
        else:
            self.pos = pos
        self.rect = None

    def set_rect(self, rect):
        self.rect = rect
        self.pos = (self.pos[0]-self.rect.w//2, self.pos[1]-self.rect.h//2)
        self.rect.topleft = self.pos






class Label(SurfaceObject):
    def __init__(self, parent, pos, text=""):
        SurfaceObject.__init__(self, parent, pos)
        self.color = WHITE
        self.font = pygame.font.SysFont("menlottc", 20)
        self.set_text(text)
        self.set_rect(self.text_surf.get_rect())

    def set_text(self, text):
        self.text = str(text)
        self.render_text()

    def set_color(self, color):
        self.color = color
        self.render_text()

    def set_font(self, name, size):
        self.font = pygame.font.SysFont(name, size)
        self.render_text()

    def render_text(self):
        self.text_surf = self.font.render(self.text, True, self.color)

    def draw(self, surface):
        surface.blit(self.text_surf, self.pos)






class Button(SurfaceObject):
    def __init__(self, parent, pos, image, hover_image=None):
        SurfaceObject.__init__(self, parent, pos)
        self.image = pygame.image.load(image)
        self.set_rect(self.image.get_rect())
        self.hovered_image = pygame.image.load(hover_image) if hover_image else None
        self.function = None
        self.draw_image = self.image

    def connect(self, func):
        self.function = func

    def check_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.on_click(event)

    def on_click(self, event):
        if self.rect.collidepoint(event.pos):
            self.function()

    def is_hovered(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def update(self):
        self.draw_image = self.image
        if self.hovered_image and self.is_hovered():
            self.draw_image = self.hovered_image

    def draw(self, surface):
        surface.blit(self.draw_image, self.pos)







class MainMenu(SurfaceObject):
    def __init__(self, parent, pos):
        SurfaceObject.__init__(self, parent, pos)
        self.main_menu = pygame.image.load("main_menu.png")
        self.set_rect(self.main_menu.get_rect())
        self.start_button = Button(self, (100, 120), "start_button.png", hover_image="start_button_hover.png")
        self.scores_button = Button(self, (100, 190), "scores_button.png", hover_image="scores_button_hover.png")

    def connect_start_button(self, func):
        self.start_button.connect(func)

    def connect_scores_button(self, func):
        self.scores_button.connect(func)

    def check_event(self, event):
        self.start_button.check_event(event)
        self.scores_button.check_event(event)

    def update(self):
        self.start_button.update()
        self.scores_button.update()

    def draw(self, surface):
        surface.blit(self.main_menu, self.pos)
        self.start_button.draw(surface)
        self.scores_button.draw(surface)






class ScoresMenu(SurfaceObject):
    def __init__(self, parent, pos):
        SurfaceObject.__init__(self, parent, pos)
        self.blank_score_menu = pygame.image.load("scores_menu.png")
        self.set_rect(self.blank_score_menu.get_rect())
        self.back_button = Button(self, (100, 270), "back_button.png", hover_image="back_button_hover.png")
        self.score_font = pygame.font.SysFont("menlottc", 11)

    def draw_scores(self, high_scores):
        self.score_menu = self.blank_score_menu.copy()
        if high_scores:
            x = 18
            y = 70
            line_height = 17
            for i, high_score in enumerate(high_scores):
                pos = str(i+1)
                name = high_score[0]
                score = str(high_score[1])
                dot_count = 19 - (len(pos) + len(name) + len(score))
                space = "" if len(name) == 15 else " "
                text = pos + " " + name + space + ("." * dot_count) + " " + score
                text_surf = self.score_font.render(text, True, WHITE)
                self.score_menu.blit(text_surf, (x, y))
                y += line_height

    def connect_back_button(self, func):
        self.back_button.connect(func)

    def check_event(self, event):
        self.back_button.check_event(event)

    def update(self):
        self.back_button.update()

    def draw(self, surface):
        surface.blit(self.score_menu, self.pos)
        self.back_button.draw(surface)







class GameoverMenu(SurfaceObject):
    def __init__(self, parent, pos):
        SurfaceObject.__init__(self, parent, pos)
        self.gameover_menu = pygame.image.load("gameover_menu.png")
        self.set_rect(self.gameover_menu.get_rect())
        self.score_label = Label(self, (130, 92), "10000")
        self.submit_button = Button(self, (100, 230), "submit_button.png", hover_image="submit_button_hover.png")
        self.main_menu_button = Button(self, (100, 270), "main_menu_button.png", hover_image="main_menu_button_hover.png")
        self.name_input = TextInput(
            text_color = WHITE,
            font_family = "menlottc",
            font_size = 14,
            max_string_length = 15,
            cursor_color = (200, 10, 10),
            pos = (40, 178),
            parent_pos = self.pos
        )

    def set_final_score(self, score):
        self.score_label.set_text(score)

    def connect_submit_button(self, func):
        self.submit_button.connect(func)

    def connect_main_menu_button(self, func):
        self.main_menu_button.connect(func)

    def get_name(self):
        return self.name_input.get_text()

    def clear_name(self):
        self.name_input.clear_text()

    def check_event(self, event):
        self.submit_button.check_event(event)
        self.main_menu_button.check_event(event)
        self.name_input.check_event(event)

    def update(self):
        self.submit_button.update()
        self.main_menu_button.update()
        self.name_input.update()

    def draw(self, surface):
        surface.blit(self.gameover_menu, self.pos)
        self.score_label.draw(surface)
        self.name_input.draw(surface)
        self.submit_button.draw(surface)
        self.main_menu_button.draw(surface)












class TetrisController(object):
    def __init__(self):
        self.WIDTH, self.HEIGHT = 600, 700

        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.background = pygame.image.load("background.png")
        self.window.blit(self.background, (0, 0))
        pygame.display.set_caption('Tetro')
        self.main_surface_object = SurfaceObject(None, (0, 0))

        self.font = pygame.font.SysFont("menlottc", 32)
        self.score_font = pygame.font.SysFont("menlottc", 11)

        self.clock = pygame.time.Clock()
        self.fps = 30

        self.level = 1
        self.score = 0
        self.lines_cleared = 0
        self.final_score = 0

        self.tetris_pos = (50, 50)
        self.scale = 30
        self.tetris = TetrisGame(self)
        self.game_done = False

        self.menu_pos = (200, 350)

        self.main_menu = MainMenu(self.main_surface_object, self.menu_pos)
        self.main_menu.connect_start_button(self.start_game)
        self.main_menu.connect_scores_button(self.show_scores_menu)
        self.display_main_menu = True

        self.scores_menu = ScoresMenu(self.main_surface_object, self.menu_pos)
        self.scores_menu.connect_back_button(self.show_main_menu)
        self.display_scores_menu = False

        self.gameover_menu = GameoverMenu(self.main_surface_object, self.menu_pos)
        self.gameover_menu.connect_submit_button(self.submit_high_score)
        self.gameover_menu.connect_main_menu_button(self.show_main_menu)
        self.display_gameover_menu = False

        self.draw_stats()

    def start_game(self):
        self.display_main_menu = False
        self.game_done = False
        self.draw_next_piece()

    def show_scores_menu(self):
        self.display_scores_menu = True
        self.display_main_menu = False
        high_scores = self.get_high_scores()
        self.scores_menu.draw_scores(high_scores)

    def show_main_menu(self):
        self.display_main_menu = True
        self.display_scores_menu = False
        self.display_gameover_menu = False

    def get_high_scores(self):
        params = {"qnt": 10, "sort": True}
        url = "http://api.ryanstella.me/tetro/high-scores"
        response = requests.get(url, params=params)
        high_scores = response.json()
        return high_scores

    def submit_high_score(self):
        name = self.gameover_menu.get_name().strip()
        if name:
            data = {"name": name, "score": self.final_score}
            url = "http://api.ryanstella.me/tetro/high-scores"
            requests.post(url, data=data)
            self.gameover_menu.clear_name()
            self.show_main_menu()

    def update_score(self, clear_count):
        if clear_count:
            self.lines_cleared += clear_count
            self.score += ((clear_count**3) + (clear_count * 10)) - 1
            self.level = self.lines_cleared // 10 + 1
            self.tetris.time_segment = 15 - self.level
            if self.tetris.time_segment == 0: self.tetris.time_segment = 1

    def game_over(self):
        self.gameover_menu.set_final_score(self.score)
        self.display_gameover_menu = True
        self.game_done = True
        self.final_score = self.score
        self.tetris.clear_grid()
        self.level = 1
        self.score = 0
        self.lines_cleared = 0
        self.tetris.time_segment = 15
        self.tetris.new_piece()

    def draw_stats(self):
        level_text = self.font.render(str(self.level), True, GRAY)
        score_text = self.font.render(str(self.score), True, GRAY)
        lines_text = self.font.render(str(self.lines_cleared), True, GRAY)
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

    def check_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.tetris.key_down(event.key)
        elif event.type == pygame.KEYUP:
            self.tetris.key_up(event.key)

    def run(self):
        running = True
        while running:

            self.clock.tick(self.fps)

            if self.display_main_menu:
                self.main_menu.update()
                self.main_menu.draw(self.window)
            elif self.display_scores_menu:
                self.scores_menu.update()
                self.scores_menu.draw(self.window)
            elif self.display_gameover_menu:
                self.gameover_menu.update()
                self.gameover_menu.draw(self.window)
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
                elif self.display_main_menu:
                    self.main_menu.check_event(event)
                elif self.display_scores_menu:
                    self.scores_menu.check_event(event)
                elif self.display_gameover_menu:
                    self.gameover_menu.check_event(event)
                else:
                    self.check_event(event)








class TetrisGame(SurfaceObject):
    def __init__(self, controller):
        self.GRID_BG = (50, 50, 50)
        self.controller = controller
        self.gw, self.gh = 300, 600
        self.grid_surface = pygame.Surface((self.gw, self.gh))
        self.grid_surface.fill(self.GRID_BG)
        self.scale = 30
        self.rows = 20
        self.cols = 10
        self.init_grid()
        self.init_pieces()
        self.init_offsets()
        rand1 = randint(0, len(self.shapes)-1)
        rand2 = randint(0, len(self.shapes)-1)
        self.piece = Piece(self, deepcopy(self.shapes[rand1]), self.piece_imgs[rand1], rand1, self.offset_indicies[rand1])
        self.next_piece = Piece(self, deepcopy(self.shapes[rand2]), self.piece_imgs[rand2], rand2, self.offset_indicies[rand2])

        self.time = 0
        self.time_segment = 15
        self.time_step = 1
        self.stats_updated = False
        self.down_down = False

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
        self.next_piece = Piece(self, deepcopy(self.shapes[randi]), self.piece_imgs[randi], randi, self.offset_indicies[randi])

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
                self.new_piece()
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

    def init_grid(self):
        self.grid = []
        self.grid.append([1] * (self.cols+2))
        for _ in range(self.rows+1):
            self.grid.append([1] + ([0] * self.cols) + [1])

    def init_offsets(self):
        self.offsets = [
            [
                [(0, 0), (0,  0), (0, 0), ( 0,  0)],
                [(0, 0), (1,  0), (0, 0), (-1,  0)],
                [(0, 0), (1, -1), (0, 0), (-1, -1)],
                [(0, 0), (0,  2), (0, 0), ( 0,  2)],
                [(0, 0), (1,  2), (0, 0), (-1,  2)]
            ],
            [
                [( 0, 0), (-1,  0), (-1, 1), (0,  1)],
                [(-1, 0), ( 0,  0), ( 1, 1), (0,  1)],
                [( 2, 0), ( 0,  0), (-2, 1), (0,  1)],
                [(-1, 0), ( 0,  1), ( 1, 0), (0, -1)],
                [( 2, 0), ( 0, -2), (-2, 0), (0,  2)]
            ],
            [
                [(0, 0), (0, -1), (-1, -1), (-1, 0)]
            ]
        ]

    def init_pieces(self):
        self.offset_indicies = [0, 0, 0, 0, 0, 1, 2]
        self.piece_imgs = [
            pygame.image.load("piece_purple.png"),
            pygame.image.load("piece_blue.png"),
            pygame.image.load("piece_orange.png"),
            pygame.image.load("piece_red.png"),
            pygame.image.load("piece_green.png"),
            pygame.image.load("piece_lightblue.png"),
            pygame.image.load("piece_yellow.png"),
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
        self.shapes = [
            [[0, 0], [-1, 0], [1, 0], [ 0, 1]],
            [[0, 0], [-1, 0], [1, 0], [-1, 1]],
            [[0, 0], [-1, 0], [1, 0], [ 1, 1]],
            [[0, 0], [-1, 1], [0, 1], [ 1, 0]],
            [[0, 0], [-1, 0], [0, 1], [ 1, 1]],
            [[0, 0], [-1, 0], [1, 0], [ 2, 0]],
            [[0, 0], [ 0, 1], [1, 1], [ 1, 0]]
        ]








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

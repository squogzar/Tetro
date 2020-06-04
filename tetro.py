import pygame
from pygame_textinput import TextInput
import requests
from random import randint
from copy import deepcopy







class SurfaceObject(object):
    def __init__(self, surface, pos, parent=None):
        self.surface = surface
        self.rect = self.surface.get_rect()
        self.parent = parent
        if self.parent:
            self.pos = (parent.pos[0] + pos[0], parent.pos[1] + pos[1])
        else:
            self.pos = pos
        self.rect.topleft = self.pos
        self.center_blit = False

    def blit_from_center(self, center_blit):
        if not self.center_blit and center_blit:
            self.center_blit = True
            self.pos = (self.pos[0]-self.rect.w//2, self.pos[1]-self.rect.h//2)
            self.rect.topleft = self.pos
        elif self.center_blit and not center_blit:
            self.pos = (self.pos[0]+self.rect.w//2, self.pos[1]+self.rect.h//2)
            self.rect.topleft = self.pos
            self.center_blit = False

    def reset_rect(self):
        new_rect = self.surface.get_rect()
        if self.center_blit:
            self.pos = (self.pos[0]+self.rect.w//2, self.pos[1]+self.rect.h//2)
            self.pos = (self.pos[0]-new_rect.w//2, self.pos[1]-new_rect.h//2)
        self.rect = new_rect
        self.rect.topleft = self.pos






class Label(SurfaceObject):
    def __init__(self, parent, pos, text=""):
        SurfaceObject.__init__(self, pygame.Surface((1,1)), pos, parent)
        self.blit_from_center(True)
        self.color = pygame.Color(255, 255, 255)
        self.font = pygame.font.SysFont("menlottc", 20)
        self.set_text(text)

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
        self.surface = self.font.render(self.text, True, self.color)
        self.reset_rect()

    def draw(self, surface):
        surface.blit(self.surface, self.pos)






class Button(SurfaceObject):
    def __init__(self, parent, pos, image, hover_image=None):
        SurfaceObject.__init__(self, pygame.image.load(image), pos, parent)
        self.blit_from_center(True)
        self.hovered_image = pygame.image.load(hover_image) if hover_image else None
        self.function = None
        self.draw_image = self.surface

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
        self.draw_image = self.surface
        if self.hovered_image and self.is_hovered():
            self.draw_image = self.hovered_image

    def draw(self, surface):
        surface.blit(self.draw_image, self.pos)







class MainMenu(SurfaceObject):
    def __init__(self, parent, pos, image):
        SurfaceObject.__init__(self, pygame.image.load(image), pos, parent)
        self.blit_from_center(True)
        self.start_button = Button(self, (100, 118), "images/start_button.png", hover_image="images/start_button_hover.png")
        self.scores_button = Button(self, (100, 189), "images/scores_button.png", hover_image="images/scores_button_hover.png")

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
        surface.blit(self.surface, self.pos)
        self.start_button.draw(surface)
        self.scores_button.draw(surface)






class ScoresMenu(SurfaceObject):
    def __init__(self, parent, pos, image):
        SurfaceObject.__init__(self, pygame.image.load(image), pos, parent)
        self.blit_from_center(True)
        self.back_button = Button(self, (100, 270), "images/back_button.png", hover_image="images/back_button_hover.png")
        self.score_font = pygame.font.SysFont("menlottc", 11)
        self.score_color = pygame.Color(255, 255, 255)

    def draw_scores(self, high_scores):
        self.score_menu = self.surface.copy()
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
                text_surf = self.score_font.render(text, True, self.score_color)
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
    def __init__(self, parent, pos, image):
        SurfaceObject.__init__(self, pygame.image.load(image), pos, parent)
        self.blit_from_center(True)
        self.score_label = Label(self, (130, 93), "")
        self.submit_button = Button(self, (100, 230), "images/submit_button.png", hover_image="images/submit_button_hover.png")
        self.main_menu_button = Button(self, (100, 270), "images/main_menu_button.png", hover_image="images/main_menu_button_hover.png")
        self.name_input = TextInput(
            text_color = pygame.Color(255, 255, 255),
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
        surface.blit(self.surface, self.pos)
        self.score_label.draw(surface)
        self.name_input.draw(surface)
        self.submit_button.draw(surface)
        self.main_menu_button.draw(surface)






class PauseMenu(SurfaceObject):
    def __init__(self, parent, pos, image):
        SurfaceObject.__init__(self, pygame.image.load(image), pos, parent)
        self.blit_from_center(True)
        self.resume_button = Button(self, (100, 230), "images/resume_button.png", hover_image="images/resume_button_hover.png")
        self.end_game_button = Button(self, (100, 270), "images/end_game_button.png", hover_image="images/end_game_button_hover.png")
        self.p_key_func = None

    def connect_resume_button(self, func):
        self.resume_button.connect(func)

    def connect_end_game_button(self, func):
        self.end_game_button.connect(func)

    def connect_p_key(self, func):
        self.p_key_func = func

    def check_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == 112:
                self.p_key_func()
        self.resume_button.check_event(event)
        self.end_game_button.check_event(event)

    def update(self):
        self.resume_button.update()
        self.end_game_button.update()

    def draw(self, surface):
        surface.blit(self.surface, self.pos)
        self.resume_button.draw(surface)
        self.end_game_button.draw(surface)







class TetrisController(object):
    def __init__(self):
        self.WIDTH, self.HEIGHT = 600, 700
        pygame.display.set_icon(pygame.image.load("images/tetro_icon.png"))
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.background = pygame.image.load("images/background.png")
        self.window.blit(self.background, (0, 0))
        pygame.display.set_caption('Tetro')
        self.main_surface_object = SurfaceObject(self.background, (0, 0))

        self.font = pygame.font.SysFont("menlottc", 32)
        self.score_font = pygame.font.SysFont("menlottc", 11)

        self.main_sound = pygame.mixer.Sound("music/tetro_song.wav")
        self.tetris_sound = pygame.mixer.Sound("music/tetris_sound.wav")
        self.clear_sound = pygame.mixer.Sound("music/clear_sound.wav")
        self.main_sound.play(loops=-1)

        self.tetro_api_url = "http://api.ryanstella.me/tetro/high-scores"

        self.clock = pygame.time.Clock()
        self.fps = 30

        self.level = 1
        self.score = 0
        self.lines_cleared = 0
        self.final_score = 0
        self.line_count_points = [10, 30, 60, 100]
        self.stats_color = pygame.Color(70, 70, 70)

        self.tetris_pos = (50, 50)
        self.scale = 30
        self.tetris = TetrisGame(self, 300, 600, self.tetris_pos, self.main_surface_object)
        self.game_done = False
        self.paused = False

        self.menu_pos = (200, 350)

        self.main_menu = MainMenu(self.main_surface_object, self.menu_pos, "images/menu_main.png")
        self.main_menu.connect_start_button(self.start_game)
        self.main_menu.connect_scores_button(self.show_scores_menu)
        self.display_main_menu = True

        self.scores_menu = ScoresMenu(self.main_surface_object, self.menu_pos, "images/menu_scores.png")
        self.scores_menu.connect_back_button(self.show_main_menu)
        self.display_scores_menu = False

        self.gameover_menu = GameoverMenu(self.main_surface_object, self.menu_pos, "images/menu_gameover.png")
        self.gameover_menu.connect_submit_button(self.submit_high_score)
        self.gameover_menu.connect_main_menu_button(self.show_main_menu)
        self.display_gameover_menu = False

        self.pause_menu = PauseMenu(self.main_surface_object, self.menu_pos, "images/menu_pause.png")
        self.pause_menu.connect_resume_button(self.toggle_pause)
        self.pause_menu.connect_end_game_button(self.end_game)
        self.pause_menu.connect_p_key(self.toggle_pause)
        self.display_pause_menu = False

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
        self.display_pause_menu = False

    def toggle_pause(self):
        self.paused = not self.paused
        self.display_pause_menu = not self.display_pause_menu

    def end_game(self):
        self.display_pause_menu = False
        self.tetris.stats_updated = True
        self.game_over()

    def get_high_scores(self):
        params = {"qnt": 10, "sort": True}
        response = requests.get(self.tetro_api_url, params=params)
        high_scores = response.json()
        return high_scores

    def submit_high_score(self):
        name = self.gameover_menu.get_name().strip()
        if name:
            data = {"name": name, "score": self.final_score}
            requests.post(self.tetro_api_url, data=data)
            self.gameover_menu.clear_name()
            self.show_main_menu()

    def cleared_value(self, clear_count):
        return ((clear_count**3) + (clear_count * 10)) - 1

    def update_score(self, clear_count):
        if clear_count:
            if clear_count == 4:
                self.tetris_sound.play()
            else:
                self.clear_sound.play()
            self.lines_cleared += clear_count
            self.score += self.line_count_points[clear_count-1]
            self.level = self.lines_cleared // 10 + 1
            self.tetris.time_segment = 15 - self.level
            if self.tetris.time_segment == 0: self.tetris.time_segment = 1

    def game_over(self):
        self.gameover_menu.set_final_score(self.score)
        self.display_gameover_menu = True
        self.paused = False
        self.display_pause_menu = False
        self.game_done = True
        self.final_score = self.score
        self.tetris.clear_grid()
        self.level = 1
        self.score = 0
        self.lines_cleared = 0
        self.tetris.time_segment = 15
        self.tetris.reset_pieces()

    def draw_stats(self):
        level_text = self.font.render(str(self.level), True, self.stats_color)
        score_text = self.font.render(str(self.score), True, self.stats_color)
        lines_text = self.font.render(str(self.lines_cleared), True, self.stats_color)
        level_w, level_h = self.font.size(str(self.level))
        score_w, score_h = self.font.size(str(self.score))
        lines_w, lines_h = self.font.size(str(self.lines_cleared))
        self.window.blit(level_text, (475-(level_w//2), 405-(level_h//2)))
        self.window.blit(score_text, (475-(score_w//2), 518-(score_h//2)))
        self.window.blit(lines_text, (475-(lines_w//2), 628-(lines_h//2)))

    def draw_next_piece(self):
        next = self.tetris.next_piece
        if next.id == 5: xoff, yoff = 445, 253
        elif next.id == 6: xoff, yoff = 445, 271
        else: xoff, yoff = 460, 271
        for sq in next.shape:
            x = sq[0] * self.scale + xoff
            y = -sq[1] * self.scale + yoff
            self.window.blit(next.piece_img, (x, y))

    def check_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == 112:
                self.toggle_pause()
        if not self.paused:
            self.tetris.check_event(event)

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
            elif self.display_pause_menu:
                self.pause_menu.update()
                self.pause_menu.draw(self.window)
            else:
                self.tetris.update()
                if not self.game_done:
                    if self.tetris.stats_updated:
                        self.window.blit(self.background, (0, 0))
                        self.draw_stats()
                        self.draw_next_piece()
                        self.tetris.stats_updated = False
                    self.tetris.draw(self.window)

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
                elif self.display_pause_menu:
                    self.pause_menu.check_event(event)
                else:
                    self.check_event(event)








class TetrisGame(SurfaceObject):
    def __init__(self, controller, gw, gh, pos, parent):
        SurfaceObject.__init__(self, pygame.Surface((gw, gh)), pos, parent)
        self.controller = controller
        self.gw, self.gh = gw, gh
        self.scale = 30
        self.rows = 20
        self.cols = 10
        self.grid_bg = pygame.Color(50, 50, 50)
        self.init_grid()
        self.init_pieces()
        self.init_offsets()
        self.reset_pieces()
        self.surface.fill(self.grid_bg)

        self.time = 0
        self.time_segment = 15
        self.time_step = 1
        self.stats_updated = False
        self.down_down = False
        self.cleared_lines = []
        self.clear_step = 0
        self.clearing_lines = False

    def check_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.key_down(event.key)
        elif event.type == pygame.KEYUP:
            self.key_up(event.key)

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

    def reset_pieces(self):
        rand1 = randint(0, len(self.shapes)-1)
        rand2 = randint(0, len(self.shapes)-1)
        self.piece = Piece(self, deepcopy(self.shapes[rand1]), self.piece_imgs[rand1], rand1, self.offset_indicies[rand1])
        self.next_piece = Piece(self, deepcopy(self.shapes[rand2]), self.piece_imgs[rand2], rand2, self.offset_indicies[rand2])

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
        valid = self.check_offsets(old_rot_pos, new_rot_pos)
        if not valid:
            self.piece.rotate_count()

    def rotate_count(self):
        old_rot_pos = self.piece.rotation
        self.piece.rotate_count()
        new_rot_pos = self.piece.rotation
        valid = self.check_offsets(old_rot_pos, new_rot_pos)
        if not valid:
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
        cleared_lines = []
        for i in range(1, self.rows+1):
            full = True
            for j in range(1, self.cols+1):
                if not self.grid[i][j]:
                    full = False
                    break
            if full:
                cleared_lines.append(i)
        return cleared_lines

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
        if self.clearing_lines:
            self.clear_lines_animation()
        else:
            self.time += self.time_step
            if self.time >= self.time_segment or self.down_down:
                self.time = 0
                if self.next_down_inter():
                    self.place_piece()
                    self.down_down = False
                    self.cleared_lines = self.clear_lines()
                    self.controller.update_score(len(self.cleared_lines))
                    if self.cleared_lines:
                        self.clearing_lines = True
                        self.turn_cleared_white()
                        return
                    self.new_piece()
                    self.stats_updated = True
                    if self.grid_intersect():
                        self.controller.game_over()
                else:
                    self.piece.i -= 1

    def turn_cleared_white(self):
        for row in self.cleared_lines:
            for j in range(1, self.cols+1):
                self.grid[row][j] = self.white_piece

    def clear_lines_animation(self):
        if self.clear_step == 5:
            self.remove_cleared_lines()
            self.clear_step = 0
            self.clearing_lines = False
            self.stats_updated = True
            self.new_piece()
        else:
            for row in self.cleared_lines:
                self.grid[row][5-self.clear_step] = None
                self.grid[row][6+self.clear_step] = None
            self.clear_step += 1

    def remove_cleared_lines(self):
        for i in range(len(self.cleared_lines)-1, -1, -1):
            row = self.cleared_lines[i]
            self.grid.pop(row)
            self.grid.append([1] + [0] * self.cols + [1])
        self.cleared_lines = []

    def draw(self, surface):
        self.surface.fill(self.grid_bg)
        if not self.clearing_lines:
            for sq in self.piece.shape:
                x = (self.piece.j + sq[0]) * self.scale
                y = self.gh - (self.piece.i + sq[1]) * self.scale
                self.surface.blit(self.piece.piece_img, (x, y))
        for gi in range(1, self.rows+1):
            for gj in range(1, self.cols+1):
                if self.grid[gi][gj]:
                    x = (gj-1) * self.scale
                    y = self.gh - (gi * self.scale)
                    self.surface.blit(self.grid[gi][gj], (x, y))
        surface.blit(self.surface, self.pos)

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
        self.white_piece = pygame.image.load("pieces/piece_white.png")
        self.offset_indicies = [0, 0, 0, 0, 0, 1, 2]
        self.piece_imgs = [
            pygame.image.load("pieces/piece_purple.png"),
            pygame.image.load("pieces/piece_blue.png"),
            pygame.image.load("pieces/piece_orange.png"),
            pygame.image.load("pieces/piece_red.png"),
            pygame.image.load("pieces/piece_green.png"),
            pygame.image.load("pieces/piece_lightblue.png"),
            pygame.image.load("pieces/piece_yellow.png")
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

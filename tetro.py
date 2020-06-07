import pygame
import requests
from random import randint
from copy import deepcopy
from widgetstuff import *
from pygame_textinput import TextInput




class MainMenu(WidgetSurface):
    def __init__(self, parent, pos, image):
        WidgetSurface.__init__(self, pygame.image.load(image), pos, parent, True)
        self.start_button = Button(self, (100, 118), "images/start_button.png", hover_image="images/start_button_hover.png")
        self.scores_button = Button(self, (55, 189), "images/scores_button.png", hover_image="images/scores_button_hover.png")
        self.options_button = Button(self, (145, 189), "images/options_button.png", hover_image="images/options_button_hover.png")
        self.add_widget(self.start_button)
        self.add_widget(self.scores_button)
        self.add_widget(self.options_button)

    def connect_start_button(self, func):
        self.start_button.connect(func)

    def connect_scores_button(self, func):
        self.scores_button.connect(func)

    def connect_options_button(self, func):
        self.options_button.connect(func)





class ScoresMenu(WidgetSurface):
    def __init__(self, parent, pos, image):
        WidgetSurface.__init__(self, pygame.image.load(image), pos, parent, True)
        self.back_button = Button(self, (100, 270), "images/back_button.png", hover_image="images/back_button_hover.png")
        self.score_text = Label(self, (100, 160), "", True)
        self.score_text.set_font("menlottc", 11)
        self.score_text.set_color((255, 255, 255))
        self.add_widget(self.back_button)
        self.add_widget(self.score_text)

    def connect_back_button(self, func):
        self.back_button.connect(func)

    def set_scores_text(self, high_scores):
        high_scores_text = ""
        if high_scores:
            for i, high_score in enumerate(high_scores):
                pos, name, score = str(i+1), high_score[0], str(high_score[1])
                dot_count = 19 - (len(pos) + len(name) + len(score))
                space = "" if len(name) == 15 else " "
                text = pos + " " + name + space + ("." * dot_count) + " " + score
                high_scores_text += text + "\n"
        self.score_text.set_text(high_scores_text)





class OptionsMenu(WidgetSurface):
    def __init__(self, parent, pos, image):
        WidgetSurface.__init__(self, pygame.image.load(image), pos, parent, True)
        self.music_volume = NumberInput(self, (53, 109), "images/arrow_left.png","images/arrow_right.png", 0, 10, 10, 1)
        self.soundfx_volume = NumberInput(self, (53, 171), "images/arrow_left.png","images/arrow_right.png", 0, 10, 10, 1)
        self.submit_button = Button(self, (100, 230), "images/submit_button.png", hover_image="images/submit_button_hover.png")
        self.back_button = Button(self, (100, 270), "images/back_button.png", hover_image="images/back_button_hover.png")
        self.add_widget(self.music_volume)
        self.add_widget(self.soundfx_volume)
        self.add_widget(self.submit_button)
        self.add_widget(self.back_button)

    def connect_submit_button(self, func):
        self.submit_button.connect(func)

    def connect_back_button(self, func):
        self.back_button.connect(func)

    def get_music_vol(self):
        return self.music_volume.get_val()

    def get_soundfx_vol(self):
        return self.soundfx_volume.get_val()





class PauseMenu(WidgetSurface):
    def __init__(self, parent, pos, image):
        WidgetSurface.__init__(self, pygame.image.load(image), pos, parent, True)
        self.resume_button = Button(self, (100, 230), "images/resume_button.png", hover_image="images/resume_button_hover.png")
        self.end_game_button = Button(self, (100, 270), "images/end_game_button.png", hover_image="images/end_game_button_hover.png")
        self.p_key = Key(112)
        self.add_widget(self.resume_button)
        self.add_widget(self.end_game_button)
        self.add_widget(self.p_key)

    def connect_resume_button(self, func):
        self.resume_button.connect(func)

    def connect_end_game_button(self, func):
        self.end_game_button.connect(func)

    def connect_p_key(self, func):
        self.p_key.connect(func)





class GameoverMenu(WidgetSurface):
    def __init__(self, parent, pos, image):
        WidgetSurface.__init__(self, pygame.image.load(image), pos, parent, True)
        self.score_label = Label(self, (130, 93), "100", True)
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
        self.add_widget(self.score_label)
        self.add_widget(self.submit_button)
        self.add_widget(self.main_menu_button)
        self.add_widget(self.name_input)

    def connect_submit_button(self, func):
        self.submit_button.connect(func)

    def connect_main_menu_button(self, func):
        self.main_menu_button.connect(func)

    def get_name(self):
        return self.name_input.get_text()

    def set_final_score(self, score):
        self.score_label.set_text(score)

    def clear_name(self):
        self.name_input.clear_text()







class Background(WidgetSurface):
    def __init__(self, parent, pos, image):
        WidgetSurface.__init__(self, pygame.image.load(image), pos, parent, False)
        self.level_label = Label(self, (475, 405), "1", True)
        self.score_label = Label(self, (475, 518), "0", True)
        self.lines_label = Label(self, (475, 628), "0", True)
        self.level_label.set_color((50, 50, 50))
        self.score_label.set_color((50, 50, 50))
        self.lines_label.set_color((50, 50, 50))
        self.level_label.set_font("menlottc", 30)
        self.score_label.set_font("menlottc", 30)
        self.lines_label.set_font("menlottc", 30)
        self.add_widget(self.level_label)
        self.add_widget(self.score_label)
        self.add_widget(self.lines_label)
        self.draw_next_piece = None

    def connect_draw_next_piece(self, func):
        self.draw_next_piece = func

    def set_level(self, level):
        self.level_label.set_text(level)

    def set_score(self, score):
        self.score_label.set_text(score)

    def set_lines(self, lines):
        self.lines_label.set_text(lines)

    def draw(self, surface):
        super().draw(surface)
        self.draw_next_piece()






class TetrisController(object):
    def __init__(self):
        self.WIDTH, self.HEIGHT = 600, 700
        pygame.display.set_icon(pygame.image.load("images/tetro_icon.png"))
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Tetro')

        self.tetro_song = pygame.mixer.Sound("music/tetro_song.wav")
        self.tetris_sound = pygame.mixer.Sound("music/tetris_sound.wav")
        self.clear_sound = pygame.mixer.Sound("music/clear_sound.wav")
        self.music = pygame.mixer.Channel(1)
        self.soundfx = pygame.mixer.Channel(2)

        self.tetro_api_url = "http://api.ryanstella.me/tetro/high-scores"

        self.clock = pygame.time.Clock()
        self.fps = 30

        self.level = 1
        self.score = 0
        self.lines_cleared = 0
        self.line_count_points = [10, 30, 60, 100]
        self.stats_color = pygame.Color(70, 70, 70)

        self.tetris_pos = (50, 50)
        self.scale = 30
        self.game_done = False
        self.paused = False

        self.menu_pos = (200, 350)

        self.background = Background(None, (0, 0), "images/background.png")
        self.background.connect_draw_next_piece(self.draw_next_piece)

        self.tetris = TetrisGame(self, 300, 600, self.tetris_pos, self.background)

        self.main_menu = MainMenu(self.background, self.menu_pos, "images/menu_main.png")
        self.main_menu.connect_start_button(self.start_game)
        self.main_menu.connect_scores_button(self.show_scores_menu)
        self.main_menu.connect_options_button(self.show_options_menu)

        self.scores_menu = ScoresMenu(self.background, self.menu_pos, "images/menu_scores.png")
        self.scores_menu.connect_back_button(self.show_main_menu)

        self.gameover_menu = GameoverMenu(self.background, self.menu_pos, "images/menu_gameover.png")
        self.gameover_menu.connect_submit_button(self.submit_high_score)
        self.gameover_menu.connect_main_menu_button(self.show_main_menu)

        self.pause_menu = PauseMenu(self.background, self.menu_pos, "images/menu_pause.png")
        self.pause_menu.connect_resume_button(self.toggle_pause)
        self.pause_menu.connect_end_game_button(self.game_over)
        self.pause_menu.connect_p_key(self.toggle_pause)

        self.options_menu = OptionsMenu(self.background, self.menu_pos, "images/menu_options.png")
        self.options_menu.connect_submit_button(self.set_options)
        self.options_menu.connect_back_button(self.show_main_menu)

        self.surfs = WidgetSurfaceHolder()
        self.surfs.add_widget_surface("background", self.background)
        self.surfs.add_widget_surface("tetris", self.tetris)
        self.surfs.add_widget_surface("main_menu", self.main_menu)
        self.surfs.add_widget_surface("scores_menu", self.scores_menu)
        self.surfs.add_widget_surface("options_menu", self.options_menu)
        self.surfs.add_widget_surface("gameover_menu", self.gameover_menu)
        self.surfs.add_widget_surface("pause_menu", self.pause_menu)
        self.surfs.activate("background", "main_menu")

    def start_game(self):
        self.level = 1
        self.score = 0
        self.lines_cleared = 0
        self.game_done = False
        self.tetris.reset()
        self.surfs.activate("background", "tetris")
        self.music.play(self.tetro_song, loops=-1)

    def show_options_menu(self):
        self.surfs.activate("background", "options_menu")

    def show_scores_menu(self):
        high_scores = self.get_high_scores()
        self.scores_menu.set_scores_text(high_scores)
        self.surfs.activate("background", "scores_menu")

    def show_main_menu(self):
        self.surfs.activate("background", "main_menu")

    def toggle_pause(self):
        if self.paused:
            self.paused = False
            self.surfs.activate("background", "tetris")
            self.music.unpause()
        else:
            self.paused = True
            self.surfs.activate("background", "pause_menu")
            self.music.pause()

    def game_over(self):
        self.paused = False
        self.game_done = True
        self.gameover_menu.set_final_score(self.score)
        self.surfs.activate_update("background", "gameover_menu")
        self.surfs.activate_draw("background", "tetris", "gameover_menu")
        self.music.fadeout(1000)

    def get_high_scores(self):
        params = {"qnt": 10, "sort": True}
        response = requests.get(self.tetro_api_url, params=params)
        high_scores = response.json()
        return high_scores

    def submit_high_score(self):
        name = self.gameover_menu.get_name().strip()
        if name:
            data = {"name": name, "score": self.score}
            requests.post(self.tetro_api_url, data=data)
            self.gameover_menu.clear_name()
            self.show_main_menu()

    def set_options(self):
        music_vol = self.options_menu.get_music_vol()
        soundfx_vol = self.options_menu.get_soundfx_vol()
        self.music.set_volume(music_vol/10)
        self.soundfx.set_volume(soundfx_vol/10)
        self.show_main_menu()

    def play_sound(self, clear_count):
        if clear_count == 4:
            self.soundfx.play(self.tetris_sound)
        else:
            self.soundfx.play(self.clear_sound)

    def update_score(self, clear_count):
        if clear_count:
            self.play_sound(clear_count)
            self.lines_cleared += clear_count
            self.score += self.line_count_points[clear_count-1]
            self.level = self.lines_cleared // 10 + 1
            self.tetris.time_segment = 15 - self.level
            if self.tetris.time_segment == 0: self.tetris.time_segment = 1
            self.background.set_level(self.level)
            self.background.set_score(self.score)
            self.background.set_lines(self.lines_cleared)

    def draw_next_piece(self):
        next = self.tetris.next_piece
        if next:
            if next.id == 5: xoff, yoff = 445, 253
            elif next.id == 6: xoff, yoff = 445, 271
            else: xoff, yoff = 460, 271
            for sq in next.shape:
                x = sq[0] * self.scale + xoff
                y = -sq[1] * self.scale + yoff
                self.window.blit(next.piece_img, (x, y))

    def run(self):
        running = True
        while running:
            self.clock.tick(self.fps)
            self.surfs.update()
            self.surfs.draw(self.window)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    self.surfs.check_event(event)





class TetrisGame(SurfaceObject):
    def __init__(self, controller, gw, gh, pos, parent):
        SurfaceObject.__init__(self, pygame.Surface((gw, gh)), pos, parent)
        self.controller = controller
        self.gw, self.gh = gw, gh
        self.scale = 30
        self.rows = 20
        self.cols = 10
        self.grid_bg = pygame.Color(50, 50, 50)
        self.piece = None
        self.next_piece = None
        self.init_grid()
        self.init_pieces()
        self.init_offsets()

        self.time = 0
        self.time_segment = 15
        self.time_step = 1
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
        elif key == 112:
            self.controller.toggle_pause()

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

    def reset(self):
        self.time_segment = 15
        self.reset_pieces()
        self.clear_grid()

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

    def check_clear_lines(self):
        self.cleared_lines = self.clear_lines()
        self.controller.update_score(len(self.cleared_lines))
        if self.cleared_lines:
            self.clearing_lines = True
            self.turn_cleared_white()

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
                    self.check_clear_lines()
                    self.new_piece()
                    self.down_down = False
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

import pygame



class Widget(object):
    def check_event(self, event): pass
    def update(self): pass
    def draw(self, surface): pass




class SurfaceObject(Widget):
    def __init__(self, surface, pos, parent=None, center_blit=False):
        Widget.__init__(self)
        self.surface = surface
        self.rect = self.surface.get_rect()
        self.center_blit = center_blit
        if parent:
            self.rect.topleft = (parent.rect.left+pos[0], parent.rect.top+pos[1])
        else:
            self.rect.topleft = pos
        if center_blit:
            self.rect.topleft = (self.rect.left-self.rect.w//2, self.rect.top-self.rect.h//2)
        self.pos = self.rect.topleft

    def reset_rect(self, new_rect):
        if self.center_blit:
            new_rect.center = self.rect.center
        else:
            new_rect.topleft = self.rect.topleft
        self.rect = new_rect
        self.pos = self.rect.topleft




class WidgetSurface(SurfaceObject):
    def __init__(self, surface, pos, parent, center_blit):
        SurfaceObject.__init__(self, surface, pos, parent, center_blit)
        self.widgets = []

    def add_widget(self, widget):
        self.widgets.append(widget)

    def check_event(self, event):
        for widget in self.widgets:
            widget.check_event(event)

    def update(self):
        for widget in self.widgets:
            widget.update()

    def draw(self, surface):
        surface.blit(self.surface, self.pos)
        for widget in self.widgets:
            widget.draw(surface)





class WidgetSurfaceHolder(object):
    def __init__(self):
        self.wss = {}
        self.update_active = []
        self.draw_active = []

    def add_widget_surface(self, name, ws):
        self.wss[name] = ws

    def activate_update(self, *args):
        self.update_active = [self.wss[name] for name in args if name in self.wss]

    def activate_draw(self, *args):
        self.draw_active = [self.wss[name] for name in args if name in self.wss]

    def activate(self, *args):
        self.update_active = [self.wss[name] for name in args if name in self.wss]
        self.draw_active = self.update_active

    def update(self):
        for ws in self.update_active:
            ws.update()

    def draw(self, surface):
        for ws in self.draw_active:
            ws.draw(surface)

    def check_event(self, event):
        for ws in self.update_active:
            ws.check_event(event)





class Label(SurfaceObject):
    def __init__(self, parent, pos, text="", center_blit=False):
        SurfaceObject.__init__(self, pygame.Surface((1,1)), pos, parent, center_blit)
        self.color = pygame.Color(255, 255, 255)
        self.font = pygame.font.SysFont("menlottc", 20)
        self.lines = []
        self.lines_height = 0
        self.gap = 5
        self.set_text(text)

    def set_gap(self, gap):
        self.gap = gap
        self.updated = True

    def set_text(self, text):
        self.text = str(text).split("\n")
        self.updated = True

    def set_color(self, color):
        self.color = color
        self.updated = True

    def set_font(self, name, size):
        self.font = pygame.font.SysFont(name, size)
        self.updated = True

    def render_text(self):
        self.lines = []
        w, h = 0, 0
        for line in self.text:
            text_surf = self.font.render(line, True, self.color)
            rect = text_surf.get_rect()
            if rect.w > w: w = rect.w
            h += rect.h + self.gap
            self.lines.append(text_surf)
        h -= self.gap
        self.line_height = (h + self.gap) / len(self.lines)
        self.reset_rect(pygame.Rect((0, 0), (w, h)))

    def update(self):
        if self.updated:
            self.render_text()
            self.updated = False

    def draw(self, surface):
        x = self.pos[0]
        y = self.pos[1]
        for line in self.lines:
            surface.blit(line, (x, y))
            y += self.line_height




class Button(SurfaceObject):
    def __init__(self, parent, pos, image, hover_image=None, center_blit=True):
        SurfaceObject.__init__(self, pygame.image.load(image), pos, parent, center_blit)
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





class NumberInput(WidgetSurface):
    def __init__(self, parent, pos, btn_left_img, btn_right_img, min, max, start, step, btn_hover_img=None):
        WidgetSurface.__init__(self, pygame.Surface((1,1)), pos, parent, False)
        self.min = min
        self.max = max
        self.val = start
        self.step = step
        left_image = pygame.image.load(btn_left_img)
        right_image = pygame.image.load(btn_right_img)
        btn_rect = left_image.get_rect()
        self.left_button = Button(self, (0, 0), btn_left_img, center_blit=False)
        self.right_button = Button(self, (btn_rect.w+15, 0), btn_right_img, center_blit=False)
        self.val_label = Label(self, ((btn_rect.w*2)+30, 0), self.val)
        self.left_button.connect(lambda: self.set_val(self.val-self.step))
        self.right_button.connect(lambda: self.set_val(self.val+self.step))
        self.add_widget(self.left_button)
        self.add_widget(self.right_button)
        self.add_widget(self.val_label)

    def set_val(self, val):
        if val > self.max:
            val = self.max
        elif val < self.min:
            val = self.min
        self.val = val
        self.val_label.set_text(self.val)

    def get_val(self):
        return self.val





class Key(Widget):
    def __init__(self, key, func=None):
        Widget.__init__(self)
        self.key = key
        self.func = func

    def connect(self, func):
        self.func = func

    def check_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == self.key:
            self.func()

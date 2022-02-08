import pygame as pg


class Input:
    
    pg.font.init()

    font = pg.font.Font(None, 32)
    color_inactive = pg.Color('lightskyblue3')
    color_active = pg.Color('dodgerblue2')
    orange = (255,127,36)
    
    colors = {True: color_active, False: color_inactive}
    
    active = False
    color = colors[active]
    
    text = ''
    done = False
    
    def __init__(self, screen: pg.display, x, y, descrp: str):
        self._descrp = descrp
        self.x = x
        self.y = y
        self._input_box = pg.Rect(x, y, 140, 32)
        self._screen = screen


    def draw(self):
        txt_surface = self.font.render(self.text, True, self.colors[self.active])
        descrp_surface = self.font.render(self._descrp, True, self.orange)
        
        width = max(200, txt_surface.get_width() + 10)
        self._input_box.w = width
        
        self._screen.blit(txt_surface, (self._input_box.x+5, self._input_box.y+5))
        self._screen.blit(descrp_surface, (self.x, self.y - 30))
        pg.draw.rect(self._screen, self.colors[self.active], self._input_box, 2)
        
    def warrning(self):
        txt_surface = self.font.render('Incorrect formula', True, (255, 0, 0))
        self._screen.blit(txt_surface, (self.x+10, self.y+6))

class Button:
    
    pg.font.init()

    font = pg.font.Font(None, 32)
    color = pg.Color('aquamarine3')
    white = (255, 255, 255)
    
    def __init__(self, screen: pg.display, x, y):
        self.x = x
        self.y = y
        self._input_box = pg.Rect(x, y, 70, 40)
        self._screen = screen

    def draw(self):
        pg.draw.rect(self._screen, self.color, self._input_box)
        txt_surface = self.font.render('Draw', True, self.white)
        self._screen.blit(txt_surface, (self.x+8, self.y+10))
from tkinter import TRUE
import pygame as pg


class Input:
    
    pg.font.init()

    font = pg.font.Font(None, 32)
    color_inactive = pg.Color('lightskyblue3')
    color_active = pg.Color('dodgerblue2')
    color_error = pg.Color('lightcoral')
    red = pg.Color('red2')

    error_surface = font.render('Error', True, red)
    
    orange = (255,127,36)
    colors = {True: color_active, False: color_inactive}
    
    active = False
    color = colors[active]
    
    text = ''
    done = False
    error = False
    
                    
    def __init__(self, screen: pg.display, x, y, descrp: str):
        self._descrp = descrp
        self.x = x
        self.y = y
        self._input_box = pg.Rect(x, y, 140, 32)
        self.error_box = pg.Rect(x + 72 , y + 34 , 128, 40)
        self._screen = screen
        
        self._cursor = len(self.text)
        self.previos_value = self._cursor
        self._cursorability = True
        self._periodacursor = 0
        self._cursor_x = self.getSize()
        self._cursor_y_1 = self.y + 4
        self._cursor_y_2 = self.y + 28
        
    def getSize(self):
        if len(self.text) > 0:
            size = 0
            for i in range(self._cursor):
                letter = self.font.render(self.text[i], True, (0, 0, 0))
                size += letter.get_size()[0]
            return size
        return 0

    def draw(self):
        if self.active:
            self._periodacursor += 1
            if self._periodacursor == 15:
                self._periodacursor = 0
                self._cursorability = not self._cursorability
                
            if self._cursorability:
                if self.previos_value != self._cursor:
                    self._cursor_x = self.getSize()
                x = self.x + self._cursor_x + 6
                pg.draw.line(self._screen, (255, 255, 255), (x, self._cursor_y_1), (x,  self._cursor_y_2), 3)
                self.previos_value = self._cursor
                
        if self.error: 
            pg.draw.rect(self._screen, self.color_error, self.error_box)
            self._screen.blit(self.error_surface, (self.x + 105 , self.y + 44))
            
        txt_surface = self.font.render(self.text, True, self.colors[self.active])
        descrp_surface = self.font.render(self._descrp, True, self.orange)
        
        width = max(200, txt_surface.get_width() + 10)
        self._input_box.w = width
        
        self._screen.blit(txt_surface, (self._input_box.x+5, self._input_box.y+5))
        self._screen.blit(descrp_surface, (self.x, self.y - 30))
        pg.draw.rect(self._screen, self.colors[self.active], self._input_box, 2)
        
    def append(self, letter):
        self.text = self.text[:self._cursor] + letter + self.text[self._cursor:]
        if self._cursor < len(self.text):
            self._cursor += 1
        
    def delete(self):
        if self._cursor == 0:
            self._cursor = 1
        self.text = self.text[:self._cursor - 1] + self.text[self._cursor:]
        if self._cursor > 0:
            self._cursor -= 1
        
    def warrning(self):
        self.error = True
        

class Button:
    
    pg.font.init()

    font = pg.font.Font(None, 32)
    white = (255, 255, 255)
    orange = (255,127,36)
    
    def __init__(self, screen: pg.display, cors, size, color, text, descrp = None):
        self.text = text[0]
        self.text_cors = text[1]
        self.color = pg.Color(color)
        self.cors = cors
        self.size = size
        self._input_box = pg.Rect(*cors, *size)
        self._screen = screen
        
        self._descrp = None
        if descrp:
            self._descrp = self.font.render(descrp, True, self.orange)
        
    

    def draw(self):
        if self._descrp:
            self._screen.blit(self._descrp, (self._input_box.x, self._input_box.y - 25))
            
        pg.draw.rect(self._screen, self.color, self._input_box)
        txt_surface = self.font.render(self.text, True, self.white)
        self._screen.blit(txt_surface, (self.cors[0] + self.text_cors[0], self.cors[1] + self.text_cors[1]))
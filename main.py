import pygame, sys, os
from text_input import *
import math
from Parcer import Parcer
from formulas import folmulas



formula = ''
allowed_values = ['x', '+', '-', '*', '/', '.', '(', ')', '[', ']', '%', '^', '&',] + [str(i) for i in range(10)]
sin = ['sin', 'cos', 'tan', 'ctn', 'log']

CORS = None
ARRANGE = 12
LIMIT = 70

black = (0, 0, 0)
white = (255, 255, 255)
grey = (211,211,211)
red = (255, 0, 0)
hex_color = (30, 30, 30)


y_AXIS = [(299, 0), (299, 600), 2]
x_AXIS = [(0, 299), (600, 299), 2]

width, height = 900, 600
clock = pygame.time.Clock()
fps = 30
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Graf")

screen.fill(white)

txt_form = Input(screen, 650, 100, 'Formula:')

draw_btn = Button(screen, (650, 134), (70, 40), 'aquamarine3', ('Draw', (8, 10)))
minus = Button(screen, (650, 250), (60, 40), 'darkorchid3', ('-', (24, 8)), 'Zoom:')
plus = Button(screen, (720, 250), (60, 40), 'firebrick2', ('+', (24, 8)))

font = pg.font.Font(None, 32)


def correctFormula(formula):
    local_form = str(formula)
    
    if local_form == '':
        return False
    
    for i in sin:
        local_form = local_form.replace(i, '')
        
    if local_form.count('(') != local_form.count(')'):
        return False
    
    if local_form.count('[') != local_form.count(']'):
        return False
    
    for l in local_form:
        if l not in allowed_values:
            return False
    return True

def getX(i: int):
    if i == None:
        return None
    return i*ARRANGE + 300

def getY(i: int):
    if i == None:
        return None
    return -i*ARRANGE + 300



def drawSqueres():
    for i in range(0, 600, ARRANGE):
        pygame.draw.line(screen, grey, (i, 0), (i, 600))
        pygame.draw.line(screen, grey, (0, i), (600, i))
        
    pygame.draw.line(screen, black, *y_AXIS)
    pygame.draw.line(screen, black, *x_AXIS)
    
        
        
def getPoints(formula: str):
    if not formula:
        return
    
    count = formula.count('x')
    formula = formula.replace('x', '{}')
    points = []
    
    for x in range(-LIMIT, LIMIT):
        try:
            form = formula.replace('x', '{}')
            if x < 0:
                form = formula.replace('{}', '${}$')
            
            x_1 = x
            x_2 = x + 1
            y_1= Parcer._eval(form.format(*([(x_1)]*count)), x_1)
            y_2 = Parcer._eval(form.format(*([(x_2)]*count)), x_2)
            
            points.append(((getX(x_1), getY(y_1)), (getX(x_2), getY(y_2))))
        except ZeroDivisionError:
            continue
        
    return points


def drawGraf():
    global CORS
    if CORS:
        for cor in CORS:
            try:
                pygame.draw.line(screen, red, *cor, 4)
            except TypeError:
                continue

def printText(txt: Input, event_key):
    if event_key == pygame.K_LEFT:
        if txt._cursor > 0:
            txt._cursor -= 1
    elif event_key == pygame.K_RIGHT:
        if txt._cursor < len(txt.text):
            txt._cursor += 1
            
    elif event_key == pg.K_BACKSPACE and txt.active == True:
        txt.delete()
    else:
        txt.append(event.unicode)
        
def resize(arg):
    global ARRANGE
    global CORS
    global LIMIT
    
    if arg == 'plus':
        if ARRANGE < 30:
            ARRANGE += 2
            if LIMIT - int(ARRANGE/2) > 0:
                LIMIT -= int(ARRANGE/2)
    if arg == 'minus':
        if ARRANGE > 4:
            ARRANGE -= 2
            LIMIT += int(ARRANGE/2)
        
    CORS = getPoints(formula)
    
txt_form.active = True
while True:
    
    pygame.display.flip()
    screen.fill(white)
    clock.tick(fps)
    
    drawSqueres()
    drawGraf()
    pygame.draw.rect(screen, hex_color, [600, 0, 300, 600])
    txt_form.draw()
    draw_btn.draw()
    minus.draw()
    plus.draw()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if txt_form._input_box.collidepoint(event.pos):
                txt_form.active = True
                
            elif minus._input_box.collidepoint(event.pos):
                resize('minus')
                    
            elif plus._input_box.collidepoint(event.pos):
                resize('plus')
                
            elif draw_btn._input_box.collidepoint(event.pos):
                if txt_form.text != '':
                    if not correctFormula(txt_form.text):
                        txt_form.error = True
                        continue
                else:
                    txt_form.text = formula
                
                formula = txt_form.text
                txt_form.error = False
                
                CORS = getPoints(formula)
                txt_form.active = False
                
            else:
                txt_form.active = False

            txt_form.color = txt_form.colors[txt_form.active]
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                resize('plus')
                    
                cors = getPoints(formula)
            elif event.key == pygame.K_DOWN:
                resize('minus')
                
            if txt_form.active:
                printText(txt_form, event.key)

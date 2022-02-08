import pygame, sys, os
from text_input import *
import math
from Parcer import Parcer



formula = ['((-x)**2/3 - ((x)**4/3 - (4*x)**2 + 4)**(1/2)/2)',
           'sin([x])', 
           'cos(x)*cos(x) + sin(x)*sin(x)',
           '20/x',
           '(ctn(x**2))**0.5',
           'tan(x) + tan([x])',
           'ctn(x)/ctn([x])',
           'tan([x])',
           '(1+x)**0.5',
           '1/tan(x)*ctn(x)'][-1]
allowed_values = ['x', '+', '-', '*', '/', '.', '(', ')', '[', ']'] + [str(i) for i in range(10)]
sin = ['sin', 'cos', 'tan', 'ctn']

black = (0, 0, 0)
white = (255, 255, 255)
grey = (211,211,211)
red = (255, 0, 0)
hex_color = (30, 30, 30)


arrange = 12
limit = 25

y_AXIS = [(299, 0), (299, 600), 2]
x_AXIS = [(0, 299), (600, 299), 2]

width, height = 900, 600
clock = pygame.time.Clock()
fps = 30
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Graf")

screen.fill(white)

txt_form = Input(screen, 650, 100, 'Formula:')
txt_zoom = Input(screen, 650, 200, 'Zoom:')
txt_points = Input(screen, 650, 300, 'Points:')
txts = [txt_form, txt_zoom, txt_points]

btn = Button(screen, 650, 500)

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
    return i*arrange + 300

def getY(i: int):
    if i == None:
        return None
    return -i*arrange + 300

def drawSqueres():
    for i in range(0, 600, arrange):
        pygame.draw.line(screen, grey, (i, 0), (i, 600))
        pygame.draw.line(screen, grey, (0, i), (600, i))
        
    pygame.draw.line(screen, black, *y_AXIS)
    pygame.draw.line(screen, black, *x_AXIS)
    
        
        
def getPoints(formula: str):
    
    count = formula.count('x')
    formula = formula.replace('x', '{}')
    points = []
    
    for x in range(-limit, limit):
        try:
            if x < 0:
                formula = formula.replace('x', '${}$')
            #print(formula.format(*([str(x)]*count)), ',', formula.format(*([str(x + 1)]*count)))
            x_1 = x
            x_2 = x + 1
            y_1= Parcer._eval(formula.format(*([(x_1)]*count)), x_1)
            y_2 = Parcer._eval(formula.format(*([(x_2)]*count)), x_2)
            
            points.append(((getX(x_1), getY(y_1)), (getX(x_2), getY(y_2))))
        except ZeroDivisionError:
            continue
        
    return points

cors = getPoints(formula)
def drawGraf():
    for cor in cors:
        try:
          pygame.draw.line(screen, red, *cor, 4)
        except TypeError:
            continue

def printText(txt: Input, event_key):
    if txt.active == True:
        if event_key == pg.K_BACKSPACE:
            txt.text = txt.text[:-1]
        else:
            txt.text += event.unicode
            
def activate(*args):
    txt_form.active = args[0]
    txt_zoom.active = args[1]
    txt_points.active = args[2]
    
        
txt_form.active = True
while True:
    
    pygame.display.flip()
    screen.fill(white)
    clock.tick(fps)
    
    drawSqueres()
    drawGraf()
    pygame.draw.rect(screen, hex_color, [600, 0, 300, 600])
    txt_form.draw()
    txt_points.draw()
    txt_zoom.draw()
    btn.draw()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if txt_form._input_box.collidepoint(event.pos):
                activate(True, False, False)
                
            elif txt_zoom._input_box.collidepoint(event.pos):
                activate(False, True, False)
                
            elif txt_points._input_box.collidepoint(event.pos):
                activate(False, False, True)
               
                
            elif btn._input_box.collidepoint(event.pos):
                if txt_form.text != '':
                    if not correctFormula(txt_form.text):
                        txt_form.warrning()
                        continue
                else:
                    txt_form.text = formula
                
                formula = txt_form.text
                
                if txt_zoom.text:
                    try:
                        arrange = int(txt_zoom.text)
                    except ValueError:
                        txt_zoom.warrning()
                else:
                    arrange = 12
                        
                if txt_points.text:
                    try:
                        limit = int(txt_points.text)
                    except ValueError:
                        txt_points.warrning()
                else:
                    limit = 25
                
                cors = getPoints(formula)
                activate(False, False, False)
                
            else:
                activate(False, False, False)
                
            txt_form.color = txt_form.colors[txt_form.active]
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if arrange < 30:
                    arrange += 3
                cors = getPoints(formula)
            elif event.key == pygame.K_DOWN:
                if arrange > 4:
                    arrange -= 3
                cors = getPoints(formula)
            for t in txts:
                printText(t, event.key)

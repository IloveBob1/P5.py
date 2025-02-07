import pygame
from pygame.locals import *
from random import uniform
from typing import Optional
from math import *
pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((10, 10))
width = screen.get_width()
height = screen.get_height()
clock = pygame.time.Clock()
fps = 60
fill_color = (255, 255, 255)
use_fill = True
stroke_color = (0, 0, 0)
stroke_width = 1
use_stroke = True
keyCode = 0

def createCanvas(w: int, h: int) -> None: 
    """
    Takes a width (w) and height (h) and sets the screen
    with dimensions of w x h
    """
    global screen, width, height
    screen = pygame.display.set_mode((w, h))
    width = w
    height = h
    
def frameRate(rate: Optional[int]=None) -> Optional[int]:
    """
    If a rate is passed, it sets the frame rate to said rate.
    Otherwise, it returns the current frame rate
    """
    global fps
    if rate:
        fps = rate
    else:
        return fps

def background(r: int, g: Optional[int]=None, b: Optional[int]=None) -> None:
    """
    Sets the background color to either (r, r, r) or (r, g, b)
    depending on if g and b are passed.
    """
    if not g and not b: screen.fill((r, r, r))
    else: screen.fill(r, g, b)
    
def fill(r: int, g: Optional[int]=None, b: Optional[int]=None) -> None:
    """
    Sets the fill color to either (r, r, r) or (r, g, b)
    depending on if g and b are passed.
    """
    global fill_color
    if not g and not b: fill_color = (r, r, r)
    else: fill_color = (r, g, b)
    
def noFill() -> None:
    """
    Removes fill
    """
    global use_fill
    use_fill = False

def stroke(r: int, g: Optional[int]=None, b: Optional[int]=None) -> None:
    """
    Sets the stroke color to either (r, r, r) or (r, g, b)
    depending on if g and b are passed
    """
    global stroke_color
    if not g and not b: stroke_color = (r, r, r)
    else: stroke_color = (r, g, b)

def strokeWidth(w: int) -> None:
    """
    Sets the stroke width to w
    """
    global stroke_width
    stroke_width = w

def noStroke() -> None:
    """
    Removes stroke
    """
    global use_stroke
    use_stroke = False

def rect(x: int, y: int, w: int, h: int) -> None:
    """
    Draws a rectangle at (x, y) with dimensions of w x h
    """
    if use_fill:
        pygame.draw.rect(screen, fill_color, (x, y, w, h))
    if use_stroke:
        pygame.draw.rect(screen, stroke_color, (x, y, w, h), stroke_width)

def constrain(val: float, minimum: float, maximum: float) -> float:
    """
    Returns val if the value doesnt go over maximum and under minimum
    if it does, it return the appropriate limit.
    """
    
    if val > maximum:
        return maximum
    elif val < minimum:
        return minimum
    else:
        return val

def dist(x0: float, y0: float, x1: float, y1: float) -> float:
    """
    Outputs the distance between point (x0, y0) and point (x1, y1)
    """
    return sqrt((y1-y0)**2 + (x1-x0)**2)

def random(mn: float, mx: Optional[float]=None) -> float:
    """
    Returns a random number between mn and mx.
    if mx is None, it will assume that that the expected range is between 0 and mn
    """
    
    if not mx:
        return uniform(0, mn)
    else:
        return uniform(mn, mx)
    
class createVector:
    def __init__(self, x: float, y: float, z: Optional[float]=None):
        """
        Creates either a 2d vector with (x, y) pr a 3d vector with (x, y, z)
        """
        self.x = x
        self.y = y
        self.z = z
    
    def mult(self, val: float) -> None:
        """
        Multiplies every axis by val
        """
        self.x *= val
        self.y *= val

################     code     ####################
class P5Variables:
    def __init__(self):
        # Enter global variables here
        # you can access global variables with vars.[variable]
        self.s = None
        self.scl = 20
        self.food = None
vars = P5Variables()

def setup():
    createCanvas(800, 800)
    vars.s = Snake()
    frameRate(10)
    pickLocation()
    
def pickLocation():
    cols = floor(width/vars.scl)
    rows = floor(width/vars.scl)
    vars.food = createVector(floor(random(cols)), floor(random(rows)))
    vars.food.mult(vars.scl)

def draw():
    background(51)
    
    if vars.s.eat(vars.food):
        pickLocation()
    vars.s.death()
    vars.s.update()
    vars.s.show()
    
    fill(255, 0, 100)
    rect(vars.food.x, vars.food.y, vars.scl, vars.scl)
    
def keyPressed():
    if keyCode == K_UP and vars.s.yspeed != 1:
        vars.s.dir(0, -1)
    elif keyCode == K_DOWN and vars.s.yspeed != -1:
        vars.s.dir(0, 1)
    elif keyCode == K_RIGHT and vars.s.xspeed != -1:
        vars.s.dir(1, 0)
    elif keyCode == K_LEFT and vars.s.xspeed != 1:
        vars.s.dir(-1, 0)

def mousePressed():
    vars.s.total += 1

class Snake():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.xspeed = 1
        self.yspeed = 0
        self.total = 0
        self.tail = []
    
    def dir(self, x, y):
        self.xspeed = x
        self.yspeed = y
    
    def eat(self, pos):
        d = dist(self.x, self.y, pos.x, pos.y)
        if d < 1:
            self.total += 1
            return True
        return False
    
    def death(self):
        for i in range(len(self.tail)):
            try:
                pos = self.tail[i]
            except IndexError:
                continue
            d = dist(self.x, self.y, pos.x, pos.y)
            if (d < 1):
                self.total = 0
                self.tail = []
        
    def update(self):
        if self.total != 0:
            if self.total > 1:
                while self.total != len(self.tail): self.tail.append(createVector(self.tail[-1].x, self.tail[-1].y))
            else:
                while self.total != len(self.tail): self.tail.append(createVector(self.x, self.y))
            
            for i in range(self.total-1):
                self.tail[i] = self.tail[i+1]
            self.tail[self.total-1] = createVector(self.x, self.y)
        
        self.x += self.xspeed*vars.scl;
        self.y += self.yspeed*vars.scl;
        
        self.x = constrain(self.x, 0, width-vars.scl)
        self.y = constrain(self.y, 0, height-vars.scl)
    
    def show(self):
        fill(255);
        for i in range(self.total):
            rect(self.tail[i].x, self.tail[i].y, vars.scl, vars.scl)
        rect(self.x, self.y, vars.scl, vars.scl)

################     end      ####################

setup()
while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            quit()
        if e.type == pygame.MOUSEBUTTONDOWN and "mousePressed" in globals():
            mousePressed()
        if e.type == pygame.KEYDOWN and "keyPressed" in globals():
            keyCode = e.key
            keyPressed()
    
    draw()
    pygame.display.flip()
    clock.tick(fps)

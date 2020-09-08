import pygame
import sys
import random
from time import sleep,time
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]


size = width, height = 400, 400
play_height = 340
play_width = 170
gap = 30
size_piece = 17

# colors
black = 88, 105, 148
blue_bg = 180, 196, 174

colors = [(55,63,81), (212, 81, 19), (249, 160, 63),
           (93,134,70),]
        


pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)

background = pygame.Surface(size)

class piece:
    def __init__(self, x, y, shape, color, orientation):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = color
        self.orientation = orientation
    def fall(self):
        self.y += size_piece
        if not pos_valid(self,locked_positions):
            self.y -=  size_piece
    def free_fall(self):
        n=0
        while 1:
            self.y += size_piece
            if not pos_valid(self,locked_positions):
                self.y -= size_piece
                break
            n+=1
        return n
    def change_orientation(self):
        previous = self.orientation
        self.orientation = (self.orientation + 1) % len(self.shape)
        if not pos_valid(self,locked_positions):
            self.orientation = previous


def get_piece():
    shape = random.choice(shapes)
    return piece(gap+size_piece*5, gap+2*size_piece, shape, colors[random.randint(0, len(colors)-1)], random.randint(0,len(shape)-1))


def print_shape(piece):
    for lines_index,lines in enumerate(piece.shape[piece.orientation]):
        for point_index,point in enumerate(lines):
            if point == '0':
                pygame.draw.rect(background,piece.color, (piece.x+(point_index-2)*size_piece,piece.y+(lines_index-2)*size_piece,size_piece,size_piece))

def pos_valid(piece,locked_positions):
    for lines_index,lines in enumerate(piece.shape[piece.orientation]):
        for point_index,point in enumerate(lines):
            if point == '0':
                curr_point_x = piece.x+(point_index-2)*size_piece
                curr_point_y = piece.y+(lines_index-2)*size_piece
                if gap + play_width< curr_point_x+size_piece or gap+play_height < curr_point_y+size_piece or curr_point_x + size_piece <= gap :
                    return False
                if locked_positions[int((curr_point_y-gap)/size_piece)][int((curr_point_x-gap)/size_piece)] != (0,0,0):
                    return False
    return True

def fallen_piece(piece,locked_positions):

    for lines_index,lines in enumerate(piece.shape[piece.orientation]):
        for point_index,point in enumerate(lines):
            if point == '0':
                curr_point_x = piece.x+(point_index-2)*size_piece
                curr_point_y = piece.y+(lines_index-2)*size_piece
                if curr_point_y+size_piece == gap+play_height:
                    return True
                elif locked_positions[int((curr_point_y-gap)/size_piece)+1][int((curr_point_x-gap)/size_piece)] != (0,0,0):
                    return True
    return False

def add_locked(piece,locked_positions):
    for lines_index,lines in enumerate(
        piece.shape[piece.orientation]):
        for point_index,point in enumerate(lines):
            if point == '0':
                curr_point_x = piece.x+(point_index-2)*size_piece
                curr_point_y = piece.y+(lines_index-2)*size_piece
                locked_positions[int((curr_point_y-gap)/size_piece)][int((curr_point_x-gap)/size_piece)]=piece.color
                n_elem[int((curr_point_y-gap)/size_piece)]+=1

def print_locked(locked_positions): 
    for y in range(20):
        for x in range(10):
            if locked_positions[y][x] != (0,0,0):
                pygame.draw.rect(background,locked_positions[y][x],(x*size_piece+gap,y*size_piece+gap,size_piece,size_piece))

def check_lines(n_elem):
    for y in range(20):
        if n_elem[y] == 10:
            return y
    return -1

def clear_line(locked_positions,line,n_elem):
    n_elem[line] = 0
    for x in range(10):
        locked_positions[line][x]=(0,0,0)
    for y in reversed(range(line)):
        for x in range(10):
            if locked_positions[y][x] != (0,0,0):
                n_elem[y] = n_elem[y]-1
                n_elem[y+1] += 1 
                previous = locked_positions[y][x]
                locked_positions[y][x]= (0,0,0)
                locked_positions[y+1][x] = previous 

def show_score(total_points,level):
    scoretext = myfont.render(str(total_points), 1, (88, 105, 148))
    leveltext = myfont.render(str(level),1,(88, 105, 148))
    scorebox = scoretext.get_rect(center=(gap*2+play_width+75,gap+35))
    levelbox = scoretext.get_rect(center=(gap*2+play_width+75,2*gap+70+35))
    screen.blit(leveltext,levelbox)
    screen.blit(scoretext, scorebox)

atual_piece = get_piece()
start_time = time()
start_time_level = time()
start_time_hard_drop = 0
locked_positions = [[(0,0,0) for _ in range(10) ]for _ in range(20)]
n_elem = [0 for _ in range (20)]
total_points = 0
myfont = pygame.font.SysFont("Arial",30)
hard_drop_mode = False
velocity = 0.5

pontuation = [40,100,300,1200]

def add_points_lines(n,level):
    total=0
    for j in reversed(range(1,5)):
        total += int(n/j)*pontuation[j-1]*(level+1)
        n = n % j
    return total

level = 0
while 1:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                atual_piece = get_piece()
            if event.key == pygame.K_RIGHT:
                atual_piece.x += size_piece 
                #print(pos_valid(atual_piece))
                if not pos_valid(atual_piece,locked_positions):
                    atual_piece.x -= size_piece
            if event.key == pygame.K_LEFT:
                atual_piece.x -= size_piece 
                #print(pos_valid(atual_piece))
                if not pos_valid(atual_piece,locked_positions):
                    atual_piece.x += size_piece 
            if event.key == pygame.K_DOWN:
                total_points += atual_piece.free_fall() 
                start_time_hard_drop = time()
                hard_drop_mode = True
            if event.key == pygame.K_UP:
                atual_piece.change_orientation()

    curr_time = time()
    if velocity > 0.1:
        velocity = 0.5+(level*(-0.02))

    if curr_time - start_time > velocity:
        #print(curr_time-start_time) 
        start_time = time()
        atual_piece.fall()

    if curr_time - start_time_level > 15:
        start_time_level = time()
        level += 1

    if curr_time - start_time_hard_drop > 0.25:
        hard_drop_mode = False

    print(hard_drop_mode)
    #print(fallen_piece(atual_piece,locked_positions))
    if not hard_drop_mode:

        if fallen_piece(atual_piece,locked_positions):
            add_locked(atual_piece,locked_positions)
            atual_piece = get_piece()
            if not pos_valid(atual_piece,locked_positions):
                sys.exit()
    

    background.fill(black)
    pygame.draw.rect(background, (blue_bg), (gap,gap,play_width,play_height))
    pygame.draw.rect(background, (blue_bg), (play_width+2*gap,gap,150,70))
    pygame.draw.rect(background, (blue_bg), (play_width+2*gap,2*gap+70,150,70))
    
    cleared_lines = 0
    while 1:
        line = check_lines(n_elem)
        if line == -1:
            break
        clear_line(locked_positions,line,n_elem)
        cleared_lines += 1

    if cleared_lines != 0:
        total_points += add_points_lines(cleared_lines,level)

    #print(n_elem)
    print_shape(atual_piece)
    print_locked(locked_positions)

    """ print(atual_piece.x)
    print(atual_piece.y)
    print(atual_piece.shape.index)
    print(atual_piece.color)
    print(atual_piece.orientation)  """
    #print(total_points)
    
    screen.blit(background,(0,0))
    show_score(int(total_points),level)
    pygame.display.flip()

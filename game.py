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
    def change_orientation(self):
        self.orientation = (self.orientation + 1) % len(self.shape)



def get_piece():
    shape = random.choice(shapes)
    return piece(gap+size_piece*5, gap+2*size_piece, shape, colors[random.randint(0, len(colors)-1)], random.randint(0,len(shape)-1))


def print_shape(piece):
    x=-2
    y=-2
    #aux_l=[] 
    for lines in piece.shape[piece.orientation]:
        for point in lines:
            #print(point,end ="")
            if point == '0':
                pygame.draw.rect(background,piece.color, (piece.x+x*size_piece,piece.y+y*size_piece,size_piece,size_piece))
            x+=1
            #aux_l.append(piece.shape[piece.orientation].index(lines))
        x = -2
        y += 1
    #print(aux_l)


def pos_valid(piece,locked_positions):
    x=-2
    y=-2
    for lines in piece.shape[piece.orientation]:
        for point in lines:
            if point == '0':
                curr_point_x = piece.x+x*size_piece
                curr_point_y = piece.y+y*size_piece
                if gap + play_width< curr_point_x+size_piece or gap+play_height < curr_point_y+size_piece or curr_point_x + size_piece <= gap :
                    return False
                if (curr_point_x,curr_point_y) in locked_positions:
                    return False
            x+=1
        x = -2
        y += 1
    return True

def fallen_piece(piece,locked_positions):
    x=-2
    y=-2
    for lines in piece.shape[piece.orientation]:
        for point in lines:
            if point == '0':
                curr_point_x = piece.x+x*size_piece
                curr_point_y = piece.y+y*size_piece

                if (curr_point_x,curr_point_y+size_piece) in locked_positions or curr_point_y+size_piece == gap+play_height:
                    return True
            x+=1
        x = -2
        y += 1
    return False

def add_locked(piece,locked_positions):
    x=-2
    y=-2
    
    for lines in piece.shape[piece.orientation]:
        for point in lines:
            if point == '0':
                curr_point_x = piece.x+x*size_piece
                curr_point_y = piece.y+y*size_piece
                locked_positions [curr_point_x,curr_point_y]=piece.color
            x+=1
        x = -2
        y += 1 

def print_locked(locked_positions):
    for key in locked_positions:
        x,y = key
        pygame.draw.rect(background,locked_positions[key],(x,y,size_piece,size_piece))


atual_piece = get_piece()
start_time = time()
locked_positions = {}

for x,y in zip([p for p in range(-2,2)],[p for p in range(-2,2)]):
    print(x,y)


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
                atual_piece.y += size_piece 
                #print(pos_valid(atual_piece))
                if not pos_valid(atual_piece,locked_positions):
                    atual_piece.y -= size_piece 
            if event.key == pygame.K_UP:
                atual_piece.change_orientation()

    curr_time = time()

    if curr_time - start_time > 0.5:
        #print(curr_time-start_time)
        start_time = time()
        atual_piece.fall()
    
    #print(fallen_piece(atual_piece,locked_positions))

    if fallen_piece(atual_piece,locked_positions):
        add_locked(atual_piece,locked_positions)
        atual_piece = get_piece()
    

    background.fill(black)
    pygame.draw.rect(background, (blue_bg), (gap,gap,play_width,play_height))
    pygame.draw.rect(background, (blue_bg), (play_width+2*gap,gap,150,70))
    pygame.draw.rect(background, (blue_bg), (play_width+2*gap,2*gap+70,150,70))
    print_shape(atual_piece)
    print_locked(locked_positions)
    
    """ print(atual_piece.x)
    print(atual_piece.y)
    print(atual_piece.shape.index)
    print(atual_piece.color)
    print(atual_piece.orientation)  """

    
    screen.blit(background,(0,0))
    pygame.display.flip()

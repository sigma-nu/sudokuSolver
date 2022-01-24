import sys
import pygame
import math

# Recursive Sudoku Solver!
#
# This script automatically solves any sudoku puzzle by using a recursive algorithm
# and back-tracking.
# 1. Find an empty cell (Empty cell = 0)
# 2. Find the first valid number for that cell and input it - This essentially creates
#    a new sudoku puzzle to solve (This is where recursion comes in!)
# 3. Recursively try to solve the new puzzle
#    - If any future empty cells have no valid numbers, the input number must be wrong
#      so set it back to empty (Back-track)
#    - If the sudoku completes it must be solved!
#
# Future improvements:
# 1. Hit spacebar and it auto-completes without animation.
# 2. Make it interactive - Attempt to solve it yourself first
# 3. Generalise it to solve any n^2 puzzle --- DONE

pygame.init()
pygame.font.init()
pygame.display.set_caption("Sudoku")

# Sudoku examples
sudoku = [[0,0,0, 2,6,0, 7,0,1], # Easy
          [6,8,0, 0,7,0, 0,9,0],
          [1,9,0, 0,0,4, 5,0,0],

          [8,2,0, 1,0,0, 0,4,0],
          [0,0,4, 6,0,2, 9,0,0],
          [0,5,0, 0,0,3, 0,2,8],
          
          [0,0,9, 3,0,0, 0,7,4],
          [0,4,0, 0,5,0, 0,3,6],
          [7,0,3, 0,1,8, 0,0,0]]

#sudoku = [[0,0,1, 3,0,2, 0,0,0], # Hard
#          [0,0,3, 0,0,7, 0,4,5],
#          [0,0,7, 0,0,0, 0,0,9],
#
#          [0,0,6, 5,0,0, 0,7,0],
#          [2,0,0, 0,0,0, 0,0,1],
#          [0,9,0, 0,0,1, 4,0,0],
#          
#          [5,0,0, 0,0,0, 9,0,0],
#          [6,1,0, 2,0,0, 8,0,0],
#          [0,0,0, 9,0,8, 5,0,0]]

#sudoku = [[ 6, 0, 0, 0,  2, 0, 0,12,  0, 0, 0,14,  0, 5, 3, 0], # Mega (Takes a long time to solve)
#          [ 0,14, 0,13,  9, 1, 0, 7, 12, 0, 0, 0,  0, 0, 0,16],
#          [ 3,15, 0, 0,  5, 0, 0,13,  0, 0, 0, 0, 14, 0, 8, 0],
#          [ 0, 9, 2,10,  0, 0, 0, 0,  7, 0, 0, 0, 13, 6, 0, 0],
#          
#          [ 0, 0, 0, 2,  0, 7,11, 9,  0, 0,15, 6,  0,10, 0, 8],
#          [ 0, 0, 8, 0,  0,12, 3,14, 16, 0, 9, 0,  6, 0, 0, 0],
#          [16, 0, 4,15,  0, 0, 0, 0,  0,10,14, 7, 11, 0, 0, 9],
#          [ 7, 3, 9, 0,  4, 0,13,10,  0, 0,12, 5,  0, 0,14, 0],
#
#          [ 9,10, 0, 0,  0, 0, 0,16,  6, 7, 0, 3,  0,15, 0, 0],
#          [ 1, 7,13, 0, 14, 0, 5, 8,  0,15, 0, 0,  0, 0, 2, 0],
#          [ 0, 0, 3, 0,  0, 0, 7, 0,  5, 2,16, 9,  0, 0,12,13],
#          [ 0, 0, 0,16, 12, 0, 0,15,  8,14, 0, 1,  0,11, 0, 7],
#          
#          [11, 0, 0, 0, 13, 0,16, 1,  0, 0, 0, 0,  0, 8, 9, 6],
#          [12, 0,15, 0,  0, 8, 0, 0,  9, 0, 4, 0,  0, 0, 0, 5],
#          [ 0, 2, 0, 1, 10, 9, 0, 0,  0,16, 5,11,  0,14,15, 0],
#          [ 0, 0, 0, 9, 11, 2, 4, 5,  0, 0, 0, 0,  1, 3, 0, 0]]

# Frame rate
FPS = 60
clock = pygame.time.Clock()

# Window size
size = width, height = 400, 400

# Border and cell dimesions
b_width = int(width/20)
b_height = int(height/20)
cell_width = (width-2*b_width)/len(sudoku)
cell_height = (height-2*b_height)/len(sudoku)

# Initialize screen
screen = pygame.display.set_mode(size)

# Colours
black = 0, 0, 0
grey = 160, 160, 160
white = 255, 255, 255
green = 0, 255, 0
red = 255, 0, 0


# Main code -----
def checkRow(board, n, y):
    return n not in board[y]

def checkColumn(board, n, x):
    for i in range(len(board)):
        if board[i][x] == n:
            return False
    return True

def checkBlock(board, n, y, x):
    blk_dim = int(math.sqrt(len(sudoku)))
    x_0 = (x//blk_dim)*blk_dim
    y_0 = (y//blk_dim)*blk_dim
    for i in range(blk_dim):
        for j in range(blk_dim):
            if board[y_0+i][x_0+j] == n:
                return False
    return True

def valid(board, n, y, x):
    return checkRow(board, n, y) and checkColumn(board, n, x) and checkBlock(board, n, y, x)

def solve(board):
    drawAll(board, 0, 0)
    pygame.display.flip()
    for y in range(len(sudoku)):
        for x in range(len(sudoku)):
            if board[y][x] == 0:
                for n in range(1, len(sudoku)+1):
                    if valid(board, n, y, x):
                        board[y][x] = n
                        drawAll(board, x, y, green)
                        solve(board)
                        board[y][x] = 0
                    else:
                        board[y][x] = n
                        drawAll(board, x, y, red)
                        board[y][x] = 0
                return
    while True:
        drawAll(sudoku)

def drawGrid():
    # Minor grid
    for j in range(len(sudoku)):
        for i in range(len(sudoku)):
            x = cell_width*i + b_width
            y = cell_height*j + b_height
            pygame.draw.rect(screen, grey, (x, y, cell_width, cell_height), 1)
    # Major grid
    blk_dim = int(math.sqrt(len(sudoku)))
    for j in range(blk_dim):
        for i in range(blk_dim):
            x = cell_width*i*blk_dim + b_width
            y = cell_height*j*blk_dim + b_height
            pygame.draw.rect(screen, black, (x, y, cell_width*blk_dim, cell_height*blk_dim), 2)

def drawNumber(board, x, y, colour=black):
    font_size = int(0.5*cell_height)
    fnt = pygame.font.SysFont('comicsans', font_size)
    text = fnt.render(str(board[y][x]), True, colour)
    text_rect = text.get_rect(center=(b_width + cell_width*(x+0.5), b_height + cell_height*(y+0.5)))
    screen.blit(text, text_rect)

def drawBox(x, y, colour):
    x_tl = x*cell_width + b_width
    y_tl = y*cell_height + b_height
    box = pygame.draw.rect(screen, colour, pygame.Rect(x_tl, y_tl, cell_width, cell_height),2)

def drawBoard(board):
    drawGrid()
    for y in range(len(sudoku)):
        for x in range((len(sudoku))):
            if board[y][x] != 0:
                drawNumber(board, x, y)

def drawAll(board, x = 0, y = 0, box_colour = None):
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    screen.fill(white)
    drawBoard(board)
    if box_colour != None:
        drawBox(x, y, box_colour)
    clock.tick(FPS)
    pygame.display.flip()


# Run -----
solve(sudoku)
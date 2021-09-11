import numpy as np
import time
import pygame
import sys

HIGHEST_PIECE = 3
DIAMETER_BIG = 600
DIAMETER_SMALL = 60
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (30, 30, 30)
WHITE = (240, 240, 240)
SCORE = 0

def create_board():
    board = np.zeros(20)
    return board

def generate_piece(board, to_gen):
    global HIGHEST_PIECE
    np.random.seed(seed = None)
    p = [0.0, 0.0, 0.0, 0.075, 0.075, 0.13, 0.17, 0.25, 0.17, 0.13]
    piece = np.random.choice(np.arange(1,11), p = p)
    piece = HIGHEST_PIECE - piece
    if piece < 1:
        piece = np.random.choice([1, 2, 3])
    if np.nonzero(board):
        min = 1
    else:
        min = np.amin(board[board>0])
    piece = np.random.choice([min, piece, -1], p = [0.05, 0.8, 0.15])
    if HIGHEST_PIECE > 11:
        piece = np.random.choice([piece, -2, -3, -4], p = [0.97, 0.1, 0.1, 0.1])
    temp = board[board != 0]
    if temp.size > 14:
        piece = np.random.choice([piece, -1])
    if piece == -3 or piece == -4:
        to_gen = False
    return piece, to_gen

def merge(board, piece):
    global SCORE
    pluses = np.where(board == -1)[0]
    temp = board[board != 0]
    s = temp.size
    cell = 0
    index = None
    blk_pluses = np.where(board == -2)[0]
    # black merging
    if blk_pluses.size != 0:
        if s > 2:
            index = blk_pluses[0]
            cell = max([cell, temp[(index+1)%s]])
            if cell == -1:
                cell = 1
            SCORE = SCORE + np.abs(2 ** cell)
            cell = cell + 3
            temp[index] = cell
            temp[index - 1], temp[(index + 1) % s] = 0, 0
            draw_board(temp, piece)
            time.sleep(1.15)
            temp = arrange(temp)
            temp = temp[temp != 0]
            s = temp.size
            print("s and index(black merging)")
            print(s)
            if index != 0:
                index = index - 1
            print(index)
            if index == s:
                index = index - s
            if index < 0:
                index = index + s

    for i in pluses:
        if temp[i-1] == temp[(i+1)%s]:
            index = i
    while index != None:
        if temp[index-1] == -1 or temp[(index+1)%s] == -1:
            break
        if temp[index-1] == temp[(index+1)%s]:
            cell = max([cell, temp[(index+1)%s]])
            cell = cell + 1
            temp[index] = cell
            SCORE = SCORE + np.abs(2**cell)
            temp[index-1], temp[(index+1)%s] = 0, 0
            draw_board(temp, piece)
            time.sleep(1.15)
            if temp[0] == 0:
                adjust = 1
            else:
                adjust = 0
            temp = arrange(temp)
            temp = temp[temp != 0]
            s = temp.size
            if s <= 2:
                break
            if index != 0:
                index = index - 1 - adjust
            if index == s:
                index = index - s
            elif index < 0:
                index = index + s
        else:
            index = None
    print("go")
    board = arrange(temp)
    return board

def drop_piece(board, ang, piece):
    qt = board[board != 0].size
    t = np.linspace(0, 2* np.pi, qt+1, endpoint= True)
    index = 0
    place = None
    for i in t:
        if ang < i:
            place = index
            break
        index = index + 1
    if place == None:
        place = 0
    temp = board.copy()
    board[place] = piece
    for i in range(place, len(board)-1):
        board[i+1] = temp[i]
    board = arrange(board)
    return board

def arrange(board):
    temp = board.copy()
    places = np.nonzero(board)
    board = create_board()
    for i in range(places[0].size):
        board[i] = temp[places[0][i]]

    return board

def check_high(board):
    max = np.amax(board)
    global HIGHEST_PIECE
    if max > HIGHEST_PIECE:
        HIGHEST_PIECE = max

def filled(board):
    full = False
    if board[-1] != 0:
        full = True

    return full

def draw_board(board, piece):
    font = pygame.font.SysFont("monospace", 15)
    b_rad = DIAMETER_BIG / 2
    s_rad = DIAMETER_SMALL / 2
    big_col = (200, 50, 0)
    big_col2 = 0.9 * big_col[0], 0.9 * big_col[1], 0.9 * big_col[2]
    pygame.draw.circle(screen, color=big_col, center=(b_rad, b_rad), radius=b_rad)
    pygame.draw.circle(screen, color=big_col2, center=(b_rad, b_rad), radius=(b_rad-5))
    board = arrange(board)
    board = board[board != 0]
    qt = board.size
    t = np.linspace(0, 2 * np.pi, qt, endpoint = False)
    for i in range(qt):
        cent_big = b_rad, b_rad
        cent_small = (b_rad - (s_rad + 10)) * np.cos(t[i]), (b_rad - (s_rad + 10)) * np.sin(t[i])
        cent = cent_big[0] + cent_small[0], cent_big[1] + cent_small[1]
        col = choose_color(board[i])
        col2 = 0.9 * col[0], 0.9 * col[1], 0.9 * col[2]
        pygame.draw.circle(screen, color=col, center=cent, radius=s_rad)
        pygame.draw.circle(screen, color=col2, center=cent, radius=(s_rad-3))
        label = font.render(str(int(board[i])), 1, (0,0,0))
        screen.blit(label, cent)
    if piece != 0:
        color = choose_color(piece)
        pygame.draw.circle(screen, color=color, center=cent_big, radius=s_rad)
        label = font.render(str(int(piece)), 1, (0,0,0))
        screen.blit(label, cent_big)
        label_score = font.render(f"SCORE: {SCORE}", 1, (200,200,200))
        screen.blit(label_score, [10, 10])
    pygame.display.update()

def choose_color(piece):
    if piece < 0:
        neg_colors = [RED, BLACK, BLUE, WHITE]
        piece = piece * (-1) - 1
        color = neg_colors[int(piece)]
        return color
    colors = np.linspace(50, 251, num = 200)
    np.random.seed(int(piece))
    r, g, b = np.random.choice(colors, 3)
    color = (r, g, b)
    return color

def take_piece(board, ang, piece):
    qt = board[board != 0].size
    t = np.linspace(0, 2 * np.pi, qt + 1, endpoint=False)
    index = 0
    place = None
    for i in t:
        if ang < i:
            place = index
            break
        index = index + 1
    if place == None:
        place = 0
    temp = board.copy()
    piece = board[place]
    if piece == -3:
        for i in range(place, len(temp) - 1):
            board[i] = temp[i+1]
    board = arrange(board)
    return board, piece

#Initializing
board = create_board()
game_over = False
for i in range(3):
    piece = np.random.choice([1, 2, 3])
    drop_piece(board, 0.1, piece)
print(board)

pygame.init()
pygame.font.init()

size = (DIAMETER_BIG, DIAMETER_BIG)
screen = pygame.display.set_mode(size)
to_gen = True
piece, to_gen = generate_piece(board, to_gen)
draw_board(board, piece)
pygame.display.update()

while not game_over:
    check_high(board)
    game_over = filled(board)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            pos = pos[0] - DIAMETER_BIG/2, pos[1] - DIAMETER_BIG/2
            dist = np.absolute(pos[0] + i*pos[1])
            if pos[0] == 0:
                tan = pos[1] * np.Inf
            else:
                tan = pos[1]/pos[0]
            ang = np.arctan(tan)
            if pos[0] < 0:
                ang = ang + np.pi
            if pos[0] > 0 and pos[1] < 0:
                ang = ang + 2 * np.pi
            if to_gen:
                board = drop_piece(board, ang, piece)
                piece, to_gen = generate_piece(board, to_gen)
                draw_board(board, piece)
                board = merge(board, piece)
            else:
                if dist > 80:
                    board, piece = take_piece(board, ang, piece)
                    to_gen = True
                else:
                    piece = -1
                draw_board(board, piece)
                board = merge(board, piece)
            print(board)

for i in board:
    SCORE = SCORE + 2**i
print(f"Score: {SCORE}")


    # board = arrange(board)
    # piece = generate_piece(board)
    # selection = int(input(f"Place to shoot the piece {str(piece)}: "))
    # board = drop_piece(board, selection, piece)
    # print(board)
    # game_over = filled(board)
    # board = merge(board)
    # print(board)
    # check_high(board)


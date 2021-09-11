import numpy as np
import pygame

HIGHEST_PIECE = 3
DIAMETER_BIG = 600
DIAMETER_SMALL = 60
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (30, 30, 30)
WHITE = (240, 240, 240)
SCORE = 0
CONVERTABLE = False
MOVE = 0
sample_moves = np.arange(0,20)
sample_moves = np.append(sample_moves, [-5])

def create_board():
    board = np.zeros(20)
    return board

def get_samples():
    return sample_moves

def get_move():
    return MOVE

def get_score():
    return SCORE

def get_game_over():
    return GAME_OVER

def get_board():
    return BOARD

def get_piece():
    return PIECE

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
        piece = np.random.choice([piece, -1], p=(0.8, 0.2))
    if piece == -3 or piece == -4:
        to_gen = False
    return piece, to_gen

def merge(board):
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
            SCORE = SCORE + np.abs(2 * cell)
            cell = cell + 3
            temp[index] = cell
            temp[index - 1], temp[(index + 1) % s] = 0, 0
            #draw_board(temp, piece)
            temp = arrange(temp)
            temp = temp[temp != 0]
            s = temp.size
            if index != 0:
                index = index - 1
            if index == s:
                index = index - s
            elif index < 0:
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
            #draw_board(temp, piece)
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
    board = arrange(temp)
    return board

def drop_piece(board, place, piece):
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

def take_piece(board, place, piece):
    global CONVERTABLE
    temp = board.copy()
    p_piece = piece
    piece = board[place]
    if p_piece == -3:
        CONVERTABLE = True
        for i in range(place, len(temp) - 1):
            board[i] = temp[i+1]
    board = arrange(board)
    return board, piece

def game_reset():
    global MOVE, SCORE, HIGHEST_PIECE
    MOVE = 0
    HIGHEST_PIECE = 3
    board = create_board()
    game_over = False
    for i in range(3):
        piece = np.random.choice([1, 2, 3])
        drop_piece(board, 0, piece)

    to_gen = True
    piece, to_gen = generate_piece(board, to_gen)
    SCORE = 0
    return board, game_over, piece, to_gen

def render():
    draw_board(BOARD, PIECE)

def play_game():
    global MOVE
    MOVE = 0
    board, game_over, piece, to_gen = game_reset()
    while not game_over:
        MOVE += 1
        check_high(board)
        game_over = filled(board)
        board = arrange(board)
        if not CONVERTABLE:
            piece, to_gen = generate_piece(board, to_gen)
        while True:
            selection = int(input(f"choose place, or '-5' to convert the piece if possible ({str(piece)}): "))
            if CONVERTABLE and selection == -5:
                piece = -1
            if selection in sample_moves:
                break

        if to_gen:
            board = drop_piece(board, selection, piece)
            print(board)
            CONVERTABLE = False
        else:
            board, piece = take_piece(board, selection, piece)
            to_gen = True
        board = merge(board)

        print(board)
        game_over = filled(board)
        check_high(board)

    for i in board:
        SCORE = SCORE + 2**i
    print(f"Score: {SCORE}")

BOARD = create_board()
GAME_OVER = False
PIECE = None
TO_GEN = True
BOARD, GAME_OVER, PIECE, TO_GEN = game_reset()

screen = pygame.display
def init():
    pygame.init()
    pygame.font.init()

    size = (DIAMETER_BIG, DIAMETER_BIG)
    global screen
    screen = pygame.display.set_mode(size)

def reset():
    global MOVE, BOARD, GAME_OVER, TO_GEN, SCORE
    BOARD, GAME_OVER, PIECE, TO_GEN = game_reset()
    SCORE = 0

def make_move(selection):
    global MOVE, BOARD, GAME_OVER, TO_GEN, CONVERTABLE, PIECE
    MOVE += 1
    MOVE += 1
    check_high(BOARD)
    GAME_OVER = filled(BOARD)
    BOARD = arrange(BOARD)
    if CONVERTABLE:
        if selection == -5:
            PIECE = -1
        CONVERTABLE = False
        TO_GEN = True
    if not CONVERTABLE and selection == -5:
        selection = 0
    if TO_GEN:
        BOARD = drop_piece(BOARD, selection, PIECE)
    else:
        BOARD, PIECE = take_piece(BOARD, selection, PIECE)
        TO_GEN = True
    BOARD = merge(BOARD)
    if not CONVERTABLE:
        PIECE, TO_GEN = generate_piece(BOARD, TO_GEN)
import numpy as np
import pygame


class Game:
    def __init__(self):
        self.HIGHEST_PIECE = 3
        self.DIAMETER_BIG = 600
        self.DIAMETER_SMALL = 60
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        self.BLACK = (30, 30, 30)
        self.WHITE = (240, 240, 240)
        self.SCORE = 0
        self.CONVERTABLE = False
        self.MOVE = 0
        self.sample_moves = np.arange(0,20)
        self.sample_moves = np.append(self.sample_moves, [-5])

        self.BOARD = self.create_board()
        self.GAME_OVER = False
        self.PIECE = None
        self.TO_GEN = True
        self.BOARD, self.GAME_OVER, self.PIECE, self.TO_GEN = self.game_reset()

        self.screen = pygame.display


    def create_board(self):
        self.BOARD = np.zeros(20)
        return self.BOARD


    def get_samples(self):
        return self.sample_moves


    def get_move(self):
        return self.MOVE


    def get_score(self):
        return self.SCORE


    def get_game_over(self):
        return self.GAME_OVER


    def get_board(self):
        return self.BOARD


    def get_piece(self):
        return self.PIECE


    def draw_board(self, board, piece):
        font = pygame.font.SysFont("monospace", 15)
        b_rad = self.DIAMETER_BIG / 2
        s_rad = self.DIAMETER_SMALL / 2
        big_col = (200, 50, 0)
        big_col2 = 0.9 * big_col[0], 0.9 * big_col[1], 0.9 * big_col[2]
        pygame.draw.circle(self.screen, color=big_col, center=(b_rad, b_rad), radius=b_rad)
        pygame.draw.circle(self.screen, color=big_col2, center=(b_rad, b_rad), radius=(b_rad-5))
        board = self.arrange(board)
        board = board[board != 0]
        qt = board.size
        t = np.linspace(0, 2 * np.pi, qt, endpoint = False)
        for i in range(qt):
            cent_big = b_rad, b_rad
            cent_small = (b_rad - (s_rad + 10)) * np.cos(t[i]), (b_rad - (s_rad + 10)) * np.sin(t[i])
            cent = cent_big[0] + cent_small[0], cent_big[1] + cent_small[1]
            col = choose_color(board[i])
            col2 = 0.9 * col[0], 0.9 * col[1], 0.9 * col[2]
            pygame.draw.circle(self.screen, color=col, center=cent, radius=s_rad)
            pygame.draw.circle(self.screen, color=col2, center=cent, radius=(s_rad-3))
            label = font.render(str(int(board[i])), 1, (0,0,0))
            self.screen.blit(label, cent)
        if piece != 0:
            color = self.choose_color(piece)
            pygame.draw.circle(self.screen, color=color, center=cent_big, radius=s_rad)
            label = font.render(str(int(piece)), 1, (0,0,0))
            self.screen.blit(label, cent_big)
            label_score = font.render(f"SCORE: {SCORE}", 1, (200,200,200))
            self.screen.blit(label_score, [10, 10])
        pygame.display.update()

        self.BOARD = board


    def choose_color(self, piece):
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


    def generate_piece(self, board, to_gen):
        np.random.seed(seed = None)
        p = [0.0, 0.0, 0.0, 0.075, 0.075, 0.13, 0.17, 0.25, 0.17, 0.13]
        piece = np.random.choice(np.arange(1,11), p=p)
        piece = self.HIGHEST_PIECE - piece
        if piece < 1:
            piece = np.random.choice([1, 2, 3])
        if np.nonzero(board):
            min = 1
        else:
            min = np.amin(board[board>0])
        piece = np.random.choice([min, piece, -1], p=[0.05, 0.8, 0.15])
        if self.HIGHEST_PIECE > 11:
            piece = np.random.choice([piece, -2, -3, -4], p=[0.97, 0.1, 0.1, 0.1])
        temp = board[board != 0]
        if temp.size > 14:
            piece = np.random.choice([piece, -1], p=(0.8, 0.2))
        if piece == -3 or piece == -4:
            to_gen = False
        return piece, to_gen


    # def merge(self, board):
    #     pluses = np.where(board == -1)[0]
    #     temp = board[board != 0]
    #     s = temp.size
    #     cell = 0
    #     index = None
    #     blk_pluses = np.where(board == -2)[0]
    #
    #     # black merging
    #     if blk_pluses.size != 0:
    #         if s > 2:
    #             index = blk_pluses[0]
    #             cell = max([cell, temp[(index+1)%s]])
    #             if cell == -1:
    #                 cell = 1
    #             self.SCORE = self.SCORE + np.abs(2 * cell)
    #             cell = cell + 3
    #             temp[index] = cell
    #             temp[index - 1], temp[(index + 1) % s] = 0, 0
    #             #draw_board(temp, piece)
    #             temp = self.arrange(temp)
    #             temp = temp[temp != 0]
    #             s = temp.size
    #             if index != 0:
    #                 index = index - 1
    #             if index == s:
    #                 index = index - s
    #             elif index < 0:
    #                 index = index + s
    #
    #     for i in pluses:
    #         if temp[i-1] == temp[(i+1)%s]:
    #             index = i
    #
    #     while index != None:
    #         if temp[index-1] == -1 or temp[(index+1)%s] == -1:
    #             break
    #
    #         if temp[index-1] == temp[(index+1)%s]:
    #             cell = max([cell, temp[(index+1)%s]])
    #             cell = cell + 1
    #             temp[index] = cell
    #             self.SCORE = self.SCORE + np.abs(2**cell)
    #             temp[index-1], temp[(index+1)%s] = 0, 0
    #             #draw_board(temp, piece)
    #             if temp[0] == 0:
    #                 adjust = 1
    #             else:
    #                 adjust = 0
    #             temp = self.arrange(temp)
    #             temp = temp[temp != 0]
    #             s = temp.size
    #             if s <= 2:
    #                 break
    #             if index != 0:
    #                 index = index - 1 - adjust
    #             if index == s:
    #                 index = index - s
    #             elif index < 0:
    #                 index = index + s
    #
    #         else:
    #             index = None
    #
    #     board = self.arrange(temp)
    #     self.BOARD = board
    #     return board


    def merge(self, board):
        linked_list = BoardLinkedList(board)

        while linked_list.get_merging_index() >= 0:
            linked_list.merge_nodes()

        board = linked_list.construct_board()
        return board


    def drop_piece(self, board, place, piece):
        temp = board.copy()
        board[place] = piece
        for i in range(place, len(board)-1):
            board[i+1] = temp[i]
        board = self.arrange(board)
        self.BOARD = board
        return board


    def arrange(self, board):
        temp = board.copy()
        places = np.nonzero(board)
        board = self.create_board()
        for i in range(places[0].size):
            board[i] = temp[places[0][i]]

        self.BOARD = board
        return board


    def check_high(self, board):
        max = np.amax(board)
        if max > self.HIGHEST_PIECE:
            self.HIGHEST_PIECE = max


    def filled(self, board):
        full = False
        if board[-1] != 0:
            full = True

        return full


    def take_piece(self, board, place, piece):
        temp = board.copy()
        p_piece = piece
        piece = board[place]
        if p_piece == -3:
            self.CONVERTABLE = True
            for i in range(place, len(temp) - 1):
                board[i] = temp[i+1]
        board = self.arrange(board)

        self.BOARD = board
        return board, piece


    def game_reset(self):
        self.MOVE = 0
        self.HIGHEST_PIECE = 3
        self.BOARD = self.create_board()
        self.GAME_OVER = False

        not_random = [2, 2, 3]
        for i in range(3):
            # piece = np.random.choice([1, 2, 3])
            piece = not_random[i]
            self.BOARD = self.drop_piece(self.BOARD, 0, piece)

        to_gen = True
        piece, to_gen = self.generate_piece(self.BOARD, to_gen)
        self.SCORE = 0

        return self.BOARD, self.GAME_OVER, self.PIECE, self.TO_GEN


    def render(self):
        self.draw_board(self.BOARD, self.PIECE)


    def play_game(self):
        self.MOVE = 0
        self.BOARD, self.GAME_OVER, self.PIECE, self.TO_GEN = self.game_reset()

        print(self.BOARD)
        while not self.GAME_OVER:
            self.MOVE += 1
            self.check_high(self.BOARD)
            self.GAME_OVER = self.filled(self.BOARD)
            self.BOARD = self.arrange(self.BOARD)
            if not self.CONVERTABLE:
                self.PIECE, self.TO_GEN = self.generate_piece(self.BOARD, self.TO_GEN)
            while True:
                selection = int(input(f"choose place, or '-5' to convert the piece if possible ({str(self.PIECE)}): "))
                if self.CONVERTABLE and selection == -5:
                    self.PIECE = -1
                if selection in self.sample_moves:
                    break

            if self.TO_GEN:
                self.BOARD = self.drop_piece(self.BOARD, selection, self.PIECE)
                self.CONVERTABLE = False
            else:
                self.BOARD, self.PIECE = self.take_piece(self.BOARD, selection, self.PIECE)
                self.TO_GEN = True
            self.BOARD = self.merge(self.BOARD)

            print(self.BOARD)
            self.GAME_OVER = self.filled(self.BOARD)
            self.check_high(self.BOARD)

        for i in self.BOARD:
            self.SCORE = self.SCORE + 2**i
        print(f"Final Score: {self.SCORE}")


    def init_screen(self):
        pygame.init()
        pygame.font.init()

        size = (self.DIAMETER_BIG, self.DIAMETER_BIG)
        self.screen = pygame.display.set_mode(size)


    def reset(self):
        self.BOARD, self.GAME_OVER, self.PIECE, self.TO_GEN = self.game_reset()
        self.SCORE = 0


    def make_move(self, selection):
        self.MOVE += 1
        self.check_high(self.BOARD)
        self.GAME_OVER = self.filled(self.BOARD)
        self.BOARD = self.arrange(self.BOARD)
        if self.CONVERTABLE:
            if selection == -5:
                self.PIECE = -1
            self.CONVERTABLE = False
            self.TO_GEN = True
        if not self.CONVERTABLE and selection == -5:
            selection = 0
        if self.TO_GEN:
            self.BOARD = self.drop_piece(self.BOARD, selection, self.PIECE)
        else:
            self.BOARD, self.PIECE = self.take_piece(self.BOARD, selection, self.PIECE)
            self.TO_GEN = True
        self.BOARD = self.merge(self.BOARD)
        if not self.CONVERTABLE:
            self.PIECE, self.TO_GEN = self.generate_piece(self.BOARD, self.TO_GEN)


class BoardLinkedList:
    def __init__(self, board: np.array):
        self.nodes = []

        board = board[np.nonzero(board)]
        for i in range(board.size):
            node = Node(value=board[i])
            self.nodes.append(node)

        for i in range(len(self.nodes)):
            if len(self.nodes) <= 1:
                break

            node = self.nodes[i]
            node.prev = self.nodes[i-1]
            node.next = self.nodes[(i+1)%len(self.nodes)]


    def get_merging_index(self) -> int:
        for i in range(len(self.nodes)):
            node = self.nodes[i]
            if node.value == -1:
                if node.next.value > 0 and node.prev.value > 0 and node.next.value == node.prev.value:
                    return i
        return -1


    def merge_nodes(self) -> None:
        merging_index = self.get_merging_index()
        if merging_index == -1:
            return None

        new_nodes = []

        node = self.nodes[merging_index]
        prev_node = node.prev
        next_node = node.next
        while prev_node.value == next_node.value and prev_node.value > 0 and prev_node != next_node:
            increment = 1
            if node.value == -2:
                increment = 3

            new_val = max(node.value, prev_node.value) + increment
            node.value = new_val
            prev_node.prev.next = node
            node.prev = prev_node.prev
            next_node.next.prev = node
            node.next = next_node.next

            prev_node = node.prev
            next_node = node.next

        next_node = node.next
        new_nodes.append(node)
        while node != next_node:
            new_nodes.append(next_node)
            next_node = next_node.next

        self.nodes = new_nodes


    def construct_board(self) -> np.array:
        board = np.zeros(20)
        first_node = self.nodes[0]

        node = first_node
        board[0] = node.value
        node = node.next
        i = 1

        while node != first_node:
            board[i] = node.value
            node = node.next
            i += 1

        return board


class Node:
    def __init__(self, value=None, next=None, prev=None):
        self.value = value
        self.next = next
        self.prev = prev


if __name__ == "__main__":
    game = Game()
    game.play_game()

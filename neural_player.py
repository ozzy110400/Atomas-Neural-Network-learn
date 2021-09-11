import console_gameplay
import numpy as np
import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from statistics import mean, median
from collections import Counter
import time

LR = 1e-3
env = console_gameplay
env.game_reset()
goal_score = 5000
score_requirement = 400
goal_moves = 10000
initial_games = 10000

def some_random_games():
    for episode in range(3):
        env.reset()
        score = 0
        for t in range(goal_moves):
            move = np.random.choice(np.arange(0, 21))
            move = env.get_samples()[move]
            env.make_move(move)
            cur_score = env.get_score()
            done = env.get_game_over()
            board = env.get_board()
            score = cur_score
            if done:
                break

#some_random_games()

def initial_population():
    env.reset()
    training_data = []
    scores = []
    accepted_scores = []
    for _ in range(initial_games):
        if _%1000 == 0:
            print(f'Game: {_//1000}K / {initial_games}')
        game_memory = []
        moves = []
        score = 0
        for _ in range(goal_moves):
            piece = env.get_piece()
            board = env.get_board()
            move = np.random.choice(np.arange(0, board.size))
            #move = env.get_samples()[move]
            env.make_move(move)
            cur_score = env.get_score()
            done = env.get_game_over()
            score = cur_score
            moves.append(move)
            board_data = np.append(board, piece)
            game_memory.append([board_data, move])
            if done:
                break
        if score >= score_requirement:
            accepted_scores.append(score)
            for data in game_memory:
                output = np.zeros(21)
                if data[1] == -5:
                    output[20] = 1
                else:
                    output[data[1]] = 1
                training_data.append([data[0], output])
        env.reset()
        scores.append(score)
    training_data_save = np.array(training_data)
    np.save('saved.npy', training_data_save)

    print('Average accepted score: ', mean(accepted_scores))
    print('Median accepted score: ', median(accepted_scores))
    print(len(accepted_scores))

    return training_data

def NN_model(input_size):
    network = input_data(shape = [None, input_size, 1], name='input')

    network = fully_connected(network, 128, activation='relu')
    network = dropout(network, 0.8)

    network = fully_connected(network, 256, activation='relu')
    network = dropout(network, 0.8)

    network = fully_connected(network, 512, activation='relu')
    network = dropout(network, 0.8)

    network = fully_connected(network, 256, activation='relu')
    network = dropout(network, 0.8)

    network = fully_connected(network, 128, activation='relu')
    network = dropout(network, 0.8)

    network = fully_connected(network, 21, activation='softmax')
    network = regression(network, optimizer='adam', learning_rate=LR, loss='categorical_crossentropy',
                         name='targets')
    model = tflearn.DNN(network, tensorboard_dir='log')

    return model

def train_model(training_data, model=False):
    X = np.array([i[0] for i in training_data]).reshape(-1, len(training_data[0][0]), 1)
    y = [i[1] for i in training_data]

    if not model:
        model = NN_model(input_size= len(X[0]))

    model.fit({'input':X}, {'targets':y}, n_epoch=20, snapshot_step=500, show_metric=True, run_id='openaistuff')

    return model

def test_model(games):
    choices = []
    scores = []
    highest_score = 0
    this_training = []
    global training_data
    for each_game in range(games):
        score = 0
        game_memory = []
        env.reset()
        for _ in range(goal_moves):
            env.init()
            env.render()
            time.sleep(0.22)
            board = env.get_board()
            piece = env.get_piece()
            board_info = np.append(board, piece)
            move = np.argmax(model.predict(board_info.reshape(-1, len(board_info), 1)))
            choices.append(move)
            env.make_move(move)
            score = env.get_score()
            game_memory.append([board_info, move])
            done = env.get_game_over()
            if done:
                if score > highest_score:
                    highest_score = score
                break
        if score >= score_requirement:
            for data in game_memory:
                output = np.zeros(21)
                if data[1] == -5:
                    output[20] = 1
                else:
                    output[data[1]] = 1
                training_data = np.append(training_data, [[data[0], output]], axis=0)
        scores.append(score)

    print(f'Highest score: {highest_score}')
    print('Average score:', sum(scores)/len(scores))
    print(f'Choices: {Counter(choices)}')


#training_data = initial_population()
training_data = np.load('resaved.npy')
model = train_model(training_data)

test_model(10)
# for i in range(10):
#     print(f'Iteration: {i}')
#     (test_model(1000))
#
#     training_data_save = np.array(training_data)
#     np.save('resaved.npy', training_data_save)
#     model = train_model(training_data, model)

#initial_population()
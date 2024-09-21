import sys
sys.path.append("C:/Users/lenovo/AppData/Local/Packages/PythonSoftwareFoundation.Python.3.9_qbz5n2kfra8p0/LocalCache/local-packages/Python39/site-packages/pygame")
import pygame
import numpy as np
from Game import GameEnvironment
from model import QNetwork, get_network_input
import torch
import cv2

grid_size = 23
framerate = 10
block_size = 30

snake_name = 'Snake_3000'

model = QNetwork(input_dim=10, hidden_dim=20, output_dim=5)
model.load_state_dict(torch.load('./model/' + snake_name))

board = GameEnvironment(grid_size, nothing=0, dead=-1, apple=1)
window_width = grid_size * block_size * 2
window_height = grid_size * block_size

pygame.init()
win = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("snake")
font = pygame.font.SysFont('Helvetica', 14)
clock = pygame.time.Clock()

VIDEO = []


def draw_board(snake, apple):
    win.fill((0, 0, 0))
    for pos in snake.prev_pos:
        pygame.draw.rect(win, (0, 255, 0), (pos[0] * block_size, pos[1] * block_size, block_size, block_size))
    pygame.draw.rect(win, (255, 0, 0), (apple.pos[0] * block_size, apple.pos[1] * block_size, block_size, block_size))


runGame = True

prev_len_of_snake = 0

while runGame:
    clock.tick(framerate)

    state_0 = get_network_input(board.snake, board.apple)
    state = model(state_0)

    action = torch.argmax(state)

    reward, done, len_of_snake = board.update_board_state(action)
    draw_board(board.snake, board.apple)

    len_snake_text = font.render('          LEN OF SNAKE: ' + str(len_of_snake), False, (255, 255, 255))
    prev_len_snake_text = font.render('          LEN OF PREVIOUS SNAKE: ' + str(prev_len_of_snake), False,
                                      (255, 255, 255))

    x_pos = int(0.75 * window_width)
    win.blit(len_snake_text, (x_pos, 40))
    win.blit(prev_len_snake_text, (x_pos, 80))

    VIDEO.append(pygame.image.tostring(win, 'RGB', False))

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            runGame = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
        paused = True
        while paused:
            clock.tick(10)
            pygame.event.pump()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    paused = False

    pygame.display.update()

    if board.game_over:
        prev_len_of_snake = len_of_snake
        board.reset_game()

fourcc = cv2.VideoWriter_fourcc(*'MPV4')
output_name = 'output_' + snake_name + '.mp4'
video_mp4 = cv2.VideoWriter(output_name, fourcc, 20.0, (window_width, window_height))

for image in VIDEO:
    image = np.frombuffer(image, np.uint8).reshape(window_height, window_width, 3)
    image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)
    video_mp4.write(image)

cv2.destroyAllWindows()
video_mp4.release()

pygame.quit()
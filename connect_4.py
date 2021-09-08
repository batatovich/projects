import numpy as np
import pygame
import sys
from scipy import signal

c1 = (80,0,250)

def create_board():
    return np.zeros((6,7))

def check_win(state):
    s1 = signal.convolve2d(state,v_k)
    s2 = signal.convolve2d(state,h_k)
    s3 = signal.convolve2d(state,d1_k)
    s4 = signal.convolve2d(state,d2_k)
    if 4 in s1 or 4 in s2 or 4 in s3 or 4 in s4:
        return True
    else:
        return False
def draw_board():
    for i in range(0,7):
        for j in range(0,6):
            pygame.draw.rect(screen,c1,(i*square_size,(j+1)*square_size,square_size,square_size))
            pygame.draw.circle(screen,'black',(int((i+1/2)*square_size),int((j+3/2)*square_size)),(square_size-2)/2)
v_k = np.array([[1,1,1,1]]) #Vertical kernel
h_k = np.transpose(v_k) #Horizontal kernel
d1_k = np.eye(4, dtype=np.uint8)
d2_k = np.fliplr(d1_k)


p1_state = np.zeros((6,7),dtype=np.uint8)
p2_state = np.zeros((6,7),dtype=np.uint8)

board = create_board()
game_over = False
turn = 1
valid_inputs = ('0','1','2','3','4','5','6')

pygame.init()
square_size = 50
screen = pygame.display.set_mode((7*square_size,7*square_size)) #Add extra row for displaying the starting line
draw_board()
pygame.display.update()
print("Game begins...")
while not game_over:
    for event in pygame.event.get(): #Gets events (like mouse clicks, etc...)
        if event.type == pygame.QUIT: #If players click on the x button
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            posx = event.pos[0]
            colour = 'yellow'
            if turn == 1:
                colour = 'red'
            else:
                colour = 'yellow'
            pygame.draw.circle(screen, colour, (posx,int(square_size/2)),(square_size-2)/2)
    
        if event.type == pygame.MOUSEBUTTONDOWN: #If players click in the screen    
            x_pos = event.pos[0]
            col = int(x_pos/square_size)
            if turn == 1: #Player 1 turn
                if board[0][col] == 0:
                    turn = 0
                    for i in range(5,-1,-1):
                        if board[i][col] == 0:
                            board[i][col] = 1
                            p1_state[i][col] = 1
                            pygame.draw.circle(screen,'red',(int((col+1/2)*square_size),int((i+3/2)*square_size)),(square_size-2)/2)
                            if check_win(p1_state) == True:
                                game_over = True
                                print("Player 1 wins the game!")
                            break
            else:
                if board[0][col] == 0:
                    turn = 1
                    for i in range(5,0,-1):
                        if board[i][col] == 0:
                            board[i][col] = 2
                            p2_state[i][col] = 1
                            pygame.draw.circle(screen,'yellow',(int((col+1/2)*square_size),int((i+3/2)*square_size)),(square_size-2)/2)
                            if check_win(p2_state) == True:
                                game_over = True
                                print("Player 2 wins the game!")
                            break
        pygame.display.update()
    
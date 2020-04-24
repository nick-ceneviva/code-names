from random import randint, shuffle
import sys
import numpy as np
import pygame
import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

CARD_DEFAULT = (235,213,179)
BLACK = (0,0,0)
TEAM1_COLOR = (61,96,152)
TEAM2_COLOR = (240,75,76)
TURN_COLOR = (92, 219, 149)
BYSTANDER_COLOR = (162,162,162)

ROW_COUNT = 5
COLUMN_COUNT = 5

pygame.init()
pygame.display.set_caption('Code Names')

font_size = 18

CARD_FONT = pygame.font.SysFont("arial", font_size)
CARD_FONT.set_bold(True)

def createBoard():

    f = open('data/words.txt', 'r')
    words = f.readlines()
    f.close()

    words = [word.strip().upper() for word in words]
    words = list(set(words))
    shuffle(words)

    return np.reshape(words[:25],(5,5))
        
def createKey():
    cards = ['1','1','1','1','1','1','1','1','1',
                '2','2','2','2','2','2','2','2',
                'X','-','-','-','-','-','-','-']

    shuffle(cards)

    fig, ax = plt.subplots()
    for x in range(0,5):
        for y in range(0,5):
            if cards[(y*5)+x] == '1':
                color = 'b'
            elif cards[(y*5)+x] == '2':
                color = 'r'
            elif cards[(y*5)+x] == 'X':
                color = 'k'
            else:
                color = 'w'
            rect = mpatches.Rectangle((0+x/5,.8-y/5),.2,.2, fill=True, edgecolor='k', facecolor=color)
            ax.add_patch(rect)

    plt.axis('off')
    plt.savefig("board.png", bbox_inches='tight')

    return np.reshape(cards[:25],(5,5))

#def sendKey():
    #https://realpython.com/python-send-email/#option-1-setting-up-a-gmail-account-for-development

def checkScore(score,board):
    game_over = False
    score['1'] = 9 - (board == '1').sum()
    score['2'] = 8 - (board == '2').sum()

    if any(x == 0 for x in score.values()):
        game_over = True

    return score, game_over

def checkGuess(selection, board, team, key):

    board[selection[0],selection[1]] = key[selection[0],selection[1]] 
    
    if key[selection[0],selection[1]] == 'X':
        result = 'Game Over'
        #print('GAME OVER!')
    elif key[selection[0],selection[1]] == '-':
        result = 'bystander'
        #print('OOPS! End of Turn')
    elif key[selection[0],selection[1]] == team:
        result = 'match'
        #print('CORRECT!')
    elif key[selection[0],selection[1]] != team:
        result = 'oppWord'
        #print('WOMP! WOMP! The other team thanks you')

    return result, board

def draw_scoreboard(team1_score, team2_score,turn):
    team1_label = CARD_FONT.render('TEAM 1', 1, TEAM1_COLOR)
    team2_label = CARD_FONT.render('TEAM 2', 1, TEAM2_COLOR)
    team1_score_label = CARD_FONT.render(team1_score, 1, TEAM1_COLOR)
    team2_score_label = CARD_FONT.render(team2_score, 1, TEAM2_COLOR)

    if turn == '1':
        pygame.draw.rect(screen, TURN_COLOR, (width/3-team1_label.get_width()/2-5, CARD_HEIGHT/4-5, team1_label.get_width()+10, team1_label.get_height()+font_size+12),3)
    else:
        pygame.draw.rect(screen, TURN_COLOR, (2*width/3-team2_label.get_width()/2-5, CARD_HEIGHT/4-5, team2_label.get_width()+10, team2_label.get_height()+font_size+12),3)
        
    screen.blit(team1_label, (width/3-team1_label.get_width()/2,CARD_HEIGHT/4))
    screen.blit(team2_label, (2*width/3-team2_label.get_width()/2,CARD_HEIGHT/4))
    screen.blit(team1_score_label, (width/3-team1_score_label.get_width()/2,CARD_HEIGHT/4+font_size+2))
    screen.blit(team2_score_label, (2*width/3-team2_score_label.get_width()/2,CARD_HEIGHT/4+font_size+2))

    pygame.display.update()


def draw_board(board):
    screen.fill((231,231,231))

    draw_scoreboard('9', '8', '1')

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            
            pygame.draw.rect(screen, CARD_DEFAULT, (GAP+c*(CARD_WIDTH+GAP), r*(CARD_HEIGHT+GAP)+CARD_HEIGHT, CARD_WIDTH, CARD_HEIGHT))
            label = CARD_FONT.render(board[r,c], 1, BLACK)
            screen.blit(label, (GAP+c*(CARD_WIDTH+GAP)+CARD_WIDTH/2-label.get_width()/2, r*(CARD_HEIGHT+GAP)+(1.5 * CARD_HEIGHT)-label.get_height()/2))

    pygame.display.update()

board = createBoard()
key = createKey()
game_over = False
endTurn = False
team = '1'
score = {}

print(board)
print(key)

CARD_HEIGHT = 100
CARD_WIDTH = 150
GAP = 10

width = COLUMN_COUNT * (CARD_WIDTH + GAP) + GAP
height = (ROW_COUNT+1) * (CARD_HEIGHT + GAP)
size = (width, height)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

correct_color = {'1':TEAM1_COLOR, '2':TEAM2_COLOR}
incorrect_color = {'1':TEAM2_COLOR, '2':TEAM1_COLOR}

while not game_over:
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            col = int(math.floor(event.pos[0]/(CARD_WIDTH + GAP)))
            row = int(math.floor(event.pos[1]/(CARD_HEIGHT + GAP))) - 1

            result, board = checkGuess([row,col], board, team, key)
            if result == 'match':
                pygame.draw.rect(screen, correct_color[team], (GAP+col*(CARD_WIDTH+GAP), row*(CARD_HEIGHT+GAP)+CARD_HEIGHT, CARD_WIDTH, CARD_HEIGHT))
            elif result == 'oppWord':
                pygame.draw.rect(screen, incorrect_color[team], (GAP+col*(CARD_WIDTH+GAP), row*(CARD_HEIGHT+GAP)+CARD_HEIGHT, CARD_WIDTH, CARD_HEIGHT))
                endTurn = True
            elif result == 'bystander':
                pygame.draw.rect(screen, BYSTANDER_COLOR, (GAP+col*(CARD_WIDTH+GAP), row*(CARD_HEIGHT+GAP)+CARD_HEIGHT, CARD_WIDTH, CARD_HEIGHT))
                endTurn = True
            elif result == 'Game Over':
                pygame.draw.rect(screen, BLACK, (GAP+col*(CARD_WIDTH+GAP), row*(CARD_HEIGHT+GAP)+CARD_HEIGHT, CARD_WIDTH, CARD_HEIGHT))
                endTurn = True  
                game_over = True 

            pygame.display.update()

            if not game_over:
                score, game_over = checkScore(score,board)

                if endTurn:
                    if team == '1':
                        team = '2'
                    else: 
                        team = '1'

                endTurn = False

                pygame.draw.rect(screen, (231,231,231), (0, CARD_HEIGHT/4-10, width, font_size*4))
                draw_scoreboard(str(score['1']), str(score['2']),team)

                pygame.display.update()

            if game_over:
                pygame.time.wait(5000)
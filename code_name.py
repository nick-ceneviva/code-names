from random import randint, shuffle
import sys
import numpy as np
import pygame
import math
import configparser
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage


# Sender email variables
CONFIG_FILE = 'config.txt'
CONFIG_PARAM = 'configuration'
CONFIG_EMAIL = 'email'
CONFIG_PASSWORD = 'password'

# Email variables
MESSAGE_SUBJECT = 'Subject'
MESSAGE_FROM = 'From'
MESSAGE_TO = 'To'
MESSAGE_SUBJECT_TEXT = 'Code Names Board'
EMAIL_TEXT = """\
Hi,
How are you?
Real Python has many great tutorials:
www.realpython.com"""
EMAIL_HTML = """\
<html>
<body>
    <img src="cid:image1" alt="Code names Key">
</body>
</html>
"""
MESSAGE_HEADER = 'Content-ID'
MESSAGE_HEADER_TEXT = '<image1>'
EMAIL_URL = 'smtp.gmail.com'
EMAIL_PORT = 465
BOARD_IMG_FILE = 'board.png'

# Game formatting variables
GAME_NAME = 'Code Names'
CARD_DEFAULT = (235,213,179)
BLACK = (0,0,0)
TEAM_1_COLOR = (61,96,152)
TEAM_2_COLOR = (240,75,76)
TURN_COLOR = (92, 219, 149)
NEUTRAL_COLOR = (162,162,162)
ROW_COUNT = 5
COLUMN_COUNT = 5
CARD_HEIGHT = 100
CARD_WIDTH = 150
GAP = 10
FONT_SIZE = 18
SCREEN_SIZE = (COLUMN_COUNT * (CARD_WIDTH + GAP) + GAP, (ROW_COUNT+1) * (CARD_HEIGHT + GAP))

# Game logic variables
BOARD_WORDS_FILE = 'data/words.txt'
TEAM_1 = '1'
TEAM_2 = '2'
MATCH_TEXT = 'match'
OPP_WORD_TEXT = 'opp_word'
NEUTRAL_TEXT = 'neutral'
GAME_OVER_TEXT = 'game_over'
CORRECT_COLOR = { TEAM_1: TEAM_1_COLOR, TEAM_2: TEAM_2_COLOR }
INCORRECT_COLOR = { TEAM_1: TEAM_2_COLOR, TEAM_2: TEAM_1_COLOR }
END_GAME_MILLIS = 5000


def handle_file(file_name, handle, lines=False):
    """ Try to open and return file. """

    with open(file_name, handle) as f:
        try:
            if lines:
                return f.readlines()
            return f.read()
        except:
            print('Error loading file.')
            sys.exit()

def create_board():
    """ Select words to create game board. """

    words = [word.strip().upper() for word in handle_file(BOARD_WORDS_FILE, 'r', True)]
    shuffle(words)
    return np.reshape(words[:25],(5,5))
        
def create_key():
    """ Create the key and output file in png format. """

    cards = ['1','1','1','1','1','1','1','1','1',
                '2','2','2','2','2','2','2','2',
                'X','-','-','-','-','-','-','-']

    shuffle(cards)

    fig, ax = plt.subplots()
    for i, card in enumerate(cards):
        color = {'1':'b', '2':'r', 'X':'k', '-': 'w'}.get(card)
        coords = (int(i % 5), int(i / 5))
        rect = mpatches.Rectangle((0+coords[0]/5,.8-coords[1]/5),.2,.2, fill=True, edgecolor='k', facecolor=color)
        ax.add_patch(rect)
    
    plt.axis('off')
    plt.savefig(BOARD_IMG_FILE, bbox_inches='tight')
    
    return np.reshape(cards[:25],(5,5))

def email_key(receiver_email):
    """ Email key to reciever. """

    # Set up sender email.
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    sender_email= config.get(CONFIG_PARAM, CONFIG_EMAIL)
    password = config.get(CONFIG_PARAM, CONFIG_PASSWORD)

    # Set up message.
    message = MIMEMultipart("alternative")
    message[MESSAGE_SUBJECT] = MESSAGE_SUBJECT_TEXT
    message[MESSAGE_FROM] = sender_email
    message[MESSAGE_TO] = receiver_email

    # Turn into plain/html MIMEText objects
    part1 = MIMEText(EMAIL_TEXT, "plain")
    part2 = MIMEText(EMAIL_HTML, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # This example assumes the image is in the current directory
    msgImage = MIMEImage(handle_file(BOARD_IMG_FILE, 'rb'))

    # Define the image's ID as referenced above
    msgImage.add_header(MESSAGE_HEADER, MESSAGE_HEADER_TEXT)
    message.attach(msgImage)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(EMAIL_URL, EMAIL_PORT, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

def check_score(board):
    """ Check score for game based on move. """

    score = {
        TEAM_1: 9 - (board == TEAM_1).sum(),
        TEAM_2: 8 - (board == TEAM_2).sum()
    }

    return score, any(x == 0 for x in score.values())

def check_guess(x, y, board, team, key):
    """ Checks if user guess is correct. """

    selection = key[x, y]
    board[x, y] = selection
    result_map = {
        'X': GAME_OVER_TEXT,
        '-': NEUTRAL_TEXT,
        team: MATCH_TEXT
    }

    return result_map.get(selection, OPP_WORD_TEXT), board


def draw_scoreboard(card_font, team_1_score, team_2_score, turn):
    """ Updates scoreboard on screen. """

    team1_label = card_font.render('TEAM 1', 1, TEAM_1_COLOR)
    team2_label = card_font.render('TEAM 2', 1, TEAM_2_COLOR)
    team1_score_label = card_font.render(str(team_1_score), 1, TEAM_1_COLOR)
    team2_score_label = card_font.render(str(team_2_score), 1, TEAM_2_COLOR)
    width = SCREEN_SIZE[0]

    if turn == '1':
        pygame.draw.rect(screen, TURN_COLOR, (width/3-team1_label.get_width()/2-5, CARD_HEIGHT/4-5, team1_label.get_width()+10, team1_label.get_height()+FONT_SIZE+12),3)
    else:
        pygame.draw.rect(screen, TURN_COLOR, (2*width/3-team2_label.get_width()/2-5, CARD_HEIGHT/4-5, team2_label.get_width()+10, team2_label.get_height()+FONT_SIZE+12),3)
    
    screen.blit(team1_label, (width/3-team1_label.get_width()/2,CARD_HEIGHT/4))
    screen.blit(team2_label, (2*width/3-team2_label.get_width()/2,CARD_HEIGHT/4))
    screen.blit(team1_score_label, (width/3-team1_score_label.get_width()/2,CARD_HEIGHT/4+FONT_SIZE+2))
    screen.blit(team2_score_label, (2*width/3-team2_score_label.get_width()/2,CARD_HEIGHT/4+FONT_SIZE+2))

    pygame.display.update()


def draw_board(screen, board, card_font):
    """ Draws board."""

    screen.fill((231,231,231))

    draw_scoreboard(card_font, '9', '8', '1')

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, CARD_DEFAULT, (GAP + c * (CARD_WIDTH + GAP), r * (CARD_HEIGHT + GAP) + CARD_HEIGHT, CARD_WIDTH, CARD_HEIGHT))
            label = card_font.render(board[r,c], 1, BLACK)
            screen.blit(label, (GAP + c * (CARD_WIDTH + GAP) + CARD_WIDTH / 2 - label.get_width() / 2, r * (CARD_HEIGHT + GAP) + (1.5 * CARD_HEIGHT) - label.get_height() / 2))

    pygame.display.update()


# Game variables.
board = create_board()
key = create_key()
game_over = False
end_turn = False
team = '1'

# Email keys.
email = input('Enter Team 1 CodeMaster:')
email_key(email)
email = input('Enter Team 2 CodeMaster:')
email_key(email)

# Start game.
pygame.init()
pygame.display.set_caption(GAME_NAME)
card_font = pygame.font.SysFont('arial', FONT_SIZE)
card_font.set_bold(True)
screen = pygame.display.set_mode(SCREEN_SIZE)
draw_board(screen, board, card_font)
pygame.display.update()


while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Get coordinates based on where user clicked.
            col = int(math.floor(event.pos[0]/(CARD_WIDTH + GAP)))
            row = int(math.floor(event.pos[1]/(CARD_HEIGHT + GAP))) - 1

            # Figure out if the user guess was correct.
            result, board = check_guess(row, col, board, team, key)

            # Options for drawing results of guess on board.
            draw_guess_options = {
                MATCH_TEXT: [CORRECT_COLOR[team], GAP + col * (CARD_WIDTH + GAP), row * (CARD_HEIGHT + GAP) + CARD_HEIGHT],
                OPP_WORD_TEXT: [INCORRECT_COLOR[team], GAP + col * (CARD_WIDTH + GAP), row * (CARD_HEIGHT + GAP) + CARD_HEIGHT],
                NEUTRAL_TEXT: [NEUTRAL_COLOR, GAP + col * (CARD_WIDTH + GAP), row * (CARD_HEIGHT + GAP) + CARD_HEIGHT],
                GAME_OVER_TEXT: [BLACK, GAP + col * (CARD_WIDTH + GAP), row * (CARD_HEIGHT + GAP) + CARD_HEIGHT]
            }

            # Draw the actual guess on the board.
            draw_guess_option = draw_guess_options.get(result)
            pygame.draw.rect(screen, draw_guess_option[0], (draw_guess_option[1], draw_guess_option[2], CARD_WIDTH, CARD_HEIGHT))
            pygame.display.update()

            # Figure out if turn is over and game is over.
            end_turn = result in (OPP_WORD_TEXT, NEUTRAL_TEXT, GAME_OVER_TEXT)
            game_over = result == GAME_OVER_TEXT
   
            if not game_over:
                score, game_over = check_score(board)
                # Switch teams, if game over.
                team = (TEAM_2 if team == TEAM_1 else TEAM_1) if end_turn else team

                # Update score board.
                pygame.draw.rect(screen, (231, 231, 231), (0, CARD_HEIGHT/4-10, SCREEN_SIZE[0], FONT_SIZE*4))
                draw_scoreboard(card_font, score[TEAM_1], score[TEAM_2], team)
                pygame.display.update()

            if game_over:
                pygame.time.wait(END_GAME_MILLIS)
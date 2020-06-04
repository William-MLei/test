## @file MenuSettings.py
# @title All menus and screens for the initiation of the game.
# @author Arshan Khan
# @date 28 March 2020
import pygame
import sys
from pygame.locals import *
from pong.PongGame import *

pygame.init()
FPS = 60
scrSize = (width,height) = (1280,800)
middleX = int(width/2)
middleY = int(height/2)
screen = pygame.display.set_mode(scrSize)
pygame.display.set_caption('Main Menu')

clock = pygame.time.Clock()

#Creating a ball for introduction animation.
ball = pygame.Rect(582,460, 104, 104)
ball_speed_x = 8
ball_speed_y = 5

#Declaring various color values.
BG = (5, 35, 60)
BLUE = (66, 133, 244)
HOVERBLUE = (36, 103, 214)
GREEN10 = (61, 220, 132)
HOVERGREEN10 = (31, 190, 102)
GREEN = (0, 200, 0)
HOVERGREEN = (0, 170, 0)
ORANGE = (240, 130, 0)
HOVERORANGE = (210, 100, 0)
RED = (200, 30, 0)
HOVERRED = (170, 0, 0)
AMBER = (255, 191, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

maxScore = -1
diff = 0

## @brief Keeps the introductory-animation-ball inside the screen
def ball_animation():
    global ball_speed_x, ball_speed_y
    # Moves the ball by one multiple of the ball speed
    ball.x += ball_speed_x
    ball.y += ball_speed_y
    # Keeps the ball in the boundaries
    if ball.top <= 0 or ball.bottom >= height:
        ball_speed_y *= -1
    if ball.left <= 0 or ball.right >= width:
        ball_speed_x *= -1

## @brief Alters the difficulty of the AI player.
# @details This function is initiated by the user by selecting a difficulty level in the main menu.
def changeDifficulty(x):
    global displayDifficulty
    if (x == 4): level = 'EASY'
    elif (x == 10): level = 'HARD'    
    elif (x == 25): level = 'INSANE'
    else: level = ''
    displayDifficulty = ('Difficulty: ' + str(level))
    return x

## @brief Alters the maximum score the game will run, at which point the game will end.
# @details This function is initiated by the user by selecting a maximum score in the main menu.
def changeMaxScore(x):
    global displayMaxScore
    displayMaxScore = ('Play up to: ' + str(x))
    return x

## @brief This function displays the transition from the main menu to the main game.
# @details This function is initiated by the user by clicking on the 'BEGIN' button.
def startGameAnimation():
    screen.fill(BG)
    fadeR, fadeG, fadeB = 5, 35, 60
    # Hard coded length of the transition screen.
    timer = 20
    while timer > 0:
        screen.fill((fadeR, fadeG, fadeB))
        fadeR = fadeR - int(5/20)
        fadeG = fadeG - int(35/20)
        fadeB = fadeB - int(60/20)
        displayText('TIP: If you feel like you are stuck, use the "R" key to RESET the BALL.', 20, middleX, height - 120, RED)
        displayText('Use the "UP"/"DOWN" arrow keys to move your PADDLE.', 20, middleX, height - 90, WHITE)
        displayText('Get the BALL  past your opponent to score.', 20, middleX, height - 60, WHITE)
        displayText('Press "ESC" to PAUSE the game.', 20, middleX, height-30, WHITE)
        timer -= 1
        pygame.display.update()
        clock.tick(8)
    displayText('Welcome to PONG', 100, middleX, middleY, WHITE)
    pygame.display.update()
    clock.tick(0.7)


click = False
displayMaxScore = 'Select the maximum score'
displayDifficulty = 'Select difficulty'
coverStart = pygame.Rect(0, 0, 1280, 800)

## @brief This class contains all visuals for the screen the user first experiences. This includes all buttons and text.
# @details This function is the first function run in the program, and is run automatically after selecting a game from the Launcher.
def main_menu():
    global diff, maxScore
    while True:
        # No condition on the while statement to keep it running at all times (for new games and such).
        screen.fill(BG)
        mx, my = pygame.mouse.get_pos()
        displayText('Use the UP / DOWN arrow keys to move your PADDLE.', 20, middleX, height - 90, WHITE)
        displayText('Get the BALL  past your opponent to score.', 20, middleX, height - 60, WHITE)
        displayText('Press "ESC" to return to the launcher.', 20, middleX, height-30, WHITE)

        #BEGIN selection of difficulty ----------------------------------------
        easyButton = pygame.Rect(middleX - 125, middleY - 75, 50, 50)
        ecolor = GREEN
        medButton = pygame.Rect(middleX - 25, middleY - 75, 50, 50)
        mcolor = ORANGE
        hardButton = pygame.Rect(middleX + 75, middleY - 75, 50, 50)
        hcolor = RED
        if easyButton.collidepoint((mx, my)):
            ecolor = HOVERGREEN
            if click:
                diff = changeDifficulty(4)
        if medButton.collidepoint((mx, my)):
            mcolor = HOVERORANGE
            if click:
                diff = changeDifficulty(10)
        if hardButton.collidepoint((mx, my)):
            hcolor = HOVERRED
            if click:
                diff = changeDifficulty(25)
        pygame.draw.ellipse(screen, ecolor, easyButton)
        pygame.draw.ellipse(screen, mcolor, medButton)
        pygame.draw.ellipse(screen, hcolor, hardButton)
        displayText('!', 20, middleX - 100, middleY - 50, WHITE)
        displayText('!!', 20, middleX, middleY - 50, WHITE)
        displayText('!!!', 20, middleX + 100, middleY - 50, WHITE)
        displayText(displayDifficulty, 25, middleX, 300, WHITE)
        #END selection of difficulty ------------------------------------------

        #BEGIN start button ---------------------------------------------------
        startButton = pygame.Rect(middleX - 125, middleY + 160, 250, 80)
        startColor = BG
        beginColor = BG
        if maxScore > 0 and diff > 0:
            startColor = GREEN10
            beginColor = WHITE
        if startButton.collidepoint((mx, my)):
            if maxScore > 0 and diff > 0:
                startColor = HOVERGREEN10
            if click:
                startGameAnimation()
                mainGame(diff, maxScore)
        pygame.draw.rect(screen, startColor, startButton)
        displayText('BEGIN', 50, middleX, middleY + 200, beginColor)
        #END start button -----------------------------------------------------
        
        #BEGIN selection of final score ---------------------------------------
        fiveButton = pygame.Rect(middleX - 125, middleY + 50, 50, 50)
        color5 = BLUE
        tenButton = pygame.Rect(middleX - 25, middleY + 50, 50, 50)
        color10 = BLUE
        fifteenButton = pygame.Rect(middleX + 75, middleY + 50, 50, 50)
        color15 = BLUE
        if fiveButton.collidepoint((mx, my)):
            color5 = HOVERBLUE
            if click:
                maxScore = changeMaxScore(5)
        if tenButton.collidepoint((mx, my)):
            color10 = HOVERBLUE
            if click:
                maxScore = changeMaxScore(10)
        if fifteenButton.collidepoint((mx, my)):
            color15 = HOVERBLUE
            if click:
                maxScore = changeMaxScore(15)
        pygame.draw.ellipse(screen, color5, fiveButton)
        pygame.draw.ellipse(screen, color10, tenButton)
        pygame.draw.ellipse(screen, color15, fifteenButton)
        displayText('5', 20, middleX - 100, middleY + 75, WHITE)
        displayText('10', 20, middleX, middleY + 75, WHITE)
        displayText('15', 20, middleX + 100, middleY + 75, WHITE)
        displayText(displayMaxScore, 25, middleX, middleY + 25, WHITE)
        #END selection of final score -----------------------------------------
        pygame.draw.rect(screen, BG, coverStart)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    import Launcher
                    Launcher.Launcher.displayLauncher()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        
        if (ball.x > 518):
            ball_animation()
        if (ball.x <= 518):
            coverStart.x = 1280

        pygame.draw.ellipse(screen, AMBER, ball)
        displayText("P   NG", 150, middleX, 200, AMBER)
 
        pygame.display.update()
        clock.tick(70)
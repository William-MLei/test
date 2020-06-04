## @title File for testing purposes only.
# @author Arshan Khan
# @date 28 March 2020
import sys
import random
import pygame
from pygame.locals import *
from pongTestFiles.Ball import *
from pongTestFiles.Paddle import *


pygame.init()
FPS = 60
scrSize = (width, height) = (1280, 800)
middleX = int(width/2)
middleY = int(height/2)
screen = pygame.display.set_mode(scrSize)
pygame.display.set_caption('Pong')

clock = pygame.time.Clock()

pygame.mixer.init()
hitPaddle = pygame.mixer.Sound('pongTestFiles/sounds/bruh.wav')
aiScored = pygame.mixer.Sound('pongTestFiles/sounds/oof.wav')
playerScored = pygame.mixer.Sound('pongTestFiles/sounds/hyesz.wav')
win = pygame.mixer.Sound('pongTestFiles/sounds/victory.wav')
lose = pygame.mixer.Sound('pongTestFiles/sounds/defeat.wav')

BG = (5, 35, 60)
WHITE = (255, 255, 255)
LIGHTGREY = (200, 200, 200)
AMBER = (255, 191, 0)
BLUE = (66, 133, 244)
HOVERBLUE = (36, 103, 214)
GREEN10 = (61, 220, 132)
GREEN = (0, 200, 0)
ORANGE = (240, 130, 0)
RED = (200, 30, 0)
ENEMYCOLOR = GREEN

click = False
gameOver = True

def displayText(text, fontsize, x, y, color):
    font = pygame.font.SysFont('rockwell', fontsize, True)
    text = font.render(text, 1, color)
    textpos = text.get_rect(centerx=x, centery=y)
    screen.blit(text, textpos)

def aiMove(ai, ball, diff):
    if diff == 25:
        aiSpeed = 9
    elif diff == 10:
        aiSpeed = 7
    else:
        aiSpeed = 6
    if ball.movement[0] > 0:
        if ball.rect.bottom > ai.rect.bottom + 9 - aiSpeed:
            ai.movement[1] = aiSpeed
        elif ball.rect.top < ai.rect.top - 9 + aiSpeed:
            ai.movement[1] = -aiSpeed
        else:
            ai.movement[1] = 0
    else:
        ai.movement[1] = 0

def calculateScore(paddleScore, aiScore, maxScore):
    finalScore = int(((paddleScore * maxScore) - aiScore) * 17)
    if finalScore == 0:
        finalScore = maxScore
    if finalScore < 0:
        finalScore == int(maxScore/3)
    return finalScore

def mainGame(difficulty, maxScore):
    global gameOver
    if maxScore <= 0:
        maxScore = 5
    if difficulty <= 0:
        difficulty = 4
    if difficulty == 10:
        ENEMYCOLOR = ORANGE
    elif difficulty == 25:
        ENEMYCOLOR = RED
    else:
        ENEMYCOLOR = GREEN

    gameOver = False
    paddle = Paddle(int(width/18), middleY, int(width/90), 100, LIGHTGREY) 
    ai = Paddle(int(width - width/18), middleY, int(width/90), 100, ENEMYCOLOR) 
    ball = Ball(middleX, middleY, 25, AMBER, [6, 6])

    while not gameOver:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit() 

            if event.type == KEYDOWN:
                if event.key == K_UP: 
                    paddle.movement[1] = -8 
                elif event.key == K_DOWN:
                    paddle.movement[1] = 8
                if event.key == K_ESCAPE or event.key == K_SPACE:
                    pauseMenu(paddle.points, ai.points)
                if event.key == K_r:
                    ball.resetBall()
            if event.type == KEYUP: 
                paddle.movement[1] = 0 

        aiMove(ai, ball, difficulty)

        screen.fill(BG)
        pygame.draw.aaline(screen, WHITE, (middleX, 0), (middleX, height))
        displayText('PAUSE the game using the "ESC" key.', 20, 1075, 25, WHITE)

        paddle.drawPaddle()
        ai.drawPaddle()
        ball.draw()

        displayText(str(paddle.points), 40, middleX - 30, 30, WHITE)
        displayText(str(ai.points), 40, middleX + 30, 30, WHITE)
        if (ai.points == maxScore):
            clock.tick(1)
            endGameMenu(0, paddle.points, ai.points, maxScore)
            gameOver = True
        if (paddle.points == maxScore):
            clock.tick(1)
            endGameMenu(1, paddle.points, ai.points, maxScore)
            gameOver = True

        if pygame.sprite.collide_mask(paddle, ball):
            hitPaddle.play()
            ball.movement[0] = -1*ball.movement[0]
            ball.movement[1] = ball.movement[1] - int(0.1*random.randrange(5, 10)*paddle.movement[1])
            if ball.movement[1] > ball.maxspeed:
                ball.movement[1] = ball.maxspeed
            if ball.movement[1] < -1*ball.maxspeed:
                ball.movement[1] = -1*ball.maxspeed

        if pygame.sprite.collide_mask(ai, ball):
            hitPaddle.play()
            ball.movement[0] = -1*ball.movement[0]
            ball.movement[1] = ball.movement[1] - int(0.1*random.randrange(5, 10)*ai.movement[1])
            if ball.movement[1] > ball.maxspeed:
                ball.movement[1] = ball.maxspeed
            if ball.movement[1] < -1*ball.maxspeed:
                ball.movement[1] = -1*ball.maxspeed

        if ball.score == 1:
            aiScored.play()
            ai.points += 1
            ball.score = 0
            clock.tick(1)
        elif ball.score == -1:
            playerScored.play()
            paddle.points += 1
            ball.score = 0
            clock.tick(1.2)

        paddle.movePaddle()
        ball.scoreGoal()
        ai.movePaddle()

        pygame.display.update()

        clock.tick(FPS)

def pauseMenu(paddleScore, aiScore):
    global click, gameOver
    pause = True
    while pause:
        screen.fill(BG)
 
        mx, my = pygame.mouse.get_pos()
       
        displayText('PAUSED', 80, middleX, 300, WHITE)
        displayText((str(paddleScore) + ' - ' + str(aiScore)), 80, middleX, 200, WHITE)
        displayText('TIP: If you feel like you are stuck, use the "R" key to RESET the BALL.', 20, middleX, height - 30, RED)

        #BEGIN selection of pause options -------------------------------------
        resumeButton = pygame.Rect(middleX - 100, middleY - 25, 200, 50)
        resumeColor = BLUE
        mainMenuButton = pygame.Rect(middleX - 100, middleY + 50, 200, 50)
        mainMenuColor = BLUE
        launcherButton = pygame.Rect(middleX - 100, middleY + 125, 200, 50)
        launcherColor = BLUE
        if resumeButton.collidepoint((mx, my)):
            resumeColor = HOVERBLUE
            if click:
                pause = False
        if mainMenuButton.collidepoint((mx, my)):
            mainMenuColor = HOVERBLUE
            if click:
                screen.fill(BG)
                gameOver = True
                pause = False
        if launcherButton.collidepoint((mx, my)):
            launcherColor = HOVERBLUE
            if click:
                import Launcher
                Launcher.Launcher.displayLauncher()
        pygame.draw.rect(screen, resumeColor, resumeButton)
        pygame.draw.rect(screen, mainMenuColor, mainMenuButton)
        pygame.draw.rect(screen, launcherColor, launcherButton)
        displayText('Resume', 25, middleX, middleY, WHITE)
        displayText('New Game', 25, middleX, middleY + 75, WHITE)
        displayText('Quit Game', 25, middleX, middleY + 150, WHITE)
        #END selection of pause options ---------------------------------------

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pause = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
       
        pygame.display.update()
        clock.tick(60)

def endGameMenu(victor, paddleScore, aiScore, maxScore):
    screen.fill(BG)
    global click
    endGame = True
    scoreNotSaved = True

    finalScore = calculateScore(paddleScore, aiScore, maxScore)
    
    if finalScore in [425, 1700, 3825]:
        displayText('+*! PERFECT SCORE !*+', 30, middleX, 150, AMBER)
    if finalScore < 0:
        displayText('THAT WAS TERRIBLE!', 30, middleX, 150, ORANGE)
    
    if (victor == 0):
        displayText('DEFEAT', 80, middleX, 200, RED)
        lose.play()
    else:
        displayText('YOU WIN!', 80, middleX, 200, GREEN10)
        win.play()
    displayText(('FINAL SCORE: ' + str(finalScore)), 40, middleX, 275, WHITE)
    displayText((str(paddleScore) + ' - ' + str(aiScore)), 110, middleX, 360, WHITE)

    while endGame:
        mx, my = pygame.mouse.get_pos()

        #BEGIN selection of pause options -------------------------------------
        mainMenuButton = pygame.Rect(middleX - 100, middleY + 100, 200, 50)
        mainMenuColor = BLUE
        launcherButton = pygame.Rect(middleX - 100, middleY + 175, 200, 50)
        launcherColor = BLUE
        if mainMenuButton.collidepoint((mx, my)):
            mainMenuColor = HOVERBLUE
            if click:
                screen.fill(BG)
                endGame = False
        if launcherButton.collidepoint((mx, my)):
            launcherColor = HOVERBLUE
            if click:
                import Launcher
                Launcher.Launcher.displayLauncher()
        pygame.draw.rect(screen, mainMenuColor, mainMenuButton)
        pygame.draw.rect(screen, launcherColor, launcherButton)
        displayText('New Game', 25, middleX, middleY + 125, WHITE)
        displayText('Quit Game', 25, middleX, middleY + 200, WHITE)
        #END selection of pause options ---------------------------------------

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    endGame = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
       
        pygame.display.update()
        clock.tick(60)
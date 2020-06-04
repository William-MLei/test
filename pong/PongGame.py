## @file PongGame.py
# @title Creating a Paddle for a player.
# @author Arshan Khan
# @date 28 March 2020
import sys
import random
import pygame
from pygame.locals import *
from pong.Ball import *
from pong.Paddle import *
import Scoreboard


#initializing pygame
pygame.init()
FPS = 60
scrSize = (width, height) = (1280, 800)
middleX = int(width/2)
middleY = int(height/2)
screen = pygame.display.set_mode(scrSize)
pygame.display.set_caption('Pong')

clock = pygame.time.Clock()

#Sound effects and music
pygame.mixer.init()
hitPaddle = pygame.mixer.Sound('pong/sounds/bruh.wav')
aiScored = pygame.mixer.Sound('pong/sounds/oof.wav')
playerScored = pygame.mixer.Sound('pong/sounds/hyesz.wav')
win = pygame.mixer.Sound('pong/sounds/victory.wav')
lose = pygame.mixer.Sound('pong/sounds/defeat.wav')

#Declaring various color values
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

# Some variables used for buttons and the main game
click = False
gameOver = True

## @brief This function simplifies displaying text, also used in MenuSettings.py
# @details This function is called when game details or information needs to be displayed to the user.
# @param text The text to be presented to the user.
# @param fontsize The desired size of the text.
# @param x The horizontal coordinate of the text, center-weighted.
# @param y The vertical coordinate of the text, center-weighted.
# @param color The desired size of the text.
def displayText(text, fontsize, x, y, color):
    font = pygame.font.SysFont('rockwell', fontsize, True)
    text = font.render(text, 1, color)
    textpos = text.get_rect(centerx=x, centery=y)
    screen.blit(text, textpos)

## @brief This function controls the AI's paddle's movement.
# @details This function is run in the game's while loop.
# @param ai This is the AI's paddle object.
# @param ball This is the game ball.
# @param diff This is the difficulty selected by the user and determines how the paddle will move.
def aiMove(ai, ball, diff):
    if diff == 25:
        aiSpeed = 9
    elif diff == 10:
        aiSpeed = 7
    else:
        aiSpeed = 6
    if ball.movement[0] > 0: #ensures that the ai moves only when the ball is directed towards it
        #the extra addition of ai.rect.height/5 ensures that the ai will miss the ball sometimes
        if ball.rect.bottom > ai.rect.bottom + 9 - aiSpeed:
            ai.movement[1] = aiSpeed
        elif ball.rect.top < ai.rect.top - 9 + aiSpeed:
            ai.movement[1] = -aiSpeed
        else:
            ai.movement[1] = 0
    else:
        ai.movement[1] = 0

## @brief Function used to calculate the score after a game is finished.
# @details This function runs right after the player or AI reaches the maximum score.
# @param paddleScore The points scored by the player.
# @param aiScore The points scored by the AI.
# @param maxScore The maximum score of the game, used in the calculation.
def calculateScore(paddleScore, aiScore, maxScore):
    finalScore = int(((paddleScore * maxScore) - aiScore) * 17)
    if finalScore == 0:
        finalScore = maxScore
    if finalScore < 0:
        finalScore == int(maxScore/3)
    return finalScore

## @brief This function includes all components, animations, and calculations of the main game.
# @details This function is run after the user clicks the 'BEGIN' button on the main menu.
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

    gameOver = False #Sets the initial state of the game
    paddle = Paddle(int(width/18), middleY, int(width/90), 100, LIGHTGREY) #creating an object for the user's paddle
    ai = Paddle(int(width - width/18), middleY, int(width/90), 100, ENEMYCOLOR) #creating an object for the ai's paddle
    ball = Ball(middleX, middleY, 25, AMBER, [6, 6]) #creating an object for the ball

    while not gameOver: #running our game loop
        for event in pygame.event.get(): #checks for various events in pygame, like keypress, mouse movement, etc
            if event.type == pygame.QUIT: #checks, if the user has clicked the close button
                quit()                    #quits the program

            if event.type == KEYDOWN: #checks whether a key has been pressed or not
                if event.key == K_UP: 
                    paddle.movement[1] = -8 
                elif event.key == K_DOWN:
                    paddle.movement[1] = 8
                if event.key == K_ESCAPE or event.key == K_SPACE:
                    pauseMenu(paddle.points, ai.points)
                if event.key == K_r:
                    ball.resetBall()
            if event.type == KEYUP:    #If the user lifts the key
                paddle.movement[1] = 0 

        aiMove(ai, ball, difficulty) #moves the ai's paddle

        screen.fill(BG)
        pygame.draw.aaline(screen, WHITE, (middleX, 0), (middleX, height))
        displayText('PAUSE the game using the "ESC" key.', 20, 1075, 25, WHITE)

        #drawing user's paddle, ai's paddle and ball
        paddle.drawPaddle()
        ai.drawPaddle()
        ball.draw()

        #displaying the points scored by the user and ai
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

        # Using pygame's collide_mask function, we can get realistic collisions between the ball and the paddle
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

        #checks whether user or ai scored a point and increments accordingly
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

        #updating the states of user's paddle, ai's paddle and ball
        paddle.movePaddle()
        ball.scoreGoal()
        ai.movePaddle()

        pygame.display.update()

        #adding the time delay based on the number of 'Frames per Second'
        clock.tick(FPS)

## @brief This function displays the pause menu and includes all buttons and text necessary for the screen.
# @details This function is run when the user pauses the game by pressing the 'ESC' button.
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

## @brief This function displays the game over screen, including all text and buttons.
# @details This function is run automatically after the player or AI reach the maximum score.
def endGameMenu(victor, paddleScore, aiScore, maxScore):
    screen.fill(BG)
    global click
    endGame = True
    scoreNotSaved = True

    # Saves the score to the scoreboard
    finalScore = calculateScore(paddleScore, aiScore, maxScore)
    Scoreboard.Scoreboard.updateScore("Pong", finalScore)
    
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
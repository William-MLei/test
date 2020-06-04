import unittest
from pongTestFiles.Ball import *
from pongTestFiles.Paddle import *
from pongTestFiles.MenuSettings import *
from pongTestFiles.PongGame import *

class testPong(unittest.TestCase):
    # Any functions not tested are better tested as a System Test
    #############################################################
    screenSize = (width, height) = (500, 500)
    screen = pygame.display.set_mode(screenSize)
    player1 = Paddle(10, 10, 20, 80, (180, 180, 180))
    player2 = Paddle(470, 200, 20, 80, (180, 180, 180))
    screen.fill((0, 0, 0))
    gameBall = Ball(int(width/2), int(height/2), 20, (255, 255, 255), [6, 6])

    # Testing Paddle.py methods -------------------------------------
    def testCreatePaddle(self):
        assert(self.player1 != None)
        assert(self.player2 != None)

    def testPaddleAttributes(self):
        assert(self.player1.x == 10)
        assert(self.player1.y == 10)
        assert(self.player1.sizex == 20)
        assert(self.player1.sizey == 80)
        assert(self.player1.color == (180, 180, 180))
        assert(self.player1.rect.top == 10)
        assert(self.player1.rect.bottom == 90)
        assert(self.player1.rect.right == 30)
    
    def testDisplayPaddles(self):
        self.player1.drawPaddle()
        self.player2.drawPaddle()
        pygame.display.update()
        # visually check if these function correctly
        
    # Testing Ball.py methods ---------------------------------------
    def testCreateBall(self):
        assert(self.gameBall != None)
    
    def testBallAttributes(self):        
        assert(self.gameBall.x == 250)
        assert(self.gameBall.y != 500)
        assert(self.gameBall.size == 20)
        assert(self.gameBall.color == (255, 255, 255))

    def testDisplayBall(self):
        self.gameBall.draw()
        pygame.display.update()
        # visually check if this functions correctly

    # Testing MenuSettings.py methods -------------------------------
    def testChangeDifficulty(self):
        desiredDifficulty = 6
        newDifficulty = changeDifficulty(desiredDifficulty)
        assert(newDifficulty == 6)
    
    def testChangeMaxScore(self):
        desiredMaxScore = 9827
        newMaxScore = changeMaxScore(desiredMaxScore)
        assert(newMaxScore == 9827)

    # Testing PongGame.py methods -----------------------------------
    def testDisplayText(self):
        displayText('TESTING', 30, 200, 100, (255, 255, 255))
        pygame.display.update()
        # visually check if this functions correctly
    
    def testCalculateScore(self):
        playerScore = 14
        enemyScore = 6
        maxScore = 14
        finalScore = calculateScore(playerScore, enemyScore, maxScore)
        assert(finalScore == 3230)
        


if __name__ == '__main__':
    unittest.main()
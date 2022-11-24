# Import necessary modules
# To see sources for these modules, and what I use from them see "Project Documentation.docx"
import pygame
from random import randrange
import datetime
import pickle

# Call the pygame.init() method, which initializes all of the pygame modules we will be using
pygame.init()

# Load the window icon to be used to display in the corner of the window, also define the window width/height
windowIcon = pygame.image.load("./2048.ico")
windowSize = (450, 450)

# Define the font used later in the program
clearSans = pygame.font.Font("./ClearSans-Bold.ttf", 30)

# Set window properties of the pygame window
pygame.display.set_caption("2048")
pygame.display.set_icon(windowIcon)

# Variables
moveCount = 0
score = 0
gameBoardSize = None
gameRunning = True

# These variables are used when the game ends to determine the total time taken
endTime = datetime.datetime.now()
finalTime = datetime.timedelta(0, 0, 0)

# This variable is used to set a stable framerate for the game, this helps to keep time more accurately
clock = pygame.time.Clock()

class Button:
    def __init__(self, color, rect, caption):
        '''Initialize variables for the button'''
        self.color = color
        self.rect = rect
        self.caption = caption
        # Set default Color so the button can be returned to this Color
        self.defaultColor = self.color
        # Create a new colour, by taking the default colour and darkening each RGB value by 10
        self.darkColor = (self.color[0] - 10, self.color[1] - 10, self.color[2] - 10)
    
    def draw(self):
        '''Draw a rectangle to the screen with the button text displayed on top'''
        pygame.draw.rect(screen, self.color, self.rect, border_radius=10)
        text = clearSans.render(self.caption, True, (247, 248, 242))
        textRect = text.get_rect(center=(self.rect[0] + (self.rect[2] / 2), self.rect[1] + (self.rect[3] / 2)))
        screen.blit(text, textRect)
    
    def click(self):
        '''Check if a mouse button has been pressed within the bounds of the button'''
        buttons = pygame.mouse.get_pressed()
        if buttons[0]:
            mousePos = pygame.mouse.get_pos()
            if mousePos[0] >= self.rect[0] - 5 and mousePos[0] <= self.rect[0] + self.rect[2] + 4:
                if mousePos[1] >= self.rect[1] - 5 and mousePos[1] <= self.rect[1] + self.rect[3] + 4:
                    return True
        return False

    def hover(self):
        '''If the mouse is hovering within the bounds of the button, replace the default colour with the dark colour, otherwise display the normal colour'''
        mousePos = pygame.mouse.get_pos()
        if mousePos[0] >= self.rect[0] - 5 and mousePos[0] <= self.rect[0] + self.rect[2] + 4:
            if mousePos[1] >= self.rect[1] - 5 and mousePos[1] <= self.rect[1] + self.rect[3] + 4:
                self.color = self.darkColor
                return
        self.color = self.defaultColor
        return



# Game menu class, used to display the Menu/High Scores at the start of the game
class Menu:
    # Used to check if the user has started the game
    gameStarted = False

    def __init__(self, size):
        '''Initialize the screen size correctly for the menu'''
        global screen
        self.size = size
        screen = pygame.display.set_mode(self.size)

        # Initialize the buttons in the main menu
        self.buttons = [
            Button((237, 207, 115), (5, 5, 190, 90), "4 x 4"),
            Button((237, 200, 80), (5, 105, 190, 90), "5 x 5"),
            Button((237, 194, 45), (5, 205, 190, 90), "6 x 6"),
        ]
    
    def sortList(self, elem):
        '''Return the first element of a list, used for sorting'''
        return elem[0]

    def getScores(self):
        '''Open the high scores file and unpickle the contents, before returning them as a list'''
        scoresList = []

        # Attempt to open the file, if it doesn't exist then return
        try:
            f = open("high_scores.bin", "rb")
        except:
            return

        # If the file does exist, unpickle the contents of the file and append them to the scoresList
        while True:
            try:
                object = pickle.load(f)
                scoresList.append(object)
            except EOFError:
                break

        # Close the file once we're done
        f.close()

        # Sort the list, if the length of the list is more than 3 then only return the first 3 items
        scoresList.sort(key=self.sortList, reverse=True)
        if len(scoresList) >= 3:
            scoresList = scoresList[:3]
        return scoresList

    def getTimes(self):
        '''Open the best times file and unpickle the contents, before returning them as a list'''
        timesList = []

        # Attempt to open the file, if it doesn't exist then return
        try:
            f = open("best_times.bin", "rb")
        except:
            return

        # If the file does exist, unpickle the contents of the file and append them to the scoresList
        while True:
            try:
                object = pickle.load(f)
                timesList.append(object)
            except EOFError:
                break

        # Close the file once we're done
        f.close()

        # Sort the list, if the length of the list is more than 3 then only return the first 3 items
        timesList.sort(key=self.sortList)
        if len(timesList) >= 3:
            timesList = timesList[:3]
        return timesList

    def drawTimes(self):
        '''Print each of the high scores on screen'''

        font = pygame.font.Font("./ClearSans-Bold.ttf", 20)
        bestTimes = self.getTimes()

        # Print the text "best times" on screen
        titleText = font.render("Best Times:", True, (119, 110, 101))
        screen.blit(titleText, (210, 10))

        # If the bestTimes list isn't empty, for each item display the time, moves and board size
        if bestTimes:
            for i in range(len(bestTimes)):
                timeText = font.render(f"Time: {bestTimes[i][0]}", True, (119, 110, 101))
                screen.blit(timeText, (220, 40 + 80 * i))
                movesText = font.render(f"Moves: {bestTimes[i][1]}", True, (119, 110, 101))
                screen.blit(movesText, (220,60 + 80 * i))
                boardText = font.render(f"Board: {bestTimes[i][2]}", True, (119, 110, 101))
                screen.blit(boardText, (220, 80 + 80 * i))
        # Else display the text "none to display" on screen
        else:
            noneText = font.render(f"None to display", True, (119, 110, 101))
            screen.blit(noneText, (220, 40))


    def drawScores(self):
        '''Print each of the best times on screen'''

        font = pygame.font.Font("./ClearSans-Bold.ttf", 20)
        highScores = self.getScores()

        # Print the text "high scores" on screen
        titleText = font.render("High Scores:", True, (119, 110, 101))
        screen.blit(titleText, (410, 10))

        # If the bestTimes list isn't empty, for each item display the time, moves and board size
        if highScores:
            for i in range(len(highScores)):
                timeText = font.render(f"Score: {highScores[i][0]}", True, (119, 110, 101))
                screen.blit(timeText, (420, 40 + 60 * i))
                movesText = font.render(f"Board: {highScores[i][1]}", True, (119, 110, 101))
                screen.blit(movesText, (420, 60 + 60 * i))
        # Else display the text "none to display" on screen
        else:
            noneText = font.render(f"None to display", True, (119, 110, 101))
            screen.blit(noneText, (420, 40))
    
    def drawText(self, text, yPos):
        '''Draw text at the horizontal center of the screen at the y position given'''
        font = pygame.font.Font("./ClearSans-Bold.ttf", 20)
        textContent = font.render(text, True, (119, 110, 101))
        textRect = textContent.get_rect(center=(290, yPos))
        screen.blit(textContent, textRect)

    def drawWindow(self):
        '''A function used to draw the main menu, buttons and high scores to the screen'''
        # Define global variables being used within the function
        global gameRunning
        global windowSize
        global gameBoardSize

        buttons = []

        # Only runs when the game hasn't been started (before a button on the menu is clicked)
        while not self.gameStarted:
            for event in pygame.event.get():
                # If the user closes the window or presses the Escape key, quit the program
                if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    gameRunning = False
                    return
            
            screen.fill((205, 193, 181))

            mousePos = pygame.mouse.get_pos()
            if mousePos[0] <= 200 and mousePos[1] <= 300:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else: pygame.mouse.set_cursor()
            
            # Check if a button has been clicked, if it has then do something different depending on which button
            for i in range(len(self.buttons)):
                self.buttons[i].draw()
                self.buttons[i].hover()
                if self.buttons[i].click():
                    if i == 0:
                        windowSize = (450, 450)
                        gameBoardSize = (4, 4)
                    elif i == 1:
                        windowSize = (560, 560)
                        gameBoardSize = (5, 5)
                    elif i == 2:
                        windowSize = (670, 670)
                        gameBoardSize = (6, 6)
                    self.gameStarted = True

            self.drawTimes()
            self.drawScores()
            self.drawText("Controls:", 310)
            self.drawText("W A S D or Arrow Keys: Move Tiles", 340)
            self.drawText("Escape: Quit", 370)

            pygame.display.flip()
            clock.tick(30)

class Tile:
    tileSize = 100
    tileGap = 10

    def __init__(self, value, xPos, yPos):
        '''Initialize the values of the class, doing some math to figure out the actual x/y of the tile instead of the 0-3 based positions'''
        self.value = value
        self.xPos = xPos * self.tileSize + ((xPos + 1) * self.tileGap)
        self.yPos = yPos * self.tileSize + ((yPos + 1) * self.tileGap)
        self.x = self.xPos
        self.y = self.yPos
        self.font = pygame.font.Font("./ClearSans-Bold.ttf", 50)
        self.hasMerged = False

    def getPos(self):
        '''Set the current Tile x and y coordinates to the calculated xPos and yPos'''
        self.x = self.xPos
        self.y = self.yPos

    def getColor(self):
        '''Return the correct background Color for the tile depending on the value'''
        if self.value == 0: return (205, 193, 181)
        elif self.value == 2: return (238, 228, 218)
        elif self.value == 4: return (236, 224, 200)
        elif self.value == 8: return (242, 177, 121)
        elif self.value == 16: return (245, 149, 99)
        elif self.value == 32: return (246, 124, 96)
        elif self.value == 64: return (246, 94, 59)
        elif self.value == 128: return (237, 207, 115)
        elif self.value == 256: return (237, 204, 98)
        elif self.value == 512: return (237, 200, 80)
        elif self.value == 1024: return (237, 197, 63)
        elif self.value == 2048: return (237, 194, 45)
        else: return (61, 58, 51)
    
    def getFontColor(self):
        '''Return the correct text Color for the tile depending on the value'''
        if self.value < 8: return (119, 110, 101)
        else: return (247, 248, 242)
    
    def getFontPos(self):
        '''Change the position of the font to the center of the tile'''
        fontRect = self.textSurface.get_rect(center=(self.x + (self.tileSize/2), self.y + (self.tileSize/2)))
        return fontRect

    def getFontSize(self):
        '''Change the size of the font depending on the tile value'''
        if self.value < 100:
            self.font = pygame.font.Font("./ClearSans-Bold.ttf", 50)
        elif self.value < 999:
            self.font = pygame.font.Font("./ClearSans-Bold.ttf", 40)
        elif self.value < 9999:
            self.font = pygame.font.Font("./ClearSans-Bold.ttf", 30)
        elif 10000 < self.value:
            self.font = pygame.font.Font("./ClearSans-Bold.ttf", 25)

    def draw(self):
        '''Draw the tile on screen'''
        self.getFontSize()
        pygame.draw.rect(screen, self.getColor(), (self.x, self.y, self.tileSize, self.tileSize), border_radius=3)
        # If the tile value is > 0, draw its value, otherwise just display an empty box
        if self.value > 0:
            self.textSurface = self.font.render(str(self.value), True, self.getFontColor())
            screen.blit(self.textSurface, self.getFontPos())

class Board:
    board = []
    placeableTiles = []
    hasWon = False
    isGameOver = False
    hasWonPreviously = False
    gotFinalTime = False
    gotFinalScore = False

    def __init__(self, boardSize):
        '''Initialize the game board, filling the board with empty tiles'''
        self.size = boardSize
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                self.board.append(Tile(0, j, i))
        pygame.mouse.set_cursor()
            
    def getPlaceableTiles(self):
        '''Check the board to see if any positions are empty'''
        self.placeableTiles = []
        for i in range(len(self.board)):
            if self.board[i].value == 0:
                self.placeableTiles.append(i)

    def spawnRandomPiece(self):
        '''Spawn a random tile in an empty position'''
        randomNumber = randrange(0, 10)
        self.getPlaceableTiles()
        # Get a random placeable tile, and replace it with either a 2 tile or a 4 tile (weighted 9:1)
        if len(self.placeableTiles) > 0:
            randomNumber = self.placeableTiles[randrange(0, len(self.placeableTiles))]
            if randomNumber != 9:
                self.board[randomNumber].value = 2
            else:
                self.board[randomNumber].value = 4

    def saveScore(self, score, boardSize):
        '''Save the score and game board size to the file "high_scores"'''
        f = open("high_scores.bin", "ab")
        pickle.dump([score, boardSize], f)
        f.close()


    def saveTime(self, time, moves, boardSize):
        '''Save the time, move count and board size to the file "best_times"'''
        f = open("best_times.bin", "ab")
        pickle.dump([time, moves, boardSize], f)
        f.close()
    
    def checkGamestate(self):
        '''Check to see if the board is full, or if the player has won'''
        # Global variables from outside of the function
        global endTime
        global finalTime

        # Check each tile in the board to check if it contains a 2048 tile. If it does, and the player hasn't already won then display the win screen
        for tile in self.board:
            if tile.value == 2048 and not self.hasWonPreviously:
                self.hasWon = True

                # If the final time hasn't been calculated, then calculate it.
                # Subtract the start time from the end time to get the final time, before removing the milliseconds
                if not self.gotFinalTime:
                    self.gotFinalTime = True
                    endTime = datetime.datetime.now()
                    finalTime = endTime-startTime
                    finalTime = str(finalTime).split(".")[0]
                    self.saveTime(finalTime, moveCount, f"{self.size[0]} x {self.size[1]}")
                
        # Check if the game is over, if it is then display the game over screen
        # Subtract the start time from the end time to get the final time, before removing the milliseconds
        if self.isGameOver and not self.gotFinalScore:
            self.gotFinalScore = True
            self.saveScore(score, f"{self.size[0]} x {self.size[1]}")
            endTime = datetime.datetime.now()
            finalTime = endTime-startTime
            finalTime = str(finalTime).split(".")[0]

        # If the player has won, they can continue playing, though they will be notified that they won, as well as their score
        if self.hasWon and not self.hasWonPreviously:
            # Display a surface over the game, with a transparent background
            winSurface = pygame.Surface((windowSize[0], windowSize[1]))
            winSurface.set_alpha(128)
            winSurface.fill((237, 207, 115))
            screen.blit(winSurface, (0, 0))

            # Define lines of text to be displayed on screen
            text = [
                "You Win!",
                f"Score: {score}",
                f"Moves: {moveCount}",
                f"Time: {finalTime}",
                "",
                "Press any direction",
                "to continue"
            ]

            # Get the required font position for each line of text from above, display it on screen
            for label in self.getFontPos(text, 60):
                screen.blit(label[0], label[1])

        # If the game is over, display thr game over screen
        elif self.isGameOver:
            # Display surface over the game, with a transparent background
            loseSurface = pygame.Surface((windowSize[0], windowSize[1]))
            loseSurface.set_alpha(128)
            loseSurface.fill((0, 0, 0))
            screen.blit(loseSurface, (0, 0))

            # Define lines of text to be displayed on screen
            text = [
                "Game Over!",
                f"Score: {score}",
                f"Moves: {moveCount}",
                f"Time: {finalTime}",
            ]

            # Get the required font position for each line of text from above, display it on screen
            for label in self.getFontPos(text, 30):
                screen.blit(label[0], label[1])
        
    def getFontPos(self, text, offset):
        '''Get horizontally centered lines of text at the vertical offset provided'''
        label = []
        for line in range(len(text)):
            textSurface = clearSans.render(text[line], True, (255, 255, 255))
            fontRect = textSurface.get_rect(center=(windowSize[0]/2, windowSize[1]/2+((line-1.5)*50)-offset))
            label.append([textSurface, fontRect])
        return label

    def setup(self):
        '''Ran at the start of the game, spawns 2 random tiles'''
        for i in range(2):
            self.spawnRandomPiece()

    def moveTiles(self, direction):
        '''Depending on which key has been pressed, move all tiles in the board in the correct direction'''
        # Global variables from outside of the function
        global score
        global moveCount

        # 0 = Up
        # 1 = Right
        # 2 = Down
        # 3 = Left

        # Each time a valid move is made, increment the move count
        if not self.isGameOver and not self.hasWon:
            moveCount += 1

        # Check if any tiles are placeable, if not then game over
        self.getPlaceableTiles()
        if len(self.placeableTiles) == 0:
            self.isGameOver = True
            
        # Check if the player has the "win" screen open, if they do then pressing a button will remove it
        # and allow them to continue playing
        if self.hasWon and not self.hasWonPreviously:
            self.hasWonPreviously = True

        # Else if the game isn't over, then continue as normal
        elif (not self.hasWon or self.hasWonPreviously) and not self.isGameOver:
            # Default some values, to be checked if they are made true later
            nonMovablePieces = 0
            hasMoved = False
            for piece in self.board:
                piece.hasMerged = False

            # For each direction, check if any of the pieces are movable, if they are then iterate through them, moving them in the correct direction
            # until they either hit a wall, or hit another tile that they cannot merge with
            if not self.isGameOver:
                if direction == 0: # Up
                    while nonMovablePieces < len(self.board):
                        for i in range(len(self.board)):
                            if i -  self.size[1]>= 0 and self.board[i].value > 0:
                                if self.board[i- self.size[1]].value == 0:
                                    self.board[i- self.size[1]].value = self.board[i].value
                                    self.board[i].value = 0
                                    hasMoved = True
                                elif self.board[i- self.size[1]].value == self.board[i].value and not self.board[i- self.size[1]].hasMerged and not self.board[i].hasMerged:
                                    self.board[i- self.size[1]].value *= 2
                                    self.board[i- self.size[1]].hasMerged = True
                                    self.board[i].value = 0
                                    hasMoved = True
                                    score += self.board[i- self.size[1]].value
                            elif i -  self.size[1] < 0: nonMovablePieces += 1
                            
                elif direction == 2: # Down
                    while nonMovablePieces < len(self.board):
                        for i in range(len(self.board)-1, -1, -1):
                            if i + self.size[1] < len(self.board) and self.board[i].value > 0:
                                if self.board[i+ self.size[1]].value == 0:
                                    self.board[i+ self.size[1]].value = self.board[i].value
                                    self.board[i].value = 0
                                    hasMoved = True
                                elif self.board[i+ self.size[1]].value == self.board[i].value and not self.board[i+ self.size[1]].hasMerged and not self.board[i].hasMerged:
                                    self.board[i+ self.size[1]].value *= 2
                                    self.board[i+ self.size[1]].hasMerged = True
                                    self.board[i].value = 0
                                    hasMoved = True
                                    score += self.board[i+ self.size[1]].value
                            elif i +  self.size[1] >= len(self.board): nonMovablePieces += 1

                elif direction == 1: # Right
                    while nonMovablePieces < len(self.board):
                        for i in range(len(self.board)-1, -1, -1):
                            canMove = True
                            boardEdges = []
                            for number in  range(self.size[1]+1):
                                boardEdges.append(number *  self.size[0])
                            for number in boardEdges:
                                if i + 1 == number: canMove = False
                            if canMove and self.board[i].value > 0:
                                if self.board[i+1].value == 0:
                                    self.board[i+1].value = self.board[i].value
                                    self.board[i].value = 0
                                    hasMoved = True
                                elif canMove and self.board[i+1].value == self.board[i].value and not self.board[i+1].hasMerged and not self.board[i].hasMerged:
                                    self.board[i+1].value *= 2
                                    self.board[i+1].hasMerged = True
                                    self.board[i].value = 0
                                    hasMoved = True
                                    score += self.board[+1].value
                            elif not canMove: nonMovablePieces += 1

                elif direction == 3: # Left
                    while nonMovablePieces < len(self.board):
                        for i in range(len(self.board)):
                            canMove = True
                            boardEdges = []
                            for number in  range(self.size[1]):
                                boardEdges.append((number *  self.size[0])-1)
                            for number in boardEdges:
                                if i - 1 == number: canMove = False
                            if canMove and self.board[i].value > 0:
                                if self.board[i-1].value == 0:
                                    self.board[i-1].value = self.board[i].value
                                    self.board[i].value = 0
                                    hasMoved = True
                                elif self.board[i-1].value == self.board[i].value and not self.board[i-1].hasMerged and not self.board[i].hasMerged:
                                    self.board[i-1].value *= 2
                                    self.board[i-1].hasMerged = True
                                    self.board[i].value = 0
                                    hasMoved = True
                                    score += self.board[i-4].value
                            elif not canMove: nonMovablePieces += 1


            # If any tiles have moved, then spawn a random piece
            if hasMoved:
                self.spawnRandomPiece()
                    
            return
    
    def generateTestTiles(self):
        '''Fill the board with a set of tiles for testing'''
        num = 2
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                self.board.append(Tile(num, j, i))
                num *= 2
    
    def draw(self):
        '''Draw the board, and everytile inside of it'''
        pygame.draw.rect(screen, (186, 173, 160), (0, 0, windowSize[0], windowSize[1]))
        for tile in self.board:
            tile.draw()

def gameSetup():
    '''If the user didn't quit the game in the menu, run this'''
    global startTime
    global screen
    global gameBoard

    screen = pygame.display.set_mode(windowSize)

    # After the game has started (the player has exited the main menu) then generate the game board
    gameBoard = Board(gameBoardSize)
    gameBoard.setup()

    # Start the game timer to be used for high scores
    startTime = datetime.datetime.now()

def main():
    '''Main game loop, runs every frame'''
    global gameRunning
    global gameBoard

    while gameRunning:
        for event in pygame.event.get():
            # If the escape key is pressed, or the window is closed, quit the application
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                gameRunning = False

            # Depending on the direction the user presses, call a function to move all tiles in the board with different inputs
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP: gameBoard.moveTiles(0)
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT: gameBoard.moveTiles(1)
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN: gameBoard.moveTiles(2)
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT: gameBoard.moveTiles(3)

        # Draw the gameboard and all the tiles inside it
        gameBoard.draw()

        # Check if the player has won, or lost
        gameBoard.checkGamestate()

        # Flip the display
        pygame.display.flip()
        clock.tick(30)

# Initialize the menu at the start of the game
m = Menu((600, 400))
m.drawWindow()

# Initialize empty variables to be used later
gameBoard = None
screen = None
startTime = None
screen = None

# Start the game
if gameRunning:
    gameSetup()
    main()
    
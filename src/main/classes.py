import pygame, sys, os
from pygame.locals import *

boardWidth = 15
boardHeight = 20

class board(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = []
        self.allCubes = []
        self.gridSize = 16

    def addCube(self, posX, posY):
        green = (0, 255, 0)
        self.board.append(cube(posX, posY, green, self))
    
    def isFree(self, x, y):
        for cube in range(0, len(self.board)):
            if self.board[cube].posX == x and self.board[cube].posY == y:
                return False
        return True
        
    def update(self):
        self.deleteFullLines()
        
    def isFull(self):
        pass
    
    def deleteFullLines(self):
        cubesInLine = 0
        deleteLines = []
        
        for ypos in range(0, self.height+1):
                for cubes in range(0, len(self.board)):
                    if self.board[cubes].posY == ypos:
                        cubesInLine += 1
                        
                if cubesInLine == self.width:
                    deleteLines.append(ypos)
                cubesInLine = 0
        cubesInLine = 0     
        
        for i in deleteLines:
            while cubesInLine < self.width:
                for cube in self.board:
                    if cube.posY == i: 
                        self.board.remove(cube)
                        cubesInLine += 1
                        print cube.posX
            cubesInLine = 0
        
        for i in deleteLines:
            for cube in self.board:
                if cube.posY < i:
                    cube.posY += 1
                    
        del deleteLines[:]
                    
    def getXPosInPixels(self, pos):
        boardPosition = 640/2-(self.width *self.gridSize/2)
        return boardPosition + self.gridSize*(pos-1)+1
    
    def getYPosInPixels(self, pos):
        boardPosition = 15
        return boardPosition + self.gridSize*(pos-1)+1
        
    
    def drawBoard(self):
        screen = pygame.display.get_surface()
        gridStartX = 640/2-(self.width*self.gridSize/2)
        gridStartY = 15
        
        # Draw gridlines
        for x in range(self.width+1):
            pygame.draw.line(screen,(100,100,100), [gridStartX+x*self.gridSize,gridStartY],
                             [gridStartX+x*self.gridSize,gridStartY+self.height*self.gridSize],1)
        
        for y in range(self.height+1):
            pygame.draw.line(screen,(100,100,100), [gridStartX,gridStartY+y*self.gridSize],
                             [gridStartX+self.width*self.gridSize,gridStartY+y*self.gridSize],1)
        
        for i in range(0, len(self.board)):
            self.board[i].drawCube()
                    
            
class blockStyle(object):
    def __init__(self, style):
        self.blockStyle = style
        
    def getStyle(self):
        return self.blockStyle

class cube(object):
    def __init__(self, posX, posY, color, board):
        self.posX = posX
        self.posY = posY
        self.gridSize = 16
        self.color = color
        self.board = board
            
    def getXPosInPixels(self, pos):
        boardPosition = 640/2-(boardWidth*self.gridSize/2)
        return boardPosition + self.gridSize*(pos-1)+1
    
    def getYPosInPixels(self, pos):
        boardPosition = 15
        return boardPosition + self.gridSize*(pos-1)+1
        
    def drawCube(self):
        screen = pygame.display.get_surface()
        pygame.draw.rect(screen, self.color, (self.getXPosInPixels(self.posX), self.getYPosInPixels(self.posY), self.gridSize-1, self.gridSize-1) )
    
    def checkIfMovePossible(self, direction):
        if direction == "DOWN":
            if self.posY < self.board.height and self.board.isFree(self.posX, self.posY+1) == True:
                return True
            else:
                return False
        elif direction == "LEFT":
            if self.posX > 1:
                return True
            else:
                return False
        elif direction == "RIGHT":
            if self.posX < self.board.width:
                return True
            else:
                return False
        
    def moveDown(self):
        self.posY += 1
    
    def moveLeft(self):
        self.posX -= 1
    
    def moveRight(self):
        self.posX += 1
    
class block(object):
    def __init__(self, width, height, blockStyle, board):
        self.blockSize = 16
        self.width = width
        self.height = height
        self.gridSize = 16
        self.currentRotation = 1
        self.isDown = False
        self.style = blockStyle
        
        self.board = board
        
        self.xPos = boardWidth/2
        self.yPos = 1
        
        self.makeNewBlock()
    
    def makeNewBlock(self):
        self.currentRotation = 1
        
        self.blockStyle = ["","","",""]
        self.allCubes = []
        rotation = -1
        
        for c in self.style:
            if c == "[":
                rotation = rotation + 1
            if c == "#" or c == "B" or c == "R" or c == "\n":
                self.blockStyle[rotation] = self.blockStyle[rotation]+c
        
        self.readNewStyle()
       
            
    def readNewStyle(self):
        currentStyle = self.blockStyle[self.currentRotation]
        col = -3
        row = -2
        
        red = (255, 0, 0)
        blue = (0, 0, 255)

        for i in range(0, len(currentStyle)):
            if currentStyle[i] == "\n":
                col = col +1
                row = -2
                continue
                
            if currentStyle[i] == "R":
                self.allCubes.append(cube(self.xPos, self.yPos, blue, self.board))
                    
            if currentStyle[i] == "B":
                thisYPos = self.yPos+col
                thisXPos = self.xPos+row
                self.allCubes.append(cube(thisXPos, thisYPos, red, self.board))
                
            row = row+1  
        
    def changeStyle(self, style):
        self.style = style
        self.isDown = False
        self.makeNewBlock()
        
    def getXPosInPixels(self, pos):
        boardPosition = 640/2-(self.width*self.gridSize/2)
        return boardPosition + self.gridSize*(pos-1)+1
    
    def getYPosInPixels(self, pos):
        boardPosition = 15
        return boardPosition + self.gridSize*(pos-1)+1
        
    def drawBlock(self):
        for i in range(len(self.allCubes)):
            self.allCubes[i].drawCube()
              
    def reload(self):
        self.xPos = 5
        self.yPos = 5  
        del self.allCubes[:]
        self.readNewStyle()   
        
    def updatePlayer(self):
        isPossible = True
        for i in range(len(self.allCubes)):
            if self.allCubes[i].checkIfMovePossible("DOWN") == False:
                isPossible = False
                self.isDown = True
                for j in range(len(self.allCubes)):
                    self.board.addCube(self.allCubes[j].posX, self.allCubes[j].posY)
                self.reload()    
                
        if isPossible == True:
            for i in range(len(self.allCubes)):
                self.allCubes[i].moveDown()
            
            
    def rotate(self):
        for i in range(len(self.allCubes)):
            if self.allCubes[i].color == (0, 0, 255):
                self.xPos = self.allCubes[i].posX
                self.yPos = self.allCubes[i].posY
                
        del self.allCubes[:]
        
        self.readNewStyle()
    
    def handlePlayerInput(self):
        key = pygame.key.get_pressed()

            
        if key[pygame.K_RIGHT]:
            isPossible = True
            for i in range(len(self.allCubes)):
                if self.allCubes[i].checkIfMovePossible("RIGHT") == False:
                    isPossible = False
            if isPossible == True:
                for i in range(len(self.allCubes)):
                    self.allCubes[i].moveRight()  
        elif key[pygame.K_LEFT]:
            isPossible = True
            for i in range(len(self.allCubes)):
                if self.allCubes[i].checkIfMovePossible("LEFT") == False:
                    isPossible = False
            if isPossible == True:
                for i in range(len(self.allCubes)):
                    self.allCubes[i].moveLeft()  
        if key[pygame.K_DOWN]:
            self.updatePlayer()  
        if key[pygame.K_UP]:
            if self.currentRotation == 3:
                self.currentRotation = 0
            else:
                self.currentRotation = self.currentRotation + 1
            self.rotate()
            
            
           
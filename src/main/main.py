import pygame, sys, os, random
from classes import *
from pygame.locals import *

blocksFile = "blocks.txt"
thisBlock = ""
allBlocks = []

boardWidth = 15
boardHeight = 20

gameOver = False

# Make all the blocks which are in file "blocks.txt"
file = open(blocksFile, "r")
while file:
    line = file.readline()
    if line.find("END") >= 0:
        break
    if line.find("/") >= 0:
        allBlocks.append(blockStyle(thisBlock))
        thisBlock = ""
        continue

    thisBlock = thisBlock + line

# Make board
gameBoard = board(boardWidth, boardHeight)

# All pygame init
pygame.init()

gameWindow = pygame.display.set_mode((640, 480))
pygame.display.set_caption('PyTetris')
clock = pygame.time.Clock()

playerBlock = block(boardWidth, boardHeight, allBlocks[random.randrange(len(allBlocks))].getStyle(), gameBoard)
pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT + 1, 150)
pygame.time.set_timer(pygame.USEREVENT + 2, 1000)

#Game loop
while gameOver == False:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            gameOver = True
        elif event.type == pygame.USEREVENT + 1:
            playerBlock.handlePlayerInput()
        elif event.type == pygame.USEREVENT + 2:
            playerBlock.updatePlayer()

    if playerBlock.isDown == True:
        playerBlock.changeStyle(allBlocks[random.randrange(len(allBlocks))].getStyle())

    gameWindow.fill((0,0,0))

    gameBoard.drawBoard()
    gameBoard.update()
    playerBlock.drawBlock()

    pygame.display.flip()

pygame.quit()

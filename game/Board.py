
from importlib.resources import path
from optparse import check_choice
import numpy as np
from .Stone import *
from tkinter import *
from enum import Enum
from .Move import *
from .PathTree import *

class Board:

    BOARD_SIZE = 8
    RECT_SIZE = 50
    CIRCLE_OFFSET = 5
    RECT_COLORS = ["grey", "red"]
    CIRCLE_COLORS = ["white", "black"]
    CIRCLE_COLOR_SELECTED = "blue"
    PLAYER_A = 0 # AI-Player
    PLAYER_B = 1 # Human-Player

    def __init__(self, canvas: Canvas):
        self._board = []
        self._playerA = []
        self._playerB = []
        self._canvas = canvas
        self._selectedStone = None
        self._turn = Board.PLAYER_B 

    def start(self) -> None:
        self.initiateBoard()
        print(self._board)

    def getPlayerOrientation(self, player):
        if(player == Board.PLAYER_A):
            return 1
        else:
            return -1 

    def initiateBoard(self) -> None:
        self._board = self.createEmptyList()
        posX = 0
        posY = -1
        for i in range(0,Board.BOARD_SIZE * Board.BOARD_SIZE,2):
            
            if i%Board.BOARD_SIZE == 0: posY += 1
            
            if posY <= 2 or posY >= 5:
                posX = i%Board.BOARD_SIZE + (1 if posY%2 == 0 else 0) # posY%2 sorgt für eine alternierende Belegung des Brettes
                if posY <=2:
                    tmpStone = Stone(posX, posY, Board.PLAYER_A)
                    self._playerA.append(tmpStone)
                    self._board[posY][posX] = tmpStone
                else:
                    tmpStone = Stone(posX, posY, Board.PLAYER_B)
                    self._playerB.append(tmpStone)
                    self._board[posY][posX] = tmpStone

    def createEmptyList(self) -> list:
        tmpList = []
        posY = -1
        for i in range(0,64):
            if i%Board.BOARD_SIZE == 0: 
                posY += 1
                tmpList.append([])

            tmpList[posY].append(None)

        return tmpList

    def draw(self):
        posX = 0
        posY = -1

        for i in range(0,Board.BOARD_SIZE * Board.BOARD_SIZE):
            if i%Board.BOARD_SIZE == 0: posY += 1

            posX = i%Board.BOARD_SIZE
            colorIndex = (i + (1 if posY%2 == 0 else 0))%2

            curLeft = posX * Board.RECT_SIZE
            curRight = posX * Board.RECT_SIZE + Board.RECT_SIZE
            curTop = posY * Board.RECT_SIZE
            curBottom = posY * Board.RECT_SIZE + Board.RECT_SIZE

            curStone = self._board[posY][posX]

            self._canvas.create_rectangle(curLeft, curTop, curRight, curBottom, fill=Board.RECT_COLORS[colorIndex], tags=["board"])

            if not curStone is None:
                self._canvas.create_oval(curLeft + Board.CIRCLE_OFFSET, curTop + Board.CIRCLE_OFFSET, curRight - Board.CIRCLE_OFFSET, curBottom - Board.CIRCLE_OFFSET, fill=Board.CIRCLE_COLORS[curStone.team], tags=["stone"])

    def redrawStones(self):
        self._canvas.delete("stone")

        stones = self._playerA + self._playerB

        for i in range(0, len(stones)):

            posX = stones[i].posX
            posY = stones[i].posY

            curLeft = posX * Board.RECT_SIZE
            curRight = posX * Board.RECT_SIZE + Board.RECT_SIZE
            curTop = posY * Board.RECT_SIZE
            curBottom = posY * Board.RECT_SIZE + Board.RECT_SIZE
            
            if stones[i].isSelected:
                curColor = Board.CIRCLE_COLOR_SELECTED
                if len(stones[i].cans) > 0: self.drawHelpers(stones[i].cans)
                    
            else:
                curColor = Board.CIRCLE_COLORS[stones[i].team]

            self._canvas.create_oval(curLeft + Board.CIRCLE_OFFSET, curTop + Board.CIRCLE_OFFSET, curRight - Board.CIRCLE_OFFSET, curBottom - Board.CIRCLE_OFFSET, fill=curColor, tags=["stone"])


    def drawHelpers(self, fields):
        for i in range(0, len(fields)):
            posX = fields[i][1]
            posY = fields[i][0]

            curLeft = posX * Board.RECT_SIZE
            curRight = posX * Board.RECT_SIZE + Board.RECT_SIZE
            curTop = posY * Board.RECT_SIZE
            curBottom = posY * Board.RECT_SIZE + Board.RECT_SIZE

            self._canvas.create_oval(curLeft + Board.CIRCLE_OFFSET, curTop + Board.CIRCLE_OFFSET, curRight - Board.CIRCLE_OFFSET, curBottom - Board.CIRCLE_OFFSET, tags=["stone"])



    def onClick(self, event):
        if self._turn != Board.PLAYER_B: return # not your turn!

        posX = int(event.x/Board.RECT_SIZE)
        posY = int(event.y/Board.RECT_SIZE)

        if not self._board[posY][posX] is None and self._board[posY][posX].team == Board.PLAYER_B:
            if not self._selectedStone is None: self._selectedStone.isSelected = False
            self._selectedStone = self._board[posY][posX]
            self._board[posY][posX].isSelected = True
            
            self.detectPossibleMoves(self._board[posY][posX])
            self.redrawStones()
        elif self._board[posY][posX] is None and not self._selectedStone is None:
            if (posY, posX) in self._selectedStone.cans:
                # valid move!
                self._board[posY][posX] = self._selectedStone
                self._board[self._selectedStone.posY][self._selectedStone.posX] = None
                self._selectedStone.posX = posX
                self._selectedStone.posY = posY
                self._selectedStone.isSelected = False
                self._selectedStone = None
                self.redrawStones()





    def changeTurn(self):
        if self._turn == Board.PLAYER_A:
            self._turn = Board.PLAYER_B
        else:
            self._turn = Board.PLAYER_A
            self.invokeAI()

    def invokeAI(self):
        print("yay")

    def buildPathTree(self, stone: Stone) -> PathTree:
        tmpPathTree = PathTree(stone.pos)

        tmpPathTree.root.add(self.startBuildingRecursion(tmpPathTree.root, stone))

        return tmpPathTree


    def startBuildingRecursion(self, parent: PathTreeNode, stone: Stone) -> None:

        orientation = self.getPlayerOrientation(stone.team)

        if stone.type == Stone.Type.Normal:
            next = [(parent.pos[0] + 1 * orientation, parent.pos[1] - 1 ), (parent.pos[0] + 1 * orientation, parent.pos[1] + 1)]
            afternext = [(parent.pos[0] + 2 * orientation, parent.pos[1] - 2 ), (parent.pos[0] + 2 * orientation, parent.pos[1] + 2)]
        else:
            next = [(parent.pos[0] + 1 , parent.pos[1] - 1), (parent.pos[0] + 1, parent.pos[1]  + 1), (parent.pos[0] - 1, parent.pos[1] - 1), (parent.pos[0] - 1, parent.pos[1] + 1)]
            afternext = next = [(parent.pos[0] + 2 , parent.pos[1] - 2), (parent.pos[0] + 2, parent.pos[1]  + 2), (parent.pos[0] - 2, parent.pos[1] - 2), (parent.pos[0] - 2, parent.pos[1] + 2)]

        for i in range (0, len(next)):

            if not self.checkIndexInRange(next[i]): continue # position out of board

            col = self.checkCollision(stone, next[i][1], next[i][0])
            
            if col == Board.CollisionType.Friend: # position blocked by own stone
                continue
            elif col == Board.CollisionType.Enemy: # position blocked by enemy => jumpable?

                if self.checkIndexInRange(afternext[i]) and self.checkCollision(stone, afternext[i][1], afternext[i][0]) == Board.CollisionType.Nothing:
                    # enemy can be jumped
                    
                    tmpNode = PathTreeNode(afternext, parent, self._board[next[i][0], next[i][1]])
                    parent.add(tmpNode)
                    self.startBuildingRecursion(self, tmpNode, stone) # start recursion here to find all possible moves

                else: # enemy can not be jumped                    
                    continue
                
            parent.add(PathTreeNode(next, parent)) # none of the upper cases applied => normal move


    def checkIndexInRange(pos: tuple) -> bool:
        if pos[1] < 0 or pos[1] > Board.BOARD_SIZE - 1: return False
        if pos[0] < 0 or pos[0] > Board.BOARD_SIZE - 1: return False
        
        return True

    
    def checkCollision(self, stone, posX, posY) -> int:
    
        if not self._board[posY][posX] is None:
            if self._board[posY][posX].team == stone.team:
                return Board.CollisionType.Friend
            else:
                return Board.CollisionType.Enemy
        else:
            return Board.CollisionType.Nothing

    class CollisionType(Enum):
        Nothing = 1
        Friend = 2
        Enemy = 3
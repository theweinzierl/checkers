from .Stone import *
from tkinter import *
from enum import Enum
from .Move import *
from .PathTree import *
import random
from .settings import *




class Board: 

    def __init__(self, canvas: Canvas):
        self._board = []
        self._playerA = []
        self._playerB = []
        self._canvas = canvas
        self._selectedStone = None
        self._turn = PLAYER_B

        self._score = {PLAYER_A: 0, PLAYER_B: 0}

    def start(self) -> None:
        self.initiateBoard()
        print(self._board)

    def getPlayerOrientation(self, player):
        if(player == PLAYER_A):
            return 1
        else:
            return -1 

    def initiateBoard(self) -> None:
        self._board = self.createEmptyList()
        posX = 0
        posY = -1
        for i in range(0,BOARD_SIZE * BOARD_SIZE,2):
            
            if i%BOARD_SIZE == 0: posY += 1
            
            if posY <= 2 or posY >= 5:
                posX = i%BOARD_SIZE + (1 if posY%2 == 0 else 0) # posY%2 sorgt für eine alternierende Belegung des Brettes
                if posY <=2:
                    tmpStone = Stone(posX, posY, PLAYER_A)
                    self._playerA.append(tmpStone)
                    self._board[posY][posX] = tmpStone
                else:
                    tmpStone = Stone(posX, posY, PLAYER_B)
                    self._playerB.append(tmpStone)
                    self._board[posY][posX] = tmpStone

    def createEmptyList(self) -> list:
        tmpList = []
        posY = -1
        for i in range(0,64):
            if i%BOARD_SIZE == 0: 
                posY += 1
                tmpList.append([])

            tmpList[posY].append(None)

        return tmpList

    def draw(self):
        posX = 0
        posY = -1

        for i in range(0,BOARD_SIZE * BOARD_SIZE):
            if i%BOARD_SIZE == 0: posY += 1

            posX = i%BOARD_SIZE
            colorIndex = (i + (1 if posY%2 == 0 else 0))%2

            curLeft = posX * RECT_SIZE
            curRight = posX * RECT_SIZE + RECT_SIZE
            curTop = posY * RECT_SIZE
            curBottom = posY * RECT_SIZE + RECT_SIZE

            curStone = self._board[posY][posX]

            self._canvas.create_rectangle(curLeft, curTop, curRight, curBottom, fill=RECT_COLORS[colorIndex], tags=["board"])

            if not curStone is None:
                self._canvas.create_oval(curLeft + CIRCLE_OFFSET, curTop + CIRCLE_OFFSET, curRight - CIRCLE_OFFSET, curBottom - CIRCLE_OFFSET, fill=CIRCLE_COLORS[curStone.team], tags=["stone"])

    def redrawStones(self):
        self._canvas.delete("stone")

        stones = self._playerA + self._playerB

        for i in range(0, len(stones)):
            if not stones[i].isVisible: continue
            posX = stones[i].posX
            posY = stones[i].posY

            curLeft = posX * RECT_SIZE
            curRight = posX * RECT_SIZE + RECT_SIZE
            curTop = posY * RECT_SIZE
            curBottom = posY * RECT_SIZE + RECT_SIZE
            
            if stones[i].isSelected:
                curColor = CIRCLE_COLOR_SELECTED
                if len(stones[i].moves) > 0: self.drawHelpers(stones[i].moves)
                    
            else:
                curColor = CIRCLE_COLORS[stones[i].team]

            self._canvas.create_oval(curLeft + CIRCLE_OFFSET, curTop + CIRCLE_OFFSET, curRight - CIRCLE_OFFSET, curBottom - CIRCLE_OFFSET, fill=curColor, tags=["stone"])

            if stones[i].type == Stone.Type.King:
                self._canvas.create_oval(curLeft + KING_OFFSET, curTop + KING_OFFSET, curRight - KING_OFFSET, curBottom - KING_OFFSET, fill=KING_COLOR, tags=["stone"])
                

    def drawHelpers(self, moves: list):
        for i in range(0, len(moves)):
            posX = moves[i].pos[1]
            posY = moves[i].pos[0]

            curLeft = posX * RECT_SIZE
            curRight = posX * RECT_SIZE + RECT_SIZE
            curTop = posY * RECT_SIZE
            curBottom = posY * RECT_SIZE + RECT_SIZE

            self._canvas.create_oval(curLeft + CIRCLE_OFFSET, curTop + CIRCLE_OFFSET, curRight - CIRCLE_OFFSET, curBottom - CIRCLE_OFFSET, tags=["stone"])



    def onClick(self, event):
        if self._turn != PLAYER_B: return # not your turn!

        posX = int(event.x/RECT_SIZE)
        posY = int(event.y/RECT_SIZE)

        selectedTile = self._board[posY][posX]

        if not selectedTile is None: # and selectedTile.team == PLAYER_B: # selected tile is stone
            if not self._selectedStone is None: self._selectedStone.isSelected = False
            self._selectedStone = selectedTile
            self._selectedStone.isSelected = True
            
            self._selectedStone.pathTree = self.buildPathTree(self._selectedStone)
            self.redrawStones()

        elif selectedTile is None and not self._selectedStone is None: # selected tile is not stone            
            self.executeMove((posY, posX), self._selectedStone)


    def executeMove(self, pos, stone):
        selectedMove = stone.getMove(pos)
        if not selectedMove is None:    
            print ("is in moves!")

            self._score[stone.team] += len(selectedMove.jumpedStones)

            # vanish jumped stones
            for jumpedStone in selectedMove.jumpedStones:
                jumpedStone.isVisible = False
                self._board[jumpedStone.posY][jumpedStone.posX] = None

            


       # if stone.team == PLAYER_B:
            # valid move!
        self._board[pos[0]][pos[1]] = stone
        self._board[stone.posY][stone.posX] = None
        stone.posX = pos[1]
        stone.posY = pos[0]
        stone.isSelected = False
        self._selectedStone = None
        self.redrawStones()
        self.changeTurn()


    def changeTurn(self):
        if self._turn == PLAYER_A:
            self._turn = PLAYER_B
        else:
            self._turn = PLAYER_A
            self.invokeAI()

    def invokeAI(self):
        # refresh Moves
        best = (0, None, None)
        moveable = []
        for stone in self._playerA:
            if not stone.isVisible: continue

            stone.pathTree = self.buildPathTree(stone)
            if stone.moves != []:
                for move in stone.moves:
                    if move.metric > best[0]:
                        best = (move.metric, move, stone)
                moveable.append(stone)

        if best[0] > 0:
            self.executeMove(best[1].pos, best[2])
        else:
            rndStone = random.choice(moveable)
            rndMove = random.choice(rndStone.moves)
            self.executeMove(rndMove.pos, rndStone)

        print("executed")
       


    def buildPathTree(self, stone: Stone) -> PathTree:
        tmpPathTree = PathTree(stone.pos)

        self.startBuildingRecursion(tmpPathTree.root, stone)

        return tmpPathTree


    def startBuildingRecursion(self, parent: PathTreeNode, stone: Stone, foundEnemy: bool = False) -> None:

        orientation = self.getPlayerOrientation(stone.team)

        if stone.type == Stone.Type.Normal:
            next = [(parent.pos[0] + 1 * orientation, parent.pos[1] - 1 ), (parent.pos[0] + 1 * orientation, parent.pos[1] + 1)]
            afternext = [(parent.pos[0] + 2 * orientation, parent.pos[1] - 2 ), (parent.pos[0] + 2 * orientation, parent.pos[1] + 2)]
        else:
            next = [(parent.pos[0] + 1 , parent.pos[1] - 1), (parent.pos[0] + 1, parent.pos[1]  + 1), (parent.pos[0] - 1, parent.pos[1] - 1), (parent.pos[0] - 1, parent.pos[1] + 1)]
            afternext = [(parent.pos[0] + 2 , parent.pos[1] - 2), (parent.pos[0] + 2, parent.pos[1]  + 2), (parent.pos[0] - 2, parent.pos[1] - 2), (parent.pos[0] - 2, parent.pos[1] + 2)]

        for i in range (0, len(next)):

            if not self.checkIndexInRange(next[i]): continue # position out of board

            col = self.checkCollision(stone, next[i][1], next[i][0])
            
            if col == Board.CollisionType.Friend: # position blocked by own stone
                continue
            elif col == Board.CollisionType.Enemy: # position blocked by enemy => jumpable?

                if self.checkIndexInRange(afternext[i]) and self.checkCollision(stone, afternext[i][1], afternext[i][0]) == Board.CollisionType.Nothing:
                    # enemy can be jumped
                    
                    tmpNode = PathTreeNode(afternext[i], parent, self._board[next[i][0]][next[i][1]])
                    parent.add(tmpNode)
                    self.startBuildingRecursion(tmpNode, stone, True) # start recursion here to find all possible moves

                else: # enemy can not be jumped                    
                    continue
            else:
                # if an enemy was found, only this path can be followed!
                if not foundEnemy: parent.add(PathTreeNode(next[i], parent)) # none of the upper cases applied => normal move


    def checkIndexInRange(self, pos: tuple) -> bool:
        if pos[1] < 0 or pos[1] > BOARD_SIZE - 1: return False
        if pos[0] < 0 or pos[0] > BOARD_SIZE - 1: return False
        
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
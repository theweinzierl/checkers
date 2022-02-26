from .Stone import *
from tkinter import *
from enum import Enum
from .Move import *
from .PathTree import *
from .settings import *
from .Brain import *


class Board: 
    class Mode(Enum):
        BotGame = 1
        OneOnOne = 2

    def __init__(self, canvas: Canvas, mode: Mode, window: Tk) -> None:
        self._board = []
        self._playerA = []
        self._playerB = []
        self._canvas = canvas
        self._selectedStone = None
        self._turn = PLAYER_B
        self._mode = mode
        self._window = window

        self._score = {PLAYER_A: 0, PLAYER_B: 0} # Player A => Computer; Player B => Mensch
        self._brain = Brain(self)

    
    def start(self) -> None:
        self.iniBoard()
        self.draw()
        
        if self._mode == Board.Mode.BotGame:
            self._window.after(BOT_DELAY, lambda: self._brain.invokeAI(self._playerB))

    """
        Initialisiert das Spielbrett
        Dabei wird ein zweidimensionales Array mit den Steinen besetzt. Leere Felder haben den Wert None.
    """
    def iniBoard(self) -> None:
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

    """
        Erstellt eine zweidimensionale Liste
        Die Felder werden mit None belegt. Die Schachtelung ist wie folgt: [Reihe][Spalte] bzw. [Y-Wert][X-Wert]
    """
    def createEmptyList(self) -> list:
        tmpList = []
        posY = -1
        for i in range(0,64):
            if i%BOARD_SIZE == 0: 
                posY += 1
                tmpList.append([])

            tmpList[posY].append(None)

        return tmpList

    """
        Zeichnet das Spielbrett
        Draw zeichnet erstmalig das Spielbrett und alle Steine. Alle weiteren Aktualisierungen der Steine werden durch redrawStones() übernommen.
    """
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

    """
        Zeichnet die Steine neu
        Dabei wird ein zweidimensionales Array mit den Steinen besetzt. Leere Felder haben den Wert None.
    """
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
                
    """
        Zeichnet die die möglichen Sprünge ein.
    """
    def drawHelpers(self, moves: list):
        for i in range(0, len(moves)):
            posX = moves[i].pos[1]
            posY = moves[i].pos[0]

            curLeft = posX * RECT_SIZE
            curRight = posX * RECT_SIZE + RECT_SIZE
            curTop = posY * RECT_SIZE
            curBottom = posY * RECT_SIZE + RECT_SIZE

            self._canvas.create_oval(curLeft + CIRCLE_OFFSET, curTop + CIRCLE_OFFSET, curRight - CIRCLE_OFFSET, curBottom - CIRCLE_OFFSET, tags=["stone"])


    """
        onClick-Callback für das Canvas-Klickereignis
    """
    def onClick(self, event):

        if self._turn != PLAYER_B: return # not your turn!

        posX = int(event.x/RECT_SIZE)
        posY = int(event.y/RECT_SIZE)

        selectedTile = self._board[posY][posX]

        if not selectedTile is None and selectedTile.team == PLAYER_B: # selected tile is stone
            if not self._selectedStone is None: self._selectedStone.isSelected = False
            self._selectedStone = selectedTile
            self._selectedStone.isSelected = True
            
            self._selectedStone.pathTree = self._brain.buildPathTree(self._selectedStone)
            self.redrawStones()
         

        elif selectedTile is None and not self._selectedStone is None: # selected tile is not stone            
            self.executeMove(self._selectedStone.getMove((posY, posX)))


    """
        Führt einen Sprung aus.
    """
    def executeMove(self, move: Move) -> None:

        if move is None: return

        stone = move.stone

        self._score[stone.team] += len(move.jumpedStones)

        # übersprüngene Steine verstecken
        for jumpedStone in move.jumpedStones:
            jumpedStone.isVisible = False
            self._board[jumpedStone.posY][jumpedStone.posX] = None           

        self._board[move.pos[0]][move.pos[1]] = stone
        self._board[stone.posY][stone.posX] = None
        stone.posX = move.pos[1]
        stone.posY = move.pos[0]
        stone.origin = move.pos # Ausführung eines Zuges muss persistent sein!
        stone.isSelected = False
        self._selectedStone = None
        self.changeTurn()

    def changeTurn(self):
        self.redrawStones()
        if self._turn == PLAYER_A:
            self._turn = PLAYER_B
            if self._mode == Board.Mode.BotGame:
                self._window.after(BOT_DELAY, lambda: self._brain.invokeAI(self._playerB))
        else:
            self._turn = PLAYER_A
            self._window.after(BOT_DELAY, lambda: self._brain.invokeAI(self._playerA))



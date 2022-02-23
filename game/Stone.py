from enum import Enum
from .Move import *
from .PathTree import *
from .settings import *


class Stone:

    class Type(Enum):
        Normal = 1
        King = 2

    def __init__(self, posX: int, posY: int, team: int):
        self._posX = posX
        self._posY = posY
        self._team = team
        self._isSelected = False
        self._type = Stone.Type.Normal
        self._pathTree = None
        self._isVisible = True
        self._moves = []
        self._origin = (posY, posX)


    @property
    def posX(self) -> int:
        return self._posX

    @posX.setter
    def posX(self, val: int):
        self._posX = val

    @property
    def posY(self) -> int:
        return self._posY

    @posY.setter
    def posY(self, val: int):
        self._posY = val
        

    @property
    def team(self) -> int:
        return self._team

    @team.setter
    def team(self, val: int):
        self._team = val

    @property
    def origin(self) -> tuple:
        return self._origin

    @origin.setter
    def origin(self, val: tuple):
        self._origin = val
        if val[0] == 0 and self._team == PLAYER_B:
            self.makeKing()
        elif val[0] == BOARD_SIZE -1 and self._team == PLAYER_A:
            self.makeKing()

    @property
    def isSelected(self) -> bool:
        return self._isSelected

    @isSelected.setter
    def isSelected(self, val: bool):
        self._isSelected = val

    @property
    def type(self) -> int:
        return self._type

    @property
    def pos(self) -> tuple:
        return (self._posY, self._posX)

    @property
    def pathTree(self) -> PathTree:
        return self._pathTree

    @pathTree.setter
    def pathTree(self, val: PathTree):
        self._pathTree = val
        self._moves = self._pathTree.getMoves()
    
    @property
    def moves(self) -> list:
        return self._moves

    @property
    def isVisible(self) -> bool:
        return self._isVisible

    @isVisible.setter
    def isVisible(self, val: bool):
        self._isVisible = val

    def getMove(self, pos: tuple) -> Move:
        for move in self._moves:
            if move.pos == pos:
                return move
        return None

    def makeKing(self):
        self._type = Stone.Type.King

    def restoreOrigin(self):
        self._posX = self._origin[1]
        self._posY = self._origin[0]
        

    
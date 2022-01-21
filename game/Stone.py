from enum import Enum
from .Move import *


class Stone:

    def __init__(self, posX: int, posY: int, team: int):
        self._posX = posX
        self._posY = posY
        self._team = team
        self._isSelected = False
        self._type = Stone.Type.Normal
        self._cans = []
        self._havetos = []

    @property
    def cans(self) -> list:
        return self._cans

    @cans.setter
    def cans(self, val: list):
        self._cans = val

    @property
    def havetos(self) -> list:
        return self._havetos

    @havetos.setter
    def havetos(self, val: list):
        self._havetos = val

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
    def isSelected(self) -> bool:
        return self._isSelected

    @isSelected.setter
    def isSelected(self, val: bool):
        self._isSelected = val

    @property
    def type(self) -> int:
        return self._type

    @property
    def pos(self) -> tuple(int):
        return (self._posY, self._posX)
    
    def makeKing(self):
        self._type = Stone.Type.King


        

    class Type(Enum):
        Normal = 1
        King = 2
from enum import Enum
from .Stone import *
from .settings import *
 
class Move:
    
    def __init__(self, pos: tuple, stone, jumpedStones: list = None) -> None:
        self._pos = pos
        self._jumpedStones = []
        self._metric = 0
        self._stone = stone

    @property
    def stone(self):
        return self._stone

    @property
    def metric(self) -> int:
        return self._metric

    @metric.setter
    def metric(self, val: int):
        self._metric = val

    @property
    def pos(self) -> tuple:
        return self._pos

    @pos.setter
    def pos(self, val: tuple):
        self._pos = val

    @property
    def jumpedStones(self) -> list:
        return self._jumpedStones

    @jumpedStones.setter
    def jumpedStones(self, val: list):
        self._jumpedStones = val

    def evaluate(self) -> None:
        tmpMetric = 0
        
        # Anzahl der übersprungenen Steine
        noOfJumpedStones = len(self._jumpedStones)
        tmpMetric += noOfJumpedStones * 1000 

        # Sprung ins Zentrum?
        if self.isCenterJump:
            tmpMetric += 100
        
        if self.isKingJump:
            tmpMetric += 100

        self._metric = tmpMetric


    def isCenterJump(self) -> bool:
        if self._stone.posX > BOARD_SIZE / 2:
            if self._pos[1] < self._stone.posX:
                return True
        else:
            if self._pos[1] > self._stone.posX:
                return True

        return False

    def isKingJump(self) -> bool:
        if self._pos[0] == 0 or self._pos[0] == BOARD_SIZE:
            return True
        else:
            return False
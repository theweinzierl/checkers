from enum import Enum
from .Stone import *


class Move:
    
    def __init__(self, pos: tuple, jumpedStones: list = None, metric:int = 0) -> None:
        self._pos = pos
        self._jumpedStones = []
        self._metric = 0

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

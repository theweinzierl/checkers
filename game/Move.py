from enum import Enum

class Move:
    
    def __init__(self, start: tuple, end: tuple = None, jumpedStone = None) -> None:
        self._start = start
        self._end = end
        self._jumpedStone = jumpedStone

    @property
    def metric(self) -> int:
        return self._metric

    @metric.setter
    def metric(self, val: int):
        self._metric = val

    @property
    def end(self) -> tuple:
        return self._end

    @end.setter
    def end(self, val: tuple):
        self._end = val

    @property
    def jumpedStone(self) -> list:
        return self._jumpedStones

    @jumpedStone.setter
    def jumpedStone(self, val: list):
        self._jumpedStone = val

class Path:

    def __init__(self, type: int = 1) -> None:
        self._list = []
        self._type = type

    @property
    def list(self) -> list:
        return self._list

    @property
    def type(self) -> int:
        return self._type

    @type.setter
    def type(self, val: int):
        self._type = val
    
    class Type(Enum):
        Possible = 1
        Obligate = 2
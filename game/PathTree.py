from .Stone import *
from .Move import *

class PathTree:
    def __init__(self, pos: tuple, stone) -> None:
        self._root = PathTreeNode(pos)
        self._stone = stone
        
    @property
    def root(self):
        return self._root  

    def getMoves(self) -> list:
        leafes = self.getLeafes()
        moves = []
        for i in range(0, len(leafes)):
            tmpMove = Move(leafes[i].pos, self._stone)
            self.getMoveRec(tmpMove, leafes[i])
            moves.append(tmpMove)

        return moves
        


    def getMoveRec(self, move: Move, node) -> None:
        if not node.jumpedStone is None:
            move.jumpedStones.append(node.jumpedStone)
        
        if not node.parent is None:
            self.getMoveRec(move, node.parent)


    def getLeafes(self) -> list:
        tmpList = []
        self.getLeafesRec(tmpList, self._root)
        return tmpList

    def getLeafesRec(self, recList: list, node):
        if len(node.children) == 0:
            if node != self._root: recList.append(node)
        else:
            for i in range(0, len(node.children)):
                self.getLeafesRec(recList, node.children[i])



class PathTreeNode:

    def __init__(self, pos: tuple, parent = None, jumpedStone = None) -> None:
        self._pos = pos
        self._jumpedStone = jumpedStone
        self._children = []
        self._parent = parent
        
    def add(self, node) -> None:
        self._children.append(node)

    @property
    def pos(self) -> tuple:
        return self._pos

    @property
    def jumpedStone(self):
        return self._jumpedStone

    @property
    def children(self) -> list:
        return self._children

    @property
    def parent(self):
        return self._parent

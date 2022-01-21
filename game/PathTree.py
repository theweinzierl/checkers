from .Stone import *

class PathTree:
    def __init__(self, pos: tuple(int)) -> None:
        self._root = PathTreeNode(pos, self)
        
    @property
    def root(self) -> PathTreeNode:
        return self._root  


class PathTreeNode:

    def __init__(self, pos: tuple(int), parent: PathTreeNode, jumpedStone: Stone = None) -> None:
        self._pos = pos
        self._jumpedStone = jumpedStone
        self._children = []
        self._parent = parent
        
    def add(self, node) -> None:
        self._children.append(node)

    @property
    def pos(self) -> tuple(int):
        return self._pos

    @property
    def jumpedStone(self) -> Stone:
        return self._jumpedStone

    @property
    def children(self) -> list:
        return self._children

    @property
    def parent(self):
        return self._parent

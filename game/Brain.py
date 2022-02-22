from .Board import *
from .PathTree import *
from .Stone import *

from .settings import *
from game import settings

class Brain:

    def __init__(self, board) -> None:
        self._boardObj = board
        self._curTeam = None
        self._max = None

    class CollisionType(Enum):
        Nothing = 1
        Friend = 2
        Enemy = 3

    def getPlayerOrientation(self, player):
        if(player == PLAYER_A):
            return 1
        else:
            return -1 

    """
        1. Mögliche Züge prüfen und zugehörigen PathTree erstellen
        buildPathTree baut rekursiv einen möglichen Sprungpfad auf. Da bei Checkers
        mehfach Sprünge möglich sind, können die Pfade unterschiedlich lang sein.
        Es werden nur PathTrees zu möglichen Zügen erstellt, d.h. builPathTree() stellt
        auch fest, ob ein Stein bewegt werden kann oder nicht.
    """
    def buildPathTree(self, stone: Stone) -> PathTree:
        tmpPathTree = PathTree(stone.pos, stone)
        self.buildPathTreeRec(tmpPathTree.root, stone)
        return tmpPathTree


    def buildPathTreeRec(self, parent: PathTreeNode, stone: Stone, foundEnemy: bool = False) -> None:

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
            
            if col == self.CollisionType.Friend: # position blocked by own stone
                continue
            elif col == self.CollisionType.Enemy: # position blocked by enemy => jumpable?

                if self.checkIndexInRange(afternext[i]) and self.checkCollision(stone, afternext[i][1], afternext[i][0]) == Brain.CollisionType.Nothing:
                    # enemy can be jumped
                    
                    tmpNode = PathTreeNode(afternext[i], parent, self._boardObj._board[next[i][0]][next[i][1]])
                    parent.add(tmpNode)
                    self.buildPathTreeRec(tmpNode, stone, True) # start recursion here to find all possible moves

                else: # enemy can not be jumped                    
                    continue
            else:
                # if an enemy was found, only this path can be followed!
                if not foundEnemy: parent.add(PathTreeNode(next[i], parent)) # none of the upper cases applied => normal move


    def checkIndexInRange(self, pos: tuple) -> bool:
        if pos[1] < 0 or pos[1] > BOARD_SIZE - 1: return False
        if pos[0] < 0 or pos[0] > BOARD_SIZE - 1: return False
        
        return True

    
    def checkCollision(self, stone: Stone, posX: int, posY: int) -> int:
    
        if not self._boardObj._board[posY][posX] is None:
            if self._boardObj._board[posY][posX].team == stone.team:
                return Brain.CollisionType.Friend
            else:
                return Brain.CollisionType.Enemy
        else:
            return Brain.CollisionType.Nothing

    def invokeAI(self):
        self._max = None
        self.max(None, self._boardObj._playerA, 1)
        self._boardObj.executeMove(self._max)
        self._boardObj.changeTurn()

    """
        Gibt alle spielbaren Steine eines Spielers zurück
    """
    def getPossibleMoves(self, stones: list) -> list:
        moveable = []
        for stone in stones:
            if not stone.isVisible: continue

            stone.pathTree = self.buildPathTree(stone)
            for move in stone.moves:
                moveable.append(move)

        return moveable

    def max(self, parentMove: Move, stones: list, depth: int) -> Move:
        
        moveables = self.getPossibleMoves(stones)

        if len(moveables) == 0 or depth == 0:
            return parentMove 
        
        maxMove = None
        for move in moveables:
            self.simExecuteMove(move)
            minMove = self.min(move, self.changeTurn(stones), depth - 1)            
            self.undoSimExecuteMove(move)
            if (maxMove is None or maxMove.metric < minMove.metric) and parentMove is None:
                self._max = maxMove
        moveables.sort(key=lambda x: x.metric)
        return moveables[0]
    
    def min(self, parentMove: Move, stones: list, depth: int) -> Move:
        
        moveables = self.getPossibleMoves(stones)

        if len(moveables) == 0 or depth == 0:
            return parentMove 
        
        for move in moveables:
            self.simExecuteMove(move)
            self.max(move, self.changeTurn(stones), depth - 1)            
            self.undoSimExecuteMove(move)

        moveables.sort(key=lambda x: x.metric, reverse=True)
        return moveables[0]


    def simExecuteMove(self, move: Move):
        
        if not move is None:    
            for jumpedStone in move.jumpedStones:
                jumpedStone.isVisible = False
                self._boardObj._board[jumpedStone.posY][jumpedStone.posX] = None

            self._boardObj._board[move.pos[0]][move.pos[1]] = move.stone
            self._boardObj._board[move.stone.posY][move.stone.posX] = None
            move.stone.posX = move.pos[1]
            move.stone.posY = move.pos[0]


    def undoSimExecuteMove(self, move: Move):

        if not move is None:    
            for jumpedStone in move.jumpedStones:
                jumpedStone.isVisible = True
                self._boardObj._board[jumpedStone.posY][jumpedStone.posX] = jumpedStone

            self._boardObj._board[move.pos[0]][move.pos[1]] = None
            self._boardObj._board[move.stone.posY][move.stone.posX] = move.stone
            move.stone.restoreOrigin()

    def changeTurn(self, player: list) -> list:
        if player == self._boardObj._playerA:
            return self._boardObj._playerB
        else:
            return self._boardObj._playerA
from .Board import *
from .PathTree import *
from .Stone import *
from .Move import *
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


    def buildPathTreeRec(self, parent: PathTreeNode, stone: Stone, foundEnemy: bool = False, depth: int = 5) -> None:

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
                    if depth == 0: continue

                    if not parent.jumpedStone is None and self._boardObj._board[next[i][0]][next[i][1]] != parent.jumpedStone:
                        # verhindern, dass übersprungener Stein von einem König wieder zurück übersprungen werden kann und es zu einer Endlosschleife kommt!
                        continue

                    tmpNode = PathTreeNode(afternext[i], parent, self._boardObj._board[next[i][0]][next[i][1]])
                    parent.add(tmpNode)
                    self.buildPathTreeRec(tmpNode, stone, True, depth - 1) # start recursion here to find all possible moves

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

    def invokeAI(self, player):
        self._max = None

        self.max(None, player, self._boardObj._board, MINIMAX_DEPTH)
        self._boardObj.executeMove(self._max)


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
        

    def max(self, parentMove: Move, stones: list, board, depth: int) -> Move:
        
        moveables = self.getPossibleMoves(stones)

        # Schlagzwang checken!
        if parentMove is None:
            obligateMove = None
            for move in moveables:
                if move.metric > 1000: # Schlagzwang!
                    if (obligateMove is None or obligateMove.metric < move.metric):
                        obligateMove = move
            if not obligateMove is None:
                self._max = obligateMove
                return 

        if len(moveables) == 0 or depth == 0:
            return parentMove 
        
        maxMove = None
        for move in moveables:
            self.simExecuteMove(move, board)
            minMove = self.min(move, self.changeTurn(stones), board, depth - 1)            
            self.undoSimExecuteMove(move, board)
            if (maxMove is None or maxMove.metric < minMove.metric) and parentMove is None:
                maxMove = minMove
                self._max = move
        
        moveables.sort(key=lambda x: x.metric)
        return moveables[0]
    
    def min(self, parentMove: Move, stones: list, board, depth: int) -> Move:
        
        moveables = self.getPossibleMoves(stones)

        if len(moveables) == 0 or depth == 0:
            return parentMove 
        
        for move in moveables:
            self.simExecuteMove(move, board)
            self.max(move, self.changeTurn(stones), board, depth - 1)            
            self.undoSimExecuteMove(move, board)

        moveables.sort(key=lambda x: x.metric, reverse=True)
        return moveables[0]


    def simExecuteMove(self, move: Move, board):        
         
        for jumpedStone in move.jumpedStones:
            jumpedStone.isVisible = False
            board[jumpedStone.posY][jumpedStone.posX] = None

        board[move.pos[0]][move.pos[1]] = move.stone
        board[move.stone.posY][move.stone.posX] = None
        move.stone.posX = move.pos[1]
        move.stone.posY = move.pos[0]


    def undoSimExecuteMove(self, move: Move, board):
         
        for jumpedStone in move.jumpedStones:
            jumpedStone.isVisible = True
            board[jumpedStone.posY][jumpedStone.posX] = jumpedStone

        board[move.pos[0]][move.pos[1]] = None
        move.stone.restoreOrigin()
        board[move.stone.posY][move.stone.posX] = move.stone
        

    def changeTurn(self, player: list) -> list:
        if player == self._boardObj._playerA:
            return self._boardObj._playerB
        else:
            return self._boardObj._playerA
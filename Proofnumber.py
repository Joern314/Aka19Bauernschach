from GameState import GameState
from Move import Move

infty = 100000000 #10^8
lazyness = 5./4.

class Knoten:
    def __init__(self, game_state: GameState, is_white, move = None):
        self.game_state = game_state
        self.is_white = is_white
        self.pn = 1
        self.dn = 1
        self.children = []
        self.move = move
        
    def reveal(self):
        imm = self.game_state.game_is_finished()
        if imm is not None:
            imm *= (+1 if self.is_white else -1)
            if imm == 0:
                imm = +1 #forcing a draw is as good as winning
            
            if imm == +1:
                self.pn = 0
                self.dn = infty
                return True
            else:
                self.pn = infty
                self.dn = 0
                return True
        
        legal_moves = self.game_state.list_all_legal_moves_wb(self.is_white)
        self.children = [Knoten( self.game_state.clone().applyMove_wb(self.is_white,m) , not self.is_white , m) for m in legal_moves]
        
        self.pn = 1
        self.dn = len(self.children)
        return False

    def df_pn(self, pnLimit, dnLimit):
        if len(self.children) == 0:
            self.reveal()
            
        while self.pn <= pnLimit and self.dn <= dnLimit:
            self.children.sort(key = lambda k: k.dn)
            # smallest = self.children[0]
            if len(self.children) >= 2:
                dn2 = self.children[1].dn
            else:
                dn2 = infty
            
            child = self.children[0]
            pn1 = child.dn
        
            child.df_pn(dnLimit - self.dn + pn1,
                        min(pnLimit, lazyness * dn2))
        
            self.pn = min(dn2, child.dn)
            self.dn = self.dn - pn1 + child.pn
        
        return
        
class ProofnumberSearch:
    def __init__(self):
        pass
    
    def find_best_move(self, board, is_white):
        root = Knoten(board, is_white)
        root.df_pn(infty-1, infty-1)
        
        if root.pn == 0: #loss
            return board.list_all_legal_moves_wb(is_white)[0] #bad but whatever
        else: # win
            root.children.sort(key = lambda k: k.dn)
            winning = root.children[0]
            return winning.move

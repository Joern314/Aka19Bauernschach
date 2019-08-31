from GameState import GameState
import threading
import concurrent.futures

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
        
    def reveal(self, proofsearch):
        imm = self.game_state.game_is_finished()
        if imm is not None:
            if imm == 0:
                imm = proofsearch.global_draw #+1 = win for white
            imm *= (+1 if self.is_white else -1)
            
            if imm == +1:
                self.pn = 0
                self.dn = infty
                return True
            else:
                self.pn = infty
                self.dn = 0
                return True
        
        legal_moves = self.game_state.list_all_legal_moves_wb(self.is_white)
        self.children = [Knoten( self.descend(m), not self.is_white , m) for m in legal_moves]
        
        self.pn = 1
        self.dn = len(self.children)
        return False
    
    def descend(self, move):
        c = self.game_state.clone()
        c.applyMove_wb(self.is_white,move)
        return c

    def df_pn(self, pnLimit, dnLimit, proofsearch):
        if len(self.children) == 0:
            self.reveal(proofsearch)
            
        while self.pn <= pnLimit and self.dn <= dnLimit:
            self.children.sort(key = lambda k: k.dn)
            # smallest = self.children[0]
            if len(self.children) >= 2:
                dn2 = self.children[1].dn
            else:
                dn2 = infty
            
            child = self.children[0]
            pn1 = child.pn
        
            child.df_pn(dnLimit - self.dn + pn1,
                        min(pnLimit, lazyness * dn2),
                        proofsearch)
        
            self.pn = min(dn2, child.dn)
            self.dn = self.dn - pn1 + child.pn
            
            self.pn = min(infty, self.pn)
            self.dn = min(infty, self.dn)
        
        return

        
class ProofnumberSearch:
    def __init__(self, board, is_white, global_draw, stop_event):
        self.board = board
        self.is_white = is_white
        self.global_draw = global_draw
        self.stop_event = stop_event
        
        self.final_won  = None
        self.final_move = None
        
    def find_best_move(self):
        root = Knoten(self.board, self.is_white)
        root.df_pn(infty-1, infty-1, self)
        
        if root.dn == 0: #loose
            return False, self.board.list_all_legal_moves_wb(self.is_white)[0] #bad but whatever
        else: # win
            root.children.sort(key = lambda k: k.dn) # find one with dn=0
            winning = root.children[0]
            return True, winning.move

    def execute(self):
        self.final_won, self.final_move = self.find_best_move()
        self.stop_event.set()
        return
        
    @staticmethod
    def find_best_move_with_globaldraw(board, is_white, global_draw):
        ps = ProofnumberSearch(global_draw)
        return ps.find_best_move(board, is_white)
        
    @staticmethod
    def find_best_move_with_draw(board, is_white):
        ev = threading.Event()
        
        pw = ProofnumberSearch(board, is_white, +1 if is_white else -1, ev)
        pb = ProofnumberSearch(board, is_white, -1 if is_white else +1, ev)
        
        tw = threading.Thread(target = ProofnumberSearch.execute, args = [pw])
        tb = threading.Thread(target = ProofnumberSearch.execute, args = [pb])
        
        tw.start()
        tb.start()
        
        tw.join()
        tb.join()
        
        if pw.final_won == pb.final_won:
#            print("agree " + str(+1 if pw.final_won else -1))
            return +1 if pw.final_won else -1, pw.final_move
        else:
            return 0, pw.final_move
        
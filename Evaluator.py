from Bewertung import *

class Evaluator:    
    def __init__(self, estimator = "unentschieden", max_depth = 100):
        self.max_depth = max_depth
        self.estimator = estimator
        self.estimate = estimate_functions[self.estimator]
        
        

    def evaluate(self, knoten, alpha, beta, depth, is_white):        
        immediate = knoten.game_is_finished()
        
        if immediate != None:
            if immediate == +1:
                return (+1 if is_white else -1), None
            elif immediate == -1:
                return (-1 if is_white else +1), None
            elif immediate == 0:
                return 0, None
            
        if depth >= self.max_depth:
            return self.estimate(knoten, is_white), None
            
        # Annahme: beta > alpha
        # liefert Bewertung + besten Zug
        # bricht ab wenn bewertung <= alpha oder >=beta

        if is_white:
            legalMoves = knoten.list_all_legal_moves() # liste aller kanten zu kindern
        else:
            legalMoves = knoten.list_all_legal_moves_b()
                        
        m = -alpha # schlechteste Stellung für den Gegner hat Wert m
        bestmove = legalMoves[0]
        
        for move in legalMoves:
            child = knoten.clone()

            if is_white:
                child.applyMove(move)
            else:
                child.applyMove_b(move)
                
            e, _ = self.evaluate(child, -beta, m, depth+1, not is_white)  # <= m, >=-beta
            if e < m: # neue schlechteste Stellung für Gegner
                bestmove = move
                m = e
                
            if m <= -beta:
                break
        return -m, bestmove
    
    def bauerndifferenz(self, knoten, alpha, beta):
        print("nondet")
        return 0, None
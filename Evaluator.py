from random import random

class Evaluator:
    evaluator_functions = {}
    def __init__(self, evaluator = "default"):
        self.max_depth = 100
        self.evaluator = evaluator
        Evaluator.evaluator_functions = {"default": self.default_evaluate,
                            "bauerndifferenz": self.bauerndifferenz}
        

    def evaluate(self, knoten, alpha, beta, is_white):
        return self.evaluator_functions[self.evaluator](knoten,alpha,beta, 0, is_white)

    def default_evaluate(self, knoten, alpha, beta, depth, is_white):        
        immediate = knoten.game_is_finished()
        
        if immediate != None:
            if immediate == +1:
                return (+1 if is_white else -1), None
            elif immediate == -1:
                return (-1 if is_white else +1), None
            elif immediate == 0:
                return 0, None
            
        if depth >= self.max_depth:
            return self.bauerndifferenz(knoten, alpha, beta)
        
        # Annahme: beta > alpha
        # liefert Bewertung + besten Zug
        # bricht ab wenn bewertung <= alpha oder >=beta

        if is_white:
            legalMoves = knoten.list_all_legal_moves() # liste aller kanten zu kindern
        else:
            legalMoves = knoten.list_all_legal_moves_b()
            
        m = -alpha # schlechteste Stellung für den Gegner hat Wert m
        bestmove = None
        
        for move in legalMoves:
            child = knoten.clone()

            if is_white:
                child.applyMove(move)
            else:
                child.applyMove_b(move)
                
            e, _ = self.default_evaluate(child, -beta, m, depth+1, not is_white)  # <= m, >=-beta
            if e < m: # neue schlechteste Stellung für Gegner
                bestmove = move
                m = e
                
            if m <= -beta:
                break
        return -m, bestmove
    
    def bauerndifferenz(self, knoten, alpha, beta):
        print("nondet")
        return 0, None
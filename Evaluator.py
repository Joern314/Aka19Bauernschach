from random import random

class Evaluator:
    def __init__(self):
        self.max_depth = 10
        pass

    def evaluate(self, knoten, alpha, beta):
        return self.evaluate_D(knoten,alpha,beta, 0)

    def evaluate_D(self, knoten, alpha, beta, depth):
        immediate = knoten.game_is_finished()
        
        if immediate != None:
            if immediate == +1:
                return +1, None
            elif immediate == -1:
                return -1, None
            elif immediate == 0:
                return 0, None
            
        if depth == self.max_depth:
            return self.heuristik(knoten, alpha, beta)
        
        # Annahme: beta > alpha
        # liefert Bewertung + besten Zug
        # bricht ab wenn bewertung <= alpha oder >=beta

        legalMoves = knoten.list_all_legal_moves() # liste aller kanten zu kindern
        m = -alpha # schlechteste Stellung für den Gegner hat Wert m
        bestmove = None
        for move in legalMoves:
            child = knoten.clone()
            child.applyMove(move)
            child.rotateBoard()
            e, _ = self.evaluate_D(child, -beta, m, depth+1)  # <= m, >=-beta
            if e < m: # neue schlechteste Stellung für Gegner
                bestmove = move
                m = e
                
            if m <= -beta:
                break
        return -m, bestmove
    
    def heuristik(self, knoten, alpha, beta):
        return (len(knoten.posWhite)-len(knoten.posBlack)+random())/1.0/(knoten.size[1]), None
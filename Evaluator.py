class Evaluator:
    def __init__(self):
        pass

    def evaluate(self, knoten, alpha, beta):
        immediate = knoten.game_is_finished()
        
        if immediate != None:
            if immediate == +1:
                return +1
            elif immediate == -1:
                return -1
            elif immediate == 0:
                return 0
            
        
        # Annahme: beta > alpha
        # liefert Bewertung + besten Zug
        # bricht ab wenn bewertung <= alpha oder >=beta

        legalMoves = knoten.list_all_legal_moves() # liste aller kanten zu kindern
        m = -alpha # schlechteste Stellung für den Gegner hat Wert m
        bestmove = None
        for move in legalMoves:
            child = knoten.clone()
            # TODO get result and break if already winning
            child.applyMove(move)
            e, _ = self.evaluate(child, -beta, m)  # <= m, >=-beta
            if m > e: # neue schlechteste Stellung für Gegner
                bestmove = move
                m = e
                
            if m <= -beta:
                break
        return -m, bestmove
    
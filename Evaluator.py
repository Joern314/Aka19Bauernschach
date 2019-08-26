class Evaluator:
    def __init__(self):
        pass
    
    def evaluate(self, knoten, alpha, beta):
        # Annahme: beta > alpha
        # liefert Bewertung + besten Zug
        # bricht ab wenn bewertung <= alpha oder >=beta

        legalMoves = knoten.listAllLegalMoves() #liste aller kanten zu kindern
        m = -alpha #schlechteste Stellung für den Gegner hat Wert m
        bestmove = None
        for move in legalMoves:
            child = knoten.clone()
            child.applyMove(move)
            e, _ = self.evaluate(child, -beta, m)  # <= m, >=-beta
            if m < e: # neue schlechteste Stellung für Gegner
                bestmove = move
                m = e
                
            if m <= -beta:
                break
        return -m, bestmove
    
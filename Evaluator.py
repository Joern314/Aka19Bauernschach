
class Evaluator(Object):
    def __init__(self):
        pass
    
    def evaluate(self, knoten, alpha, beta):
        # liefert Bewertung, optimalen Move
        # bricht ab wenn bewertung <= alpha oder >=beta

        legalMoves = knoten.listLegalMoves() #liste aller kanten zu kindern
        m = -alpha #
        bestmove = None
        for move in legalMoves:
            child = knoten.copy()
            child.applyMove(move)
            e,_ = self.evaluate(child, -beta, m)
            if e < m:
                m = e
                bestmove = move
            if m <= -beta:
                break
        return -m, bestmove
    
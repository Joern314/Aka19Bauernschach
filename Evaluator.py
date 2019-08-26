
class Evaluator(Object):
    def __init__(self):
        pass
    
    def evaluate(knoten, alpha, beta):
        """liefert Bewertung, optimalen Move"""
        legalMoves = knoten.listLegalMoves()
        m = -alpha
        bestmove = None
        for move in legalMoves:
            child = knoten.copy()
            child.applyMove(move)
            e,_ = evaluate(child, -beta, m)
            if e < m:
                m = e
                bestmove = move
            if m <= -beta:
                break
        return -m, bestmove
    
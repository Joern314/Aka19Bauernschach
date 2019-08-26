class Evaluator:
    def __init__(self):
        pass
    
    def evaluate(self, knoten, alpha, beta):
        # liefert Bewertung
        # bricht ab wenn bewertung <= alpha oder >=beta

        legalMoves = knoten.listLegalMoves() #liste aller kanten zu kindern
        m = -alpha  #unsere beste Wahl. Schlechter als alpha ist uninteressant
        for move in legalMoves:
            child = knoten.copy()
            child.applyMove(move)
            e = self.evaluate(child, -beta, m)  #bessere züge als m sind nicht interessant weil Gegner zieht
            m = min(m,e)
            if m <= -beta:
                break
        return -m
    
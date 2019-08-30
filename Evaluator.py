import Bewertung
import time
import random
import bisect

class Hasher:
    def __init__(self):
        self.table = {}

    def key(self, knoten, is_white):
        if is_white:
            return (knoten.white << 64) | (knoten.black)
        else:
            return (knoten.black << 64) | (knoten.white)
        
    def get(self, knoten, is_white):
        return self.table.get(self.key(knoten, is_white))
        
    def insert(self, knoten, is_white, val):
        self.table[self.key(knoten, is_white)] = val
        

class Evaluator:    
    def __init__(self, estimator = "unentschieden", max_costs = 100):
        self.max_costs = max_costs
        self.estimator = estimator
        self.estimate = Bewertung.estimate_functions[self.estimator]
        self.hasher = Hasher()
        self.oldhasher = Hasher()
        self.aborted = False
        self.max_depth = 0
        
    def begin_evaluate(self, knoten, costs, is_white):
        hardend = time.time() + costs - 0.1

        self.max_depth = 5
        lastres = 0
        lastmov = None
        while True:
            self.oldhasher , self.hasher = self.hasher , Hasher()
            
            res,mov = self.evaluate(knoten, -100, +100, hardend, 0, is_white)
            
            if self.aborted: #we're out of time! discard that result
                return lastres, lastmov
            
            lastres = res
            lastmov = mov
            
            self.max_depth += 4 #let's try again with higher depth
        
    def evaluate(self, knoten, alpha, beta, hardend, depth, is_white):
        res,mov = self.evaluate_inner(knoten, alpha, beta, hardend, depth, is_white)
        
        self.hasher.insert(knoten, is_white, res)        
        
        return res, mov
            
    def evaluate_inner(self, knoten, alpha, beta, hardend, depth, is_white):        
        if self.aborted:
            return 0,None
        
        immediate = knoten.game_is_finished()
        
        if immediate != None:
            if immediate == +1:
                return (+1 if is_white else -1), None
            elif immediate == -1:
                return (-1 if is_white else +1), None
            elif immediate == 0:
                return 0, None

        if depth >= self.max_depth:
            #end early and give estimate only
            return self.estimate(knoten, is_white), None

        if time.time() > hardend:
            self.aborted = True
            return 0, None
                    
        # Annahme: beta > alpha
        # liefert Bewertung + besten Zug
        # bricht ab wenn bewertung <= alpha oder >=beta

        if is_white:
            legalMoves = knoten.list_all_legal_moves() # liste aller kanten zu kindern
        else:
            legalMoves = knoten.list_all_legal_moves_b()
                        
        m = -alpha # schlechteste Stellung für den Gegner hat Wert m
        bestmove = None
        
        sort_moves = []
        
        for move in legalMoves:
            child = knoten.clone()

            if is_white:
                child.applyMove(move)
            else:
                child.applyMove_b(move)
                
            estimate = self.oldhasher.get(child, not is_white)
            if estimate != None:
                bew = estimate
            else:
                bew = 0.0
            sort_moves.append((bew,move))
        
        sort_moves.sort(key = lambda t: t[0])
        
        for tup in sort_moves:
            move = tup[1]
            e, _ = self.evaluate(child, -beta, m, hardend, depth+1, not is_white)  # <= m, >=-beta
            if e < m: # neue schlechteste Stellung für Gegner
                bestmove = move
                m = e
                
            if m <= -beta:
                break
        return -m, bestmove
    
    def bauerndifferenz(self, knoten, alpha, beta):
        print("nondet")
        return 0, None
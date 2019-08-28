from Move import *


class GameState:

    def __init__(self, size_x, size_y):
        self.size = (size_x, size_y)
        self.posWhite = []
        self.posBlack = []
        self.lastpassed = False
        self.thispassed = False

    def populate_bauern(self):  # Argument positions?
        for i in range(self.size[0]):
            # zwei Reihen Bauern
            self.posWhite.append((i, 0))
            self.posBlack.append((i, self.size[1]-1))

    def getSize(self):
        return self.size

    def list_all_legal_moves(self):
        retVal = []
        for bauer in self.posWhite:
            for richtung in [-1,0,+1]:
                move = Move(bauer, richtung)
                if self.checkIfLegal(move):
                    retVal.append(move)
                    
        if len(retVal) == 0:
            move = Move(None,None, True) # Pass
            retVal.append(move)

        return retVal

    def rotateBoard(self):
        black = []
        white = []
        for figur in self.posWhite:
            black.append((figur[0],self.size[1] - 1 - figur[1]))
        for figur in self.posBlack:
            white.append((figur[0], self.size[1] -1 - figur[1]))
        self.posWhite=white
        self.posBlack=black


    def clone(self):
        x, y = self.size
        g = GameState(x, y)
        g.posWhite = self.posWhite.copy()
        g.posBlack = self.posBlack.copy()
        g.lastpassed = self.lastpassed
        g.thispassed = self.thispassed
        return g

    # TODO sanity checking?
    def applyMove(self, move : Move):
        
        self.lastpassed = self.thispassed
        self.thispassed = False
        
        if move.is_passing():
            self.thispassed = True
            return

        # delete the bauer from the pos* array
        # and add it again with the new position

        self.posWhite.remove(move.get_figur())

        # branch for straight (0) or hit (-1, +1)
        if move.get_richtung() == 0:
            self.posWhite.append((move.get_figur()[0], move.get_figur()[1]+1))

        elif move.get_richtung() == +1:
            self.posWhite.append((move.get_figur()[0]+1, move.get_figur()[1]+1))
            self.posBlack.remove((move.get_figur()[0]+1, move.get_figur()[1]+1))

        elif move.get_richtung() == -1:
            self.posWhite.append((move.get_figur()[0]-1, move.get_figur()[1]+1))
            self.posBlack.remove((move.get_figur()[0]-1, move.get_figur()[1]+1))


    def checkIfLegal(self, move: Move):        
        x, y = move.figur
        if move.is_passing():
            return True # assumes pass is only considered if no other moves were allowed
        elif not (x,y) in self.posWhite:
            return False #not a white pawn
        # gerade ziehen
        elif move.richtung == 0:
            return (x,y+1) not in (self.posWhite + self.posBlack) #if y+1 was oob then the game would already have ended
        # "+1" schlagen (nach rechts schlagen)
        elif move.richtung == +1:
            if x+1 >= self.size[0]: # oob, again y+1 can be assumed in bounds
                return False 
            
            if (x+1,y+1) in self.posWhite: # can't take white
                return False
            
            return (x+1,y+1) in self.posBlack # need take black
        # "-1" schlagen (nach links schlagen)
        elif move.richtung == -1:
            if x-1 < 0: #oob
                return False
            
            if (x-1,y+1) in self.posWhite:
                return False
            
            return (x-1,y+1) in self.posBlack
        else:
            return False # illegal direction?


    def game_is_finished(self): #+1=win 0=draw -1=loss None=not finished
        # one figure has traversed the board to the opponent’s side
        for figure in self.posWhite:
            if figure[1] == self.size[1]-1:
                return +1

        for figure in self.posBlack:
            if figure[1] == 0:
                return -1

        # no legal moves
        if self.lastpassed and self.thispassed:
            return 0
        return None

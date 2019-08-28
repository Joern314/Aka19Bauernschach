import Move


class GameState:

    def __init__(self, size_x, size_y):
        self.size = (size_x, size_y)
        self.weissAmZug = True
        self.posWhite = []
        self.posBlack = []
        self.populate_bauern()

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
            move = Move((0,0),0, True) #Pass
            retVal.append(move)

        return retVal

    # TODO
    def rotateBoard():
        pass

    def clone(self):
        x, y = self.size
        g = GameState(x, y)
        g.weissAmZug = self.weissAmZug
        g.posWhite = self.posWhite
        g.posBlack = self.posBlack

    # TODO sanity checking?
    def applyMove(self, move : Move):
        if move.is_passing():
            return

        # delete the bauer from the pos* array
        # and add it again with the new position

        posWhite.remove(move.get_figur())

        # branch for straight (0) or hit (-1, +1)
        if move.get_richtung() == 0:
            posWhite.append((move.get_figur()[0], move.get_figur()[1]+1))

        elif move.get_richtung() == +1:
            posWhite.append((move.get_figur()[0]+1, move.get_figur()[1]+1))

        elif move.get_richtung() == -1:
            posWhite.append((move.get_figur()[0]-1, move.get_figur()[1]+1))


    # TODO
    def checkIfLegal(self, move: Move):
        x, y = move.figur
        if move.is_passing():
            return True #assumes pass is only considered if no other moves were allowed
        # gerade ziehen
        elif move.richtung == 0:
            return (x,y+1) not in [self.posWhite + self.posBlack] #if y+1 was oob then the game would already have ended
        # "+1" schlagen (nach rechts schlagen)
        elif move.richtung == +1:
            if x+1 >= self.size[0]: #oob, again y+1 can be assumed in bounds
                return False 
            
            if (x+1,y+1) in self.posWhite: #can't take white
                return False
            
            return (x+1,y+1) in self.posBlack #need take black
        # "-1" schlagen (nach links schlagen)
        elif move.richtung == -1:
        try:
            if x-1 < 0: #oob
                return False
            
            if (x-1,y+1) in self.posWhite:
                return False
            
            return (x-1,y+1) in self.posBlack
        else:
            return False #illegal direction?

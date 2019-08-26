import Move

class GameState:
    size  # (x, y)
    posWhite # array
    posBlack # array
    weissAmZug # bool # brauchen wir das?
    #geschlagen (?)

    def __init__(size_x, size_y):
        self.size = (size_x, size_y)
        self.weissAmZug = True
        populateBauern()


    def populateBauern(self): # Argument positions?

        for i in range(self.size[0]):
            # zwei Reihen Bauern
            self.posWhite.append((i, 0))
            self.posBlack.append((i, self.size[1]-1))


    def getSize(self):
        return self.size


    def listAllLegitMoves(self):
        retVal = []
        for bauer in self.posWhite:
            # gerade ziehen
            try:
                [self.posWhite + self.posBlack].index((x,y+1))
            except ValueError:
                if bauer[1] + 1 < self.size[1]:
                    retVal.append((bauer[0],bauer[1],0))

            # "+1" schlagen (nach rechts schlagen)
            try:
                [self.posWhite + self.posBlack].index((x+1,y+1))
            except ValueError:
                if bauer[1] + 1 < self.size[1] \
                  and bauer[0] + 1 < self.size[0]:
                    retVal.append((bauer[0],bauer[1],+1))


            # "-1" schlagen (nach links schlagen)
            try:
                [self.posWhite + self.posBlack].index((x-1,y+1))
            except ValueError:
                if bauer[1] + 1 < self.size[1] \
                  and bauer[0] - 1 < self.size[0]:
                    retVal.append((bauer[0],bauer[1],-1))

        return retVal


    # TODO
    def rotateBoard():
        pass


    # TODO sanity checking?
    def applyMove(self, move : Move):
        if move.is_passing():
            return

        # delete the bauer from the pos* array
        # and add it again with the new position

        posWhate.remove(move.get_figur())

        # branch for straight (0) or hit (-1, +1)
        if move.get_richtung() == 0:
            posWhate.append((move.get_figur()[0], move.get_figur()[1]+1))

        elif move.get_richtung() == +1:
            posWhate.append((move.get_figur()[0]+1, move.get_figur()[1]+1))

        elif move.get_richtung() == -1:
            posWhate.append((move.get_figur()[0]-1, move.get_figur()[1]+1))


    # TODO
    def copy(self):
        pass


    # TODO
    def checkIfLegal(self, move : Move):
        pass

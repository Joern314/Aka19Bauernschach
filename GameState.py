from Move import Move
#from numpy import ,uint8
#from Bitreverse import reverse_bits

# GAMESTATE

class GameState:
    # MATH FUNCTIONS
    def move_up(self, pawn):
        npawn = pawn << (1)
        self.white = (self.white & ~pawn) | npawn
    def move_up_b(self, pawn):
        npawn = pawn >> (1)
        self.black = (self.black & ~pawn) | npawn
    
    def move_left(self, pawn):
        npawn = pawn >> (8 - 1)
        self.white = (self.white & ~pawn) | npawn
        self.black = (self.black & ~npawn)
    def move_left_b(self, pawn):
        npawn = pawn >> (8 + 1)
        self.black = (self.black & ~pawn) | npawn
        self.white = (self.white & ~npawn)

    def move_right(self, pawn):
        npawn = pawn << (8 + 1)
        self.white = (self.white & ~pawn) | npawn
        self.black = (self.black & ~npawn)
    def move_right_b(self, pawn):
        npawn = pawn << (8 - 1)
        self.black = (self.black & ~pawn) | npawn
        self.white = (self.white & ~npawn)

    def __init__(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y

        self.white = (0)
        self.black = (0)

        self.lastpassed = 0
        
        self.blackmask = (0x0101010101010101)
        self.whitemask = self.blackmask << (size_y-1)

    def populate_bauern(self):  # Argument positions?
        for i in range(self.size_x):
            # zwei Reihen Bauern
            self.white      |= (1 << (i*8 + 0))
            self.black      |= (1 << (i*8 + self.size_y-1))

    def extract_all_moves(self, retVal, turnmask, direction):
        while turnmask:
            pawn = turnmask & (-turnmask)
            turnmask = turnmask & (turnmask-(1))
            retVal.append(Move(pawn, direction))

    def list_all_legal_moves(self):
        retVal = []
        self.extract_all_moves(retVal, self.white & (self.black << (8 - 1)), -1)
        self.extract_all_moves(retVal, self.white & (self.black >> (8 + 1)), 1)
        self.extract_all_moves(retVal, self.white & ~((self.black >> (1)) | (self.white >> (1))),    0)
        if len(retVal) == 0:
            retVal.append(Move(0,0)) #pass
        return retVal

    def list_all_legal_moves_b(self):
        retVal = []
        self.extract_all_moves(retVal, self.black & (self.white << (8 + 1)), -1)
        self.extract_all_moves(retVal, self.black & (self.white >> (8 - 1)), 1)
        self.extract_all_moves(retVal, self.black & ~((self.white << (1)) | (self.black << (1))),    0)
        if len(retVal) == 0:
            retVal.append(Move(0,0)) #pass
        return retVal

#    def rotateBoard(self):
 #       self.white, self.black = reverse_bits(self.black), reverse_bits(self.white)
  #      self.lossmask, self.winmask = reverse_bits(self.winmask), reverse_bits(self.lossmask)


    def clone(self):
        g = GameState(self.size_x, self.size_y)
        g.white = self.white
        g.black = self.black
        g.lastpassed = self.lastpassed
        return g

    def applyMove(self, move : Move):
        self.lastpassed >>= 1
        
        if move.is_passing():
            self.lastpassed |= 0b10
        elif move.richtung == 0:
            self.move_up(move.figur)
        elif move.richtung == 1:
            self.move_right(move.figur)
        else:
            self.move_left(move.figur)

    def applyMove_b(self, move : Move):
        self.lastpassed >>= 1

        if move.is_passing():
            self.lastpassed |= 0b10
        elif move.richtung == 0:
            self.move_up_b(move.figur)
        elif move.richtung == 1:
            self.move_right_b(move.figur)
        else:
            self.move_left_b(move.figur)

        
    def printMe(self):
        print(bin(self.white)+" "+bin(self.black))

    def game_is_finished(self): #+1=win white 0=draw -1=win black None=not finished
        # one figure has traversed the board to the opponent’s side
        if (self.white & self.whitemask) != 0:
            return +1
        elif (self.black & self.blackmask) != 0:
            return -1
        elif self.lastpassed == 3:
            return 0
        else:
            return None

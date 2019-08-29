from Move import Move
from numpy import uint64
from Bitreverse import reverse_bits

# GAMESTATE

class GameState:
    # MATH FUNCTIONS
    def extract_next_pawn(self, bitmask):
        return bitmask & (-bitmask)
    def delete_next_pawn(self, bitmask):
        return bitmask & (bitmask-uint64(1))

    def get_turnmask_up(self):
        return self.white & ~((self.black >> uint64(1)) | (self.white >> uint64(1)))
    def get_turnmask_up_b(self):
        return self.black & ~((self.white << uint64(1)) | (self.black << uint64(1)))
    def get_turnmask_left(self):
        return self.white & (self.black << uint64(8 - 1))
    def get_turnmask_left_b(self):
        return self.black & (self.white << uint64(8 + 1))
    def get_turnmask_right(self):
        return self.white & (self.black >> uint64(8 + 1))
    def get_turnmask_right_b(self):
        return self.black & (self.white >> uint64(8 - 1))

    def move_up(self, pawn):
        npawn = pawn << uint64(1)
        self.white = (self.white & ~pawn) | npawn
    def move_up_b(self, pawn):
        npawn = pawn >> uint64(1)
        self.black = (self.black & ~pawn) | npawn
    
    def move_left(self, pawn):
        npawn = pawn >> uint64(8 - 1)
        self.white = (self.white & ~pawn) | npawn
        self.black = (self.black & ~npawn)
    def move_left_b(self, pawn):
        npawn = pawn >> uint64(8 + 1)
        self.black = (self.black & ~pawn) | npawn
        self.white = (self.white & ~npawn)

    def move_right(self, pawn):
        npawn = pawn << uint64(8 + 1)
        self.white = (self.white & ~pawn) | npawn
        self.black = (self.black & ~npawn)
    def move_right_b(self, pawn):
        npawn = pawn << uint64(8 - 1)
        self.black = (self.black & ~pawn) | npawn
        self.white = (self.white & ~npawn)

    def is_game_won(self):
        return (self.white & self.whitemask) != 0
    def is_game_won_b(self):
        return (self.black & self.blackmask) != 0
    def is_game_draw(self):
        return self.lastpassed and self.thispassed

    # expand math
    def extractMove(self, bitmask, direction):
        pawn = self.extract_next_pawn(bitmask)
        move = Move(pawn, direction)
        return self.delete_next_pawn(bitmask), move

    def __init__(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y

        self.white = uint64(0)
        self.black = uint64(0)

        self.lastpassed = False
        self.thispassed = False
        
        self.whitemask = uint64(0)
        self.blackmask = uint64(0)

    def populate_bauern(self):  # Argument positions?
        for i in range(self.size_x):
            # zwei Reihen Bauern
            self.white      |= uint64(1 << (i*8 + 0))
            self.black      |= uint64(1 << (i*8 + self.size_y-1))
            self.whitemask  |= uint64(1 << (i*8 + self.size_y-1))
            self.blackmask  |= uint64(1 << (i*8 + 0))

    def extract_all_moves(self, retVal, turnmask, direction):
        while turnmask != 0:
            turnmask, move = self.extractMove(turnmask, direction)
            retVal.append(move)

    def list_all_legal_moves(self):
        retVal = []
        self.extract_all_moves(retVal, self.get_turnmask_up(),    0)
        self.extract_all_moves(retVal, self.get_turnmask_right(), 1)
        self.extract_all_moves(retVal, self.get_turnmask_left(), -1)
        if len(retVal) == 0:
            retVal.append(Move(0,0)) #pass
        return retVal

    def list_all_legal_moves_b(self):
        retVal = []
        self.extract_all_moves(retVal, self.get_turnmask_up_b(),    0)
        self.extract_all_moves(retVal, self.get_turnmask_right_b(), 1)
        self.extract_all_moves(retVal, self.get_turnmask_left_b(), -1)
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
        g.thispassed = self.thispassed
        g.winmask = self.winmask
        g.lossmask = self.lossmask
        return g

    def applyMove(self, move : Move):
        self.lastpassed = self.thispassed
        self.thispassed = False
        
        if move.is_passing():
            self.thispassed = True
        elif move.richtung == 0:
            self.move_up(move.figur)
        elif move.richtung == 1:
            self.move_right(move.figur)
        else:
            self.move_left(move.figur)

    def applyMove_b(self, move : Move):
        self.lastpassed = self.thispassed
        self.thispassed = False
        
        if move.is_passing():
            self.thispassed = True
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
        if self.is_game_won():
            return +1
        elif self.is_game_won_b():
            return -1
        elif self.is_game_draw():
            return 0
        else:
            return None

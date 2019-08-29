from Move import Move
from numpy import uint64
from Bitreverse import reverse_bits

# GAMESTATE

class GameState:
    # MATH FUNCTIONS
    def extract_next_pawn(self, bitmask):
        return bitmask & (-bitmask)
    def delete_next_pawn(self, bitmask):
        return bitmask & (bitmask-1)
    def get_turnmask_up(self):
        return self.white & ~((self.black >> 1) | (self.white >> 1))
    def get_turnmask_left(self):
        return self.white & (self.black << (8 - 1))
    def get_turnmask_right(self):
        return self.white & (self.black >> (8 + 1))

    def move_up(self, pawn):
        npawn = pawn << 1
        self.white = (self.white & ~pawn) | npawn
    
    def move_left(self, pawn):
        npawn = pawn >> (8 - 1)
        self.white = (self.white & ~pawn) | npawn
        self.black = (self.black & ~npawn)

    def move_right(self, pawn):
        npawn = pawn << (8 + 1)
        self.white = (self.white & ~pawn) | npawn
        self.black = (self.black & ~npawn)

    def is_game_lost(self):
        return (self.black & self.lossmask) != 0
    
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
        
        self.lossmask = uint64(0)

    def populate_bauern(self):  # Argument positions?
        for i in range(self.size_x):
            # zwei Reihen Bauern
            self.white    |= uint64(1 << (i*8 + 0))
            self.black    |= uint64(1 << (i*8 + self.size_y-1))
            self.lossmask |= uint64(1 << (i*8 + 1))

    def getSize(self):
        return self.size

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
            move = Move(0,0) # Pass
            retVal.append(move)

        return retVal

    def rotateBoard(self):
        self.white, self.black = reverse_bits(self.black), reverse_bits(self.white)
        self.lossmask = reverse_bits(self.lossmask)


    def clone(self):
        g = GameState(self.size_x, self.size_y)
        g.white = self.white
        g.black = self.black
        g.lastpassed = self.lastpassed
        g.thispassed = self.thispassed
        g.lossmask = self.lossmask
        return g

    # TODO sanity checking?
    def applyMove(self, move : Move):
        
        self.lastpassed = self.thispassed
        self.thispassed = False
        
        if move.is_passing():
            self.thispassed = True
            return
        
        if move.richtung == 0:
            self.move_up(move.figur)
        elif move.richtung == 1:
            self.move_right(move.figur)
        elif move.richtung == -1:
            self.move_left(move.figur)
        else:
            print("ill. move")
            #error
            return

    def game_is_finished(self): #+1=win 0=draw -1=loss None=not finished
        # one figure has traversed the board to the opponent’s side
        if self.is_game_lost():
            return -1
        elif self.is_game_draw():
            return 0
        else:
            return None

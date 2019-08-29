import math
from Bitreverse import reverse_bits
from numpy import uint64

class Move:
    def __init__(self, figur, richtung):
        self.figur = figur  # bitmask
        self.richtung = richtung  # -1,0,1

    def is_passing(self):
        return self.figur == 0

    def get_richtung(self):
        return self.richtung

    def get_figur(self):
        return self.figur
    
    def get_x(self):
        return int(math.log2(self.figur) / 8)

    def get_y(self):
        return int(math.log2(self.figur))%8
        
    def copy(self):
        return Move(self.figur, self.richtung)
    
    @staticmethod
    def parse_move(movecode):
        if movecode == "pass":
            return Move(0,0)
        else:
            x, y, r = movecode.split(",")
            x,y,r = int(x),int(y),int(r)
            move = Move(uint64(1 << (x*8+y)), r)
            return move

    @staticmethod
    def write_move(move):
        if move.is_passing():
            return "pass"
        else:
            return str(move.get_x()) + "," + str(move.get_y()) + "," + str(move.richtung)

class Move:
    def __init__(self, figur, richtung, passing=False):
        self.figur = figur  # x,y
        self.richtung = richtung  # -1,0,1
        self.passing = passing  # true,false

    def is_passing(self):
        return self.passing

    def get_richtung(self):
        return self.richtung

    def get_figur(self):
        return self.figur
    
    def rotateBoard(self, board):
        self.figur = (self.figur[0], board.size[1]-1 - self.figur[1])

    @staticmethod
    def parse_move(movecode, invert, gamestate):
        if movecode == "pass":
            return Move(None, None, passsing=True)
        else:
            x, y, r = movecode.split(",")
            return Move((int(x), int(y) if not invert else gamestate.size[1]-1-int(y)), int(r))

    @staticmethod
    def write_move(move, invert, gamestate):
        if move.passing:
            return "pass"
        else:
            return str(move.figur[0]) + "," + str(move.figur[1] if not invert else gamestate.size[1]-1-move.figur[1]) + "," + str(move.richtung)

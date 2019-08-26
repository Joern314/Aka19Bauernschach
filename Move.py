class Move:
    def __init__(self, figur, richtung, passing = False):
    	self.figur = figur #x,y
    	self.richtung = richtung #-1,0,1
    	self.passing = passing # true,false

    def is_passing(self):
        return self.passing

    def get_richtung(self):
        return self.richtung

    def get_figur(self):
        return self.figur

	@staticmethod	
    def parse_move(movecode)
    	if movecode is "pass":
            return Move(None, None, passsing = True)
        else:
            x, y, r = movecode.split(",")
            return Move((x, y), r)

    @staticmethod
    def write_move(move):
        if move.passing:
            return "pass"
        else:
            return move.x + "," + move.y + "," + move.direction

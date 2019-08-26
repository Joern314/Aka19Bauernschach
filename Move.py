class Move:
    def __init__(self, figur, richtung, passing = False):
    	self.figur = figur #x,y
    	self.richtung = richtung #-1,0,1
    	self.passing = passing # true,false

    @staticmethod	
    def parseMove(movecode: str):
        if movecode is "pass":
            return Move(None, None, passsing = True)
        else:
            x, y, r = movecode.split(",")
            return Move((x, y), r)

    @staticmethod
    def writeMove(move):
        if move.passing:
            return "pass"
        else:
            return move.x + "," + move.y + "," + move.direction
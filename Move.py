class Move:
    def __init__(self, figur, richtung, passing = False: bool):
    	self.figur = figur
    	self.richtung = richtung
    	self.passing = passing

	@staticmethod	
    def create_from_movecode(movecode: str):
    	if movecode = "pass":
            return Move(None, None, passsing = True)
        else:
            x, y, r = movecode.split(",")
            return Move((x, y), r)


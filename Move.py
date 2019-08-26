class Move:
    def __init__(self, figur, richtung, passing = False)
    	self.figur = figur
    	self.richtung = richtung
    	self.passing = passing

    def is_passing(self):
        return self.passing

    def get_richtung(self):
        return self.richtung

    def get_figur(self):
        return self.figur

	@staticmethod	
    def create_from_movecode(movecode)
    	if movecode = "pass":
            return Move(None, None, passsing = True)
        else:
            x, y, r = movecode.split(",")
            return Move((x, y), r)


import math
import Evaluator
import GameState
import Move

class Client:
    def __init__(self):
        self.black_or_white = None
        self.innerstate = GameState()
        self.evaluator = Evaluator()
        pass

    def parseMove(self, string):
        pass
    
    def writeMove(self, string):
        pass
    
    def findBestMove(self):
        rating, move = self.evaluator.evaluate(self.innerstate, -math.inf, math.inf)
        return move
    
    def run(self):
        

if __name__ == "__main__":
    # main function
    client = Client()
    client.run()

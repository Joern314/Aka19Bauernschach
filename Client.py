import math
import sys
import Evaluator
import GameState
import Move

class Client:
    def __init__(self, width, height):
        self.black_or_white = None
        self.innerstate = GameState(width, height)
        self.evaluator = Evaluator()
        pass
    
    def findBestMove(self):
        rating, move = self.evaluator.evaluate(self.innerstate, -math.inf, math.inf)
        return move
    
    def run(self):
        

if __name__ == "__main__":
    if len(sys.argv) == 3: #python3 Client.py width height
        width =  int(sys.argv[1])
        height = int(sys.argv[2])
    else:
        width = 2
        height = 4
        
    # main function
    client = Client(width, height)
    client.run()
    
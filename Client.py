import math
import sys
from Evaluator import Evaluator
from GameState import GameState
from Move import Move


class Client:
    def __init__(self, width, height, name="JJF"):
        self.color = ""
        self.width = width
        self.height = height
        self.innerstate = GameState(width, height)
        self.evaluator = Evaluator()
        self.name = name

        self.innerstate.populate_bauern()


    def find_best_move(self):
        rating, move = self.evaluator.evaluate(self.innerstate, -100, 100)
        return move

    def connect(self):
        print(self.name)

    def start_game(self):
        self.color = input()
        print("ok")
        self.innerstate = GameState(self.width, self.height)
        self.innerstate.populate_bauern()
        
    def end_game(self):
        movestring = input()
        if movestring == "done":
            return
        else:
            return #error!

    def run(self):
        self.connect()
        while True:
            turn = "white"
            self.start_game()
            while True:
                if turn == self.color:
                    move = self.find_best_move()
                    print(Move.write_move(move, turn == "black", self.innerstate))
                else:
                    movestring = input()
                    if movestring == "done":
                        break
                    else:
                        move = Move.parse_move(movestring, turn == "black", self.innerstate)

                if not self.innerstate.checkIfLegal(move):
                    print("uups") #error
                self.innerstate.applyMove(move)
                self.innerstate.rotateBoard()
                turn = self.invert_turn(turn)
                
                if self.innerstate.game_is_finished() != None:
                    self.end_game()
                    break

    @staticmethod
    def invert_turn(turn):
        return "black" if turn == "white" else "white"

def main():
    if len(sys.argv) >= 3:  # python3 Client.py width height
        width = int(sys.argv[1])
        height = int(sys.argv[2])
    else:
        width = 2
        height = 4
        
    name = "JJF"
    if len(sys.argv) >= 4:
        name = sys.argv[3]
    # main function
    client = Client(width, height, name=name)
    client.run()

def test():
    c = Client(4,4)
    turn = False
    while not c.innerstate.game_is_finished():
        move = c.find_best_move()
        print(Move.write_move(move, turn, c.innerstate))
        c.innerstate.applyMove(move)
        c.innerstate.rotateBoard()
        turn = not turn

if __name__ == "__main__":
    test()
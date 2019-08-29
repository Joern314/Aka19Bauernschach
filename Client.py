import math
import sys
import argparse
from Evaluator import Evaluator
from GameState import GameState
from Move import Move


class Client:
    def __init__(self, width, height, evaluator = "default", name="JJF"):
        self.color = ""
        self.width = width
        self.height = height
        self.innerstate = GameState(width, height)
        self.evaluator = Evaluator(evaluator)

        self.name = name

        self.innerstate.populate_bauern()


    def find_best_move(self, is_white):
        rating, move = self.evaluator.evaluate(self.innerstate, -100, 100, is_white)
        return move

    def connect(self):
        print(self.name)

    def start_game(self):
        self.color = input()
        print("ok")
        self.innerstate = GameState(self.width, self.height)
        self.innerstate.populate_bauern()
        
    def end_game(self):
#        print("finished: " + str(self.innerstate.game_is_finished()))
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
#                self.innerstate.printMe()
                if turn == self.color:
                    move = self.find_best_move(turn == "white")
                    print(Move.write_move(move))
                else:
                    movestring = input()
                    if movestring == "done":
                        break
                    else:
                        move = Move.parse_move(movestring)

                if turn == "white":
                    self.innerstate.applyMove(move)
                else:
                    self.innerstate.applyMove_b(move)
                turn = self.invert_turn(turn)
                
                if self.innerstate.game_is_finished() != None:
                    self.end_game()
                    break

    @staticmethod
    def invert_turn(turn):
        return "black" if turn == "white" else "white"

def main():
    e = Evaluator()
    parser = argparse.ArgumentParser()
    parser.add_argument("x", type = int)
    parser.add_argument("y", type = int)
    parser.add_argument("evaluator", choices = e.evaluator_functions.keys())
    parser.add_argument("-n", "--name")
    args = parser.parse_args()
    del(e)
    if not args.name:
        name = "JJF_{}x{}_{}".format(args.x, args.y, args.evaluator)
    else:
        name = args.name

    # main function
    client = Client(args.x, args.y, evaluator = args.evaluator, name=name)
    client.run()

def test():
    c = Client(4,4)
    is_white = True
    while c.innerstate.game_is_finished() is None:
        move = c.find_best_move(is_white)
        print(Move.write_move(move))
        if is_white:
            c.innerstate.applyMove(move)
        else:
            c.innerstate.applyMove_b(move)
        is_white = not is_white
    print("result for white = " + str(c.innerstate.game_is_finished()))

if __name__ == "__main__":
    if len(sys.argv) == 1:
        test()
    else:
        main()
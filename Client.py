import sys
import math
import argparse
from Evaluator import Evaluator
from GameState import GameState
from Move import Move
from Bewertung import estimate_functions


class Client:
    def __init__(self, width, height, evaluator = "default", name="JJF", max_costs = 100):
        self.color = ""
        self.width = width
        self.height = height
        self.innerstate = GameState(width, height)
        self.max_costs = max_costs
        self.evaluator = evaluator
        self.turncount = 0

        self.name = name

        self.innerstate.populate_bauern()


    def find_best_move(self, is_white):
        evalu = Evaluator(self.evaluator, self.max_costs)
        rating, move = evalu.begin_evaluate(self.innerstate, self.max_costs, is_white)
        return move

    def connect(self):
        print(self.name)

    def start_game(self):
        self.color = input()
        print("ok")
        self.innerstate = GameState(self.width, self.height)
        self.innerstate.populate_bauern()
        self.turncount = 0
        
    def end_game(self):
#        print("finished: " + str(self.innerstate.game_is_finished()))
        movestring = input()
        if movestring == "done":
            return
        else:
            return #error!

    def prepare_strategy(self):
        pass

    def run(self):
        self.connect()
        while True:
            turn = "white"
            self.start_game()
            while True:
#                self.innerstate.printMe()
                if turn == self.color:
                    self.prepare_strategy()
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
                self.turncount += 1
                
                if self.innerstate.game_is_finished() != None:
                    self.end_game()
                    break

    @staticmethod
    def invert_turn(turn):
        return "black" if turn == "white" else "white"

    def test(self):
        is_white = True
        while c.innerstate.game_is_finished() is None:
            self.prepare_strategy()
            move = self.find_best_move(is_white)
            print(Move.write_move(move))
            if is_white:
                self.innerstate.applyMove(move)
            else:
                self.innerstate.applyMove_b(move)
            is_white = not is_white
            self.turncount += 1
        print("result for white = " + str(self.innerstate.game_is_finished()))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("x", type = int)
    parser.add_argument("y", type = int)
    parser.add_argument("evaluator", choices = estimate_functions.keys())
    parser.add_argument("-n", "--name")
    parser.add_argument("-c", "--costs", type = float)
    args = parser.parse_args()

    if not args.costs:
        max_costs = 5.0
    else:
        max_costs = args.costs

    if not args.name:
        name = "JJF_{}x{}_{}_{}".format(args.x, args.y, args.evaluator, max_costs)
    else:
        name = args.name
        

    # main function
    client = Client(args.x, args.y, evaluator = args.evaluator, name=name, max_costs = max_costs)
    client.run()

if __name__ == "__main__":
    if len(sys.argv) >= 5 and sys.argv[1] == "test":
        size = int(sys.argv[2])
        evaluator = sys.argv[3]
        costs = float(sys.argv[4])
        c = Client(size, size, evaluator, "test", costs)
        for i in range(1):
            c.test()
    else:
        main()
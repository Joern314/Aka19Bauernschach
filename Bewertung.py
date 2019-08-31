from GameState import GameState
import Bits

def bewerte_unentschieden(board, is_white): # bewerte aus sicht des aktuellen spielers
    return 0

def bewerte_figurzahl(board, is_white):
    return (Bits.popcount(board.white) - Bits.popcount(board.black))/float(board.size_x) * (+1 if is_white else -1)

def bewerte_kills(board: GameState, is_white):
    if not is_white:
        moved_b = (0 | (board.black >> 1)) & ~(board.white)
        moved_w = board.white
    else:
        moved_w = (0 | (board.white << 1)) & ~(board.black)
        moved_b = board.black
    
    kill_wr = moved_b & (board.white << (8+1))
    kill_wl = moved_b & (board.white >> (8-1))
    kill_w = Bits.popcount(kill_wr) + Bits.popcount(kill_wl)
    
    kill_br = moved_w & (board.black << (8-1))
    kill_bl = moved_w & (board.black >> (8+1))
    kill_b = Bits.popcount(kill_br) + Bits.popcount(kill_bl)
        
    return (kill_w-kill_b) / 32.0 * (+1 if is_white else -1)

def bewerte_mix(board, is_white):
    return (bewerte_kills(board, is_white) + bewerte_figurzahl(board, is_white)) / 2

estimate_functions = {
    "unentschieden": bewerte_unentschieden,
    "figurzahl": bewerte_figurzahl,
    "kills": bewerte_kills,
    "mix": bewerte_mix
}
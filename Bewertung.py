from GameState import GameState
import Bits

def bewerte_unentschieden(board, is_white): # bewerte aus sicht des aktuellen spielers
    return 0

def bewerte_figurzahl(board, is_white):
    pawns_white = board.list_all_pawns(board.white)
    pawns_black = board.list_all_pawns(board.black)
    
    return (len(pawns_white) - len(pawns_black))/float(board.size_x) * (+1 if is_white else -1)

def bewerte_forward(board, is_white):
    pawns_white = board.list_all_pawns(board.white)
    pawns_black = board.list_all_pawns(board.black)
    
    bew = 0
    
    for pawn in pawns_white:
        h = Bits.get_y(pawn)
        bew += h * 0.5 + 1
    for pawn in pawns_black:
        h = board.size_y-1 - Bits.get_y(pawn)
        bew -= h * 0.5 + 1
    
    maxbew = float(8+8*0.5*4)
    return bew / maxbew * (+1 if is_white else -1)

def bewerte_freeline(board, is_white):
    set_col_w = 0
    w = board.white
    set_col_b = 0
    b = board.black
    for i in range(8):
        if ((w & 0xFF) != 0) and ((b & 0xFF) == 0):
            set_col_w+=1
        if ((w & 0xFF) == 0) and ((b & 0xFF) != 0):
            set_col_b+=1
        w >>= 8
        b >>= 8
        
    return (set_col_w - set_col_b) / 10 * (+1 if is_white else -1)



estimate_functions = {
    "unentschieden": bewerte_unentschieden,
    "forward": bewerte_forward,
    "figurzahl": bewerte_figurzahl,
    "freeline": bewerte_freeline
}
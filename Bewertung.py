from GameState import GameState

def bewerte_unentschieden(board, is_white): # bewerte aus sicht des aktuellen spielers
    return 0

def bewerte_figurzahl(board, is_white):
    pawns_white = board.list_all_pawns(board.white)
    pawns_black = board.list_all_pawns(board.black)
    
    return (len(pawns_white) - len(pawns_black))/float(board.size_x) * (+1 if is_white else -1)

def bewerte_moves(board: GameState, is_white):
    if is_white:
        moved_b = (board.black | (board.black >> 1)) & ~(board.white)
        kill_wr = moved_b & (board.white << (8+1))
        kill_wl = moved_b & (board.white >> (8-1))
        

estimate_functions = {
    "unentschieden": bewerte_unentschieden,
    "figurzahl": bewerte_figurzahl,
    "moves": bewerte_moves
}
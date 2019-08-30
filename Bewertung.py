

def bewerte_unentschieden(board, is_white): # bewerte aus sicht des aktuellen spielers
    return 0

def bewerte_figurzahl(board, is_white):
    pawns_white = board.list_all_pawns(board.white)
    pawns_black = board.list_all_pawns(board.black)
    
    return (len(pawns_white) - len(pawns_black))/float(board.size_x) * (+1 if is_white else -1)
from numpy import zeros
from numba import jit

from .constants import (
    VERBOSITY, MAXI, MAXJ, MAXPIECE, PIECENO, NPDTYPE, MAPNUM, IMAPNUM,
    IS_W_PAWN, IS_B_PAWN, IS_ENPASSANT, EMPTY, W_QUEEN, B_QUEEN,
    IS_KING_CASTLING, CASTLE_KING_X, CASTLING_KING_CASTLE_DEST_X,
    IS_QUEEN_CASTLING, CASTLE_QUEEN_X, CASTLING_QUEEN_CASTLE_DEST_X,
    NBDTYPE
    )


def parse_match_from_movlst(match, game_array):
    match.ucimovements = game_array
    match.B[0, ...] = __init_board_num(MAXI, MAXJ)
    match.pieces[0, ...] = __find_pieces_num(match.B[0, ...])
    for m in range(len(match)):
        # Update the board with next movement
        match.B[m+1, ...] = __move_board_num(
            match.B[m, ...].copy(),
            match.movements[m],
            )

        # Find all active pieces
        match.pieces[m+1, ...] = __find_pieces_num(match.B[m+1, ...])

        # Find any newly promoted pawn
        match.promoted[m+1, ...] = __find_promoted_num(
            match.B[m+1, ...],
            match.pieces[m+1, ...],
            match.promoted[m, ...].copy(),
            )


@jit(NBDTYPE[:](NBDTYPE[:, :]), nopython=True)
def __find_pieces_num(board):
    # Old version, exact copy of C code
    pieces = zeros(MAXPIECE, NPDTYPE)
    for i in range(MAXI):
        for j in range(MAXJ):
            for pz in range(MAXPIECE):
                if (board[i, j] == MAPNUM(pz)):
                    pieces[pz] = 1
    return pieces


@jit(NBDTYPE[:](NBDTYPE[:, :], NBDTYPE[:], NBDTYPE[:]), nopython=True)
def __find_promoted_num(board, active_pieces, promoted):
    # We could track movements results and avoid all these iterations...
    for i in range(MAXI):
        for j in range(MAXJ):
            pz = board[i, j]
            pzn = IMAPNUM(pz)
            if (IS_W_PAWN(pz) and j == MAXJ and promoted[pzn] == 0):
                promoted[pzn] = W_QUEEN
            elif (IS_B_PAWN(pz) and j == 0 and promoted[pzn] == 0):
                promoted[pzn] = B_QUEEN
    return promoted


@jit(NBDTYPE[:, :](NBDTYPE[:, :], NBDTYPE[:]), nopython=True)
def __move_board_num(board, movement):
    (x0, y0, xf, yf) = movement[:]
    pz = board[x0, y0]
    # Check for king castling
    if (IS_KING_CASTLING(pz, x0, xf)):
        # Move the castle
        board[CASTLING_KING_CASTLE_DEST_X, y0] = board[CASTLE_KING_X, y0]
        board[CASTLE_KING_X, y0] = EMPTY
        # if (VERBOSITY):
        #    print("KING CASTLING")
    # Check for queen castling
    elif (IS_QUEEN_CASTLING(pz, x0, xf)):
        # Move the castle
        board[CASTLING_QUEEN_CASTLE_DEST_X, y0] = board[CASTLE_QUEEN_X, y0]
        board[CASTLE_QUEEN_X, y0] = EMPTY
        # if (VERBOSITY):
        #    print("QUEEN CASTLING")
    # Check for enpassant capture
    elif (IS_ENPASSANT(pz, board[xf, yf], y0, yf)):
        # Remove en-passant captured piece
        board[xf, y0] = EMPTY

    # And finally, perform the movement
    board[xf, yf] = board[x0, y0]
    board[x0, y0] = EMPTY
    return board


@jit(NBDTYPE[:, :](NBDTYPE, NBDTYPE), nopython=True)
def __init_board_num(xsz, ysz):
    b = zeros((xsz, ysz), NPDTYPE)
    for j in range(MAXJ):
        for i in range(MAXI):
            if (j == 0):
                b[i, j] = MAPNUM(i)
            elif (j == 1):
                b[i, j] = MAPNUM(MAXI + i)
            elif (j == MAXJ-2):
                b[i, j] = MAPNUM(PIECENO + MAXI + i)
            elif (j == MAXJ-1):
                b[i, j] = MAPNUM(PIECENO + i)
            else:
                b[i, j] = EMPTY
    return b

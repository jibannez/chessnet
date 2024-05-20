# from numpy import nonzero
from numba import jit, void
from numpy import array


from .constants import (
    MAXI, MAXJ, IMAPNUM, MAPCELL, INVALID_KING, SUMDIM2,
    IS_WHITE, IS_BLACK,
    IS_EMPTY, IS_OCCUPIED, IS_OUTSIDE,
    IS_CASTLE, IS_W_CASTLE,
    IS_BISHOP, IS_W_BISHOP,
    IS_QUEEN, IS_W_QUEEN,
    IS_KNIGHT, IS_W_KNIGHT,
    IS_W_PAWN, IS_B_PAWN,
    IS_W_PAWN_ROW, IS_B_PAWN_ROW,
    IS_W_KING, IS_B_KING, IS_KING_ACCESIBLE,
    NBDTYPE, NPDTYPE,
    CHECK_KNIGHT, CHECK_W_PAWN, CHECK_B_PAWN, CHECK_KING, CHECK_KING_AS_QUEEN, 
    CHECK_CASTLE, CHECK_BISHOP, CHECK_QUEEN, W_KING_IDX, B_KING_IDX,
    )


def compute_match(match):
    for moveno in range(len(match)+1):
        compute_state(match, moveno)


def compute_state(board_state, moveno=None):
    """
     Calculates the contact matrix between each pair of pieces.
     The values between pairs of the same colour indicate "protection", while
     values between pairs of different colour indicate "threat".
     A value of 1 indicates "protection"/"threat" and a value of 0 indicates
     no "protection"/"threat".
    """
    if moveno is None:
        # The input object is a BoardState instance
        X = board_state.X
        S = board_state.S
        B = board_state.B
        Kw = board_state.Kw
        Kb = board_state.Kb
        promoted = board_state.promoted.squeeze()
    else:
        # The input object is a Match instance
        X = board_state.X[moveno, ...]
        S = board_state.S[moveno, ...]
        B = board_state.B[moveno, ...]
        Kw = board_state.Kw[moveno, ...]
        Kb = board_state.Kb[moveno, ...]
        Kw = Kw.reshape((1,)+Kw.shape)
        Kb = Kb.reshape((1,)+Kb.shape)
        promoted = board_state.promoted[moveno, ...]
    compute_board_matrices(B, X, S, promoted, Kw, Kb)


@jit(void(NBDTYPE[:, :], NBDTYPE[:, :], NBDTYPE[:, :],
          NBDTYPE[:], NBDTYPE[:,:], NBDTYPE[:,:]), nopython=True)
def compute_board_matrices(B, X, S, promoted, Kw, Kb):
    # Set default king movement for test runs
    bKing = array([INVALID_KING, INVALID_KING])
    wKing = array([INVALID_KING, INVALID_KING])

    # Exhaustive board search to find the pieces
    for i in range(MAXI):
        for j in range(MAXJ):
            # Continue searching the board if cell is empty
            if IS_EMPTY(B[i, j]):
                continue

            # Get piece ID
            p = B[i, j]

            # Get piece's 0-based index for cm matrix
            pn = IMAPNUM(p)

            # Correct type of piece for upgraded pawns
            if promoted[pn] != 0:
                p = promoted[pn]
                pn = IMAPNUM(p)

            # Store Cell number in 0-based indexing
            cn = MAPCELL(i,j)

            #Store position of this piece in the board using matrix X
            X[pn, cn] = 1

            if IS_CASTLE(p):
                CHECK_CASTLE(B, S, i, j, p, pn)

            elif IS_BISHOP(p):
                CHECK_BISHOP(B, S, i, j, p, pn)

            elif IS_QUEEN(p):
                CHECK_QUEEN(B, S, i, j, p, pn)

            elif IS_KNIGHT(p):
                CHECK_KNIGHT(B, S, i, j, p, pn)

            elif IS_W_PAWN(p):
                CHECK_W_PAWN(B, S, i, j, p, pn)

            elif IS_B_PAWN(p):
                CHECK_B_PAWN(B, S, i, j, p, pn)

            elif IS_B_KING(p):
                # Only store movements, we need to know all threats before
                bKing[0] = i
                bKing[1] = j

            elif IS_W_KING(p):
                # Only store movements, we need to know all threats before
                wKing[0] = i
                wKing[1] = j

    # WHITE KING: check now with all potential threats computed
    Accb = SUMDIM2(S[16:, :])
    CHECK_KING(B, S, Accb, wKing, bKing, W_KING_IDX)

    # BLACK KING: check now with all potential threats computed
    Accw = SUMDIM2(S[:16, :])
    CHECK_KING(B, S, Accw, bKing, wKing, B_KING_IDX)

    # Compute kings accesibility
    CHECK_KING_AS_QUEEN(B, Kw, wKing[0], wKing[1])
    CHECK_KING_AS_QUEEN(B, Kb, bKing[0], bKing[1])


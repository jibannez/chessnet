import os
from numpy import array, logical_and, logical_or, zeros, sum
from numpy import int_ as npint_
from numpy import uint8 as npuint8
from numba import jit, bool_,void
from numba import int_ as nbint_
from numba import uint8 as nbuint8

install_path = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(install_path, 'data')
testdirectory = data_path
testfilename = os.path.join(testdirectory, 'test', 'enroque_rey.pgn')
testmultifilename = os.path.join(testdirectory, 'fischer_60_mem.pgn')
EPD_init_board = b'RNBKQBNR/PPPPPPPP/8/8/8/8/pppppppp/rnbkqbnr'

VERBOSITY = False


"""
/////////////////////////////////////////////////////////////
//BOARD STRUCTURE AND CODING CONVENTIONS
/////////////////////////////////////////////////////////////

CHARACTER CODIFICATION

   J0 J1 J2 J3 J4 J5 J6 J7
   -----------------------
I0 | A I              i a|
I1 | B J              j b|
I2 | C K              k c|
I3 | D L              l d|
I4 | E M              m e|
I5 | F N              n f|
I6 | G O              o g|
I7 | H P              p h|
   -----------------------
    WHITE           BLACK


NUMERICAL CODIFICATION - if EMPTY = 0

   J0 J1 J2 J3 J4 J5 J6 J7
   -----------------------
I0 | 1 9            25 17|
I1 | 2 10           26 18|
I2 | 3 11           27 19|
I3 | 4 12           28 20|
I4 | 5 13           29 21|
I5 | 6 14           30 22|
I6 | 7 15           31 23|
I7 | 8 16           32 24|
--------------------------
    WHITE           BLACK
"""
# Piece names
PIECE_NAMES = (
    "RLw", "NLw", "BLw", "Qw ",  "Kw ",  "BRw", "NRw", "RRw",
    "p1w", "p2w", "p3w", "p4w", "p5w", "p6w", "p7w", "p8w",
    "RLb", "NLb", "BLb", "Qb ",  "Kb ",  "BRb", "NRb", "RRb",
    "p8b", "p7b", "p6b", "p5b", "p4b", "p3b", "p2b", "p1b",
)

FALSE = 0
TRUE = not FALSE
EMPTY = 0

NPDTYPE = npint_
# NPDTYPE = npuint8
NBDTYPE = nbint_
# NBDTYPE = nbuint8

BOARDX = 8
BOARDY = 8
PAWNNO = BOARDX*2
MAXPIECES = BOARDX*4

UCISZ = 4
UCISZ_NUM = 4
MAXI = 8
MAXJ = 8
PIECENO = MAXI*2
MAXPIECE = PIECENO*2
BOARDSZ = MAXI * MAXJ
BASEW_NUM = 65  # ASCCI Code for A
BASEB_NUM = 97  # ASCII Code for a
BASEW = 'A'
BASEB = 'a'

ASCII_1 = 49  # ASCII Code for 1
ASCII_a = 97  # ASCII Code for a
UCI_OFFSET = array((ASCII_a, ASCII_1, ASCII_a, ASCII_1))

KNIGHT_MOVENO = 8
PAWN_MOVENO = 4
KING_MOVENO = 8

KNIGHT_MOVES = ((-1, 2), (1, 2), (2, 1), (2, -1),
                (1, -2), (-1, -2), (-2, -1), (-2, 1))
KING_MOVES = ((-1, -1), (-1, 0), (-1, 1), (0, -1),
              (0, 1), (1, -1), (1, 0), (1, 1))
PAWN_MOVES_W = ((-1, 1), (0, 1), (1, 1), (0, 2))
PAWN_MOVES_B = ((-1, -1), (0, -1), (1, -1), (0, -2))

INVALID_KING = -1

# X coordinates of figures starting at ZERO
# They are identical for both players due to
# the king/queen assimetry.
CASTLE_QUEEN_X = 0
KNIGHT_QUEEN_X = 1
BISHOP_QUEEN_X = 2
QUEEN_X        = 3
KING_X         = 4
BISHOP_KING_X  = 5
KNIGHT_KING_X  = 6
CASTLE_KING_X  = 7

# Castling cordinates, starting at ZERO
# Again identical for both players due to
# the king/queen assimetry.
CASTLING_KING_KING_DEST_X    = 6
CASTLING_KING_CASTLE_DEST_X  = 5
CASTLING_QUEEN_KING_DEST_X   = 2
CASTLING_QUEEN_CASTLE_DEST_X = 3

# NUMERICAL CODES OF PIECES, STARTING AT ONE!
W_CASTLE_QUEEN = 1 + EMPTY
W_KNIGHT_QUEEN = 2 + EMPTY
W_BISHOP_QUEEN = 3 + EMPTY
W_QUEEN        = 4 + EMPTY
W_KING         = 5 + EMPTY
W_BISHOP_KING  = 6 + EMPTY
W_KNIGHT_KING  = 7 + EMPTY
W_CASTLE_KING  = 8 + EMPTY

W_PAWN_CASTLE_QUEEN = 9  + EMPTY
W_PAWN_KNIGHT_QUEEN = 10 + EMPTY
W_PAWN_BISHOP_QUEEN = 11 + EMPTY
W_PAWN_QUEEN        = 12 + EMPTY
W_PAWN_KING         = 13 + EMPTY
W_PAWN_BISHOP_KING  = 14 + EMPTY
W_PAWN_KNIGHT_KING  = 15 + EMPTY
W_PAWN_CASTLE_KING  = 16 + EMPTY

B_CASTLE_QUEEN = 17 + EMPTY
B_KNIGHT_QUEEN = 18 + EMPTY
B_BISHOP_QUEEN = 19 + EMPTY
B_QUEEN        = 20 + EMPTY
B_KING         = 21 + EMPTY
B_BISHOP_KING  = 22 + EMPTY
B_KNIGHT_KING  = 23 + EMPTY
B_CASTLE_KING  = 24 + EMPTY

B_PAWN_CASTLE_QUEEN = 25 + EMPTY
B_PAWN_KNIGHT_QUEEN = 26 + EMPTY
B_PAWN_BISHOP_QUEEN = 27 + EMPTY
B_PAWN_QUEEN        = 28 + EMPTY
B_PAWN_KING         = 29 + EMPTY
B_PAWN_BISHOP_KING  = 30 + EMPTY
B_PAWN_KNIGHT_KING  = 31 + EMPTY
B_PAWN_CASTLE_KING  = 32 + EMPTY


@jit(NBDTYPE(NBDTYPE), nopython=True)
def MAPNUM(X):
    return X + EMPTY + 1


@jit(NBDTYPE(NBDTYPE,NBDTYPE), nopython=True)
def MAPCELL(i, j):
    return i*MAXI + j


@jit(NBDTYPE(NBDTYPE), nopython=True)
def IMAPNUM(X):
    return X - EMPTY - 1


@jit(NBDTYPE[:](NBDTYPE[:]), nopython=True)
def MAPNUM_VEC(X):
    return X + EMPTY + 1


@jit(NBDTYPE[:](NBDTYPE[:]), nopython=True)
def IMAPNUM_VEC(X):
    return X - EMPTY - 1


@jit(NBDTYPE[:](NBDTYPE[:, :]), nopython=True)
def SUMDIM1(A):    
    n,m = A.shape
    out = zeros((n,), dtype=NPDTYPE)
    #sum(A,axis=0,out=Aout)
    #return Aout 
    for i in range(n):
        for j in range(m):
            out[i] += A[i,j]
    return out


@jit(NBDTYPE[:](NBDTYPE[:, :]), nopython=True)
def SUMDIM2(A):    
    n, m = A.shape
    out = zeros((m,), dtype=NPDTYPE)
    #sum(A,axis=0,out=Aout)
    #return Aout 
    for i in range(n):
        for j in range(m):
            out[j] += A[i,j]
    return out


# Macros to detect if a cell is empty or occupied
@jit(bool_(NBDTYPE), nopython=True)
def IS_EMPTY(X):
    return X == EMPTY


@jit(bool_(NBDTYPE), nopython=True)
def IS_PROMOTED(X):
    return X != 0


@jit(bool_(NBDTYPE), nopython=True)
def IS_OCCUPIED(X):
    return X != EMPTY


@jit(bool_(NBDTYPE, NBDTYPE), nopython=True)
def IS_OUTSIDE(I, J):
    return I < 0 or I >= MAXI or J < 0 or J >= MAXJ


@jit(bool_(NBDTYPE, NBDTYPE, NBDTYPE, NBDTYPE), nopython=True)
def IS_KING_ACCESIBLE(x1, y1, x2, y2):
    """Checks if the (x1,y1) position can be accesed by a king in (x2,y2)"""
    if x2 == INVALID_KING or y2 == INVALID_KING:
        # This test makes non sense if king's location is not valid
        return False
    elif abs(x1 - x2) < 2 and abs(y1 - y2) < 2:
        return True
    else:
        return False


# Macros to detect the identity of a piece
@jit(bool_(NBDTYPE), nopython=True)
def IS_W_PAWN(X):
    return X >= W_PAWN_CASTLE_QUEEN and X <= W_PAWN_CASTLE_KING


@jit(bool_(NBDTYPE), nopython=True)
def IS_B_PAWN(X):
    return X >= B_PAWN_CASTLE_QUEEN and X <= B_PAWN_CASTLE_KING


@jit(bool_(NBDTYPE), nopython=True)
def IS_PAWN(X):
    return IS_W_PAWN(X) or IS_B_PAWN(X)


@jit(bool_[:](NBDTYPE[:]), nopython=True)
def IS_W_PAWN_VEC(X):
    return logical_and(X >= W_PAWN_CASTLE_QUEEN, X <= W_PAWN_CASTLE_KING)


@jit(bool_[:](NBDTYPE[:]), nopython=True)
def IS_B_PAWN_VEC(X):
    return logical_and(X >= B_PAWN_CASTLE_QUEEN, X <= B_PAWN_CASTLE_KING)


@jit(bool_[:](NBDTYPE[:]), nopython=True)
def IS_PAWN_VEC(X):
    return logical_or(IS_W_PAWN_VEC(X), IS_B_PAWN_VEC(X))


@jit(bool_(NBDTYPE), nopython=True)
def IS_W_CASTLE_QUEEN(X):
    return X == W_CASTLE_QUEEN


@jit(bool_(NBDTYPE), nopython=True)
def IS_W_CASTLE_KING(X):
    return X == W_CASTLE_KING


@jit(bool_(NBDTYPE), nopython=True)
def IS_W_CASTLE(X):
    return IS_W_CASTLE_QUEEN(X) or IS_W_CASTLE_KING(X)


@jit(bool_(NBDTYPE), nopython=True)
def IS_B_CASTLE_QUEEN(X):
    return X == B_CASTLE_QUEEN


@jit(bool_(NBDTYPE), nopython=True)
def IS_B_CASTLE_KING(X):
    return X == B_CASTLE_KING


@jit(bool_(NBDTYPE), nopython=True)
def IS_B_CASTLE(X):
    return IS_B_CASTLE_QUEEN(X) or IS_B_CASTLE_KING(X)


@jit(bool_(NBDTYPE), nopython=True)
def IS_CASTLE(X):
    return IS_B_CASTLE(X) or IS_W_CASTLE(X)


@jit(bool_(NBDTYPE), nopython=True)
def IS_W_KNIGHT_QUEEN(X):
    return X == W_KNIGHT_QUEEN


@jit(bool_(NBDTYPE), nopython=True)
def IS_W_KNIGHT_KING(X):
    return X == W_KNIGHT_KING


@jit(bool_(NBDTYPE), nopython=True)
def IS_W_KNIGHT(X):
    return IS_W_KNIGHT_QUEEN(X) or IS_W_KNIGHT_KING(X)


@jit(bool_(NBDTYPE), nopython=True)
def IS_B_KNIGHT_QUEEN(X):
    return X == B_KNIGHT_QUEEN


@jit(bool_(NBDTYPE), nopython=True)
def IS_B_KNIGHT_KING(X):
    return X == B_KNIGHT_KING


@jit(bool_(NBDTYPE), nopython=True)
def IS_B_KNIGHT(X):
    return IS_B_KNIGHT_QUEEN(X) or IS_B_KNIGHT_KING(X)


@jit(bool_(NBDTYPE), nopython=True)
def IS_KNIGHT(X):
    return IS_B_KNIGHT(X) or IS_W_KNIGHT(X)


@jit(bool_(NBDTYPE), nopython=True)
def IS_W_BISHOP_QUEEN(X):
    return X == W_BISHOP_QUEEN


@jit(bool_(NBDTYPE), nopython=True)
def IS_W_BISHOP_KING(X):
    return X == W_BISHOP_KING


@jit(bool_(NBDTYPE), nopython=True)
def IS_W_BISHOP(X):
    return IS_W_BISHOP_QUEEN(X) or IS_W_BISHOP_KING(X)


@jit(bool_(NBDTYPE), nopython=True)
def IS_B_BISHOP_QUEEN(X):
    return X == B_BISHOP_QUEEN


@jit(bool_(NBDTYPE), nopython=True)
def IS_B_BISHOP_KING(X):
    return X == B_BISHOP_KING


@jit(bool_(NBDTYPE), nopython=True)
def IS_B_BISHOP(X):
    return IS_B_BISHOP_QUEEN(X) or IS_B_BISHOP_KING(X)


@jit(bool_(NBDTYPE), nopython=True)
def IS_BISHOP(X):
    return IS_B_BISHOP(X) or IS_W_BISHOP(X)


@jit(bool_(NBDTYPE), nopython=True)
def IS_W_QUEEN(X):
    return X == W_QUEEN


@jit(bool_(NBDTYPE), nopython=True)
def IS_W_KING(X):
    return X == W_KING


@jit(bool_(NBDTYPE), nopython=True)
def IS_B_QUEEN(X):
    return X == B_QUEEN


@jit(bool_(NBDTYPE), nopython=True)
def IS_B_KING(X):
    return X == B_KING


@jit(bool_(NBDTYPE), nopython=True)
def IS_KING(X):
    return IS_W_KING(X) or IS_B_KING(X)


@jit(bool_(NBDTYPE), nopython=True)
def IS_QUEEN(X):
    return IS_W_QUEEN(X) or IS_B_QUEEN(X)


@jit(bool_(NBDTYPE), nopython=True)
def IS_WHITE(X):
    return X >= W_CASTLE_QUEEN and X <= W_PAWN_CASTLE_KING


@jit(bool_(NBDTYPE), nopython=True)
def IS_BLACK(X):
    return X >= B_CASTLE_QUEEN and X <= B_PAWN_CASTLE_KING


@jit(bool_(NBDTYPE), nopython=True)
def IS_W_EMPTY(X):
    return not IS_WHITE(X)


@jit(bool_(NBDTYPE), nopython=True)
def IS_B_EMPTY(X):
    return not IS_BLACK(X)


# Macros to detect special movements that are not evident
# in algebraic coding (castling and enpassant captures)
@jit(bool_(NBDTYPE, NBDTYPE, NBDTYPE), nopython=True)
def IS_KING_CASTLING(PZ, X0, XF):
    return IS_KING(PZ) and X0 == KING_X and XF == CASTLING_KING_KING_DEST_X


@jit(bool_(NBDTYPE, NBDTYPE, NBDTYPE), nopython=True)
def IS_QUEEN_CASTLING(PZ, X0, XF):
    return IS_KING(PZ) and X0 == KING_X and XF == CASTLING_QUEEN_KING_DEST_X


@jit(bool_(NBDTYPE), nopython=True)
def IS_W_ENPASSANT_ROW(X):
    return X == 4  # ROW BEFORE WHITE CAPTURES BLACK


@jit(bool_(NBDTYPE), nopython=True)
def IS_B_ENPASSANT_ROW(X):
    return X == 3  # ROW BEFORE BLACK CAPTURES WHITE


@jit(bool_(NBDTYPE), nopython=True)
def IS_W_PAWN_ROW(X):
    return X == 1


@jit(bool_(NBDTYPE), nopython=True)
def IS_B_PAWN_ROW(X):
    return X == 6


@jit(bool_(NBDTYPE, NBDTYPE), nopython=True)
def IS_PAWN_CAPTURE(Y0, YF):
    return Y0 != YF


@jit(bool_(NBDTYPE, NBDTYPE, NBDTYPE, NBDTYPE), nopython=True)
def IS_W_ENPASSANT(PZ1, DEST, X0, YF):
    return IS_W_PAWN(PZ1) and IS_PAWN_CAPTURE(X0, YF) and IS_W_ENPASSANT_ROW(X0) and IS_W_EMPTY(DEST)


@jit(bool_(NBDTYPE, NBDTYPE, NBDTYPE, NBDTYPE), nopython=True)
def IS_B_ENPASSANT(PZ1, DEST, X0, YF):
    return IS_B_PAWN(PZ1) and IS_PAWN_CAPTURE(X0, YF) and IS_B_ENPASSANT_ROW(X0) and IS_B_EMPTY(DEST)


@jit(bool_(NBDTYPE, NBDTYPE, NBDTYPE, NBDTYPE), nopython=True)
def IS_ENPASSANT(PZ, DEST, Y0, YF):
    return IS_W_ENPASSANT(PZ, DEST, Y0, YF) or IS_B_ENPASSANT(PZ, DEST, Y0, YF)


# Check the different directions of movement
# The position of IS_OCCUPIED call determines
# whether we check until last free place
@jit(void(NBDTYPE[:, :], NBDTYPE[:, :],
          NBDTYPE, NBDTYPE, NBDTYPE, NBDTYPE), nopython=True)
def CHECK_DOWN(B, S, i, j, p, pn):
    for n in range(j-1, -1, -1):
        c = B[i, n]
        cn = MAPCELL(i, n)
        S[pn, cn] += 1
        if IS_OCCUPIED(c):
            break


@jit(void(NBDTYPE[:, :], NBDTYPE[:, :],
          NBDTYPE, NBDTYPE, NBDTYPE, NBDTYPE), nopython=True)
def CHECK_UP(B, S, i, j, p, pn):
    for n in range(j+1, MAXJ):
        c = B[i, n]
        cn = MAPCELL(i, n)
        S[pn, cn] += 1
        if IS_OCCUPIED(c):
            break


@jit(void(NBDTYPE[:, :], NBDTYPE[:, :],
          NBDTYPE, NBDTYPE, NBDTYPE, NBDTYPE), nopython=True)
def CHECK_LEFT(B, S, i, j, p, pn):
    for n in range(i-1, -1, -1):
        c = B[n, j]
        cn = MAPCELL(n, j)
        S[pn, cn] += 1
        if IS_OCCUPIED(c):
            break


@jit(void(NBDTYPE[:, :], NBDTYPE[:, :],
          NBDTYPE, NBDTYPE, NBDTYPE, NBDTYPE), nopython=True)
def CHECK_RIGHT(B, S, i, j, p, pn):
    for n in range(i+1, MAXI):
        c = B[n, j]
        cn = MAPCELL(n, j)
        S[pn, cn] += 1
        if IS_OCCUPIED(c):
            break



@jit(void(NBDTYPE[:, :], NBDTYPE[:, :],
          NBDTYPE, NBDTYPE, NBDTYPE, NBDTYPE), nopython=True)
def CHECK_UPLEFT(B, S, i, j, p, pn):
    m = i
    for n in range(j+1, MAXJ):
        m -= 1
        if m < 0:
            break
        c = B[m, n]
        cn = MAPCELL(m, n)
        S[pn, cn] += 1
        if IS_OCCUPIED(c):
            break


@jit(void(NBDTYPE[:, :], NBDTYPE[:, :],
          NBDTYPE, NBDTYPE, NBDTYPE, NBDTYPE), nopython=True)
def CHECK_DOWNLEFT(B, S, i, j, p, pn):
    m = i
    for n in range(j-1, -1, -1):
        m -= 1
        if m < 0:
            break
        c = B[m, n]
        cn = MAPCELL(m, n)
        S[pn, cn] += 1
        if IS_OCCUPIED(c):
            break


@jit(void(NBDTYPE[:, :], NBDTYPE[:, :],
          NBDTYPE, NBDTYPE, NBDTYPE, NBDTYPE), nopython=True)
def CHECK_UPRIGHT(B, S, i, j, p, pn):
    m = i
    for n in range(j+1, MAXJ):
        m += 1
        if m >= MAXI:
            break
        c = B[m, n]
        cn = MAPCELL(m, n)
        S[pn, cn] += 1
        if IS_OCCUPIED(c):
            break


@jit(void(NBDTYPE[:, :], NBDTYPE[:, :],
          NBDTYPE, NBDTYPE, NBDTYPE, NBDTYPE), nopython=True)
def CHECK_DOWNRIGHT(B, S, i, j, p, pn):
    m = i
    for n in range(j-1, -1, -1):
        m += 1
        if m >= MAXI:
            break
        c = B[m, n]
        cn = MAPCELL(m, n)
        S[pn, cn] += 1
        if IS_OCCUPIED(c):
            break


@jit(void(NBDTYPE[:, :], NBDTYPE[:, :],
          NBDTYPE, NBDTYPE, NBDTYPE, NBDTYPE), nopython=True)
def CHECK_CASTLE(B, S, i, j, p, pn):
    CHECK_UP(B, S, i, j, p, pn)
    CHECK_DOWN(B, S, i, j, p, pn)
    CHECK_LEFT(B, S, i, j, p, pn)
    CHECK_RIGHT(B, S, i, j, p, pn)


@jit(void(NBDTYPE[:, :], NBDTYPE[:, :],
          NBDTYPE, NBDTYPE, NBDTYPE, NBDTYPE), nopython=True)
def CHECK_BISHOP(B, S, i, j, p, pn):
    CHECK_UPLEFT(B, S, i, j, p, pn)
    CHECK_DOWNLEFT(B, S, i, j, p, pn)
    CHECK_UPRIGHT(B, S, i, j, p, pn)
    CHECK_DOWNRIGHT(B, S, i, j, p, pn)


@jit(void(NBDTYPE[:, :], NBDTYPE[:, :],
          NBDTYPE, NBDTYPE, NBDTYPE, NBDTYPE), nopython=True)
def CHECK_QUEEN(B, S, i, j, p, pn):
    CHECK_UP(B, S, i, j, p, pn)
    CHECK_DOWN(B, S, i, j, p, pn)
    CHECK_LEFT(B, S, i, j, p, pn)
    CHECK_RIGHT(B, S, i, j, p, pn)
    CHECK_UPLEFT(B, S, i, j, p, pn)
    CHECK_DOWNLEFT(B, S, i, j, p, pn)
    CHECK_UPRIGHT(B, S, i, j, p, pn)
    CHECK_DOWNRIGHT(B, S, i, j, p, pn)


@jit(void(NBDTYPE[:, :], NBDTYPE[:, :], NBDTYPE, NBDTYPE), nopython=True)
def CHECK_KING_AS_QUEEN(B, S, i, j):
    CHECK_QUEEN(B, S, i, j, 0, 0)


@jit(void(NBDTYPE[:, :], NBDTYPE[:, :],
          NBDTYPE, NBDTYPE, NBDTYPE, NBDTYPE), nopython=True)
def CHECK_KNIGHT(B, S, i, j, p, pn):
    for (x, y) in KNIGHT_MOVES:
        x += i
        y += j
        if IS_OUTSIDE(x, y):
            continue
        c = B[x, y]
        cn = MAPCELL(x, y)
        S[pn, cn] += 1
        if IS_OCCUPIED(c):
            break


@jit(void(NBDTYPE[:, :], NBDTYPE[:, :],
          NBDTYPE, NBDTYPE, NBDTYPE, NBDTYPE), nopython=True)
def CHECK_W_PAWN(B, S, i, j, p, pn):
    for (x, y) in PAWN_MOVES_W:
        if y == 2 and not IS_W_PAWN_ROW(j):
            continue
        x += i
        y += j
        if IS_OUTSIDE(x, y):
            continue
        c = B[x, y]
        if IS_OCCUPIED(c) and (x == i):
            # We have someone just in front blocking!!
            continue
        else:
            # Space accessible and empty or ready to eat
            cn = MAPCELL(x, y)
            S[pn, cn] += 1
    


@jit(void(NBDTYPE[:, :], NBDTYPE[:, :],
          NBDTYPE, NBDTYPE, NBDTYPE, NBDTYPE), nopython=True)
def CHECK_B_PAWN(B, S, i, j, p, pn):
    for (x, y) in PAWN_MOVES_B:
        if y == -2 and not IS_B_PAWN_ROW(j):
            continue
        x += i
        y += j
        if IS_OUTSIDE(x, y):
            continue
        c = B[x, y]
        if IS_OCCUPIED(c) and (x == i):
            # We have someone just in front blocking!!
            continue
        else:
            # Space accessible and empty or ready to eat
            cn = MAPCELL(x, y)
            S[pn, cn] += 1


@jit(void(NBDTYPE[:, :], NBDTYPE[:, :], NBDTYPE[:],
          NBDTYPE[:], NBDTYPE[:], NBDTYPE), nopython=True)
def CHECK_KING(B, S, A2, king1, king2, pn):
    if king1[0] != INVALID_KING:
        # for (n = 0; n < KING_MOVENO; n += 1 )
        for (x, y) in KING_MOVES:
            x += king1[0]
            y += king1[1]
            cn = MAPCELL(x, y)
            # Cells outside board or accessible by opponent are not accessible
            if IS_OUTSIDE(x, y) or A2[cn] > 0:
                continue
            # Because the other king may not be added to S yet, check it
            if IS_KING_ACCESIBLE(x, y, king2[0], king2[1]):
                continue

            # Add this cell to accesibility of this king
            S[pn, cn] += 1

W_KING_IDX = IMAPNUM(W_KING)
B_KING_IDX = IMAPNUM(B_KING)
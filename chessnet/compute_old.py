# from numpy import nonzero
from numba import jit, void

from .constants import (
    MAXI, MAXJ, IMAPNUM, INVALID_KING,
    IS_EMPTY, IS_OCCUPIED, IS_OUTSIDE,
    KNIGHT_MOVES, KING_MOVES, PAWN_MOVES,
    IS_CASTLE, IS_W_CASTLE,
    IS_BISHOP, IS_W_BISHOP,
    IS_QUEEN, IS_W_QUEEN,
    IS_KNIGHT, IS_W_KNIGHT,
    IS_W_PAWN, IS_B_PAWN,
    IS_W_PAWN_ROW, IS_B_PAWN_ROW,
    IS_W_KING, IS_B_KING, IS_KING_ACCESIBLE,
    NBDTYPE, NPDTYPE,
    )

# from .printers import (
#     print_debug_calcCM1_num,
#     print_debug_calcCM2_num,
#     )

from . import util


logger = util.get_logger('compute')


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
        cm = board_state.cm
        bAccessible = board_state.bAccessible
        wAccessible = board_state.wAccessible
        b = board_state.board
        # pPawns = board_state.pPawns
        promoted = board_state.promoted
    else:
        # The input object is a Match instance
        cm = board_state.cm[moveno, ...]
        bAccessible = board_state.bAccessible[moveno, ...]
        wAccessible = board_state.wAccessible[moveno, ...]
        b = board_state.board[moveno, ...]
        # pPawns = board_state.pPawns[moveno, ...]
        promoted = board_state.promoted[moveno, ...]
    compute_board_matrices(cm, b, bAccessible, wAccessible, promoted)


@jit(void(NBDTYPE[:, :], NBDTYPE[:, :], NBDTYPE[:, :], NBDTYPE[:, :], NBDTYPE[:]), nopython=True)
def compute_board_matrices(cm, b, bAccessible, wAccessible, promoted):

    # Set default king movement for test runs
    bKing = [INVALID_KING, INVALID_KING]
    wKing = [INVALID_KING, INVALID_KING]

    # Exhaustive board search the  to find pieces
    # Numpy way
    # pzs_idx = nonzero(b != EMPTY)
    # pzs_id = b[pzs_idx]
    # pzs_id_num = IMAPNUM(pzs_id)
    # for p, pn, i,j in zip(pzs_id, pzs_id_num, *pzs_idx):
    for i in range(MAXI):
        for j in range(MAXJ):
            # Continue searching the board if cell is empty
            if IS_EMPTY(b[i, j]):
                continue
            # Get piece ID
            p = b[i, j]

            # Get piece's 0-based index for cm matrix
            pn = IMAPNUM(p)

            # Correct type of piece for upgraded pawns
            if promoted[pn] != 0:
                p = promoted[pn]
                pn = IMAPNUM(p)

            # logger.debug(str(pn)+"pn= " + PIECE_NAMES[pn])

            # CASTLE
            if IS_CASTLE(p):
                # if VERBOSITY: prNBDTYPEdebug_calcCM1_num("Castle", pn, i, j)
                # Calculate possible moves
                # 1) DOWN
                # (n = j-1; n >= 0; n--)
                for n in range(j-1, -1, -1):
                    c = b[i, n]
                    if IS_OCCUPIED(c):
                        cn = IMAPNUM(c)
                        # logger.debug(str(cn)+"cn= " + PIECE_NAMES[cn])
                        cm[pn, cn] = 1
                        # if VERBOSITY: prNBDTYPEdebug_calcCM2_num(cn, i, n)
                        break
                    else:
                        # Space accessible but empty
                        if IS_W_CASTLE(p):
                            wAccessible[i, n] += 1
                        else:
                            bAccessible[i, n] += 1

                # 2) UP
                # (n = j+1; n < MAXJ; n += 1)
                for n in range(j+1, MAXJ):
                    c = b[i, n]
                    if IS_OCCUPIED(c):
                        cn = IMAPNUM(c)
                        cm[pn, cn] = 1
                        # logger.debug(str(cn)+"cn= " + PIECE_NAMES[cn])
                        # if VERBOSITY: prNBDTYPEdebug_calcCM2_num(cn, i, n)
                        break
                    else:
                        # Space accessible but empty
                        if IS_W_CASTLE(p):
                            wAccessible[i, n] += 1
                        else:
                            bAccessible[i, n] += 1

                # 3) LEFT
                # (n = i-1; n >= 0; n--)
                for n in range(i-1, -1, -1):
                    c = b[n, j]
                    if IS_OCCUPIED(c):
                        cn = IMAPNUM(c)
                        # logger.debug(str(cn)+"cn= " + PIECE_NAMES[cn])
                        cm[pn, cn] = 1
                        # if VERBOSITY: prNBDTYPEdebug_calcCM2_num(cn, n, j)
                        break
                    else:
                        # Space accessible but empty
                        if IS_W_CASTLE(p):
                            wAccessible[n, j] += 1
                        else:
                            bAccessible[n, j] += 1

                # 4) RIGHT
                # (n = i+1; n < MAXI; n += 1)
                for n in range(i+1, MAXI):
                    c = b[n, j]
                    if IS_OCCUPIED(c):
                        cn = IMAPNUM(c)
                        # logger.debug(str(cn)+"cn= " + PIECE_NAMES[cn])
                        cm[pn, cn] = 1
                        # if VERBOSITY: prNBDTYPEdebug_calcCM2_num(cn, n, j)
                        break
                    else:
                        # Space accessible but empty
                        if IS_W_CASTLE(p):
                            wAccessible[n, j] += 1
                        else:
                            bAccessible[n, j] += 1

            # BISHOP
            elif IS_BISHOP(p):
                # if VERBOSITY: prNBDTYPEdebug_calcCM1_num("Bishop", pn, i, j)

                # 1) DOWN LEFT
                # (n = j-1, m = i-1; n >= 0 && m >= 0; n--, m--)
                m = i
                for n in range(j-1, -1, -1):
                    m -= 1
                    if m < 0:
                        break
                    c = b[m, n]
                    if IS_OCCUPIED(c):
                        cn = IMAPNUM(c)
                        # logger.debug(str(cn)+"cn= " + PIECE_NAMES[cn])
                        cm[pn, cn] = 1
                        # if VERBOSITY: prNBDTYPEdebug_calcCM2_num(cn, m, n)
                        break
                    else:
                        # Space accessible but empty
                        if IS_W_BISHOP(p):
                            wAccessible[m, n] += 1
                        else:
                            bAccessible[m, n] += 1

                # 2) UP LEFT
                # (n = j+1, m = i-1; n < MAXJ && m >= 0; n += 1, m--)
                m = i
                for n in range(j+1, MAXJ):
                    m -= 1
                    if m < 0:
                        break
                    c = b[m, n]
                    if IS_OCCUPIED(c):
                        cn = IMAPNUM(c)
                        # logger.debug(str(cn)+"cn= " + PIECE_NAMES[cn])
                        cm[pn, cn] = 1
                        # if VERBOSITY: prNBDTYPEdebug_calcCM2_num(cn, m, n)
                        break
                    else:
                        # Space accessible but empty
                        if IS_W_BISHOP(p):
                            wAccessible[m, n] += 1
                        else:
                            bAccessible[m, n] += 1

                # 3) DOWN RIGHT
                # for (n = j-1, m = i+1; n >= 0 && m < MAXI; n--, m += 1)
                m = i
                for n in range(j-1, -1, -1):
                    m += 1
                    if m >= MAXI:
                        break
                    c = b[m, n]
                    if IS_OCCUPIED(c):
                        cn = IMAPNUM(c)
                        # logger.debug(str(cn)+"cn= " + PIECE_NAMES[cn])
                        cm[pn, cn] = 1
                        # if VERBOSITY: prNBDTYPEdebug_calcCM2_num(cn, m, n)
                        break
                    else:
                        # Space accessible but empty
                        if IS_W_BISHOP(p):
                            wAccessible[m, n] += 1
                        else:
                            bAccessible[m, n] += 1

                # 4) UP RIGHT
                # for (n = j+1, m = i+1; n < MAXJ && m < MAXI; n += 1, m += 1)
                m = i
                for n in range(j+1, MAXJ):
                    m += 1
                    if m >= MAXI:
                        break
                    c = b[m, n]
                    if IS_OCCUPIED(c):
                        cn = IMAPNUM(c)
                        # logger.debug(str(cn)+"cn= " + PIECE_NAMES[cn])
                        cm[pn, cn] = 1
                        # if VERBOSITY: prNBDTYPEdebug_calcCM2_num(cn, m, n)
                        break
                    else:
                        # Space accessible but empty
                        if IS_W_BISHOP(p):
                            wAccessible[m, n] += 1
                        else:
                            bAccessible[m, n] += 1

            # QUEEN
            elif IS_QUEEN(p):
                # if VERBOSITY: prNBDTYPEdebug_calcCM1_num("Queen", pn, i, j)
                # Calculate possible moves
                # 1) DOWN
                # for (n = j-1; n >= 0; n--)
                for n in range(j-1, -1, -1):
                    c = b[i, n]
                    if IS_OCCUPIED(c):
                        cn = IMAPNUM(c)
                        # logger.debug(str(cn)+"cn= " + PIECE_NAMES[cn])
                        cm[pn, cn] = 1
                        # if VERBOSITY: prNBDTYPEdebug_calcCM2_num(cn, i, n)
                        break
                    else:
                        # Space accessible but empty
                        if IS_W_QUEEN(p):
                            wAccessible[i, n] += 1
                        else:
                            bAccessible[i, n] += 1

                # 2) UP
                # for (n = j+1; n < MAXJ; n += 1)
                for n in range(j+1, MAXJ):
                    c = b[i, n]
                    if IS_OCCUPIED(c):
                        cn = IMAPNUM(c)
                        # logger.debug(str(cn)+"cn= " + PIECE_NAMES[cn])
                        cm[pn, cn] = 1
                        # if VERBOSITY: prNBDTYPEdebug_calcCM2_num(cn, i, n)
                        break
                    else:
                        # Space accessible but empty
                        if IS_W_QUEEN(p):
                            wAccessible[i, n] += 1
                        else:
                            bAccessible[i, n] += 1

                # 3) LEFT
                # for (n = i-1; n >= 0; n--)
                for n in range(i-1, -1, -1):
                    c = b[n, j]
                    if IS_OCCUPIED(c):
                        cn = IMAPNUM(c)
                        # logger.debug(str(cn)+"cn= " + PIECE_NAMES[cn])
                        cm[pn, cn] = 1
                        # if VERBOSITY: prNBDTYPEdebug_calcCM2_num(cn, n, j)
                        break
                    else:
                        # Space accessible but empty
                        if IS_W_QUEEN(p):
                            wAccessible[n, j] += 1
                        else:
                            bAccessible[n, j] += 1

                # 4) RIGHT
                # for (n = i+1; n < MAXI; n += 1)
                for n in range(i+1, MAXI):
                    c = b[n, j]
                    if IS_OCCUPIED(c):
                        cn = IMAPNUM(c)
                        # logger.debug(str(cn)+"cn= " + PIECE_NAMES[cn])
                        cm[pn, cn] = 1
                        # if VERBOSITY: prNBDTYPEdebug_calcCM2_num(cn, n, j)
                        break
                    else:
                        # Space accessible but empty
                        if IS_W_QUEEN(p):
                            wAccessible[n, j] += 1
                        else:
                            bAccessible[n, j] += 1

                # 5) DOWN LEFT
                # for (n = j-1, m = i-1; n >= 0 && m >= 0; n--, m--)
                m = i
                for n in range(j-1, -1, -1):
                    m -= 1
                    if m < 0:
                        break
                    c = b[m, n]
                    if IS_OCCUPIED(c):
                        cn = IMAPNUM(c)
                        # logger.debug(str(cn)+"cn= " + PIECE_NAMES[cn])
                        cm[pn, cn] = 1
                        # if VERBOSITY: prNBDTYPEdebug_calcCM2_num(cn, m, n)
                        break
                    else:
                        # Space accessible but empty
                        if IS_W_QUEEN(p):
                            wAccessible[m, n] += 1
                        else:
                            bAccessible[m, n] += 1

                # 6) UP LEFT
                # for (n = j+1, m = i-1; n < MAXJ && m >= 0; n += 1, m--)
                m = i
                for n in range(j+1, MAXJ):
                    m -= 1
                    if m < 0:
                        break
                    c = b[m, n]
                    if IS_OCCUPIED(c):
                        cn = IMAPNUM(c)
                        # logger.debug(str(cn)+"cn= " + PIECE_NAMES[cn])
                        cm[pn, cn] = 1
                        # if VERBOSITY: prNBDTYPEdebug_calcCM2_num(cn, m, n)
                        break
                    else:
                        # Space accessible but empty
                        if IS_W_QUEEN(p):
                            wAccessible[m, n] += 1
                        else:
                            bAccessible[m, n] += 1

                # 7) DOWN RIGHT
                # for (n = j-1, m = i+1; n >= 0 && m < MAXI; n--, m += 1)
                m = i
                for n in range(j-1, -1, -1):
                    m += 1
                    if m >= MAXI:
                        break
                    c = b[m, n]
                    if IS_OCCUPIED(c):
                        cn = IMAPNUM(c)
                        # logger.debug(str(cn)+"cn= " + PIECE_NAMES[cn])
                        cm[pn, cn] = 1
                        # if VERBOSITY: prNBDTYPEdebug_calcCM2_num(cn, m, n)
                        break
                    else:
                        # Space accessible but empty
                        if IS_W_QUEEN(p):
                            wAccessible[m, n] += 1
                        else:
                            bAccessible[m, n] += 1

                # 8) UP RIGHT
                # for (n = j+1, m = i+1; n < MAXJ && m < MAXI; n += 1, m += 1)
                m = i
                for n in range(j+1, MAXJ):
                    m += 1
                    if m >= MAXI:
                        break
                    c = b[m, n]
                    if IS_OCCUPIED(c):
                        cn = IMAPNUM(c)
                        # logger.debug(str(cn)+"cn= " + PIECE_NAMES[cn])
                        cm[pn, cn] = 1
                        # if VERBOSITY: prNBDTYPEdebug_calcCM2_num(cn, m, n)
                        break
                    else:
                        # Space accessible but empty
                        if IS_W_QUEEN(p):
                            wAccessible[m, n] += 1
                        else:
                            bAccessible[m, n] += 1

            # KNIGHT
            elif IS_KNIGHT(p):
                # if VERBOSITY: prNBDTYPEdebug_calcCM1_num("Knight", pn, i, j)
                # for (n = 0; n < KNIGHT_MOVENO; n += 1 )
                for (x, y) in KNIGHT_MOVES:
                    # x = i + KNIGHT_MOVES[n,0];
                    # y = j + KNIGHT_MOVES[n,1];
                    x += i
                    y += j
                    if IS_OUTSIDE(x, y):
                        continue
                    c = b[x, y]
                    if IS_OCCUPIED(c):
                        cn = IMAPNUM(c)
                        # logger.debug(str(cn)+"cn= " + PIECE_NAMES[cn])
                        cm[pn, cn] = 1
                        # if VERBOSITY: prNBDTYPEdebug_calcCM2_num(cn, x, y)
                    else:
                        # Space accessible but empty
                        if IS_W_KNIGHT(p):
                            wAccessible[x, y] += 1
                        else:
                            bAccessible[x, y] += 1

            # WHITE PAWN
            elif IS_W_PAWN(p):
                # if VERBOSITY: prNBDTYPEdebug_calcCM1_num("White pawn", pn, i, j)
                # for (n = 0; n < PAWN_MOVENO; n += 1 )
                for (x, y) in PAWN_MOVES:
                    # if (PAWN_MOVES[n,1] == 2 && !IS_W_PAWN_ROW(j))
                    if y == 2 and not IS_W_PAWN_ROW(j):
                        continue
                    x += i
                    y += j
                    if IS_OUTSIDE(x, y):
                        continue
                    c = b[x, y]
                    if IS_OCCUPIED(c):
                        if (x == i):
                            # We have someone just in front blocking!!
                            continue
                        cn = IMAPNUM(c)
                        # logger.debug(str(cn)+"cn= " + PIECE_NAMES[cn])
                        cm[pn, cn] = 1
                        # if VERBOSITY: prNBDTYPEdebug_calcCM2_num(cn, x, y)
                    else:
                        # Space accessible but empty
                        wAccessible[x, y] += 1

            # BLACK PAWN
            elif IS_B_PAWN(p):
                # if VERBOSITY: prNBDTYPEdebug_calcCM1_num("Black pawn", pn, i, j)
                # for (n = 0; n < PAWN_MOVENO; n += 1 )
                for (x, y) in PAWN_MOVES:
                    if y == 2 and not IS_B_PAWN_ROW(j):
                        continue
                    x += i
                    y = j - y
                    if IS_OUTSIDE(x, y):
                        continue
                    c = b[x, y]
                    if IS_OCCUPIED(c):
                        if (x == i):
                            # We have someone just in front blocking!!
                            continue
                        cn = IMAPNUM(c)
                        # logger.debug(str(cn)+"cn= " + PIECE_NAMES[cn])
                        cm[pn, cn] = 1
                        # if VERBOSITY: prNBDTYPEdebug_calcCM2_num(cn, x, y)
                    else:
                        # Space accessible but empty
                        bAccessible[x, y] += 1

            elif IS_B_KING(p):
                bKing[0] = i
                bKing[1] = j

            elif IS_W_KING(p):
                wKing[0] = i
                wKing[1] = j

    # WHITE KING
    # if VERBOSITY: prNBDTYPEdebug_calcCM1_num("White king", pn, i, j)

    if wKing[0] != INVALID_KING:
        # for (n = 0; n < KING_MOVENO; n += 1 )
        for (x, y) in KING_MOVES:
            x += wKing[0]
            y += wKing[1]
            if IS_OUTSIDE(x, y) or bAccessible[x, y]:
                continue
            if IS_KING_ACCESIBLE(x, y, bKing[0], bKing[1]):
                continue
            c = b[x, y]
            if IS_OCCUPIED(c):
                cn = IMAPNUM(c)
                # logger.debug(str(cn)+"cn= " + PIECE_NAMES[cn])
                cm[pn, cn] = 1
                # if VERBOSITY: prNBDTYPEdebug_calcCM2_num(cn, x, y)
            else:
                # Space accessible but empty
                wAccessible[x, y] += 1
    # elif VERBOSITY:
    #    print("This must be a test run, skip missing white king evaluation")

    # BLACK KING
    # if VERBOSITY:
    #    prNBDTYPEdebug_calcCM1_num("Black king", pn, i, j)

    if bKing[0] != INVALID_KING:
        # for (n = 0; n < KING_MOVENO; n += 1 )
        for (x, y) in KING_MOVES:
            x += bKing[0]
            y += bKing[1]
            if IS_OUTSIDE(x, y or wAccessible[x, y]):
                continue
            if IS_KING_ACCESIBLE(x, y, wKing[0], wKing[1]):
                continue
            c = b[x, y]
            if IS_OCCUPIED(c):
                cn = IMAPNUM(c)
                # logger.debug(str(cn)+"cn= " + PIECE_NAMES[cn])
                cm[pn, cn] = 1
                # if VERBOSITY: prNBDTYPEdebug_calcCM2_num(cn, x, y)
            else:
                # Space accessible but empty
                bAccessible[x, y] += 1
    # elif VERBOSITY:
    #    print("This must be a test run, skip missing black king evaluation")

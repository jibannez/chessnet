from collections import OrderedDict

from .constants import (
    MAXI, MAXJ, MAXPIECE, IMAPNUM, PIECENO, PIECE_NAMES, IS_EMPTY)

TEXT_WIDTH = 100


def print_debug_calcCM1_num(pzname, pn, i, j):
    print("%d(%s) - %s in position %d:%d\n" %
          (pn, pzname, PIECE_NAMES[pn], i, j))


def print_debug_calcCM2_num(pn, i, j):
    print(" Contact with %d(%s) in %d:%d\n" %
          (pn, PIECE_NAMES[pn], i, j))


def print_match_boards(match):
    for g in range(len(match)+1):
        print("\n\n\n" + TEXT_WIDTH*"=")
        print("\nBoard state at movement %d \n" % g)
        print(TEXT_WIDTH*"=")
        print_board_txt_num(match.B[g, ...])


def print_match_pieces(match):
    for g in range(len(match)+1):
        print("\n\n\n" + TEXT_WIDTH*"=")
        print("\nPieces at movement %d \n" % g)
        print(TEXT_WIDTH*"=")
        print_pieces_num(match.pieces[g, ...])


def print_match_promoted(match):
    for g in range(len(match)+1):
        print("\n\n\n" + TEXT_WIDTH*"=")
        print("\nPromoted pawns at movement %d \n" % g)
        print_promoted_num(match.promoted[g, ...])


def print_match_num(match):
    for g in range(len(match)+1):
        print("\n\n\n" + TEXT_WIDTH*"=")
        print("\nBoard state at movement %d \n" % g)
        print(TEXT_WIDTH*"=")
        print_board_txt_num(match.B[g, ...])
        #print("\nAccesibility matrix of white player\n\n")
        #print_board_num2(match.wAccessible[g, ...])
        #print("\nAccesibility matrix of black player\n\n")
        #print_board_num2(match.bAccessible[g, ...])
        #print("\nConnectivity matrix combined\n\n")
        #print_contact_matrix_num(match.cm[g, ...])
        print("\nActive pieces\n")
        print_pieces_num(match.pieces[g, ...])
        print("\nPromoted pawns\n")
        print_promoted_num(match.promoted[g, ...])


def print_state_num(state):
    print("\n\n\n" + TEXT_WIDTH*"=")
    print(TEXT_WIDTH*"=")
    print_board_txt_num(state.B)
    #print("\nAccesibility matrix of white player\n\n")
    #print_board_num2(state.wAccessible)
    #print("\nAccesibility matrix of black player\n\n")
    #print_board_num2(state.bAccessible)
    #print("\nConnectivity matrix combined\n\n")
    #print_contact_matrix_num(state.cm)
    #print("\nActive pieces\n")
    print_pieces_num(state.pieces)
    print("\nPromoted pawns\n")
    print_promoted_num(state.promoted)


def print_pieces_num(pieces):
    print("-"*TEXT_WIDTH)
    for i in range(MAXPIECE):
        if (i == PIECENO):
            print("#", end='')
        else:
            print("|", end='')
        print(" %1d" % pieces[i], end='')
    print("\n"+"-"*TEXT_WIDTH)


def print_promoted_num(pieces):
    print("-"*TEXT_WIDTH)
    for i in range(MAXPIECE):
        print("|", end='')
        if ((i < MAXI) or (i >= PIECENO and i < PIECENO + MAXI)):
            print("  ", end='')
        else:
            print(" %1d" % pieces[i], end='')
    print("\n"+"-"*TEXT_WIDTH)


def print_board_num2(b):
    # print("     [0] [1] [2] [3] [4] [5] [6] [7] \n")
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    print("     J0  J1  J2  J3  J4  J5  J6  J7  ")
    print("    +---+---+---+---+---+---+---+---+")
    for i in range(MAXI):
        print(" I%d |" % i, end='')
        for j in range(MAXJ):
            if (IS_EMPTY(b[i, j])):
                print("   |", end='')
            else:
                print(" %d |" % b[i, j], end='')
        # print(" %d", MAXI-i)
        print(" %c" % letters[i])
    print("    +---+---+---+---+---+---+---+---+")
    print("      1   2   3   4   5   6   7   8  ")
    # print("      a   b   c   d   e   f   g   h  \n")


def print_board_txt_num(b):
    # print("     [0] [1] [2] [3] [4] [5] [6] [7] \n")
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    print("     J0  J1  J2  J3  J4  J5  J6  J7  ")
    print("    +---+---+---+---+---+---+---+---+")
    for i in range(MAXI):
        print(" I%d |" % i, end='')
        for j in range(MAXJ):
            if (IS_EMPTY(b[i, j])):
                print("   |", end='')
            else:
                pn = IMAPNUM(b[i, j])
                print("%3s|" % PIECE_NAMES[pn], end='')
        print(" %c" % letters[i])
        print("    +---+---+---+---+---+---+---+---+")
    print("      1   2   3   4   5   6   7   8 ")
    # print("      a   b   c   d   e   f   g   h  \n")


def print_contact_matrix_num(cm):
    # n2a_map = get_NUM2ASCII_map()

    print("    ", end='')
    for i in range(MAXPIECE):
        print(" %3s" % PIECE_NAMES[i], end='')

    print("\n    +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+\n")
    for i in range(MAXPIECE):
        # print("%c ", map[i])
        print("%3s |" % PIECE_NAMES[i], end='')
        for j in range(MAXPIECE):
            if IS_EMPTY(cm[i, j]):
                if (j == PIECENO-1):
                    print("   #", end='')
                else:
                    print("   |", end='')
            else:
                if (j == PIECENO-1):
                    print("%2d #" % cm[i, j], end='')
                else:
                    print("%2d |" % cm[i, j], end='')

        print(" %3s " % PIECE_NAMES[i], end='')
        print("\n")
        if (i == PIECENO-1):
            print("    +===+===+===+===+===+===+===+===+===+===+===+===+===+===+===+===+===+===+===+===+===+===+===+===+===+===+===+===+===+===+===+===+\n")
        else:
            print("    +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+\n")

    print("    ", end='')
    for i in range(MAXPIECE):
        print(" %3s" % PIECE_NAMES[i], end='')
    print("\n")


def get_ASCII2NUM_map():
    table = OrderedDict()
    for pz in range(PIECENO):
        # Enconde white pieces ID as 0-15
        table['A'+pz] = pz
        # Enconde black pieces ID as 16-31
        table['a'+pz] = pz+PIECENO
    return table


def get_NUM2ASCII_map():
    table = OrderedDict()
    for pz in range(PIECENO):
        # Enconde white pieces ID as 0-15
        table[pz] = 'A'+pz
        # Enconde black pieces ID as 16-31
        table[pz+PIECENO] = 'a'+pz
    return table

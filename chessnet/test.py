from numpy import array, zeros
from numpy.testing import assert_array_equal

from . import util
from . import parse
from .constants import NPDTYPE
from .compute import compute_match, compute_state, compute_board_matrices
from .classes import MatchSet, Match, BoardState
from .testdata import test_board, test_wAccessible, test_bAccessible, test_cm, test_promoted, test_match
from .printers import print_contact_matrix_num
# def test_numbers_3_4():
#     assert multiply(3,4) == 12


# def test_strings_a_3():
#     assert multiply('a',3) == 'aaa'
def test_match():
    pass


def test_compute_boards():
    for (board, wAccessible, bAccessible, cm, promoted) in zip(test_board, test_wAccessible, test_bAccessible, test_cm, test_promoted):
        # Arrays that will store the computed values
        bs = BoardState(board)
        bs.compute()

        #cm_ = zeros(cm.shape, dtype=NPDTYPE)
        X = zeros(bs.X.shape, dtype=NPDTYPE)
        S = zeros(bs.S.shape, dtype=NPDTYPE)
        Kw = zeros(bs.wKing_as_Queen.shape, dtype=NPDTYPE)
        Kb = zeros(bs.bKing_as_Queen.shape, dtype=NPDTYPE)
        # bAccessible_ = zeros(bAccessible.shape, dtype=NPDTYPE)
        # wAccessible_ = zeros(wAccessible.shape, dtype=NPDTYPE)
        promoted_ = zeros(promoted.shape, dtype=NPDTYPE)

        # Perform computation
        compute_board_matrices(board, X, S, promoted_,Kw,Kb)

        # Assert that expected values are equal to computed values
        print_contact_matrix_num(cm)
        print("="*70)
        print_contact_matrix_num(bs.cm)
        print("="*70)
        print_contact_matrix_num(abs(bs.cm-cm))
        assert_array_equal(cm.sum(), bs.cm.sum())
        assert_array_equal(cm, bs.cm)
        assert_array_equal(X, bs.X)
        assert_array_equal(S, bs.S)
        assert_array_equal(Kw, bs.wKing_as_Queen)
        assert_array_equal(Kb, bs.bKing_as_Queen)
        # assert_array_equal(bAccessible, bAccessible_)
        #assert_array_equal(wAccessible, wAccessible_)
        assert_array_equal(promoted, promoted_)


def test_compute_boards_initial():
    # Sample test of a single board state. This is already tested in the first board from testdata import

    # Well known expecte values
    board = array([
       [1,  9,  0,  0,  0,  0, 25, 17],
       [2, 10,  0,  0,  0,  0, 26, 18],
       [3, 11,  0,  0,  0,  0, 27, 19],
       [4, 12,  0,  0,  0,  0, 28, 20],
       [5, 13,  0,  0,  0,  0, 29, 21],
       [6, 14,  0,  0,  0,  0, 30, 22],
       [7, 15,  0,  0,  0,  0, 31, 23],
       [8, 16,  0,  0,  0,  0, 32, 24]], dtype=NPDTYPE)

    wAccessible = array([
       [0, 0, 3, 1, 0, 0, 0, 0],
       [0, 0, 3, 1, 0, 0, 0, 0],
       [0, 0, 4, 1, 0, 0, 0, 0],
       [0, 0, 3, 1, 0, 0, 0, 0],
       [0, 0, 3, 1, 0, 0, 0, 0],
       [0, 0, 4, 1, 0, 0, 0, 0],
       [0, 0, 3, 1, 0, 0, 0, 0],
       [0, 0, 3, 1, 0, 0, 0, 0]], dtype=NPDTYPE)

    bAccessible = array([
       [0, 0, 0, 0, 1, 3, 0, 0],
       [0, 0, 0, 0, 1, 3, 0, 0],
       [0, 0, 0, 0, 1, 4, 0, 0],
       [0, 0, 0, 0, 1, 3, 0, 0],
       [0, 0, 0, 0, 1, 3, 0, 0],
       [0, 0, 0, 0, 1, 4, 0, 0],
       [0, 0, 0, 0, 1, 3, 0, 0],
       [0, 0, 0, 0, 1, 3, 0, 0]], dtype=NPDTYPE)

    cm = array([
       [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
       [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], dtype=NPDTYPE)

    promoted = array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=NPDTYPE)

    # Arrays that will store the computed values
    cm_ = zeros(cm.shape, dtype=NPDTYPE)
    bAccessible_ = zeros(bAccessible.shape, dtype=NPDTYPE)
    wAccessible_ = zeros(wAccessible.shape, dtype=NPDTYPE)
    promoted_ = zeros(promoted.shape, dtype=NPDTYPE)

    # Perform computation
    compute_board_matrices(cm_, board, bAccessible_, wAccessible_, promoted_)

    # Assert that expected values are equal to computed values
    assert_array_equal(cm, cm_)
    assert_array_equal(bAccessible, bAccessible_)
    assert_array_equal(wAccessible, wAccessible_)
    assert_array_equal(promoted, promoted_)

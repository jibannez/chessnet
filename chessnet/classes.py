from numpy import (
    array, zeros, ones, matrix, matmul, dot, vstack, hstack, flipud, fliplr)

from . import util
from . import compute
from . import printers
import math
import pandas as pd


from .parse import parse_match_from_movlst

from .constants import (
    testmultifilename, testfilename, W_KING_IDX, B_KING_IDX,
    BOARDSZ, MAXI, MAXJ, MAXPIECES, PIECENO, NPDTYPE, PAWNNO, UCI_OFFSET,
    )

import matplotlib.pyplot as plt

U = matrix(ones((1, PIECENO)))
V = matrix(ones((1, BOARDSZ)))

vector_names = [
    'pieceno',
    'accesible',
    'Dconnectance',
    'Aconnectance',
    'Iconnectance',
    'Cconnectance',
    'king_accesibility',
    'defense_on_king',
    'attack_on_king',
    ]

matrix_names = ['B', 'S', 'X', 'Sw', 'Sb', 'Xw', 'Xb', 'Dw', 'Db',
                'Aw', 'Ab', 'Iw', 'Ib', 'Cw', 'Cb']


class MatchSet:

    def __init__(self, pgn_fname=None, png_dir=None, recursive=False):
        """Constructor of class MatchSet. This object encapsulates
        the metadata, movements, and states of a set of matches especified
        in the arguments.

        INPUT:
            pgn_fname: (str, None)
                path to a multi match png file.
            pgn_dir: (str, None)
                path to a directory with multiple pgn files.
            recursive: (bool)
                if a directory was provided, this flag determines
                the recursive exploration of the directory.
        """
        # Initialize instance logger
        self.logger = util.get_logger('MatchSet')
        # Load match set with the method required by the input arguments
        # !TODO: A hibrid loader, with multiple files in a path each of which
        # can be either single or multimatch pgn files.
        if pgn_fname is not None:
            # We have a multi match pgn
            self.logger.info('Loading multi match pgn file: ' + pgn_fname)
            self._movements_set, self._metadata_set, self._game_set =\
                util.load_multipgn_file(pgn_fname)
        elif png_dir is not None:
            # We have a directory with multiple one-match pgn files
            self.logger.info('Loading multi pgn directory: ' + pgn_fname)
            self._movements_set, self._metadata_set, self._game_set =\
                util.load_multipgn_directory(pgn_fname, recursive)
        else:
            # If no input is provided, just load a default test file
            self.logger.info(
                'Loading default test multi match pgn file: ' + testmultifilename)
            self._movements_set, self._metadata_set, self._game_set =\
                util.load_multipgn_file(testmultifilename)

        # Once the pgn information has been loaded, create Match instances out
        # of each of the matches present.
        L = len(self._movements_set)
        self._match_set = list()
        self.invalid = list()
        for i, (m, h) in enumerate(zip(self._movements_set, self._metadata_set)):
            match = Match(m, (i+1, L), metadata=h)
            # If everything went fine, append match and continue
            if match.is_valid_match:
                self._match_set.append(match)
            else:
                self.invalid.append(match)

    def __getitem__(self, val):
        """Specialized item getter of class MatchSet. It returns the
        index specified by val argument from the private list of matchs

        INPUT:
            val: (int)
                index of the desired board state in the match.
        """
        return self._match_set[val]

    def __len__(self):
        """Specialized class length, equal to the total number of matches
        """
        return len(self._match_set)

    def __str__(self):
        """Specialized class string representation, calls iteratively the
        printers of Match instances in the MatchSet.
        """
        for match in self:
            print(match)
            
    def export_to_csv(self):
      for i,match in enumerate(self) : match.ToPandas(None).to_csv(str(i).zfill(math.trunc(math.log10(len(self)))+1)+'.csv',index=False) 

    @property
    def B(self):
        return [match.B for match in self]

    @property
    def S(self):
        return [match.S for match in self]

    @property
    def X(self):
        return [match.X for match in self]

    @property
    def Sw(self):
        return [match.Sw for match in self]

    @property
    def Sb(self):
        return [match.Sb for match in self]

    @property
    def Xw(self):
        return [match.Xw for match in self]

    @property
    def Xb(self):
        return [match.Xb for match in self]

    @property
    def Dw(self):
        # Defensive network
        #return self.Xw*self.Sw.transpose()
        return [match.Dw for match in self]

    @property
    def Db(self):
        # Defensive network for black
        #return self.Xb*self.Sb.transpose()
        return [match.Db for match in self]

    @property
    def Iw(self):
        # Influence network for white
        #return self.Sw*self.Sw.transpose()
        return [match.Iw for match in self]

    @property
    def Ib(self):
        # Influence network for black
        #return self.Sb*self.Sb.transpose()
        return [match.Ib for match in self]

    @property
    def Aw(self):
        # Attack network for white
        #return self.Sw*self.Xb.transpose()
        return [match.Aw for match in self]

    @property
    def Ab(self):
        # Attack network for black
        #return self.Sb*self.Xa.transpose()
        return [match.Ab for match in self]

    @property
    def Cw(self):
        # Clash network for white
        #return self.Sw*self.Sb.transpose()
        return [match.Cw for match in self]

    @property
    def Cb(self):
        # Clash network for black
        #return self.Sb*self.Sw.transpose()
        return [match.Cb for match in self]

    @property
    def cm(self):
        return [match.cm for match in self]

    @property
    def w_pieceno(self):
        #return U*self.Xw*V.transpose()
        return [match.w_pieceno for match in self]

    @property
    def b_pieceno(self):
        #return U*self.Xb*V.transpose()
        return [match.b_pieceno for match in self]

    @property
    def w_accesible(self):
        #return U*self.Sw*V.transpose()
        return [match.w_accesible for match in self]

    @property
    def b_accesible(self):
        #return U*self.Sb*V.transpose()
        return [match.b_accesible for match in self]

    @property
    def w_Dconnectance(self):
        #return U*self.Dw*U.transpose()
        return [match.w_Dconnectance for match in self]

    @property
    def b_Dconnectance(self):
        #return U*self.Db*U.transpose()
        return [match.b_Dconnectance for match in self]

    @property
    def w_Iconnectance(self):
        #return U*self.Iw*U.transpose()
        return [match.w_Iconnectance for match in self]

    @property
    def b_Iconnectance(self):
        #return U*self.Ib*U.transpose()
        return [match.b_Iconnectance for match in self]

    @property
    def w_Aconnectance(self):
        #return U*self.Aw*U.transpose()
        return [match.w_Aconnectance for match in self]

    @property
    def b_Aconnectance(self):
        #return U*self.Ab*U.transpose()
        return [match.b_Aconnectance for match in self]

    @property
    def w_king_accesibility(self):
        #return matmul(matmul(U, self.Ab), U.transpose())).squeeze()
        return [match.w_king_accesibility for match in self]

    @property
    def b_king_accesibility(self):
        #return matmul(matmul(U, self.Aw), U.transpose())).squeeze()
        return [match.w_defense_on_king for match in self]

    @property
    def w_defense_on_king(self):
        #return (matmul(matmul(U, self.Sw), self.Kw)).squeeze() / self.Kw.sum())
               #matmul(matmul(U, self.Kw), V.transpose())).squeeze())
        return [match.w_defense_on_king for match in self]

    @property
    def b_defense_on_king(self):
        #return (matmul(matmul(U, self.Sb), self.Kb)).squeeze() / self.Kb.sum())
               #matmul(matmul(U, self.Kb), V.transpose())).squeeze())
        return [match.b_defense_on_king for match in self]

    @property
    def w_attack_on_king(self):
        #return matmul(matmul(U, self.Sw), self.Kb)).squeeze()
        return [match.w_attack_on_king for match in self]

    @property
    def b_attack_on_king(self):
        #return matmul(matmul(U, self.Sb), self.Kw)).squeeze()
        return [match.b_attack_on_king for match in self]

    @property
    def pieces(self):
        return [match.pieces for match in self]

    @property
    def promoted(self):
        return [match.promoted for match in self]

    def compute(self):
        """Computes all the board states in every match of the match set.
        This should not usually be called because Match instances automatically
        run this computation on initialization, but for testing changes
        maybe handy to be able to recompute everything.
        """
        for i, match in enumerate(self):
            msg = "Computing boards for match number %d" % (i + 1)
            self.logger.info(msg)
            match.compute()

    def plot(self, vname):
        n = len(self)
        [r, c] = util.get_closest_pair(n)
        fig = plt.figure()
        for i, match in enumerate(self):
            ax = fig.add_subplot(r, c, i+1)
            match.plot(vname, ax)
            ax.set_xticks([])
            ax.set_yticks([])
        fig.suptitle(vname, fontsize=20)

    def plot_all(self):
        for vname in vector_names:
            self.plot(vname)


class Match:

    def __init__(self, init_param=testfilename, idx=None, metadata=None):
        """Constructor of class Match. This object encapsulates
        the metadata, movements, and board and matrix states
        for a set of movements especified in init_param.

        INPUT:
            init_param: (str,list(str))
                either a list of parsed movements, or a
                string with a path to a pgn file to be parsed.

            idx: (int, None)
                an index to order the match within a MatchSet
        """
        # self.init_match(init_param, idx, metadata)
        # self.init_arrays()
        # self.parse_match()
        # self.compute()
        # self.is_valid_match = True
        try:
            self.init_match(init_param, idx, metadata)
            self.init_arrays()
            self.parse_match()
            self.compute()
            self.is_valid_match = True
        except:
            self.is_valid_match = False

    def __getitem__(self, val):
        """ Get item special method implements specialized access to
        objects properties. In this case, it behabes like a list:
        it takes an integer value as index and returns a BoardState
        instance created on the fly with the information contained
        in the global match's arrays. The particular behavior numpy slices
        as mere views without no coping makes this object creating relatively
        cheap for the few situations where inspecting an individual board
        state is required. Therefore, any modification to the arrays in the
        board state will be propageted back to the original arrays in match
        instance.

        INPUT:
            val: (int)
                index of the desired board state in the match.
        """
        board = BoardState()
        board.B = self.B[val, ...]
        board.X = self.X[val, ...]
        board.S = self.S[val, ...]
        board.Kw = self.Kw[val, ...]
        board.Kb = self.Kb[val, ...]
        board.pieces = self.pieces[val, ...]
        board.promoted = self.promoted[val, ...]
        # board.pPawns = self.pPawns[val, ...]
        if val > 0:
            board.ucimovement = self.ucimovements[val]
            board.movement = self.movements[val]
        return board

    def __str__(self):
        """Custom class string generator
        """
        msg = 40*"-" + "\n"
        if self.idx is not None:
            msg += "\tMetadata for match %d\n" % self.idx
        else:
            msg += "\tMetadata for current match\n"
        msg += 40*"-" + "\n"
        for k, v in self.metadata.items():
            msg += "\t%10s  %20s\n" % (k, v)
        return msg

    def __len__(self):
        """Custom object length, it is equal to number of movements.
        It is important to remember that there is always one more board
        for any number of movements.
        """
        return len(self.ucimovements)

    def plot(self, vname, ax=None):
        b = getattr(self, 'b_'+vname)
        w = getattr(self, 'w_'+vname)
        # if b.ndim >= 1:
        #    print('This property is network!!')
        if ax is None:
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1)
            do_label = True
        else:
            do_label = False
        # ~ ax.hold('on')
        if self.winner[0] == 'White':
            wstyle = 'r'
            bstyle = 'k--'
        elif self.winner[0] == 'Black':
            wstyle = 'r--'
            bstyle = 'k'
        else:
            wstyle = 'r--'
            bstyle = 'k--'
        ax.plot(w, wstyle)
        ax.plot(b, bstyle)
        if do_label:
            ax.legend(['white','black'])
            ax.set_title('-'.join(self.winner))

    def plot_all(self):
        n = len(vector_names)
        [r, c] = util.get_closest_pair(n)
        fig = plt.figure()
        fig.suptitle('-'.join(self.winner), fontsize=20)
        for i, vname in enumerate(vector_names):
            ax = fig.add_subplot(r, c, i+1)
            self.plot(vname, ax)
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_title(vname)
        # ax.legend(['white','black'])

    def ToPandas(self, vec):
        var_dict={}
        var_names=vector_names if vec is None else vec
        
        for var in var_names:
            var_dict['b_'+var]= getattr(self, 'b_'+var)
            var_dict['w_'+var]= getattr(self, 'w_'+var)
        df=pd.DataFrame(var_dict)
        df['winner']=self.winner[0]
        
        return df
         
    @property
    def winner(self):
        if self.metadata['Result'] == '1-0':
            return ('White', self.metadata['White'])
        elif self.metadata['Result'] == '0-1':
            return ('Black', self.metadata['Black'])
        else:
            return ('tables', 'None')

    @property
    def Xw(self):
        return self.X[:, :PIECENO, :]

    @property
    def Xb(self):
        return self.X[:, PIECENO:, :]
        #return self.X[:, -1:15:-1, :]

    @property
    def Sw(self):
        return self.S[:, :PIECENO, :]

    @property
    def Sb(self):
        return self.S[:, PIECENO:, :]
        #return self.S[:, -1:15:-1, :]

    @property
    def Dw(self):
        # Defensive network
        #return self.Xw*self.Sw.transpose()
        return array([board.Dw for board in self])

    @property
    def Db(self):
        # Defensive network for black
        #return self.Xb*self.Sb.transpose()
        return array([board.Db for board in self])

    @property
    def Iw(self):
        # Influence network for white
        #return self.Sw*self.Sw.transpose()
        return array([board.Iw for board in self])

    @property
    def Ib(self):
        # Influence network for black
        #return self.Sb*self.Sb.transpose()
        return array([board.Ib for board in self])

    @property
    def Aw(self):
        # Attack network for white
        #return self.Sw*self.Xb.transpose()
        return array([board.Aw for board in self])

    @property
    def Ab(self):
        # Attack network for black
        #return self.Sb*self.Xa.transpose()
        return array([board.Ab for board in self])

    @property
    def Cw(self):
        # Clash network for white
        #return self.Sw*self.Sb.transpose()
        return array([board.Cw for board in self])

    @property
    def Cb(self):
        # Clash network for black
        #return self.Sb*self.Sw.transpose()
        return array([board.Cb for board in self])

    @property
    def cm(self):
        # Clash network for black
        #return self.Sb*self.Sw.transpose()
        return array([board.cm for board in self])

    @property
    def w_pieceno(self):
        #return U*self.Xw*V.transpose()
        return array([board.w_pieceno for board in self])

    @property
    def b_pieceno(self):
        #return U*self.Xb*V.transpose()
        return array([board.b_pieceno for board in self])

    @property
    def w_accesible(self):
        #return U*self.Sw*V.transpose()
        return array([board.w_accesible for board in self])

    @property
    def b_accesible(self):
        #return U*self.Sb*V.transpose()
        return array([board.b_accesible for board in self])

    @property
    def w_Dconnectance(self):
        #return U*self.Dw*U.transpose()
        return array([board.w_Dconnectance for board in self])

    @property
    def b_Dconnectance(self):
        #return U*self.Db*U.transpose()
        return array([board.b_Dconnectance for board in self])

    @property
    def w_Iconnectance(self):
        #return U*self.Iw*U.transpose()
        return array([board.w_Iconnectance for board in self])

    @property
    def b_Iconnectance(self):
        #return U*self.Ib*U.transpose()
        return array([board.b_Iconnectance for board in self])

    @property
    def w_Aconnectance(self):
        #return U*self.Aw*U.transpose()
        return array([board.w_Aconnectance for board in self])

    @property
    def b_Aconnectance(self):
        #return U*self.Ab*U.transpose()
        return array([board.b_Aconnectance for board in self])

    @property
    def w_Cconnectance(self):
        #return U*self.Dw*U.transpose()
        return array([board.w_Cconnectance for board in self])

    @property
    def b_Cconnectance(self):
        #return U*self.Db*U.transpose()
        return array([board.b_Cconnectance for board in self])

    @property
    def w_king_accesibility(self):
        #return array(matmul(matmul(U, self.Ab), U.transpose())).squeeze()
        return array([board.w_king_accesibility for board in self])

    @property
    def b_king_accesibility(self):
        #return array(matmul(matmul(U, self.Aw), U.transpose())).squeeze()
        return array([board.w_defense_on_king for board in self])

    @property
    def w_defense_on_king(self):
        #return (array(matmul(matmul(U, self.Sw), self.Kw)).squeeze() / self.Kw.sum())
               #array(matmul(matmul(U, self.Kw), V.transpose())).squeeze())
        return array([board.w_defense_on_king for board in self])

    @property
    def b_defense_on_king(self):
        #return (array(matmul(matmul(U, self.Sb), self.Kb)).squeeze() / self.Kb.sum())
               #array(matmul(matmul(U, self.Kb), V.transpose())).squeeze())
        return array([board.b_defense_on_king for board in self])

    @property
    def w_attack_on_king(self):
        #return array(matmul(matmul(U, self.Sw), self.Kb)).squeeze()
        return array([board.w_attack_on_king for board in self])

    @property
    def b_attack_on_king(self):
        #return array(matmul(matmul(U, self.Sb), self.Kw)).squeeze()
        return array([board.b_attack_on_king for board in self])

    def init_match(self, init_param, idx, metadata):
        # Init instance logger
        self.logger = util.get_logger('Match')
        # Set index print if any
        if idx is not None:
            if isinstance(idx, int):
                self.logger.info('Creating Match instance %d ' % idx)
                self.idx = idx
            elif isinstance(idx, tuple):
                self.logger.info('Creating Match instance %d of %d ' % idx)
                self.idx = idx[0]
                self.total_matches = idx[1]
            else:
                print(idx)

        else:
            self.idx = None
        # Select appropiate initialization depending on the init_param
        if isinstance(init_param, str):
            # We have a file name, load the movements
            self.filename = init_param
            self.load_match(init_param)
        elif isinstance(init_param, list):
            # We have a list of movements
            self.filename = None
            self.ucimovements = init_param
            self.metadata = metadata
        else:
            raise ValueError('Unknown initialization parameter')

    def init_arrays(self, movements=None):
        """
        Initialize to zero all the data stuctures, parses uci
        movements if any, and attemps to fill the arrays parsing
        the board states from the sequence of movements.

        INPUT:
            movements (lst(str))
        """
        if movements is not None:
            self.ucimovements = movements

        L = len(self.ucimovements)+1
        self.B = zeros((L, MAXI, MAXJ), dtype=NPDTYPE)
        self.X = zeros((L, MAXPIECES, BOARDSZ), dtype=NPDTYPE)
        self.S = zeros((L, MAXPIECES, BOARDSZ), dtype=NPDTYPE)
        self.Kw = zeros((L, BOARDSZ), dtype=NPDTYPE)
        self.Kb = zeros((L, BOARDSZ), dtype=NPDTYPE)
        self.pieces = zeros((L, MAXPIECES), dtype=NPDTYPE)
        self.promoted = zeros((L, MAXPIECES), dtype=NPDTYPE)
        self.movements = self.parse_ucimovements(self.ucimovements)

    def parse_match(self, movements=None):
        if movements is not None:
            parse_match_from_movlst(self, movements)
        else:
            parse_match_from_movlst(self, self.movements)

    def load_match(self, fname):
        self.ucimovements, self.metadata , self.game= util.load_pgn(fname)

    def parse_ucimovements(self, movements):
        # mlist = list()
        # for l in movements:
        #     print(l)
        #     mlist.append([*l][:4])
        # return array(mlist) - UCI_OFFSET
        return array([[*l][:4] for l in movements]) - UCI_OFFSET

    def compute(self):
        compute.compute_match(self)

    def print(self, n=None):
        if n:
            printers.print_board_txt_num(self[n])
        else:
            printers.print_match_num(self)

    def print_boards(self, n=None):
        if n:
            printers.print_board_txt_num(self.B[n, ...])
        else:
            printers.print_match_boards(self)


class BoardState:

    def __init__(self, board=None, movement=None):
        """Constructor of class Match. This object encapsulates
        the metadata, movements, and board and matrix states
        for a set of movements especified in init_param.

        INPUT:
            init_param: (str,list(str))
                either a list of parsed movements, or a
                string with a path to a pgn file to be parsed.

            idx: (int, None)
                an index to order the match within a MatchSet
        """
        # Init instance logger
        self.logger = util.get_logger('BoardState')
        self.init_board(board, movement)

    def init_board(self, board=None, movement=None):
        """
        """
        self.set_board(board)
        self.ucimovement = movement
        if movement is not None and len(movement) >= 4:
            self.movement = self.parse_ucimovement(movement)
        else:
            self.movement = None

        self.X = zeros((MAXPIECES, BOARDSZ), dtype=NPDTYPE)
        self.S = zeros((MAXPIECES, BOARDSZ), dtype=NPDTYPE)
        self.pieces = zeros((1, MAXPIECES), dtype=NPDTYPE)
        self.promoted = zeros((1, MAXPIECES), dtype=NPDTYPE)
        self.Kw = zeros((1, BOARDSZ), dtype=NPDTYPE)
        self.Kb = zeros((1, BOARDSZ), dtype=NPDTYPE)

    def set_board(self, board=None):
        # This is mostly intended for testing, so we only ask for a board matrix,
        # and assume that all the other matrices (promoted, pieces, etc) are at the
        # initial state. Actually, we don't really care about these, the point
        # here is to know the CM and Accesibility matrices of a certain
        # board configuration.
        if board is None:
            self.B = zeros((MAXI, MAXJ), dtype=NPDTYPE)
        elif isinstance(board, (str, bytes)):
            # This should be an epd encoded board
            self.B = util.parse_epd_board(board)
            self.logger.info('Parsed EPD board:')
            self.logger.info(board)
            self.logger.info(self.board)
        else:
            self.B = board

    def parse_ucimovement(self, movement):
        """
        """
        return array(*movement) - UCI_OFFSET

    @property
    def cm(self):
        # Contact matrix
        #return vstack([hstack([self.Dw, fliplr(self.Aw)]),
        #               hstack([flipud(self.Ab), flipud(fliplr(self.Db))])])
        return vstack([hstack([self.Dw, self.Aw]),
                       hstack([self.Ab, self.Db])])

    @property
    def Xw(self):
        # Extended board state for white
        return self.X[:PIECENO, :]

    @property
    def Xb(self):
        # Extended board state for black
        return self.X[PIECENO:, :]
        #return self.X[-1:15:-1, :]

    @property
    def Sw(self):
        # Accesible network
        return self.S[:PIECENO, :]

    @property
    def Sb(self):
        # Accesible network for black
        return self.S[PIECENO:, :]
        # return self.S[-1:15:-1, :]

    @property
    def Dw(self):
        # Defensive network
        return matmul(self.Sw, self.Xw.transpose()).transpose()

    @property
    def Db(self):
        # Defensive network for black
        return matmul(self.Sb, self.Xb.transpose()).transpose()

    @property
    def Iw(self):
        # Influence network for white
        return matmul(self.Sw, self.Sw.transpose()).transpose()

    @property
    def Ib(self):
        # Influence network for black
        return matmul(self.Sb, self.Sb.transpose()).transpose()

    @property
    def Aw(self):
        # Attack network for white
        return matmul(self.Sw, self.Xb.transpose())

    @property
    def Ab(self):
        # Attack network for black
        return matmul(self.Sb, self.Xw.transpose())

    @property
    def Cw(self):
        # Clash network for white
        return matmul(self.Sw, self.Sb.transpose())

    @property
    def Cb(self):
        # Clash network for black
        return matmul(self.Sb, self.Sw.transpose())

    @property
    def w_pieceno(self):
        return array(matmul(matmul(U, self.Xw), V.transpose())).squeeze()

    @property
    def b_pieceno(self):
        return array(matmul(matmul(U, self.Xb), V.transpose())).squeeze()

    @property
    def w_accesible(self):
        return array(matmul(matmul(U, self.Sw), V.transpose())).squeeze()

    @property
    def b_accesible(self):
        return array(matmul(matmul(U, self.Sb), V.transpose())).squeeze()

    @property
    def w_Dconnectance(self):
        return array(matmul(matmul(U, self.Dw), U.transpose())).squeeze()

    @property
    def b_Dconnectance(self):
        return array(matmul(matmul(U, self.Db), U.transpose())).squeeze()

    @property
    def w_Iconnectance(self):
        return array(matmul(matmul(U, self.Iw), U.transpose())).squeeze()

    @property
    def b_Iconnectance(self):
        return array(matmul(matmul(U, self.Ib), U.transpose())).squeeze()

    @property
    def w_Aconnectance(self):
        return array(matmul(matmul(U, self.Aw), U.transpose())).squeeze()

    @property
    def b_Aconnectance(self):
        return array(matmul(matmul(U, self.Ab), U.transpose())).squeeze()

    @property
    def w_Cconnectance(self):
        return array(matmul(matmul(U, self.Cw), U.transpose())).squeeze()

    @property
    def b_Cconnectance(self):
        return array(matmul(matmul(U, self.Cb), U.transpose())).squeeze()

    @property
    def w_king_accesibility(self):
        #return array(matmul(self.Sw[W_KING_IDX,:].reshape((1, BOARDSZ)), V.transpose())).squeeze()
        return self.S[W_KING_IDX,:].sum()

    @property
    def b_king_accesibility(self):
        #return array(matmul(self.Sb[B_KING_IDX,:].reshape((1,BOARDSZ)), V.transpose())).squeeze()
        return self.S[B_KING_IDX,:].sum()

    @property
    def w_defense_on_king(self):
        return (array(matmul(matmul(U, self.Sw), self.Kw)).squeeze() / self.Kw.sum())

    @property
    def b_defense_on_king(self):
        return (array(matmul(matmul(U, self.Sb), self.Kb)).squeeze() / self.Kb.sum())

    @property
    def w_attack_on_king(self):
        return array(matmul(matmul(U, self.Sw), self.Kb)).squeeze()

    @property
    def b_attack_on_king(self):
        return array(matmul(matmul(U, self.Sb), self.Kw)).squeeze()

    def compute(self):
        compute.compute_state(self)

    def print(self):
        printers.print_state_num(self)

    def print_board(self):
        printers.print_board_txt_num(self.B)

import os
import chess
import chess.pgn
import logging
import time
import math

from . import constants as K


def get_logger(name, level=logging.INFO, use_console=True, use_logfile=False):
    """Returns a new logger instance configured for the calling context

    INPUT:
        name: (str)
            Text string that will identify this logger instance.

        level: (int)
            default logging level.

        use_console: (bool)
            Activates console logging.

        use_logfile: (bool)
            Activates logfile logging.
    """
    # Define formats for logging
    LOG_MSGFORMAT = '%(asctime)-15s %(levelname)s -> %(name)s: %(message)s'
    LOG_DATEFORMAT = '%Y/%m/%d %I:%M:%S %p'

    # Set the required loggers
    loggers = list()
    if use_logfile:
        DATEFMT = "%Y-%m-%d_%H-%M"
        CURRDATE = time.strftime(DATEFMT)
        # create file handler which logs even debug messages
        fh = logging.FileHandler('pychess_'+CURRDATE+'.log', mode='w')
        fh.setLevel(level)
        loggers.append(fh)

    if use_console:

        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(level)
        loggers.append(ch)

    # Get basic handler properties
    logging.basicConfig(
        level=logging.DEBUG,
        format=LOG_MSGFORMAT,
        datefmt=LOG_DATEFORMAT,
        handlers=loggers,
        )

    return logging.getLogger(name)

    # create formatter and add it to the handlers
    # formatter = logging.Formatter(LOG_MSGFORMAT, datefmt=LOG_DATEFORMAT)
    # fh.setFormatter(formatter)
    # ch.setFormatter(formatter)

    # # add the handlers to the logger
    # logger.addHandler(fh)
    # logger.addHandler(ch)


def get_files_in_dir(inpath):
    """
    """
    onlyfiles = list()
    for f in os.listdir(inpath):
        tmppath = os.path.join(inpath, f)
        if os.path.isfile(tmppath):
            onlyfiles.append(tmppath)
    return onlyfiles


def get_files_in_dir_recursive(inpath):
    """
    """
    onlyfiles = list()
    for (dirpath, dirnames, filenames) in os.walk(inpath):
        onlyfiles.extend([os.path.join(dirpath, fname) for fname in filenames])
    return onlyfiles


def load_pgn(fname=K.testfilename):
    """
    """
    with open(fname) as pgnfile:
        game = chess.pgn.read_game(pgnfile)
        metadata = game.headers
        movements = [board.uci().encode() for board in game.mainline()]
    return movements, metadata, game


def load_multipgn_file(fname=K.testmultifilename):
    """
    """
    mov_lst = list()
    meta_lst = list()
    game_lst = list()
    
    with open(fname) as pgnfile:
        while True:
            game = chess.pgn.read_game(pgnfile)
            if game is not None:
                meta_lst.append(game.headers)
                movements = [b.uci().encode() for b in game.mainline()]
                mov_lst.append(movements)
                game_lst.append(game)
            else:
                break
                
    return mov_lst, meta_lst, game_lst


def load_multipgn_directory(inpath=K.testdirectory, recursive=False):
    """
    """
    if recursive:
        fnames = get_files_in_dir_recursive(inpath)
    else:
        fnames = get_files_in_dir(inpath)

    mov_lst  = list()
    meta_lst = list()
    game_lst = list()
    for fname in fnames:
        with open(fname) as pgnfile:
            while True:
                game = chess.pgn.read_game(pgnfile)
                game_lst.append(game)
                if game is not None:
                    meta_lst.append(game.headers)
                    movements = [b.uci().encode() for b in game.main_line()]
                    mov_lst.append(movements)
                else:
                    break
    return mov_lst, meta_lst,game_lst

def get_closest_pair(n):
    #return (5, 12)
    root = math.ceil(math.sqrt(n))
    #p0 = root * root
    p1 = (root - 1) * root
    if p1 < n:
        return (root, root)
    else:
        return (root, root-1)

# def parse_epd_board(board):
#     epd_symbols = 'RNBKQPrnbkqp'
#     overlap_map = {
#         b'Z': b'B',
#         b'Y': b'K',
#         b'X': b'P',
#         b'V': b'N',
#         b'z': b'b',
#         b'y': b'k',
#         b'x': b'p',
#         b'v': b'n',
#     }

#     epd_map = {
#         'R': (b'A', b'H'),
#         'N': (b'Z', b'G'),
#         'B': (b'C', b'F'),
#         'K': (b'D',),
#         'Q': (b'E', b'E', b'E', b'E', b'E', b'E', b'E', b'E', b'E'),
#         'P': (b'I', b'J', b'Y', b'L', b'M', b'V', b'O', b'X'),
#         'r': (b'a', b'h'),
#         'n': (b'z', b'g'),
#         'b': (b'c', b'f'),
#         'k': (b'd',),
#         'q': (b'e', b'e', b'e', b'e', b'e', b'e', b'e', b'e', b'e'),
#         'p': (b'i', b'j', b'y', b'l', b'm', b'v', b'o', b'x')}

#     if isinstance(board, str):
#         board = board.encode()
#     board = board.split(b' ')[0]
#     for i in range(1, 9):
#         board = board.replace(str(i).encode(), b'0'*i)
#     for symbol in epd_symbols:
#         i = board.find(symbol.encode())
#         count = 0
#         while(i > -1):
#             board = board.replace(symbol.encode(), epd_map[symbol][count], 1)
#             count += 1
#             i = board.find(symbol.encode())
#     for key, rep in overlap_map.items():
#         board = board.replace(key, rep)
#     board = [list(row.decode()) for row in board.split(b'/')]
#     return np.array(board, NPDTYPE='S1').T

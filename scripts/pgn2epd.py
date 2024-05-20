import chess
import chess.pgn
import numpy as np


def pretty_print(epd):
    print(np.array(list(epd)).reshape((8, 8)).T)


def extend_epd(epd, truncate=True):
    if truncate:
        epd = epd.split(' ')[0]
    epd = epd.replace('/', '')
    for n in range(1, 9):
        if str(n) in epd:
            epd = epd.replace(str(n), str(0)*n)
    return epd


def png2epd(fname, extend=True, truncate=True, outname=None):
    with open(fname) as pgnfile:
        game = chess.pgn.read_game(pgnfile)
        board = game.board()
        if extend is True:
            epd = [extend_epd(board.epd(), truncate)]
        else:
            epd = [board.epd()]
        node = game
        for move in game.main_line():
            node = node.variation(move)
            board = node.board()
            if extend:
                epd.append(extend_epd(board.epd(), truncate))
            else:
                epd.append(board.epd())
    if outname is not None:
        with open(outname, 'w') as file:
            for line in epd:
                file.write("%s\n" % line)
    return epd


def png2san(fname, outname=None):
    with open(fname) as pgnfile:
        game = chess.pgn.read_game(pgnfile)
        movements = [board.uci() for board in game.main_line()]
    if outname is not None:
        np.savetxt(outname, movements, '%s')
    return movements


if __name__ == '__main__':
    inname = "data/enroque_rey.pgn"
    TEST = 'SAN'  # 'EPD'
    if TEST == 'EPD':
        outname = 'outputfile.epd'
        epd_game = png2epd(inname, True, True, outname)
        # print('\n'.join(epd_game))
        [pretty_print(epd_board) for epd_board in epd_game]
    elif TEST == 'SAN':
        outname = 'outputfile.san'
        san_game = png2san(inname, outname='outputfile.san')
        print(san_game)

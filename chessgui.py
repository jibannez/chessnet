
from matplotlib.widgets import Slider, Button

import matplotlib.pyplot as plt 
from matplotlib import cm 
from matplotlib.colors import ListedColormap, LinearSegmentedColormap 
import numpy as np 
import matplotlib.image as mpimg
import matplotlib.gridspec as gridspec

class ChessGUI :
  """ A matplotlib GUI for a chessnet match"""
  import chess 
  import chessnet 
  
  dict_pieces = {
     '♚':'bK',
     '♛':'bQ',
     '♜':'bR',
     '♝':'bB',
     '♞':'bN',
     '♟':'bP',
     '⭘':'B',
     '♙':'wP',
     '♘':'wN',
     '♗':'wB',
     '♖':'wR',
     '♕':'wQ',
     '♔':'wK'}  
  
  match=None
  match_len=0
  game=None
  moves=None
  current_pos=0
  
  fig=None
  plots_ax=None
  board_ax=None
  text_ax=None
  slide_ax=None
  slide=None
  
  def __init__ (self, match,game,pos=0) :
    self.current_pos=pos
    self.match=match
    self.match_len=len(match)
    self.game=game
    self.moves=list(game.mainline())
    
    
  def plot_chess_board(self, ax):
    size = 8 
    chessboard = np.zeros((size,size)) 
   
    chessboard[1::2,0::2] = 1 
    chessboard[0::2,1::2] = 1 
   
    color_b = np.array([248/256, 238/256, 158/256, 1]) 
    color_w = np.array([139/256, 184/256, 96/256, 1]) 
    newcmp = ListedColormap([color_w,color_b]) 
   
    ax.set_xlim([-0.5,7.5])
    ax.set_ylim([-0.5,7.5])
    ax.set_xticks([0,1,2,3,4,5,6,7])
    ax.set_xticklabels(['a','b','c','d','e','f','g','h'])
    ax.set_yticks([0,1,2,3,4,5,6,7])
    ax.set_yticklabels([1,2,3,4,5,6,7,8])
    # ~ ax.set_yticklabels([8,7,6,5,4,3,2,1])
    
    ax.imshow(chessboard, cmap=newcmp) 
  
  
  def plot_chess_piece(self, ax,piece,x,y):
    if piece != 'B':
      ax.imshow(mpimg.imread('./images/'+piece+'.png'),extent=[x-0.5,x+0.5,y-0.5,y+0.5]) 

  def plot_chess(self, ax,board):
    self.plot_chess_board(ax)
    str_board=board.unicode().replace(' ','').split('\n')
    print(str_board)
    for row,rpieces in enumerate(str_board):
      print("piece: '" +rpieces+"'")
      for col,piece in enumerate(list(rpieces)):
        # ~ print("piece: '" +piece+"' - "+self.dict_pieces[piece]+"-"+str(row)+"-"+str(col))
        self.plot_chess_piece(ax,self.dict_pieces[piece],col,7-row)


  def plot_chess2(self,ax,board):
    import tempfile
    import chess
    from cairosvg import svg2png
    fp = tempfile.NamedTemporaryFile()
    svg2png(bytestring=chess.svg.board(board),write_to=fp)
    ax.imshow(plt.imread(fp.name))
    fp.close()
  
  def do_line_plots(self, ax, match, vname, pos=None, do_label=True):
    b = getattr(self.match, 'b_' + vname)
    w = getattr(self.match, 'w_' + vname)
    if self.match.winner[0] == 'White':
        wstyle = 'r'
        bstyle = 'k--'
    elif self.match.winner[0] == 'Black':
        wstyle = 'r--'
        bstyle = 'k'
    else:
        wstyle = 'r--'
        bstyle = 'k--'
    ax.plot(w, wstyle)
    ax.plot(b, bstyle)
    if pos is not None:
      ax.vlines(pos,min(min(b),min(w)),max(max(b),max(w)))
    if do_label:
        # ~ ax.legend(['white','black'])
        ax.set_title(vname)

  def plot_metadata(self, ax,match):
    output_str=""
    for k,v in dict(match.metadata).items():
      output_str+=k+' - '+v+'\n'
    ax.text(0,0,output_str,fontsize=20)

  def plot_update(self, pos):
    self.current_pos=int(pos) 
    
    self.board_ax.clear()
    self.plot_chess(self.board_ax,self.moves[self.current_pos].board())
    for name,ax in zip(chessnet.classes.vector_names,self.plots_ax):
      ax.clear()
      self.do_line_plots(ax, self.match, name, self.current_pos)
    self.fig.canvas.draw()
    return
    
  def slider_on_changed(self, val):
    self.plot_update(int(val))

  def on_key(self, event):
    pos=0
    print('you pressed', event.key, event.xdata, event.ydata, self.current_pos)
    if event.key == 'right' : 
      pos=self.current_pos+1 if self.current_pos < self.match_len-1  else 0
    if event.key == 'left' : 
      pos=self.current_pos-1 if self.current_pos > 0 else self.match_len-1
    self.plot_update(pos)
    self.slider.set_val(pos)
  
  def on_click(self,event):
    print(event.xdata, event.ydata)
    self.plot_update(int(event.xdata))
    self.slider.set_val(int(event.xdata))
    
  def start(self):
    import chessnet
    
    # Create figure space
    self.fig = plt.figure(figsize=(8, 6), dpi=80) 
    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()

    gs = gridspec.GridSpec(100,100)
    self.board_ax  = plt.subplot(gs[0:50,0:24])   
    self.slider_ax = plt.subplot(gs[55:60,0:24]) 
    self.plots_ax = list()
    
    # create plot space
    for i, name in enumerate(chessnet.classes.vector_names):
      row = int(i/3)
      col = i % 3 + 1
      ax = plt.subplot(gs[row*33+1:(row+1)*33, col*25+1:(col+1)*25])
      self.do_line_plots(ax, m, name)
      self.plots_ax.append(ax)
    
    # crate metadta space
    self.text_ax=plt.subplot(gs[70:,0:24])
    self.text_ax.set_axis_off()
    self.plot_metadata(self.text_ax,m)

    self.slider = Slider(self.slider_ax, 'Move', 0, len(self.match), valinit=0,valfmt='%d')
    self.slider.on_changed(self.slider_on_changed) 
    
    self.plot_chess(self.board_ax,self.moves[0].board())
    cidk = self.fig.canvas.mpl_connect('key_press_event', self.on_key)
    cidc = self.fig.canvas.mpl_connect('button_press_event', self.on_click)
    plt.show()           


if __name__ == '__main__':
    import sys
    import chess 
    import chessnet 
    matchset = chessnet.MatchSet()


    # ~ gmoves=list(g.mainline())


    m=matchset[0]
    g=matchset._game_set[0]
    Gui=ChessGUI(m,g)
    Gui.start()
    sys.exit(main(sys.argv))





    
  



    

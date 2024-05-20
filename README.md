# *chessnet*: A network analysis library for chess
 
[OFFICIAL GIT REPOSITORY](https://git.kabe.es/Chess/chessnet) 


[GIT REPOSITORY OF THE OLD C VERSION](https://git.kabe.es/Chess/chess-clib) 

## About

This utility calculates the connectivity matrices defined in the manuscript. The two basic matrices are X and S, that encode the current positions and the positions of the board that are accesible following chess rules respectively, using a 32x64 representation (pieces x cells). For the king there is an addtional basic matrix, K, that stands for the accesible regions from the king's position that a queen could reach. The aim of this matrix is to estimate the amount of exposure of the king. All these matrices are computed by the python code in computation.py (and the auxiliar module constants.py), using numba jit to accelerate calculations (the final perfomance is only 30% slower than our original C library, whereas a pure python implemention is around 100 times slower). The remaining variables computed in the library are computed as properties of python objects (BoardState, Match, MatchSet, explained below) defined in classes.py. The matrices computed are (w:=white, b:=black):
 - Xw and Xb, the positions of the pieces for each color.
 - Sw and Sb, the accessible position of the pieces for each color.
 - Iw and Ib, the respective influence networks, computed as the matrix product of Sw and Sw', and Sb and Sb'.
 - Dw and Db, the respective defense networks, computed as the matrix product of Sw and Xw, and Sb and Xb.
 - Aw and Ab, the respective attack networks, computed as the matrix product of Sb and Xw, and Sw and Xb.
 - Cw and Cb, the respective clash networks,  computed as the matrix product of Sw and Sb', and Sb and Sw'.

The scalar values computed for each state of the board are usually split by color, with a name that starts with 'w_' or 'b_'. Among these variables there are number of pieces and acessible cells, the connectance of I, D, A, C networks, and the accessiblity, defense and attack on the kings.

Additional development based on the library can be performed either by classical procedural coding (a-la-matlab scripts), as one would do in an interactive interpreter session, or by subclassing any of the basic classes to implement the additional analyses or plots.


## Numerical codification of the pieces

This scheme represents the piece codes at the initial state of board. If a cell is empty, its value is 0

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

	     J0  J1  J2  J3  J4  J5  J6  J7  
	    +---+---+---+---+---+---+---+---+
	 I0 |RLw|p1w|   |   |   |   |p8b|RLb| a
	    +---+---+---+---+---+---+---+---+
	 I1 |NLw|p2w|   |   |   |   |p7b|NLb| b
	    +---+---+---+---+---+---+---+---+
	 I2 |BLw|p3w|   |   |   |   |p6b|BLb| c
	    +---+---+---+---+---+---+---+---+
	 I3 |Qw |p4w|   |   |   |   |p5b|Qb | d
	    +---+---+---+---+---+---+---+---+
	 I4 |Kw |p5w|   |   |   |   |p4b|Kb | e
	    +---+---+---+---+---+---+---+---+
	 I5 |BRw|p6w|   |   |   |   |p3b|BRb| f
	    +---+---+---+---+---+---+---+---+
	 I6 |NRw|p7w|   |   |   |   |p2b|NRb| g
	    +---+---+---+---+---+---+---+---+
	 I7 |RRw|p8w|   |   |   |   |p1b|RRb| h
	    +---+---+---+---+---+---+---+---+
	      1   2   3   4   5   6   7   8 

## Install

The library is a pure python package that uses numba to accelerate computations. The other two dependencies required are numpy and python-chess. For the network analisis of the contact matrices and to develop custom algorithms that are not part of this package. networkx is an interesting starting point,

You can use your preferred method to install the python dependencies (system packages, pip, conda...), although I would personally recommend using conda for the core scientific python environment, and pip for python-chess. Just as an example, here is how you would setup the development enviroment with conda in linux:

	# Download miniconda installer (only needed if you do not have installed conda in your computer)
	https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh

	# change permissions, execute it, and proceed to install it
	chmod +x Miniconda3-latest-Linux-x86_64.sh
	./Miniconda3-latest-Linux-x86_64.sh

	# create a conda environment
	conda create -n chess pip ipython numpy numba xarray pandas scipy matplotlib networkx

	# activate environment
	source activate chess

	# install python-chess with pip
	pip install python-chess

	# clone chessnet and install with user privileges
	git clone https://git.kabe.es/Chess/chessnet.git
	cd chessnet
	python setup.py install

	# to test everything went fine, open ipython and load module and default matchset
	ipython
	import chessnet
	ms = chessnet.MatchSet()


The library has been developed with python>3.5 in mind, so you should not expect it to work with python 2.X (minimal changes would be required, I guess). The compatibility of this library is [was? now byte data is not widely used] particulary problematic due to the use of byte data type to represent strings.


## Usage

To use the python library, you only need to import it. You can do it either by adding its directory to the PYTHONPATH enviroment variable (i.e., .bashrc and friends), by running the script from this directory, or by installing in the system path with the setup.py installer.

#### Basic use
The library is organized around three python classes: BoardState, Match, and MatchSet. They are hierarchically nested, meaning that a MatchSet is a set of ordered Match intances glued together. As an example, this is how you would load a default MatchSet (that uses the file with the 60 matches selected by Fichser in his book), and instantiate a specific match from the set:
	
	import chessnet
	
	# load default match set
	matchset = chessnet.MatchSet()
	
	# get the 5th match
	match = matchset[4] 
	
	# display match's metadata
	print(match)
	
	# get 11th board state
	bs = match[10]
	
	# prints all matrices
	bs.print()
	
	# gets the conectivity matrix
	bs.Xw
	
	# this the same matrix as above
	match.Xw[10,...]
	
	# b2 is the same state as bs
	b2 = matchset[4][10]
	
	# Print the board in the last movement of last match
	matchset[-1][-1].print_board()

The case is a bit more complicated for the relationship between Match and BoardState classes. To allow for numpy-like indexing at top speed, the default implementation of Match does not include a set of BoardState instances. All the matrices of the full match are actually 3D arrays, so there is no direct access to BoardState instances. It also aligns with the basic use of the library, that is more optimized to analyze whole matches than single movements. 

To facilitate the inspection of single board states, whenever a match instance is indexed, it will create a BoardState instance on the fly, and it pass the array views of the specific match state.

#### Loading matches from files
A sample session, where the file 'plenty_of_matches.pgn' contains a multi-match pgn and the file 'one_match.pgn' contains only one match, and the directory path *my_pgn_database_path* contains multiple one-match pgn files:

	import chessnet

	# This command would analyze all matches in the file
	matchset = chessnet.MatchSet('plenty_of_matches.pgn')

	# This command would analyze all matches in the directory
	matchset = chessnet.MatchSet(my_pgn_database_path)

	# This command would analyze only the first match
	match = chessnet.Match('plenty_of_matches.pgn')

	# This command would analyze the only match
	match = chessnet.Match('one_match.pgn')


#### Accessing the matrices of a Match instance
To retrieve the matrices contained in a Match instance, we should note that they are properties of Match object with 3 dimensions [MOVEMENT_NO, X_DIM, Y_DIM] or less (some are only 2D, like the active pieces). There is no need to instantiate the matrices in a local variable as done in the code below, it simply illustrates how they are used.
	
	# Fetch match's board
	board = match.B

	# These are the basic matrices computed in numba
	X = match.X
	S = match.S
	Kw = match.Kw
	Kb = match.Kb

	# These are the per-color basic matrices, a numpy-view of the original
	Xw = match.Xw
	Xb = match.Xb
	Sw = match.Sw
	Sb = match.Sb

	# These are the matrices that encode the different networks considered so far
	Iw = match.Iw
	Ib = match.Ib
	Aw = match.Aw
	Ab = match.Ab
	Dw = match.Dw
	Db = match.Db
	Cw = match.Cw
	Cb = match.Cb

	# Here you can find all active pieces
	active_pieces = match.pieces
	
	# And the promoted pawns
	promoted = match.promoted

	# These are the scalar properties of the networks computed so far.
	... use some introspection or read classes.py to find out an updated version.

#### Accessing the matrices of a MatchState instance
The full matrices for all dataset are also exposed as properties of the MatchSet class. However, the length dimension of each match is different and thus cannot be concatenated in a homogeneous 4D array. For this reason all matches matrices are provided as a list of 3D arrays (created on the fly as references to numpy objects, so low cost). Conversion to a heterogeneous 4D object array has no point over a plain list, is costly, and creates some cases of awkward syntax.

	# Fetch matchset's board
	board = matchset.B

	# These are the basic matrices computed in numba
	X = matchset.X
	S = matchset.S
	Kw = matchset.Kw
	Kb = matchset.Kb
	
	# get conectivity matrix of first match in the set
	X_first = matchset[0].X
	
	# this is the same final DCM matrix
	X_first = matchset.X[0]


#### How to integrate analyses of contact matrix by subclassing Match class

There are two simple ways to develop further analyses based on this library. The most straightforward is to use an independent procedural library that uses the objects of chessnet library as containers of their input arrays. For example:

	import chessnet

	def my_analysis(match):
		X = match.X
		S = match.S

		# do_something with X and S to obtain measure
		...

		return measure

	m = chessnet.Match()

	result = my_analysis(m)

The other method is to subclass Match and to add the analysis as properties of the subclass. Using subclassing may provide a simple and intuitive way to access data, and also allows for encapsulation if the analysis becomes too complex. It is also compatible with a procedural library of analysis. These functions can be called with the appropriate parameters from the class property getters. For example:
	
	import matplotlib.pyplot as plt
	import chessnet
	import analysis # this is another python module with functions that compute network measures

	classdef ConectivityAnalysis(chessnet.Match):
		def __init__(self, *args, **kwargs):
			# initialize super class, in this case, it will
			# load a match and compute its matrices.
			super.__init__(*args, **kwargs)

		@property
		def path_length(self):
			# note that self.cm is a 3D array, with the succesive 
			# board states in the first dimension. Therefore, the function
			# analysis.path__length should be properly vectorized to support
			# this kind of computation. An axis parameter is usually a good
			# idea to indicate the dimension along which the computations
			# will be performed. In this case, it should default to axis=0
			return analysis.path_length(self.cm)

		@property
		def path_length_Aw(self):
			return analysis.path_length(self.Aw)

		@property
		def path_length_Dw(self):
			return analysis.path_length(self.Dw)

		@property
		def path_length_Iw(self):
			return analysis.path_length(self.Iw)

		@property
		def path_length_Cw(self):
			return analysis.path_length(self.Cw)

		@property
		def path_length_Ab(self):
			return analysis.path_length(self.Ab)

		@property
		def path_length_Db(self):
			return analysis.path_length(self.Db)

		@property
		def path_length_Ib(self):
			return analysis.path_length(self.Ib)

		@property
		def path_length_Cb(self):
			return analysis.path_length(self.Cb)

		def plot_path_lengths(self):
			# Plot the full connectivity matrix path length
			fig1 = plt.figure()
			ax = fig1.add_subplot(111)
			ax.plot(self.path_length, label='full')
			ax.plot(self.path_length_Aw, label='Aw')
			ax.plot(self.path_length_Dw, label='Dw')
			ax.plot(self.path_length_Iw, label='Iw')
			ax.plot(self.path_length_Cw, label='Cw')
			ax.plot(self.path_length_Ab, label='Ab')
			ax.plot(self.path_length_Db, label='Db')
			ax.plot(self.path_length_Ib, label='Ib')
			ax.plot(self.path_length_Cb, label='Cb')
			ax.set_title('Path lengths')
			ax.legend()

#### Use BoardState to test specific movements
To test specific states of the board we can use the BoardState class:

	# Create empty BoardState instance
	bs = chessnet.BoardState()

	# Set the board state with an EPD string
	# for details about the format, see below
	bs.set_board(chessnet.K.EPD_BOARD_STRING)

	# Or with a 2D numpy array of integers
	# for details about the format, see constants.py
	bs.set_board(NUMPY_INT32_2D_ARRAY)

	# Compute DCM and accesibility matrices
	bs.compute()
	
	# Print result
	bs.print()
	
	# Get reference to DCM matrix
	X = bs.X
	S = bs.S


#### Specifying states of the board
A sample EPD board string with the initial board state can be found in constants file. I reproduce here for reference on how to encode the board in this format:

	EPD_BOARD_STRING = 'RNBKQBNR/PPPPPPPP/8/8/8/8/pppppppp/rnbkqbnr'
	
For more information about chess formats, please check the following links:

[Algebraic Notation (SAN)](https://en.wikipedia.org/wiki/Algebraic_notation_(chess)) 

[Portable game notation (PGN)](https://en.wikipedia.org/wiki/Portable_Game_Notation) 

[Extended Position Notation (EPD)](https://en.wikipedia.org/wiki/Extended_position_description) 

Internally, we use SAN to represent movements, and EPD to represent states in a human readable way (because the actual board states are encoded as 8x8 matrices with the numeric per piece defined in constants.py)

#### Aditional information
For any further information, either contact me directly or, even better, check the source code. The library is relatively simple and I tried to reduce the interfaces to the minimal expression. 

Once I upload the code to our git repository you could also create issues to solve doubts on how to use it, or to report bugs or propose improvements. The idea is that you will not need to do much changes in the basic library in order to develop analytic methods. In other words, development from here should be mostly independent from the develoment performed until now for this library.

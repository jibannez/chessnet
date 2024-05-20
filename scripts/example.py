import matplotlib.pylab as plt
import  pandas as pd
import chessnet

# Loading 
matchset = chessnet.MatchSet()
match=matchset[0];
match.plot_all()
match.print_boards()

import numpy as np
lW=[ m.w_Dconnectance for m in matchset if m.winner[0] == 'White' ] + [ m.b_Dconnectance for m in matchset if m.winner[0] == 'Black' ]
lL=[ m.b_Dconnectance for m in matchset if m.winner[0] == 'White' ] + [ m.w_Dconnectance for m in matchset if m.winner[0] == 'Black' ]
a=max([len(l) for l in lW])

mW=[]
mL=[]
for i in range(a):
    mW+=[np.mean([lW[j][i] for j in range(len(lW)) if i < len(lW[j])])]
for i in range(a):
    mL+=[np.mean([lL[j][i] for j in range(len(lL)) if i < len(lL[j])])]
#plt.plot(range(len(mW)),mW,'r-', range(len(mL)),mL,'k-')

sW=[]
sL=[]
for i in range(a):
    sW+=[np.std([lW[j][i] for j in range(len(lW)) if i < len(lW[j])])]
for i in range(a):
    sL+=[np.std([lL[j][i] for j in range(len(lL)) if i < len(lL[j])])]

fig, ax = plt.subplots( 1, 1, figsize=(16,8) )
ax.plot(range(len(mW)),mW,'r--', range(len(mL)),mL,'k--')
ax.fill_between(range(len(sW)),sW,color='red', alpha=0.5) 
ax.fill_between(range(len(sL)),sL,color='gray', alpha=0.5) 

ax.set_ylabel('I connectance')
ax.set_xlabel('State')


plt.show()

# Export indexes of all matches to csv
matchset.export_to_csv() 

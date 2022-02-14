# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 14:58:13 2022

@author: ncuesuser
"""

import matplotlib.pyplot as plt
import numpy as np
import routine as rout
################## Parameter Input ############################################
filepath_image="Data/girl-portrait-2.jpg"
iteration=5000
max_string=4000

################## Computation ################################################
image=rout.crop_image(filepath_image)
string=rout.iteration(image,5000)
coord=np.array(string)
np.savetxt("Output/coordinate.txt",coord)

fig = plt.figure(figsize=[8,8])
ax = fig.add_subplot(111)
ax.plot(coord[:max_string,0],coord[:max_string,1],c='k',lw=0.1)
ax.scatter(coord[:,0],coord[:,1],c='r',s=2)
ax.set_ylim(coord[:,1].max(),coord[:,1].min())
ax.set_xlim(coord[:,0].min(),coord[:,0].max())
ax.set_xticks([])
ax.set_yticks([])
ax.set_aspect(1)
ax.axis('off')
plt.savefig("Output/stringart.png",dpi=500,format="PNG")
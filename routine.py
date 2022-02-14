# -*- coding: utf-8 -*-
"""
Created on Thu Feb  3 21:08:52 2022

@author: syahdansur@gmail.com
"""

import matplotlib.pyplot as plt
import numpy as np
from skimage import io
from PIL import Image, ImageDraw

def crop_image(filepath):
    img=Image.open(filepath).convert("L")
    npImage=np.array(img)
    ny,nx=np.array(npImage.shape)
    r=np.array(npImage.shape).min()/2
    x0=int(nx/2)
    y0=int(ny/2)
    # Create same size alpha layer with circle
    alpha = Image.new('L',(nx,ny),0)
    draw = ImageDraw.Draw(alpha)
    
    draw.pieslice([x0-r,y0-r,x0+r,y0+r],0,360,fill=255)
    npAlpha=np.array(alpha)

    npImage=npImage*npAlpha
    return npImage

def coord_sphere(image,dteta):
    ny,nx=np.array(image.shape)
    r=np.array(image.shape).min()/2
    x0=nx/2
    y0=ny/2
    teta=np.arange(0,360+dteta,dteta)
    xi=x0+r*np.cos(teta*np.pi/180)
    yi=y0+r*np.sin(teta*np.pi/180)
    return (np.vstack((xi,yi)).T).tolist()
    
def line_choose(image,nx,ny,current_pos,pos):
    neighbors=pos.copy()
    neighbors.remove(current_pos)
    avg=[]
    for i in neighbors:
        alpha=Image.new('LA',(nx,ny),0)
        line=ImageDraw.Draw(alpha)
        line.line([tuple(current_pos),tuple(i)],fill='black',width=0)
        npalpha=np.array(alpha)[:,:,-1]/255
        n_pixel=npalpha.sum()
        avg_black=np.sum(image*npalpha)/n_pixel
        avg.append([avg_black,n_pixel])
    
    max_coord=np.argmax(np.array(avg)[:,0])
    
    alpha=Image.new('LA',(nx,ny),0)
    line=ImageDraw.Draw(alpha)
    line.line([tuple(current_pos),tuple(neighbors[max_coord])],fill="black",width=0)
    npalpha=np.array(alpha)[:,:,-1]/255
    mask=(npalpha-1)*-1
    new_image=mask*image
    
    return neighbors[max_coord],new_image

def iteration(image,n_iteration):
    sphere=coord_sphere(1-image,2)    
    ny,nx=np.array(image.shape)
    initial=sphere[0]
    new_img=image.copy()
    pos=[initial]
    i=0
    while i<=n_iteration:
        next_pos,new_img=line_choose(new_img, nx, ny,initial, sphere)
        plt.plot([initial[0],next_pos[0]],
                 [initial[1],next_pos[1]],lw=0.1,c='k')
        print("Iteration=",i)
        initial=next_pos
        pos.append(initial)
        i+=1
    return pos      
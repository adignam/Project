#Project
import numpy as np
import matplotlib.pyplot as plt
import math
import scipy.misc

def make_circle(x_axis,y_axis,R=510,xc=512.,yc=512.):
    size=x_axis*y_axis           #Initialise size
    x_centre=xc#x_axis/2
    y_centre=yc#y_axis/2   
    #Create list
    x=np.arange(size*1.) % x_axis
    y=np.arange(size*1.) % y_axis    
    #Reshape to form array
    x = np.reshape(x, (x_axis,y_axis))
    #y array
    y=np.rot90(np.reshape(y, (x_axis,y_axis)))
    #Subtract centre points
    x=x-x_centre
    y=y-y_centre    
    #Square array
    x=np.square(x)
    y=np.square(y)    
    r1=np.add(x,y)
    #Square root arrays
    r=np.sqrt(r1)
    #Make circle of given stellar radius
    mask=(r<=R)
    r=r*mask
    #Plot stellar model    
    #plt.imshow(mask, cmap=plt.cm.binary)
    #plt.ylim([0,1024])
    return r, mask
    
def limb_darkening(a,b,r,mask):
    #Calculates limb darkening for the star    
    mu=np.sqrt(1-r**2)
    LD=r*0.
    LD[mask==1]=1-(a*(1-mu[mask==1]))-(b*((1-mu[mask==1])**2))
    return LD
    
def spectrum(r, A, sigma):  
    #Plots the spectrum of the star
    veq=2.
    vrot=(np.arange(1024)-512)/512.*veq
    v=np.arange(-12,12,0.02345)  
    flux=np.zeros(np.shape(v))
    fstar=-np.sum(r,0) 
    vx=np.zeros(len(vrot))
    
    Gauss=1-A*np.exp((-(v-vx)**2)/(2*sigma**2))
    for i in range(0,len(vrot)):       
        flux=fstar[i]*Gauss
        i+=1
    plt.plot(v,-flux)    

    
def planet_motion(coeff,i,Rstar,phase,phase_bin,centre):
    
    phase=np.arange(-phase,phase,phase_bin)
    x=coeff*np.sin(2*np.pi*phase)*Rstar+centre   
    y=coeff*np.cos(i)*np.cos(2*np.pi*phase)*Rstar+centre
    Rplanet = Rstar/2

    for i in range(0,200):
        r,mask=make_circle(1024,1024,Rplanet,x[i],y[i])
        mask=1-mask
        spectrum(mask, 0.9, 0.7)
        star=limb_darkening(0.3,0.3,r,mask)*mask
        spectrum(star, 0.9, 0.7)
        
        
star=make_circle(1024,1024,510)           #make star 

planet=make_circle(1024,1024,256)         #make planet

planet_motion(8.84,1.,512,0.1,0.001,512)            # coeff=8.84,i = 1.14959 for hd189733b

#plt.imshow(star, cmap=plt.cm.binary)
#scipy.misc.imsave('project_image.jpg', -star)

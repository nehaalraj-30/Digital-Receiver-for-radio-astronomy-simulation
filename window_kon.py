from math import sin,pi,cos
import numpy as np
def hanning(digital_values,alpha): #digital_values are 16k, alpa is from 0,4, 2 is hanning
    windowed_signal_hann=digital_values.copy()
    l=len(digital_values)
    for i in range(l):
            windowed_signal_hann[i]=digital_values[i]*(sin((i/l)*pi)**alpha) 
            
    gain = np.abs(np.sum(windowed_signal_hann)/l)                             
    return windowed_signal_hann,gain

def tri(digital_values):
    tri_digital_values=digital_values.copy()
    l=len(digital_values)
    for i in range(l):
            if i<=l/2:
                tri_digital_values[i]=digital_values[i]*2*(i/l)
            else:
                tri_digital_values[i]=digital_values[i]*2*(1-(1/l))
    gain = np.abs(np.sum(tri_digital_values)/l)           
    return tri_digital_values,gain

def hamming(digital_values,alpha):
    hamm_digital_values=digital_values.copy()
    l=len(digital_values)
    for i in range(l):
            hamm_digital_values[i]=digital_values[i]*(alpha-((1-alpha)*cos(((2*i)/l)*pi)))
    gain = np.abs(np.sum(hamm_digital_values)/l)       
    return hamm_digital_values ,gain

def blackman1(digital_values,level=0):
    blm_digital_values=digital_values.copy()
    l=len(digital_values)
    a0=[0.42323,0.44959,0.35875,0.40217]
    a1=[0.49755,0.49364,0.48829,0.49703]
    a2=[0.07922,0.05677,0.14128,0.09392]
    a3=[0000000,0000000,0.01168,0.00183]
    for i in range(l):
        blm_digital_values[i]=digital_values[i]*(a0[level]-(a1[level]*cos(2*pi*i/l))+(a2[level]*cos(4*pi*i/l))-(a3[level]*cos(6*pi*i/l)))
    gain = np.abs(np.sum(blm_digital_values)/l)    
    return blm_digital_values,gain      
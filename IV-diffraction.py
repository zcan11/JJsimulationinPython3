# -*- coding: utf-8 -*-
"""
Created on Tue April 30th 20:03:05 2017

@author: Can Zhang
"""

"""
Goal/purpose: this program will import one single ivsweep txt file
and load the data into 4 vectors V,I,dV,dI,B, and it will also calculate 
how many data points is in each file, and we will use that as the index limit 
to find the switching current

Author(s):Can Zhang

Date: April 30th, 2017

"""

###################################
# Import libraries 
###################################

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from itertools import islice
import numpy as np
import csv
import glob
import os
from decimal import *
from scipy.signal import savgol_filter
from scipy.signal import argrelextrema

#from scipy.signal import savgol_filter

plt.close("all")

###################################
# Define and initialize variables
###################################

flie_size=0
all_files=[]
list_of_files=[]
new_list=[]
###############################################################################
# Loop doing the work, with additional detail explained in comments within the loop
###############################################################################

temp_point=['20mK','100mK','200mK','300mK','400mK']
def load_files():
    
    # this calculate how many rows of data point in each file
    for name in temp_point:
        Ic_array  = [] 
        Bext_array= [] 
        dVolt_array=[]
        plot_labels=[]
        file_path='/'.join([name,'ivsweep*.txt'])

        
        list_of_files=glob.glob(file_path)
        for file_name in list_of_files:
            

            
            # now we open each individual txt file, and load the data inside it
            f = list(csv.reader(open(file_name, 'r'), delimiter='\t'))
            for lines in islice(f,24,None):
            
                c0=float(lines[0])/200
                c1=float(lines[1])
                c2=float(lines[2])
                c3=float(lines[3])
                c4=float(lines[4])
                if (c4/c2>15):
                    Bext_array.append(np.mean(c0))
                    Ic_array.append(c1)
                    dVolt_array.append(c2)
                    break
            #print(len(Bext_array),len(Ic_array),len(dVolt_array))
        
        final_txt='.'.join(['devH',name[-5:-2],'txt'])
        np.savetxt(final_txt,sorted(zip(Bext_array,Ic_array)),delimiter='\t')
        new_list.append(final_txt)
    return new_list
    

###############################################################################
# End of loop. Print the results.
###############################################################################
def main():
    txt_file=load_files()
    for file in txt_file:
        
        data=np.loadtxt(file,delimiter='\t')
        Bext= (data.T[0])/(1e-1)
        Ic= (data.T[1])
        Icmax_Index=argrelextrema(Ic, np.greater,order=6)
        Icmin_Index=argrelextrema(Ic, np.less,order=6)
        Bext[:]=[x -(Bext[Icmin_Index[0][2]]-0.0) for x in Bext]

    #Ic=[(y-(1.2e-3)*(6*x-0.4*x**2)) for x,y in zip(Bext,Ic)]
    #Ic=savgol_filter(Ic,53,4)
        plt.plot(Bext/(1e-1),Ic/(1e-6),'.-',markersize=3)
        plt.xlabel("Bext(mT)")
        plt.ylabel("Ic(uA)")
        plt.title("Josephson Junction Ic vs B diffraction") 
    
    
        plt.savefig("Ic_vs_Bext.png")

        np.savetxt(file,sorted(zip(Bext,Ic)),delimiter='\t')

if __name__=="__main__":
    main()
    
print("all done. Result is... ")

################################################################################
# Make informative comments on the results you just found, like how quickly
# the series converges, and its comparison to the true value of pi.
################################################################################

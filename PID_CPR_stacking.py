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

import matplotlib.pyplot as plt
from itertools import islice
import numpy as np
import glob
import os
from scipy.signal import argrelextrema
from scipy.signal import savgol_filter
from scipy.signal import find_peaks_cwt


plt.close("all")

###################################
# Define and initialize variables
###################################

list_of_files=[]
new_file_list=[]
average_zero=0.0
skewness=[]
temperature=[]
Ibig=[]
Ismall=[]
Icmax_Index=[]
Icmin_Index=[]
flux_period=0.7030918
std_origin=0.0

###############################################################################
# Loop doing the work, with additional detail explained in comments within the loop
###############################################################################


new_list=[]

f,((ax1,ax2),(ax3,ax4))=plt.subplots(2,2)



def load_txt():
    # this calculate how many rows of data point in each file
    #list_of_files=glob.glob('Iplus_Bext.24.txt')
    list_of_files=glob.glob('devF*txt')
    
    # create 2 vectors Ic and Bext, each individual IV file will contribute 
    # one data point in the Ic vs Bext diffraction pattery plot
    
    # file_name is each of the file name element in the array of list of files
    for file_name in list_of_files:
        # using np.loadtxt file to load the data in each txt file
        data=np.loadtxt(file_name,delimiter='\t',skiprows=20)
        Bext= (data.T[0]/(1e-2))
        Ic  = (data.T[1]/(1e-6))
        Ic=[(y-(5.5e-3)*(x)) for x,y in zip(Bext,Ic)]
               
        file_split=file_name.split(".")
        # replace the old number with new number with leading zeros
        num_new = str("%04d"%(int(file_split[1])))
        new_file='.'.join([num_new,'txt'])
        new_list.append(str(new_file))
        new_list.sort(key=lambda x: (x.split(".")[1],x))
        ax1.plot(Bext,Ic,".-",markersize=1)
        ax1.set_title("raw data")
        ax1.set_ylabel("Ic(uA)")
        ax1.set_xlabel("Bext(mT)")



        # save the new processed data into a new_file txt file
        np.savetxt(new_file,sorted(zip(Bext,Ic)),delimiter='\t')
        
        
    return new_list
'''    
def define_origin():
    file='devF.800.txt'
    data=np.loadtxt(file,delimiter='\t',skiprows=20)
    Bext=(data.T[0])/(1e-1)
    Ic=(data.T[1])
    Ic=savgol_filter(Ic,51,3)
    Icmax_Index=argrelextrema(Ic, np.greater,order=5)
    Icmin_Index=(argrelextrema(Ic, np.less,order=5))
    
    std_origin=Bext[Icmax_Index[0][2]]
    flux_period=(Bext[Icmin_Index[0][2]]-Bext[Icmin_Index[0][0]])/2
    print(flux_period,'flux_period')

    return std_origin, flux_period
'''
def stacking_CPR():
    new_file_list=load_txt()
    #print(one_flux)
    
    i=0
    for file2 in new_file_list:
        i+=1
        file_split=file2.split(".")
        data=np.loadtxt(file2,delimiter='\t')
        file_split=file2.split(".")
        labeling2=''.join([str(int(file_split[0])),'mK'])
        Bext=(data.T[0])
        Ic=(data.T[1])
                   
        ax2.plot(Bext,Ic,".-",markersize=1,label=labeling2)
        ax2.legend(loc=2,bbox_to_anchor=(1.05,1.0),borderaxespad=0.)
        ax2.set_title("reordered the x axis")
        ax2.set_ylabel("Ic(uA)")
        ax2.set_xlabel("Bext(mT)")
        
        Ic=savgol_filter(Ic,51,2)
        Icmax_Index=argrelextrema(Ic, np.greater,order=5)
        Icmin_Index=(argrelextrema(Ic, np.less,order=5))
        
        one_period=(Bext[Icmin_Index[0][2]]-Bext[Icmin_Index[0][0]])/2
        print(one_period)
        Bext[:]=[(flux_period)/(one_period)*x for x in Bext]
        Bext[:]=[x- Bext[Icmax_Index[0][2]] for x in Bext]
        Icmin_Index=(argrelextrema(Ic, np.less,order=5))
        one_period=(Bext[Icmin_Index[0][2]]-Bext[Icmin_Index[0][0]])/2
        #print(one_period)
        
        ax3.plot(Bext,Ic,".-",markersize=1)
        ax3.set_title("smoothed")
        ax3.set_xlim(-1.5,1.5)
        ax3.set_ylabel("Ic(uA)")
        ax3.set_xlabel("Bext(mT)")
        
        
        temperature.append(int(file_split[0]))
        temperature.sort()
        #print(temperature)
            
        phi_max1=np.pi*((Bext[Icmax_Index[0][-2]]-Bext[Icmin_Index[0][-2]]))/one_period

        
        phi_max=np.pi*((Bext[Icmax_Index[0][0]]-Bext[Icmin_Index[0][0]]+Bext[Icmax_Index[0][1]]-Bext[Icmin_Index[0][1]])/2)/one_period
        #print(phi_max1,phi_max)
        skewness.append(abs(2*phi_max1/np.pi-1))
        
    ax4.plot(temperature,skewness,".-",markersize=6)
    ax4.set_title("device-F ")
    ax4.set_ylabel("sknewness")
    ax4.set_xlabel("Temperature(mK)")
    plt.tight_layout()

    plt.savefig("device-F.png",bbox_inches='tight')
    #plt.tight_layout()
    plt.show()
       
 
   
    
def main():
    #processing_data()
    stacking_CPR()
    
    

if __name__=="__main__":
    main()


###############################################################################
# End of loop. Print the results.
###############################################################################

print("all done. Result is... ")
################################################################################
# Make informative comments on the results you just found, like how quickly
# the series converges, and its comparison to the true value of pi.
################################################################################

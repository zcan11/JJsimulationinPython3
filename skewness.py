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

###############################################################################
# Loop doing the work, with additional detail explained in comments within the loop
###############################################################################


new_list=[]



def load_txt_files():
    # this calculate how many rows of data point in each file
    #list_of_files=glob.glob('Iplus_Bext.24.txt')
    list_of_files=glob.glob('Iplus_*txt')
    
    # create 2 vectors Ic and Bext, each individual IV file will contribute 
    # one data point in the Ic vs Bext diffraction pattery plot
    
    # file_name is each of the file name element in the array of list of files
    for file_name in list_of_files:
        # using np.loadtxt file to load the data in each txt file
        data=np.loadtxt(file_name,delimiter='\t',skiprows=14)
        Bext= (data.T[0]/(1e-2))
        Ic  = (data.T[1]/(1e-6))
        Ic=savgol_filter(Ic,51,4)
        Ic=[(y-(3.2e-3)*(1-0.5*x**2)) for x,y in zip(Bext,Ic)]
               
        file_split=file_name.split(".")
        # replace the old number with new number with leading zeros
        num_new = str("%04d"%(int(file_split[1])))
        new_file='.'.join([num_new,'txt'])
        new_list.append(str(new_file))
        new_list.sort(key=lambda x: (x.split(".")[1],x))
        # save the new processed data into a new_file txt file
        np.savetxt(new_file,sorted(zip(Bext,Ic)),delimiter='\t')
        
    return new_list

#plt.figure()

"""    
def processing_data():
    new_file_list=load_txt_files()
    f,(ax1,ax2,ax3)=plt.subplots(3,sharex=True)

    
    i=0
    for file in new_file_list:
        i+=1
        data=np.loadtxt(file,delimiter='\t')
        Bext=(data.T[0])
        Ic=(data.T[1])
        Ic=savgol_filter(Ic,51,4)
        
        file_split=file.split(".")
        labeling=''.join([str(int(file_split[0])),'mK'])
        
        
        
        #horizontal shifting
        Icmax_Index=argrelextrema(Ic, np.greater,order=4)
        Icmin_Index=(argrelextrema(Ic, np.less,order=3))
        Bext[:]=[x -(Bext[Icmax_Index[0][2]]-average_zero) for x in Bext]
        
        one_period=(Bext[Icmax_Index[0][4]]-Bext[Icmax_Index[0][0]])/4
        #pmax=2.5*one_period
        pmax=2.5*2*np.pi/6.09
        major_ticks=np.linspace(-pmax,pmax,11)

        #print(np.sum(one_period))
        #cut = (Bext%(one_period/4) ==0)
        
        # the plt.subplot(A,B,C) creat a A raw and B column subplot in one figure
        # you put the line right before you are going to plot the fiture
        # C is the current figure that you want to put into the subplot.
        
        #f,(ax1,ax2,ax3)=plt.subplot(3,sharex=True)
        ax1.plot(Bext,Ic,".-",markersize=2,label=labeling)
        ax1.set_ylabel("Ic(uA)")
        ax1.set_title("Ic vs B for Asymmetric SQUID")
        ax1.legend(loc=2,bbox_to_anchor=(1.05,1.0),borderaxespad=0.)

        
       
        #ax2=plt.subplot(3,1,2,sharex=ax1)
        #vertical shifting
        Imid=1/2*(max(Ic)+min(Ic))
        Ic=Ic-Imid
        ax2.plot(Bext,Ic,".-",markersize=2,label=labeling)
        ax2.set_xticks(major_ticks)
        ax2.xaxis.grid(True,which='major',color='r',linestyle='-',linewidth=1)
        ax2.set_ylabel("Ic(uA)")
        
        #ax3=plt.subplot(3,1,3,sharex=ax1)
        # plot each txt file, and create a legend for each corresponding plot
        Inorm=1/2*(abs(max(Ic))+abs(min(Ic)))
        Ic[:]=[x/Inorm for x in Ic]
        ax3.plot(Bext,Ic,".-",markersize=2,label=labeling)
        ax3.set_xticks(major_ticks)
        ax3.xaxis.grid(True,which='major',color='r',linestyle='-',linewidth=1)
        ax3.set_xlabel("Bext(mT)")
        ax3.set_ylabel("Ic(uA)")

        #plt.subplots_adjust(hspace=0)
  
        #Ibig.append(0.5*(max(Ic)+min(Ic)))
        #Ismall.append(0.5*(max(Ic)-min(Ic)))
        
        
               
  
    #print(skewness)    
    ax2.plot(Bext,0.25*np.cos(6.08*(Bext)),"-",markersize=5,label='Symmetric SQUID')
    ax3.plot(Bext,0.25*np.cos(6.08*(Bext)),"-",markersize=5,label='Symmetric SQUID')
    plt.savefig("Ic_vs_Bext_shifted_zoom_in_device_B.png",bbox_inches='tight')
    plt.show()
    
    #return new_file_list
"""   
    
def skewness_vs_T():
    #new_file_list=processing_data()
    #print(new_file_list)
    new_file_list=load_txt_files()
    
    f,(ax1,ax2)=plt.subplots(1,2)
   
    i=0
    for file2 in new_file_list:
        i+=1
        data=np.loadtxt(file2,delimiter='\t')
        Bext=(data.T[0])
        Ic=(data.T[1])
        Ic=savgol_filter(Ic,51,4)
        
        file_split=file2.split(".")
        labeling2=''.join([str(int(file_split[0])),'mK'])
        print(labeling2)
               
        #horizontal shifting
        Icmax_Index=argrelextrema(Ic, np.greater,order=4)
        Icmin_Index=(argrelextrema(Ic, np.less,order=3))
        Bext[:]=[x -(Bext[Icmax_Index[0][2]]-average_zero) for x in Bext]
        
        one_period=(Bext[Icmax_Index[0][4]]-Bext[Icmax_Index[0][0]])/4
        #pmax=2.5*one_period
        pmax=2.5*2*np.pi/6.09
        major_ticks=np.linspace(-pmax,pmax,11)
        #vertical shifting
        Imid=1/2*(max(Ic)+min(Ic))
        Ic=Ic-Imid
        Inorm=1/2*(abs(max(Ic))+abs(min(Ic)))
        Ic[:]=[x/Inorm for x in Ic]
        ax1.plot(Bext,Ic,".-",markersize=2,label=labeling2)
        ax1.set_xticks(major_ticks)
        ax1.xaxis.grid(True,which='major',color='r',linestyle='-',linewidth=1)
        ax1.set_xlabel("Bext(mT)")
        ax1.set_xlim(-0.5,1.5)
        ax1.set_ylabel("Ic(uA)")
        ax1.set_title("Ic vs B for Asymmetric SQUID zoom in")
        ax1.legend(loc=2,bbox_to_anchor=(1.05,1.0),borderaxespad=0.)
        #ax1.set(adjustable='box-forced',aspect='equal')
        ax1.set_ylim(-1.5,1.5)
        
        temperature.append(int(file_split[0]))
        temperature.sort()
        #print(temperature)
            
        phi_max1=np.pi*((Bext[Icmax_Index[0][1]]-Bext[Icmin_Index[0][1]]))/one_period

        
        phi_max=np.pi*((Bext[Icmax_Index[0][1]]-Bext[Icmin_Index[0][1]]+Bext[Icmax_Index[0][2]]-Bext[Icmin_Index[0][2]]+Bext[Icmax_Index[0][3]]-Bext[Icmin_Index[0][3]])/3)/one_period
        #print(phi_max1,phi_max)
        skewness.append(abs(2*phi_max/np.pi-1))
        a=''.join(['skewness',str(i)])
    print('tempearture:', temperature)
    print('skewness:', skewness)
    ax2.plot(temperature,skewness,".-",markersize=5)
    ax2.set_xlabel("Temperature(mK)")
    #ax2.set_xlim()
    ax2.set_ylabel("Skewness")
    ax2.set_title("Skewnss vs Temperature for Asymmetric SQUID")
    #ax2.set(adjustable='box-forced',aspect='equal')
        
    ax1.plot(Bext,0.25*np.cos(6.08*(Bext)),"-",markersize=5,label='Symmetric SQUID')
    plt.subplots_adjust(hspace=0.5)
    plt.tight_layout()
    
    plt.savefig("Skewness_vs_Temperature.png",bbox_inches='tight')
    plt.show()
        
    
   
    
def main():
    #processing_data()
    skewness_vs_T()
    #print(type(ax1.get_figure())
    #print(type(ax4.subplot(1,2,1))
    #ax5=plt.subplot(1,2,2)
    #ax5.plot(temperature,skewness,".-",markersize=2,label=labeling)
    #ax5.set_xlabel("Temperature(mK)")
    #ax5.set_ylabel("Skewness")
    #ax5.set_title("Skewness vs Temperature for Asymmetric SQUID")
    #plt.savefig("Skewness vs Temperature.png",bbox_inches='tight')

    
    
    #ax2=plt.subplot(1,2,2)
    #ax2.plot(temperature,skewness,".-",markersize=2)
    #plt.savefig("Ic_vs_Bext_shifted_zoom_in_device_B.png",bbox_inches='tight')
    

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

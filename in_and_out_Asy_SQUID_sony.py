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
#from scipy.signal import savgol_filter

plt.close("all")

###################################
# Define and initialize variables
###################################

flie_size=0
all_files=[]
list_of_files=[]
###############################################################################
# Loop doing the work, with additional detail explained in comments within the loop
###############################################################################


new_list=[]



def load_files():
    # this calculate how many rows of data point in each file
    list_of_files=glob.glob('Iplus_*.txt')
    
    # create 2 vectors Ic and Bext, each individual IV file will contribute 
    # one data point in the Ic vs Bext diffraction pattery plot
    
    # file_name is each of the file name element in the array of list of files
    for file_name in list_of_files:
        
        Ic_array  = [] #[None]*(len(list_of_files))
        Bext_array= [] #[None]*(len(list_of_files))
        dVolt_array=[]
        plot_labels=[]
        
        # for each individual file name, we split the file name according to its
        # index of temperature
        file_split=file_name.split(".")
        
        # convert the string of the number index into integer
        num_old = int(file_split[1])
        
        # this would be the legend array for each plot 
        plot_labels.append('.'.join([str(num_old),'mK']))
        
        # replace the old number with new number with leading zeros
        num_new = str("%04d"%num_old)
        new_file='.'.join([num_new,'txt'])
        output=open(new_file,'w+')
        writer=csv.writer(output,delimiter='\t')
        # open new file names and write the processed data into it
        
        

        
        # now we open each individual txt file, and load the data inside it
        f = list(csv.reader(open(file_name, 'r'), delimiter='\t'))
        for lines in islice(f,20,None):
            
            c0=float(lines[0])/(1e-3)
            c1=float(lines[1])/(1e-6)
            c1=c1-6e-5*(1+0.1*c0-0.5*(c0)**2)
            c2=float(lines[2])/(1e-6)
           
            Bext_array.append(c0)
            Ic_array.append(c1)
            dVolt_array.append(c2)
            
        #print(Ic_array)
        Imid=1/2*(max(Ic_array)+min(Ic_array))
        Ic_array[:]=[x-Imid for x in Ic_array]
        writer.writerows(zip(Bext_array,Ic_array,dVolt_array))
        new_list.append(str(new_file))
        new_list.sort(key=lambda x: (x.split(".")[1],x))
        output.close()
        #print(Ic_array)
    return new_list

    
#fig, ax=plt.subplots()
def main():
    new_file_list=load_files()    
    for file in new_file_list:
        
        with open(file) as f:
            lines=f.readlines()
            Ic =[line.split()[1] for line in lines]
            Bext=[line.split()[0] for line in lines]

        #new_list.sort(key=lambda x: (x.split(".")[1],x))
        # sort the roder of file by substring which is the index name
        file_split=file.split(".")
        #print(file_split[0])
        labeling=''.join([str(int(file_split[0])),'mK'])
        #print(labeling)
        Ic_array1=savgol_filter(Ic,51,5)
        
        # plot each txt file, and create a legend for each corresponding plot
        
        plt.plot(Bext,Ic_array1,".-",markersize=1,label=labeling)
        plt.legend(loc=2,bbox_to_anchor=(1.05,1.0),borderaxespad=0.)
           
        #ax.legend()

        
# bbox_to_anchor=(1.05,1.0) anchors the legend to a point outside the figure 
# in the upper right corner
# loc=2, anchors the uppder left corner of the legend to the location(1.05,1)
        
        
    
    plt.xlabel("Bext(mT)")
    plt.ylabel("Ic(uA)")
    plt.title("Josephson Junction Ic vs B diffraction----- Can Zhang") 
    
    #plt.tight_layout()

    plt.savefig("Ic_vs_Bext_stacked.png",bbox_inches='tight')
    plt.show()
# bbox_inches='tight' will make sure the legend won't be cutoff of the 
# figure when saving        
        
        

#print(main())
### this part that extract the information of crtical current
### probably needs more wook to make it more rigorous 
###
           
       
        

"""
def main():
    list_of_files= read_file()
    #print("total number of data point is {0}".format(file_size))
    
    #fig = plt.figure()
    plt.plot(Bext,Ic,".")
    
    
    plt.xlabel("Bext(mT)")
    plt.ylabel("Ic(uA)")
    plt.title("Josephson Junction Ic vs B diffraction----- Can Zhang") 
    
    
    plt.savefig("Ic_vs_Bext.png")

"""

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

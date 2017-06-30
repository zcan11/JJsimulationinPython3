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
from matplotlib import cm
from itertools import islice
import numpy as np
import csv
import glob
import os
import shutil
plt.close("all")

###################################
# Define and initialize variables
###################################

flie_size=0
new_list=[]
all_files=[]
#file_name=[]
#creaete 5 empty vectors to be filled by the data import from the txt file


###############################################################################
# Loop doing the work, with additional detail explained in comments within the loop
###############################################################################
def load_directory():
    # first load all the txt files uder the directory
    all_files = glob.glob('*.txt')
    #print(all_files)
    #flie_size=len(all_files)
    for title in all_files:
        #split the file name into three parts with "." as the delimiter
        file_split=title.split(".")
        
        # convert the string of the number index into integer
        num_old = int(file_split[1])
        # replace the old number with new number with leading zeros
        num_new = str("%04d"%num_old)
        
        #now create new file names for each file so they would be loaded in 
        # correct incremental order
        name_new=".".join([file_split[0],num_new,"txt"])
        # append the corrected name to the new_list
        os.rename(title,name_new)
        new_list.append(name_new)
        # sort the new list by incremental order        
        new_list.sort(key=lambda x: (x.split(".")[1],x))
        # sort the roder of file by substring which is the index name
    file_size=len(new_list)
    return new_list
        
Ic_array  = [] #[None]*(len(list_of_files))
Bext_array= [] #[None]*(len(list_of_files))


def read_file():
    # this calculate how many rows of data point in each file
    total_lines=0
    list_of_files=load_directory()
    
    # create 2 vectors Ic and Bext, each individual IV file will contribute 
    # one data point in the Ic vs Bext diffraction pattery plot
    
    for file_name in list_of_files:
        f = list(csv.reader(open(file_name, 'r'), delimiter='\t'))
        for lines in islice(f,23,None):
            total_lines+=1
            V=(float(lines[0])/(1e-6))
            I=(float(lines[1])/(1e-6))
            dV=(float(lines[2])/(1e-6))
            dI=np.mean(float(lines[3])/(1e-6))
            Bext=(float(lines[4])/(1e-3))
### this part that extract the information of crtical current
### probably needs more wook to make it more rigorous 
###
                        
            if dV/dI>8:
                Ic_array.append(I)
                break
            
        Bext_array.append(np.mean(float(lines[4])/1e-3))
    return Ic_array, Bext_array


def main():
    Ic, Bext= read_file()
    #print("total number of data point is {0}".format(file_size))
    
    #fig = plt.figure()
    plt.plot(Bext,Ic,".")
    
    
    plt.xlabel("Bext(mT)")
    plt.ylabel("Ic(uA)")
    plt.title("Josephson Junction Ic vs B diffraction----- Can Zhang") 
    
    
    plt.savefig("Ic_vs_Bext.png")


if __name__=="__main__":
    main()



###############################################################################
# End of loop. Print the results.
###############################################################################

print("all done. Result is... ")
plt.savefig("IV.png")

################################################################################
# Make informative comments on the results you just found, like how quickly
# the series converges, and its comparison to the true value of pi.
################################################################################

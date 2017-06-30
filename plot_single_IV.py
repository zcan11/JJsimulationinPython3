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
import csv

plt.close("all")

###################################
# Define and initialize variables
###################################

Voltage=[]
Current=[]
dVolt=[]
dIbias=[]
Bext=[]

#creaete 5 empty vectors to be filled by the data import from the txt file

###############################################################################
# Loop doing the work, with additional detail explained in comments within the loop
###############################################################################
def readFile():
    f = list(csv.reader(open("ivsweepvsF20mK10nA.9.txt", 'r'), delimiter='\t'))
    total_lines=len(f)-23
    for lines in islice(f,23,None):
        Voltage.append(float(lines[0])/(1e-6))
        Current.append(float(lines[1])/(1e-6))
        dVolt.append(float(lines[2])/(1e-6))
        dIbias.append(float(lines[3])/(1e-6))
        Bext.append(float(lines[4])/(1e-3))
        
    return Voltage, Current, dVolt, dIbias, Bext,total_lines
    
def main():
    V,I,dV,dI,B,file_size=readFile()
    print("total number of data point is {0}".format(file_size))
    
    fig = plt.figure()
    plt.plot(I,V,".")
    
    
    plt.xlabel("I(uA)")
    plt.ylabel("V(uV)")
    plt.title("Josephson Junction IV plot----- Can Zhang") 
    
    
    plt.savefig("IV.png")


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

# -*- coding: utf-8 -*-
"""
Created on Sat Mar 04 22:33:55 2017
This is a line to line translation from Erik's Matlab simulation to python code

%Explanation of base program

%The program splits a single junciton up into xmax discrete sections.  Each
%section has a supercurrent density, and a phase difference that is
%contributed to by the field (PhaseF), and an arbitrary phase set at x=1
%called Phase1.  For each value of field and Phase1 the supercurrent at
%each point is calculated and the net supercurrent (sum along the junction)
%is calcualted to find the supercurrent carried at that phase and that
%field.  To find the maximum supercurrent for a given field, the max of
%that vector is taken, and can be plotted against the magnetic field.  This
%is the exact measurment of the critical current vs field that we do in the
%lab.  

@author: can
"""

###################################
# Import libraries 
###################################

import numpy as np
import operator
import matplotlib
import matplotlib.pyplot as plt


###################################
# Define and initialize variables
###################################

xmax=51
xArray = np.linspace(1, xmax, xmax, endpoint=True)

SCurrentMag=1.0
SCurrentNoiseMag=0.
# instead of defining a vector with zero and fill them in the loop
# i jsut create a vector with incremental value here
SCurrentDensity=(SCurrentNoiseMag*np.ones(xmax)+SCurrentMag*np.ones(xmax))/(xmax)
pi_true=np.pi

pmax=101
Phase1Min=-0*pi_true
Phase1Max=2*pi_true
Phase1=np.linspace(0, 2*pi_true, pmax, endpoint=True)


fmax=1001
FluxMin=-3
FluxMax=3
FluxinJunc= np.linspace(FluxMin, FluxMax, fmax, endpoint=True)

Phase1MaxSC=np.zeros(fmax)

SCurrent=np.zeros((xmax,fmax,pmax))
SCurrentNet=np.zeros(pmax)
MaxSCurrentNet=np.zeros(fmax)
IndexMax=np.zeros(fmax)


# And so on...1

###############################################################################
# Loop doing the work, with additional detail explained in comments within the loop
###############################################################################

#   Most of your (well-commented) code goes here.

for i in range(0,fmax):
    
    PhaseF=2*pi_true*FluxinJunc[i]*np.transpose(xArray)/xmax;

    for j in range(0, pmax):
        SCurrent=np.transpose(SCurrentDensity)*np.sin(Phase1[j]+PhaseF)
        SCurrentNet[j]=sum(SCurrent)
        
    IndexMax[i],MaxSCurrentNet[i]=max(enumerate(SCurrentNet),key=operator.itemgetter(1))

    Phase1MaxSC[i]=Phase1[int(IndexMax[i])]
        


#########################################3
######################################
# End of loop. Print the results.
print("all done. Result is... ")
plt.figure()
ax = plt.gca()

plt.subplot(1,2,1)
plt.plot(FluxinJunc,MaxSCurrentNet,'o', markersize=2)
plt.xlabel("FluxinJunc")
plt.ylabel("Ic")
plt.title("Fraunhoffer Diffraction pattern of Ic vs Flux-Can Zhang")



plt.subplot(1,2,2)
plt.plot(FluxinJunc,Phase1MaxSC,'o', markersize=2)
plt.xlabel("FluxinJunc")
# this arbitrary phase is the phase that maximized the critical current
plt.ylabel("Arbitrary Phase")
plt.title("Arbitrary Phase vs Flux-Can Zhang")

plt.savefig("Bext_vs_Ic_and_B_vs_Phase.png")

print("all done")


###############################################################################


################################################################################
# Make informative comments on the results you just found, like how quickly
# the series converges, and its comparison to the true value of pi.
################################################################################
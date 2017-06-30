#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 23:54:26 2017

@author: zcan11
"""

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


"""
%Explanation of base program
%The program splits a squid into two junctions that have xmax discrete sections. Each
%section has a supercurrent density, and a phase difference that is
%contributed to by the field (PhaseF) in the junction, the field in the squid loop,
%and an arbitrary phase set at x=1 %called Phase1. These phase factors are
%all summed along the junction to determine the local phase difference
%across the junction at each point. For each value of field and Phase1 the
%supercurrent at each point is calculated and the net supercurrent (sum
%along the junction and then the sum of the two junctions together)
%is calcualted to find the supercurrent carried at that phase and that
%field. To find the maximum supercurrent for a given field, the max of
%that vector is taken for that field value. The minimum can be calculated
%to find the negative critical current. Both of these can be plotted
%against the magnetic field that is applied. This is the exact measurment
%of the critical current vs field that we do in the lab.
%This version is the most basic version of the squid. It runs through
%Junction asymmetry.
%
%
%
%
%
Critical Current Asymmetry
Junction Area Asymmetry
Critical Current density variation along each junction
Squid Loop size variation
Changes in the field scan range
%Abreviations used
%Junction=Junc
%Super Current = SCur or just SC
%Step Size = SS sufix
%Width = Wid
%Length = Len
%Magnitude = Mag
%% Clearing memory and input screen
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
pi_true=np.pi

xmax1=51
xmax2=51
xArray1 = np.linspace(1, xmax1, xmax1, endpoint=True)
xArray2 = np.linspace(1, xmax1, xmax1, endpoint=True)

# Setting the maximum critical current of each arm of the SQUID leads
SCurrentMag1=1.0
SCurrentMag2=1.0

# setting noise of each arm of the SQUID leads
SCurrentNoiseMag1=0.
SCurrentNoiseMag2=0.

# instead of defining a vector with zero and fill them in the loop
# i jsut create a vector with incremental value here
SCurrentDensity1=(SCurrentNoiseMag1*np.ones(xmax1)+SCurrentMag1*np.ones(xmax1))/(xmax1)
SCurrentDensity2=(SCurrentNoiseMag2*np.ones(xmax2)+SCurrentMag2*np.ones(xmax2))/(xmax2)



# settting the geometric factor for the SQUID
LoopWidth=1
LoopLength=5
LoopArea=LoopWidth*LoopLength

# junction geometry of each SQUID arm
Junction_Width1=0.01
Junction_Length1=0.01
Junction_area1=Junction_Width1*Junction_Length1

Junction_Width2=0.01
Junction_Length2=0.01
Junction_area2=Junction_Width2*Junction_Length2

# phase loop parameter
pmax=101
Phase0Min=-0*pi_true
Phase0Max=2*pi_true
Phase0=np.linspace(0, 2*pi_true, pmax, endpoint=True)

# field parameter for flux in the junction.
fmax=401
FluxMin=-3
FluxMax=3
FluxinJunc1= np.linspace(FluxMin, FluxMax, fmax, endpoint=True)
FluxinJunc2= np.linspace(FluxMin, FluxMax, fmax, endpoint=True)
Fluxinloop=np.zeros(fmax)

Phase1MaxSC=np.zeros(fmax)

SCurrent1=np.zeros((xmax1,fmax,pmax))
SCurrent2=np.zeros((xmax2,fmax,pmax))

SCurrentNet=np.zeros(pmax)
MaxSCurrentNet=np.zeros(fmax)
IndexMax=np.zeros(fmax)


# And so on...1

###############################################################################
# Loop doing the work, with additional detail explained in comments within the loop
###############################################################################

#   Most of your (well-commented) code goes here.

for i in range(0,int(fmax-1)):
    
    PhaseF=2*pi_true*FluxinJunc[i]*np.transpose(xArray)/xmax;

    for j in range(0, int(pmax-1)):
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

plt.savefig("B vs Ic and B vs Phase.png")

print("all done")


###############################################################################


################################################################################
# Make informative comments on the results you just found, like how quickly
# the series converges, and its comparison to the true value of pi.
################################################################################
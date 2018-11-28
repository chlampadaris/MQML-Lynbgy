from __future__ import division, print_function
import csv
import numpy as np
import matplotlib.pyplot as plt

#_____________________________________________________________________________#
#__________________FUNCTIONS DEFINITIONS______________________________________#
#_____________________________________________________________________________#

# capacitance from COMSOL
def capacitance(width): # in F and width in um
    lo=0.25*10**(-6)
    x = np.array([lo,2*lo,3*lo,4*lo])
    y = np.array([0.55e-15, 1.04e-15, 1.53e-15, 2.02e-15])
    linear_fit = np.polyfit(x,y, deg=1)
    a = linear_fit[0]
    b = linear_fit[1]
    return a*width+b


# Close all the previously open figures
plt.close("all")

#_____________________________________________________________________________#
#_________________PARAMETERS DEFINITIONS______________________________________#
#_____________________________________________________________________________#

# MAGNETIC FIELD STEPS
B = [0,1,2,3,6,9]  #T
# DEVICE
QDev = 'PiciChip1Red' #device
# SWEEPS
sweep = ['up', 'down']
# DEFINE THE INITIAL NUM0BER IF THE RUNNING RESULTS DATABASE
count=1
# TEMPERATURE
T = 1.7 # K0
# CHANNEL LENGHT
L = 0.5e-6 # um
# NW WIDTH
W = 100e-9 #nm

#_____________________________________________________________________________#
#_________________INSERT DATA_________________________________________________#
#_____________________________________________________________________________#

Vg = []
I  = []
QG = []
QGrc = []
G  = []
Ig = []
counti=count
for i in range(len(B)):
    Vg.append([])
    I .append([])
    QG.append([])
    QGrc.append([])
    G .append([])  
    Ig.append([])
    for j in range(len(sweep)):
        Vg[i].append([])
        I[i] .append([])
        QG[i].append([])
        QGrc[i].append([])
        G[i] .append([])
        Ig[i].append([])
        name = "results-" + "{:.0f}".format(counti) + "-1.csv"
        counti = counti+1
        with open( name, 'rb' ) as csv_file : 
            print (name)
            csv_reader = csv.reader(csv_file, delimiter=',', quotechar='|')
            line_count = 0
            for format_line in csv_reader:
                if line_count == 0:
                    #print ('Column names are', format_line)
                    line_count = line_count + 1
                else:
                    Vg[i][j].append(float(format_line[1]))
                    I[i][j] .append(float(format_line[3]))
                    QGrc[i][j].append(float(format_line[2]))
                    Rc = 1e2
                    Go = 7.7480917310*10**(-5)
                    gg = float(format_line[2])
#                    print ((((gg*Go)**(-1)-Rc))**(-1)/Go)
                    conducatance = (-Rc+(gg*Go)**(-1))**(-1)
                    QG[i][j].append(float(conducatance/Go))
                    G[i][j] .append(float(conducatance))
                    Ig[i][j].append(float(format_line[4]))
                    line_count = line_count + 1
# Sort ascending by voltage 
for i in range(len(B)):
    for j in range(len(sweep)):
        idx      = np.argsort(Vg[i][j])
        Vg[i][j] = np.array(Vg[i][j])[idx]
        I[i][j]  = np.array(I[i][j])[idx]
        QG[i][j] = np.array(QG[i][j])[idx]
        QGrc[i][j] = np.array(QGrc[i][j])[idx]
        G[i][j]  = np.array(G[i][j])[idx]
        Ig[i][j] = np.array(Ig[i][j])[idx]


# Calculate capacitance
C = capacitance(L)


#_____________________________________________________________________________#
#_________________PLOTTING____________________________________________________#
#_____________________________________________________________________________#

colours = ['r', 'c', 'y', 'b', 'm', 'g','r', 'c', 'y', 'b', 'm', 'g','r', 'c', 'y', 'b', 'm', 'g']
transparency = [1.,0.2]
# PLOT 0
# QG - Vg
fig0, ax0 = plt.subplots(1,2,figsize=(12, 6))
for j in range(len(B)):
    for i in range(len(sweep)):
        ax0[0].set_title("Data with contact resistance")
        ax0[1].set_title("Data without contact resistance")
        ax0[0].set_xlabel("Gate Voltage (V)")
        ax0[0].set_ylabel(r"Quantized conductance $(2e^2/h)$")
        ax0[0].set_ylim(8.5,13.5)
        ax0[1].set_ylim(8.5,13.5)
        ax0[0].xaxis.grid(True)
        ax0[0].yaxis.grid(True)
        ax0[1].xaxis.grid(True)
        ax0[1].yaxis.grid(True)

        box1 = ax0[0].get_position()
        box2 = ax0[1].get_position()
        ax0[0].set_position([box1.x0-0.006, box1.y0, box1.width, box1.height])
        ax0[1].set_position([box2.x0-0.008, box2.y0, box2.width, box2.height])

        ax0[0].plot(Vg[j][i], QGrc[j][i],'.', c=colours[j],alpha = transparency[i], label="B = "+"{:.1f}".format(B[j]) + " T; sweep "+"{0:s}".format(sweep[i]),picker=2)        
        ax0[1].plot(Vg[j][i], QG[j][i], c=colours[j],alpha = transparency[i], label="B = "+"{:.1f}".format(B[j]) + " T; sweep "+"{0:s}".format(sweep[i]),picker=2)
fig0.legend(loc='center right', bbox_to_anchor=(0.995, 0.5))
plt.show()

# PLOT 01
# QG - Vg
fig1, ax1 = plt.subplots(2,1,figsize=(7.5, 6))
for j in range(len(B)):
    for i in range(len(sweep)):
        ax1[1].set_xlabel("Gate Voltage (V)")
        ax1[0].set_ylabel(r"Current $A$")
        ax1[1].set_ylabel(r"Current leakage $A$")
        box1 = ax1[0].get_position()
        box2 = ax1[1].get_position()
        ax1[0].set_position([box1.x0+0.0055, box1.y0+0.002, box1.width * 0.95, box1.height])
        ax1[1].set_position([box2.x0+0.0055, box2.y0, box2.width * 0.95, box2.height])
        ax1[0].plot(Vg[j][i], I[j][i], c=colours[j],alpha = transparency[i], label="B = "+"{:.1f}".format(B[j]) + " T; sweep "+"{0:s}".format(sweep[i]),picker=2)
        ax1[1].plot(Vg[j][i], Ig[j][i], c=colours[j],alpha = transparency[i], label="B = "+"{:.1f}".format(B[j]) + " T; sweep "+"{0:s}".format(sweep[i]),picker=2)
fig1.legend(loc='center right', bbox_to_anchor=(0.95, 0.5))
plt.show()



#_____________________________________________________________________________#
#_________________SAVE FIGURES________________________________________________#
#_____________________________________________________________________________#
"""
fig1.savefig()
fig2.savefig()
fig0.savefig()
"""
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 19:12:39 2021

@author: Mikael & Seif

Total simulation (all parts combined)
"""

import numpy as np
import csv

"""We define our starting variables"""

# inhabitants per region:
# inputting the number of inhabitants
print("\nEstimate the current population of the canton of Vaud.")
habTotalEstim = input("\nIf you do not know, press Enter...")
habTotal = 815300

# making sure that the population value input is relevant
# (that it is an integer and that it is not too far from the current population of the canton):


if habTotalEstim == "":

    print("\nNo received value, we shall then take the value of 2020 which is 815300 people.\n")
    habTotalEstim = habTotal

else:
    try:
        habTotalEstim = int(habTotalEstim)

    except ValueError:
        print("\nReceived value is not an integer, we shall take the value of 2020 which is 815300 people.\n")
        habTotalEstim = habTotal

    if habTotalEstim < 0:
        print("\nReceived value is negative, we shall take the value of 2020 which is 815300 people.\n")
        habTotalEstim = habTotal


if habTotalEstim != habTotal:

    if np.abs((habTotalEstim) - habTotal) > 100000:
        print("\nReceived value is too far from official values, we shall take the value of 2020 which is 815300 people.\n")
        habTotalEstim = habTotal

    else:
        print("\nReceived value is within a reasonable range from official values, we shall then base all our calculations on this value.\n")



# we have the inhabitance percentage of the inhabitants
# of a region with respect to the canton
prophabLausanne = 0.25
prophabOuest = 0.25
prophabLaCote = 0.14
prophabNord = 0.10

"""We can easily calculate the number of people from which
TRIDEL collects waste from the previous data.
WARNING: we weigh the number of inhabitants by a factor of 1/2
for the inhabitants of Nord and La Côte regions"""


habLausanne  = habTotal * prophabLausanne
habOuest = habTotal * prophabOuest
habLaCote = habTotal * 0.5 * prophabLaCote
habNord = habTotal * 0.5 * prophabNord
habChargTot = habLausanne + habOuest + habLaCote + habNord
habChargLst = np.array([habLausanne, habOuest, habLaCote, habNord])

#waste per person per region [kg/year] : wastehabRegion

wastehabLausanne = 185.1
wastehabNord = 151.4
wastehabOuest = 130.8
wastehabLaCote = 147.3
wasteHabLst = np.array([wastehabLausanne, wastehabNord, wastehabOuest,  wastehabLaCote])

"""we can calculate the inhabitants' waste average,
weighted by the number of inhabitants of each city per year [kg/year]"""


wastePondLst = (wasteHabLst * (habChargLst / habChargTot))
wasteAvg = np.sum(wastePondLst)
#print(wastePondLst, wasteAvg)

"""We compute the total waste quantity per day,
for that, we estimate a sigma of 20% times wasteAvg,
and randomly (but following a normal distribution) generate
a value of the total waste quantity each day [kg/day]"""


sigmaWasteAvg = 0.2 * wasteAvg
wasteYearArray = np.random.normal(wasteAvg, sigmaWasteAvg, size=(365))
wasteDayArray = (wasteYearArray / 365) * habChargTot

#converting the array to a list

wasteDayLst = []

for i in wasteDayArray:
    wasteDayLst.append([i])


"""We now create a CSV file containing the data we have generated"""

print("Creating a CSV file for the generated values of waste per day...\n")
with open("wasteDayLst.csv", "w", newline= "") as file:
    writer = csv.writer(file)
    writer.writerows(wasteDayLst)


"""We run the second part of the code, written in C."""

print("Running the program computing the values...\n")

import os

# testing whether the executable file is at the right place
# The program then waits for the user to execute part 2 to resume

while not os.path.exists("Part2TRIDEL.exe"):
   print("\nPart2TRIDEL.exe does not exist or isn't in the same folder as the program.\n")
   print("Please, compile Part2TRIDEL.c or add the .exe file in the same folder,\n")
   input("Then, come back to the Python terminal and press enter to continue...")
   print("\n")

os.startfile(r"Part2TRIDEL.exe")

print("Creating a CSV file of calculated Power output...\n")
print("Creating a CSV file of Variance calculated Power output...\n")
print("Creating a CSV file of the needed fuel if the output is negative...\n")


# waiting for the PowerOutput CSV file to be written
# before running the last part

import time
time.sleep(0.5)

###########################################################################
###########################################################################

"""Interpreting the results"""

import matplotlib.pyplot as plt

"""Part 1: CSV file reading"""
# 1st we need to import the CSV file of Power outputs into a table

PowerTable = np.genfromtxt('PowerTable.csv', delimiter = ',', dtype = 'float64') # [MW]

wasteDayLst = np.genfromtxt('wasteDayLst.csv', delimiter = ',', dtype = 'float64') # [Kg]
wasteDayLst /= 1000 # conversion from [kg] to [tonnes]

varPowerTable = np.genfromtxt('varPowerTable.csv', delimiter = ',', dtype = 'float64') # [MW]

FuelNeededDay = np.genfromtxt('FuelNeededDay.csv', delimiter = ',', dtype = 'float64') # [Tons]

"""Part 2: initializing reference values"""
# These values are given in [MWh] per month

TridelValues = np.array([4942.84, 4909.77, 4959.43, 5041.34, 5876.92, 1396.43, 7550.33, 8926.98, 8242.48, 6819.23, 5744.39, 5439.18]) #[MWh / month]
TridelValues = TridelValues / (30.4 * 24) # converting [MWh] to [MW]

# Modifying the dimension of the arrays, in order for it to be possible
# to plot official and calculated values together

daysInMonths = [31, 28, 30, 31, 30, 31, 31, 31, 30, 31, 30, 31]
DayTridelVal = []

for i in range(len(TridelValues)):
    repeatedValue = np.repeat(TridelValues[i], daysInMonths[i])
    DayTridelVal = np.concatenate((DayTridelVal, repeatedValue))


"""Part 3 energy output plot"""
# We divide our plot into four subplots:

days = np.array([day + 1 for day in range(365)])

wasteDay = np.array(wasteDayLst)

Fueltest = np.zeros(365)
fig, axs = plt.subplots(2, 2)
# Plotting calculated output values against true values
axs[0, 0].plot(days, PowerTable, 'tab:orange', label="Calculated Power")
axs[0, 0].plot(days, DayTridelVal, 'tab:red', label="Official Power production")
axs[0, 0].set_title('Calc. and true Power output')
axs[0, 0].set(ylabel="[MW]")

# Plotting mass of waste per day
axs[1, 0].plot(days, wasteDay)
axs[1, 0].set_title('Waste weight')
axs[1, 0].set(ylabel="[tons]")
axs[1, 0].set(xlabel="[days]")

# Plotting calculated output values with variance against true values
axs[0, 1].plot(days, varPowerTable, 'tab:orange', label="Calc. Power with variance")
axs[0, 1].plot(days,DayTridelVal, 'tab:red', label="Official Power production")
axs[0, 1].set_title('Calc. variance and true output')

# Plotting minimal fuel mass in order to conduct combustion
# with our added variance model
axs[1, 1].plot(days, FuelNeededDay, 'tab:brown')
axs[1, 1].set_title('Minimal fuel needed')
axs[1, 1].set(xlabel="[days]")

plt.tight_layout()
plt.show()

print("\nTHE END\n")

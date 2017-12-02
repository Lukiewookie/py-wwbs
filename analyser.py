#!/usr/bin/python3

import pandas as pd
import matplotlib.pyplot as plt


data = pd.read_csv('outfile.csv')

data["download"].plot(secondary_y=True, label="Download", legend="True")
data["upload"].plot(secondary_y=True, label="Upload", legend="True")

data["temp"].plot(legend=True)
data["speed"].plot(legend=True)
data["clouds"].plot(legend=True)
try:
    data["rain"].plot(legend=True)
except TypeError as e:
    pass
try:
    data["snow"].plot(legend=True)
except TypeError as e:
    pass
data["humidity"].plot(legend=True)
#data["press"].plot(legend=True)

plt.draw()
plt.show()

import pandas as pd
import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_context("paper", font_scale=2.)
import matplotlib as mpl
mpl.rcParams['figure.figsize'] = 12, 8
from sklearn import gaussian_process



datafile = "sm_37_90.csv"
df = pd.read_csv(datafile)
df['time'] = pd.to_datetime(df['time'])
df = df.set_index('time')

df['LST_Day_1km'].plot()
plt.title("Modis Land Surface Temperature")
plt.ylabel("Temperature (K)")
plt.xlabel("Time")
plt.savefig("modis_temperature.pdf")
plt.close()


df['prcp'].plot()
plt.title("TRMM Daily Precipitation")
plt.ylabel("Precipitation (mm/hr)")
plt.xlabel("Time")
plt.savefig("trmm_precip.pdf")
plt.close()

df['soil_moisture'].plot()
plt.title("AMSR-E Soil Moisture")
plt.ylabel("Soil Moisture (g/cm$^3$)")
plt.xlabel("Time")
plt.savefig("amsre_soil_moisture.pdf")
plt.show()







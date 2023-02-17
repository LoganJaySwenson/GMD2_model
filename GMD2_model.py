# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 14:06:20 2023

@author: Logan
"""

# Import libraries
import sys
import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import flopy

# Set dir
os.chdir("C:/Users/Logan/OneDrive - University of Kansas/GMD2_model")

# Set model path
model_path = "./GMD2_transient"

# Load GMD2 trans_2d model
ml = flopy.modflow.Modflow.load("trans_2d.nam", model_ws = model_path,
                               exe_name = "mf2005", version = "mf2005")

# Plot active model domain
fig = plt.figure(figsize = (8,8))
plt.title("Equus Beds Aquifer\nActive Area")
ml.modelgrid.set_coord_info()
mapview = flopy.plot.PlotMapView(model = ml)
quadmesh = mapview.plot_ibound()
plt.show()

# Get stress periods
fname = os.path.join(model_path, "trans_2d.hds")
hdobj = flopy.utils.HeadFile(fname)
stress_periods = hdobj.get_kstpkper()
print(stress_periods)


# Get simulated heads & saturated thickness for 1945
s1 = hdobj.get_data(kstpkper=(0,0))
st1 = ml.modelgrid.saturated_thick(s1, mask=-99.9)
s1[s1 == -99.9] = np.nan

# Get simulated heads & saturated thickness for 2016
s145 = hdobj.get_data(kstpkper=(9,144))
st145 = ml.modelgrid.saturated_thick(s145, mask=-99.9)
s145[s145 == -99.9] = np.nan

# Plot simulated heads in 1945
fig = plt.figure(figsize=(15, 10))
plt.title("Equus Beds Aquifer\nSimulated Heads in 1945")
mapview = flopy.plot.PlotMapView(model = ml)
quadmesh = mapview.plot_ibound()
quadmesh = mapview.plot_array(s1, alpha=0.5)
plt.colorbar(quadmesh, shrink=0.5)
plt.show()

# Plot simulated heads in 2016
fig = plt.figure(figsize=(15, 10))
plt.title("Equus Beds Aquifer\nSimulated Heads in 2016")
mapview = flopy.plot.PlotMapView(model = ml)
quadmesh = mapview.plot_ibound()
quadmesh = mapview.plot_array(s145, alpha=0.5)
plt.colorbar(quadmesh, shrink=0.5)
plt.show()

# Get the change in simulated head
sdiff = np.subtract(s145, s1)

# Let's deal with impossible values
sdiff_sorted = sdiff[~np.isnan(sdiff)] #remove all nan values to plot histogram!
fig = plt.figure(figsize = (8,8))
plt.hist(sdiff_sorted, bins=np.arange(min(sdiff_sorted), max(sdiff_sorted) + 1, 1))
plt.xlim(-100, 40)
plt.show()

# Set arbitrary bounds based on visual assessment
sdiff[sdiff < -60] = np.nan
sdiff[sdiff > 40] = np.nan

# Plot the change in simulated head between 1945 and 2016!
fig = plt.figure(figsize=(15, 10))
plt.title("Difference in Simulated Heads between 1945 and 2016")
mapview = flopy.plot.PlotMapView(model = ml)
quadmesh = mapview.plot_ibound()
quadmesh = mapview.plot_array(sdiff, alpha=0.5)
plt.colorbar(quadmesh, shrink=0.5)
plt.show()




# Plot saturated thickness in 1945
fig = plt.figure(figsize=(15, 10))
plt.title("Equus Beds Aquifer\nSaturated Thickness in 1945")
mapview = flopy.plot.PlotMapView(model = ml)
quadmesh = mapview.plot_ibound()
quadmesh = mapview.plot_array(st1, alpha=0.5)
plt.colorbar(quadmesh, shrink=0.5, label = "Saturated thickness (ft)")
plt.show()


# Plot saturated thickness in 2016
fig = plt.figure(figsize=(15, 10))
plt.title("Equus Beds Aquifer\nSimulated Heads in 2016")
mapview = flopy.plot.PlotMapView(model = ml)
quadmesh = mapview.plot_ibound()
quadmesh = mapview.plot_array(st145, alpha=0.5)
plt.colorbar(quadmesh, shrink=0.5, label = "Saturated thickness (ft)")
plt.show()


# Get the change in saturated thickness between 1945 and 2016!
stdiff = np.subtract(st145, st1)
# Let's deal with impossible values!
stdiff_sorted = stdiff[~np.isnan(stdiff)] #remove all nan values to plot histogram!
fig = plt.figure(figsize = (8,8))
#plt.title("Change in Saturated Thickness between 1945 and 2016 (ft)")
plt.hist(stdiff_sorted, bins=np.arange(min(stdiff_sorted), max(stdiff_sorted) + 2, 2))
plt.xlabel("Change in saturated thickness between 1945 and 2016 (ft)")
plt.ylabel("Number of model cells")
plt.show()

# Set arbitrary bounds based on visual assessment
stdiff[stdiff < -60] = np.nan
stdiff[stdiff > 40] = np.nan

# Plot change in saturated thickness from 1945 to 2016
fig = plt.figure(figsize=(15, 10))
plt.title("Change in Saturated Thickness between 1945 and 2016")
mapview = flopy.plot.PlotMapView(model = ml)
quadmesh = mapview.plot_ibound()
quadmesh = mapview.plot_array(stdiff, alpha=0.5)
plt.colorbar(quadmesh, shrink=0.5, label = "ft")
plt.show()
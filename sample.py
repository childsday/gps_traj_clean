import pandas as pd
from traj import traj, traj_cutoff, traj_resample

# Set the maximum number of columns to display
pd.set_option('display.max_columns', 100)

# Read the data from taxi1.csv and taxi2.csv files
data1 = pd.read_csv(r'testdata/taxi1.csv', parse_dates=True)
data2 = pd.read_csv(r'testdata/taxi2.csv', parse_dates=True)

# Concatenate the data from both files into a single DataFrame
data = pd.concat([data1, data2])

# Segment the trajectory data
oddata = traj.traj_sege(data)

# Segment the trajectory data with splitting
oddata = traj.traj_sege(oddata, split=True)


# Calculate the delta of trajectory data within specified distance and velocity ranges
oddata = traj.traj_delta(oddata, dis_range=[0, 16*1800], v_range=[0, 16])

# Perform cutoff based on distance gap
oddata = traj_cutoff.cutoff(oddata, disgap=[[116.51135, 39.93883], [116.25788, 39.92787], 2000])

# Perform cutoff based on time gap
oddata = traj_cutoff.cutoff(oddata, timegap=3600)

# Resample the trajectory data
oddata = traj_resample.resample(oddata)

#plot trajectory
from traj_plot import plot
plot.traj_plot(oddata)

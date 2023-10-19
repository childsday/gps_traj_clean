import pandas as pd
from traj.dis import dis


def traj_delta(oddata, time_range=[0, 3600], dis_range=[0, 999999], v_range=[0, 34], geo=True, keep=False):
    # Initialize a counter variable
    p = 0

    # Iterate over unique values in the 'id' column of the input DataFrame
    for id in oddata['id'].unique():
        # Filter the DataFrame for the current 'id' and sort it by 'stime'
        traj = oddata[oddata['id'] == id].sort_values(['stime']).reset_index(drop=True)

        # Convert 'stime' column to datetime format
        traj['stime'] = pd.to_datetime(traj['stime'])

        # Calculate the time difference between consecutive rows and convert it to seconds
        traj['tdelta'] = traj['stime'].shift(-1) - traj['stime']
        traj['tdelta'] = traj['tdelta'].dt.total_seconds()

        # Shift 'slon' and 'slat' columns to get the next longitude and latitude values
        traj['elon'] = traj['slon'].shift(-1)
        traj['elat'] = traj['slat'].shift(-1)

        # Calculate the distance between consecutive points using the 'dis' function from the 'traj.dis' module
        traj['delta'] = traj.apply(lambda x: dis(x['slon'], x['slat'], x['elon'], x['elat'], geo=geo), axis=1)

        # Calculate the velocity by dividing the distance by the time difference
        traj['vdelta'] = traj['delta'] / traj['tdelta']

        # Drop unnecessary columns
        traj = traj.drop(['elon', 'elat'], axis=1)

        # Filter the DataFrame based on time_range, dis_range, and v_range
        if time_range:
            traj = traj[(traj['tdelta'] > time_range[0]) & (traj['tdelta'] < time_range[1])]
        if dis_range:
            traj = traj[(traj['delta'] > dis_range[0]) & (traj['delta'] < dis_range[1])]
        if v_range:
            traj = traj[(traj['vdelta'] > v_range[0]) & (traj['vdelta'] < v_range[1])]

        # Drop additional columns if keep is False
        if keep is False:
            traj = traj.drop(['vdelta', 'tdelta', 'delta'], axis=1)

        # Concatenate the filtered DataFrame with the previous ones
        if p == 0:
            oddata1 = traj
        else:
            oddata1 = pd.concat([oddata1, traj])

        # Increment the counter
        p += 1

    return oddata1


def traj_sege(data, split=False):
    if split is False:
        # Rename columns for consistency
        data.columns = ['id', 'stime', 'slon', 'slat']

        # Sort the DataFrame by 'id' and 'stime'
        oddata = data.sort_values(by=['id', 'stime'])

        # Shift 'slon', 'slat', and 'stime' columns to get the next longitude, latitude, and time values
        oddata['elon'] = oddata['slon'].shift(-1)
        oddata['elat'] = oddata['slat'].shift(-1)
        oddata['etime'] = oddata['stime'].shift(-1)

        # Filter the DataFrame to keep only rows where the 'id' is the same as the next row
        oddata = oddata[oddata['id'].shift() == oddata['id']]

        # Create 's_geometry' and 'e_geometry' columns with tuples of (slon, slat) and (elon, elat) respectively
        oddata['s_geometry'] = oddata.apply(lambda z: (z.slon, z.slat), axis=1)
        oddata['e_geometry'] = oddata.apply(lambda z: (z.elon, z.elat), axis=1)
    else:
        # Select specific columns for split mode
        oddata = data[['id', 'stime', 'slon', 'slat', 's_geometry']]

    return oddata







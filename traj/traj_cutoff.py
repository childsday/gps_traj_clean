import pandas as pd
import geopandas as gpd
from traj.dis import dis

# Disable chained assignment warning
pd.options.mode.chained_assignment = None


def cutoff(oddata, timedelta=None, timegap=None, disgap=None, minlen=5):
    # Get unique values of 'id' column
    li = oddata['id'].unique()

    # Initialize a counter variable
    p = 0

    # Iterate over unique 'id' values
    for id in li:
        # Filter the DataFrame for the current 'id' and sort it by 'stime'
        traj = oddata[oddata['id'] == id].sort_values(['stime']).reset_index(drop=True)

        # Convert 'stime' column to datetime format
        traj['stime'] = pd.to_datetime(traj['stime'])

        # Apply timedelta condition if provided
        if timedelta:
            traj['ins'] = traj['stime'].shift(-1) - traj['stime']
            traj['ins'] = traj['ins'].dt.total_seconds()
            traj['ins'] = traj['ins'].apply(lambda x: 0 if x < timedelta else 1)

        # Apply timegap condition if provided
        if timegap:
            timegap = timegap - 600
            traj['ins'] = 1
            box = traj.index.values.tolist()
            poi1, poi2 = 0, 1
            while poi2 < len(box):
                if traj.loc[poi2, 'stime'] <= traj.loc[poi1, 'stime'] + pd.Timedelta(seconds=timegap):
                    traj.loc[poi2 - 1, 'ins'] = 0
                    poi2 += 1
                else:
                    poi2 += 1
                    poi1 = poi2

        # Apply disgap condition if provided
        if disgap:
            traj['ins'] = 0
            traj['dis1'] = traj.apply(lambda x: dis(x['slon'], x['slat'], disgap[0][0], disgap[0][1]), axis=1)
            traj['dis2'] = traj.apply(lambda x: dis(x['slon'], x['slat'], disgap[1][0], disgap[1][1]), axis=1)
            traj['ins'] = traj.apply(lambda x: 1 if x['dis1'] < disgap[2] or x['dis2'] < disgap[2] else 0, axis=1)
            traj = traj.drop(['dis1', 'dis2'], axis=1)

        # Get indices where 'ins' is 1 and drop the 'ins' column
        cutoff = traj[traj['ins'] == 1].index.values.tolist()
        traj = traj.drop(['ins'], axis=1)

        # Initialize a counter variable
        p1 = 0

        # Process cutoff segments
        if len(cutoff) > 0:
            if not disgap:
                poi1, poi2 = 0, cutoff[0]
            else:
                if len(cutoff) > 1:
                    poi1, poi2 = cutoff[0], cutoff[1]
                else:
                    continue

            # Convert 'id' column to string
            traj['id'] = traj['id'].astype(str)

            # Iterate over cutoff segments
            for j in range(len(cutoff)):
                if len(traj.loc[poi1:poi2, 'id']) > minlen:
                    if p1 == 0:
                        traj1 = traj.loc[poi1:poi2]
                        traj1['id'] = traj1['id'] + ' ' + str(j)
                    else:
                        traj2 = traj.loc[poi1:poi2]
                        traj2['id'] = traj2['id'] + ' ' + str(j)
                        traj1 = pd.concat([traj1, traj2])
                    p1 += 1
                poi1 = poi2
                if j == len(cutoff) - 1:
                    poi2 = len(traj)
                else:
                    poi2 = cutoff[j + 1]

            traj = traj1

        else:
            continue

        # Apply additional disgap condition if provided
        if disgap:
            for i in traj['id'].unique():
                sege = traj[traj['id'] == i]
                ox, oy, dx, dy = sege.head(1)['slon'], sege.head(1)['slat'], sege.tail(1)['slon'], sege.tail(1)['slat']
                od = dis(ox, oy, dx, dy)
                if od < disgap[2] * 2:
                    traj = traj[traj['id'] != i]

        # Check if the length of traj is greater than minlen
        if len(traj) > minlen:
            p += 1
        else:
            continue

        # Iterate over unique 'id' values in traj
        for i in traj['id'].unique():
            sege = traj[traj['id'] == i]

        # Concatenate the filtered DataFrame with the previous ones
        if p == 1:
            oddata1 = traj
        else:
            oddata1 = pd.concat([oddata1, traj])

    # Convert the resulting DataFrame to a GeoDataFrame
    return gpd.GeoDataFrame(oddata1)

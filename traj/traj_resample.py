import pandas as pd

#This function samples the oddata dataframe with a factor of k.
def resample(oddata, k=2, default=False):
    # Iterate through each unique 'id'
    for traj in oddata.id.unique().tolist():

        # Get indices of rows with same 'id'
        ind = oddata[oddata['id'] == traj].index.values.tolist()

        if default is True:
            # Drop every kth row
            oddata = oddata.drop([ind[_ * k] for _ in range(len(ind) // k)])

        else:
            # Retain rows where timestamp is at least k seconds apart
            ind1 = []
            poi1, poi2 = 0, 1
            tim = oddata.iloc[ind].copy()

            while poi2 < len(ind) - 1:
                if tim.iloc[poi2].stime >= tim.iloc[poi1].stime + pd.Timedelta(seconds=k):
                    ind1.append(ind[poi2 - 1])
                    poi2 += 1
                else:
                    poi2 += 1
                    poi1 = poi2

    return oddata

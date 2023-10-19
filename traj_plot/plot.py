def traj_plot(data):
    import matplotlib.pyplot as plt
    traj_collect={}
    for id in data['id'].unique():
        traj_collect[id]=data[data['id']==id]['s_geometry'].values.tolist()

        plt.plot([point[0] for point in traj_collect[id]], [point[1] for point in traj_collect[id]], marker='o')

    # Set the x and y axis labels
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')

    # Set the title of the plot
        plt.title('GPS Trajectory')

    # Display the plot
        plt.show()
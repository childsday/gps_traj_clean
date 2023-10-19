import geopandas as gpd
import pandas as pd
from shapely import Point, LineString
import osmnx as ox

def road_loader(point):
    # Check if the length of the 'point' parameter is less than 2
    if len(point) < 2:
        # If the length is less than 2, create a road graph from a single point within a specified distance
        road_graph = ox.graph_from_point(point, dist=500, network_type='all')
    else:
        # If the length is 2 or more, create a road graph from a bounding box defined by the points
        road_graph = ox.graph_from_bbox(point[0], point[1], point[2], point[3])

    # Create a dictionary to store the road attributes
    bucket = {'s': [], 'e': [], 'geometry': [], 's_geometry': [], 'e_geometry': [], 'len': [], 'highway': []}

    # Iterate over the edges of the road graph
    for s, e, data in road_graph.edges(data=True):
        # Check if the 'geometry' attribute is missing in the edge data
        if 'geometry' not in data:
            # If missing, create a LineString geometry from the start and end points of the edge
            p1 = Point(road_graph.nodes[s]['x'], road_graph.nodes[s]['y'])
            p2 = Point(road_graph.nodes[e]['x'], road_graph.nodes[e]['y'])
            data.update({'geometry': LineString((p1, p2))})

        # Append the attributes to the corresponding lists in the 'bucket' dictionary
        bucket['s'].append(s)
        bucket['e'].append(e)
        bucket['geometry'].append(LineString((p1, p2)))
        bucket['s_geometry'].append(p1)
        bucket['e_geometry'].append(p2)
        bucket['len'].append(data['length'])
        bucket['highway'].append(data['highway'])

    # Create a pandas DataFrame from the 'bucket' dictionary
    gpd_edges = pd.DataFrame(bucket, columns=('s', 'e', 'geometry', 's_geometry', 'e_geometry', 'len', 'highway'))

    # Convert the pandas DataFrame to a GeoDataFrame
    gpd_edges = gpd.GeoDataFrame(gpd_edges)

    # Set the coordinate reference system (CRS) of the GeoDataFrame to match the road graph
    gpd_edges.crs = road_graph.graph['crs']

    # Create a new column in the GeoDataFrame containing the bounding box of each geometry
    gpd_edges['bbox'] = gpd_edges.apply(lambda row: row['geometry'].bounds, axis=1)

    # Return the GeoDataFrame
    return gpd_edges

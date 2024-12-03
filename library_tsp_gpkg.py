import numpy as np
import pandas as pd
import geopandas as gpd
import googlemaps
from tqdm import tqdm
from datetime import datetime
from osgeo import ogr, osr
osr.UseExceptions()

def compute_optimal_path(origin, destinations, api_key, loop):
    '''
    Compute the optimal path between points by solving the traveling salesman problem with a 
    fixed point of origin and the possibility of looping back to the point of origin at the end 
    of the path. The distance used is the actual driving distance obtained with the googlemaps 
    API distance_matrix.
    To solve the traveling salesman problem, the function uses a Branch-and-Bound algorithm. 
    It explores all the branch of the path, pruning when the distance is longer than the best path.
    Points to visit can be indicated in latitude, longitude, address or location name format.

    Display the optimal path and the distance in kilometer.

    :param origin: Initial point.
    :param destinations: list of points to visit.
    :param api_key: Google Maps API key.
    :param loop: If True, return to starting point after visiting all points.

    :return: pandas.DataFrame with points and their index in optimal order, the distance with 
    the previous step, the latitude and longitude, and the coordinate system to consider.
    '''
    client = googlemaps.Client(key=api_key)  # initialize the Google Maps client
    destinations.insert(0, origin)  # add the origin at the beginning of the destination list
    n = len(destinations)  # total number of points in the route
    dist_matrix = np.zeros((n, n))  # initialize the distance matrix

    # distance matrix using Google Maps Distance Matrix API
    with tqdm(total=n * (n - 1), desc="Computing Distance Matrix") as pbar:  # Initialize tqdm progress bar
        for i in range(n):
            for j in range(n):
                if i != j:  # skip self-to-self distances
                    response = client.distance_matrix(destinations[i], destinations[j], 
                                                      language='English', departure_time=datetime.now())  # use of the distance matrix googlemaps API
                    distance = response['rows'][0]['elements'][0]['distance']['value']  # extract the distance value
                    dist_matrix[i][j] = round(distance / 1000.0, 3)  # convert meters to kilometers
                    pbar.update(1)  # Update the progress bar

    # initialize variables for the best distance and path
    best_dist = float('inf')
    best_path = []

    # branch-and-Bound function for Travelling Salesman Problem with fixed origin
    def solve_tsp_fixed_start(path, dist):
        nonlocal best_dist, best_path

        # base case: Check if all points have been visited
        if len(path) == n:  # check if the complete path is the best
            if loop:  # add distance to return to the origin if looping is required
                dist += dist_matrix[path[-1]][path[0]] 
            if dist < best_dist:  # update the best solution if the path is shorter
                best_dist = dist
                best_path = path[:]
            return

        # pruning: cut the branch if current distance > best distance
        if dist >= best_dist:
            return

        # explore unvisited nodes, adding one node to the path at each step
        for i in range(1, n):  # start from 1 to do not revisit the origin point (0)
            if i not in path:
                solve_tsp_fixed_start(path + [i], dist + dist_matrix[path[-1]][i])

    # start the recursive TSP solution with the origin (index 0)
    solve_tsp_fixed_start([0], 0)

    # append the origin to the path if the loop is required
    if loop:
        best_path.append(0)

    # collect geospatial and distance data for the optimal path
    path_data = []
    origin_latlong = client.geocode(origin)[0]['geometry']['location']
    path_data.append({  # info for the origin
        'index': 0,
        'adress': origin,
        'km': 0.0,
        'lat': origin_latlong['lat'],
        'long': origin_latlong['lng'],
        'RS': 'WGS84'})  # coordinate reference system

    for index in range(1, len(best_path)):  # compute the latitude and longitude for each point
        i = best_path[index]
        prev_i = best_path[index - 1]
        geocode_data = client.geocode(destinations[i])[0]['geometry']['location']  # use of the geocode googlemaps API

        path_data.append({  # add the data of each point of the optimal path to the dictionary
            'index': i,
            'adress': destinations[i],
            'km': dist_matrix[prev_i][i],  # distance between consecutive points
            'lat': geocode_data['lat'],
            'long': geocode_data['lng'],
            'RS': 'WGS84'})
    
    path_df = pd.DataFrame(path_data)

    print("Optimal path:\n")  # display the optimal path and total distance
    for i in range(0, len(path_df)):
        print(f"- {i} - {path_df.adress[i]} ({path_df.km[i]} km)")
    print(f"\nOptimal distance: {path_df.km.sum()} km")

    return path_df
    
def export_to_geopackage(df):
    '''
    Converts a DataFrame containing geospatial data (minimum latitude and longitude) into a 
    GeoPackage file. The function takes a DataFrame with columns such as 'lat' (latitude), 
    'long' (longitude) and converts it into a GeoDataFrame using the WGS84 coordinate reference 
    system. Each point geometry is then written in a GeoPackage file.

    :param df: pandas.DataFrame containing geospatial data with 'lat' and 'long' columns.

    :return: None. The function outputs a GeoPackage file named 'output.gpkg'.
    '''
    lat_column = None
    long_column = None

    for col in df.columns:
        if col.lower() in ['lat', 'latitude']:
            lat_column = col
        elif col.lower() in ['long', 'longitude']:
            long_column = col
    
    if lat_column is None or long_column is None:
        raise ValueError("Missing latitude and longitude columns")

    # create a GeoDataFrame using latitude and longitude columns
    gdf = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df[long_column], df[lat_column]),
        crs='WGS84')  # set the coordinate reference system

    # initialize the output file
    geopackage_path = "output.gpkg"  # set the path of the output file
    driver = ogr.GetDriverByName("GPKG")  # initialize a GeoPackage driver
    data_source = driver.CreateDataSource(geopackage_path)  # create or overwrite the GeoPackage file
    spatial_ref = osr.SpatialReference()  # define the coordinate system
    spatial_ref.SetWellKnownGeogCS("WGS84")  # set WGS84 as the CRS

    # create a layer for the points
    layer = data_source.CreateLayer("points_layer", spatial_ref, ogr.wkbPoint)

    # add fields for each column in the DataFrame
    for col in gdf.columns:
        if col != "geometry":
            ogr_type = ogr.OFTString if gdf[col].dtype == "object" else ogr.OFTReal
            layer.CreateField(ogr.FieldDefn(col, ogr_type))

    # add each row from the GeoDataFrame to the GeoPackage
    for _, row in gdf.iterrows():
        feature = ogr.Feature(layer.GetLayerDefn())
        for col in gdf.columns:
            if col != "geometry":
                feature.SetField(col, row[col])
        feature.SetGeometry(ogr.CreateGeometryFromWkb(row.geometry.wkb))
        layer.CreateFeature(feature)

    data_source = None  # close the file to finalize the GeoPackage

    print("GeoPackage created")

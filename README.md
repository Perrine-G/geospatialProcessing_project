# Geospatial Processing project
As part of the Geospatial Processing course at Politecnico di Milano, fall 2024, this project aims to create a Python library.
This library is composed of two functions.

## Path optimisation using googlemaps library
tsp_googlemaps_fixed_start computes the optimal path between points by solving the traveling salesman problem with a fixed point of origin and the possibility of looping back to the point of origin at the end of the path. The distance used is the actual driving distance obtained with the googlemaps API distance_matrix.
To solve the traveling salesman problem, the function uses a Branch-and-Bound algorithm. It explores all the branch of the path, pruning when the distance is longer than the best path.
Points to visit can be indicated in latitude, longitude, address or location name format.

To use the library, your Google Maps API key must provide access to ditance_matrix and geocode.

Display the optimal path and the distance in kilometer.

Input: 
origin: initial point
destinations: list of points to visit
API_key: Google Maps API key
loop: If True, return to starting point after visiting all points

Output:
return a pandas.DataFrame with points and their index in optimal order, the distance with the previous step, the latitude and longitude, and the coordinate system to consider

## GeoPackage file export from a points pandas.DataFrame
gpkg_export(df) converts a DataFrame containing geospatial data (minimum latitude and longitude) into a GeoPackage file.
The function takes a DataFrame with columns such as 'lat' (latitude), 'long' (longitude) and converts it into a GeoDataFrame using the WGS84 coordinate reference system. Each point geometry are then written in a GeoPackage file.

Input:
pandas.DataFrame containing geospatial data with 'lat' and 'long' columns

Output:
The function outputs a GeoPackage file named 'output.gpkg'

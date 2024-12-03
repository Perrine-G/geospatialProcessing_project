# Geospatial Processing Project

As part of the **Geospatial Processing course** at *Politecnico di Milano*, Fall 2024, this project aims to create a Python library.  
The library consists of two functions:

---

## 1. Path Optimization Using the Google Maps Library

The `tsp_googlemaps_fixed_start` function computes the optimal path between a set of points by solving the **Traveling Salesman Problem (TSP)** with a fixed starting point. Optionally, it can loop back to the origin at the end of the route.

### Key Features:
- **Distance Metric:** Actual driving distance obtained from the Google Maps API `distance_matrix`.
- **Algorithm:** A **Branch-and-Bound algorithm** that explores all possible paths, pruning branches when the distance exceeds the current best path.

### **Input Parameters:**
- `origin`: Initial point.
- `destinations`: A list of points to visit (latitude/longitude, address, or location name formats supported).
- `API_key`: Google Maps API key with access to `distance_matrix` and `geocode`.
- `loop`: If `True`, returns to the starting point after visiting all locations.

### **Output:**
Returns a `pandas.DataFrame` with the following columns:
- Optimal order of points.
- Distance to the previous point (in kilometers).
- Latitude and longitude coordinates.
- Coordinate system to use.

### **Usage Notes:**
Your **Google Maps API key** must have access to the `distance_matrix` and `geocode` services.

---

## 2. GeoPackage Export from a Pandas DataFrame

The `gpkg_export` function converts a pandas DataFrame containing geospatial data into a **GeoPackage file**.  
It transforms the input data into a GeoDataFrame using the **WGS84 coordinate reference system** and writes it as a GeoPackage.

### **Input Parameters:**
- A `pandas.DataFrame` containing:
  - `lat`: Latitude of the point.
  - `long`: Longitude of the point.

### **Output:**
A GeoPackage file named `output.gpkg` containing the geospatial data.

---

## Installation & Usage

1. **Install Required Libraries:**  
   Ensure the following Python libraries are installed:
   - `googlemaps`
   - `pandas`
   - `geopandas`

   Install missing dependencies with:
   ```bash
   pip install googlemaps pandas geopandas

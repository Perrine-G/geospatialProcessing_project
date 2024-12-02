import unittest
import pandas as pd
import geopandas as gpd

from library_tsp_gpkg import tsp_googlemaps_fixed_start, gpkg_export

class Test_TSPGoogleMaps(unittest.TestCase):
        
    def test_loop_true(self):
        # test with loop=True
        loop = True
        origin = "Politecnico di Milano"
        destinations = [
            "Notre Dame de Paris",
            "48.8583701, 2.2944813",
            "Calanque de Port Pin",
            "Piazza del Duomo, 50122 Firenze FI, Italie"]
        api_key = "Input the API key"
        
        result = tsp_googlemaps_fixed_start(origin, destinations, api_key, loop)

        expected_order = [0, 2, 1, 3, 4, 0]
        actual_order = result['index'].tolist()

        self.assertEqual(actual_order, expected_order, "path optimization incorrect") # check the optimized path
        self.assertIsInstance(destinations, list, "input not list") # check that the input is a list
    
    def test_loop_false(self):
        # test with loop=False
        loop = False
        origin = "Politecnico di Milano"
        destinations = [
            "Notre Dame de Paris",
            "48.8583701, 2.2944813",
            "Calanque de Port Pin",
            "Piazza del Duomo, 50122 Firenze FI, Italie",]
        api_key = "Input the API key"

        result = tsp_googlemaps_fixed_start(origin, destinations, api_key, loop)

        expected_order = [0, 4, 3, 1, 2]
        actual_order = result['index'].tolist()

        self.assertEqual(actual_order, expected_order, "path optimization incorrect") # check the optimized path

class Test_gpkgExport(unittest.TestCase):

    def test_gpkgExpor(self):

        data = {
            'lat': [48.8583701, 40.712776, 41.902782, 51.507351],
            'long': [2.2944813, -74.0060, 12.496366, -0.127758],
            'name': ['Paris', 'New York', 'Rome', 'London']}
        df = pd.DataFrame(data)
    
        lat_column = None
        long_column = None
    
        for col in df.columns:
            if col.lower() in ['lat', 'latitude']:
                lat_column = col
            elif col.lower() in ['long', 'longitude']:
                long_column = col
    
        self.assertIsNotNone(lat_column, "'lat' or 'latitude' column missing")
        self.assertIsNotNone(long_column, "'long' or 'longitude' column missing")
            
        gpkg_export(df)

        gdf_exported = gpd.read_file("output.gpkg")

        self.assertEqual(len(df), len(gdf_exported), "Number of points in the geopackage does not correspond with the number of points in the dataFrame")

if __name__ == '__main__':
    unittest.main()
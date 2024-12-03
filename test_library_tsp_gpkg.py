import unittest
import pandas as pd
import geopandas as gpd
from library_tsp_gpkg import tsp_googlemaps_fixed_start, gpkg_export

class TestTSPGoogleMaps(unittest.TestCase):
    """Test cases for tsp_googlemaps_fixed_start function."""

    def test_loop_true(self):
        """Test tsp_googlemaps_fixed_start with loop=True."""
        loop = True
        origin = "Politecnico di Milano"
        destinations = [
            "Notre Dame de Paris",
            "48.8583701, 2.2944813",
            "Calanque de Port Pin",
            "Piazza del Duomo, 50122 Firenze FI, Italie"
        ]
        #api_key = "Input the API key"
        api_key = "AIzaSyAMsr4GGdiQS7FWsN5xgu7z8_qj6tpacTg"
        
        result = tsp_googlemaps_fixed_start(origin, destinations, api_key, loop)

        # Expected result: order of destinations
        expected_order = [0, 2, 1, 3, 4, 0]
        actual_order = result['index'].tolist()

        # Validate the path optimization
        self.assertEqual(actual_order, expected_order, "Path optimization is incorrect")
        
        # Ensure the destinations input is a list
        self.assertIsInstance(destinations, list, "Input destinations must be a list")
    
    def test_loop_false(self):
        """Test tsp_googlemaps_fixed_start with loop=False."""
        loop = False
        origin = "Politecnico di Milano"
        destinations = [
            "Notre Dame de Paris",
            "48.8583701, 2.2944813",
            "Calanque de Port Pin",
            "Piazza del Duomo, 50122 Firenze FI, Italie"
        ]
        #api_key = "Input the API key"
        api_key = "AIzaSyAMsr4GGdiQS7FWsN5xgu7z8_qj6tpacTg"

        result = tsp_googlemaps_fixed_start(origin, destinations, api_key, loop)

        # Expected result: order of destinations
        expected_order = [0, 4, 3, 1, 2]
        actual_order = result['index'].tolist()

        # Validate the path optimization
        self.assertEqual(actual_order, expected_order, "Path optimization is incorrect")

class TestGPKGExport(unittest.TestCase):
    """Test cases for gpkg_export function."""

    def test_gpkg_export(self):
        """Test the export of a DataFrame to a GeoPackage."""
        # Sample data
        data = {
            'lat': [48.8529682, 43.7734385, 45.468503, 43.2038947],
            'long': [2.3499021, 11.256550, 9.182402699999999, 5.5106835],
            'name': ['Notre Dame de Paris', 'Piazza del Duomo, Firenze', 'Politecnico di Milano', 'Calanque de Port Pin']
        }
        df = pd.DataFrame(data)
    
        # Identify latitude and longitude columns
        lat_column = None
        long_column = None
    
        for col in df.columns:
            if col.lower() in ['lat', 'latitude']:
                lat_column = col
            elif col.lower() in ['long', 'longitude']:
                long_column = col
    
        # Ensure required columns exist
        self.assertIsNotNone(lat_column, "'lat' or 'latitude' column is missing")
        self.assertIsNotNone(long_column, "'long' or 'longitude' column is missing")
            
        # Export to GeoPackage
        gpkg_export(df)

        # Verify exported GeoPackage content
        gdf_exported = gpd.read_file("output.gpkg")

        # Validate the number of points
        self.assertEqual(
            len(df), len(gdf_exported),
            "Number of points in the GeoPackage does not match the input DataFrame"
        )

if __name__ == '__main__':
    unittest.main()

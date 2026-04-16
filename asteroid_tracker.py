# Class that will manage a collection of near earth objects.
import json
from pathlib import Path
from datetime import datetime
from asteroid import Asteroid
from functions import get_dataset_bounds, normalize_value

class AsteroidTracker:
    '''
    Manages a collection of Asteroid objects loaded from a NASA NeoWs JSON file.

    Holds a list of Asteroid instances and provides methods
    for filtering, sorting, and analyzing asteroid risk data. Handles file I/O
    with exception handling for missing or corrupt JSON files.

    Attributes:
        file_path: String path to the JSON data file.
        asteroids: List of Asteroid objects parsed from the data file.
        bounds: Dictionary containing min/max values for diameter, velocity, and miss_distance 
                across the full dataset. This is computed via get_dataset_bounds.
    '''

    def __init__(self, file_path='data/data.json'):
        '''
        Initializes AsteroidTracker by loading the data and creating Asteroid objects.

        Reads the NASA NeoWs data file, parses through every asteroid entry, and builds
        a list of Asteroid instances. Also computes dataset bounds for use in
        normalization and analysis.

        Args:
            file_path: The path to the JSON file containing asteroid data.
        '''
        # Variables needed to store the file path, list of asteroids, and min/max bounds
        self.file_path = file_path
        self.asteroids = []
        self.bounds = {}

        # Attempt to load and parse the JSON data file
        try:
            # Assign the path for the data file and checks if it exists beforehand.
            data_path = Path(file_path)
            if not data_path.exists():
                raise FileNotFoundError(f"No data file found at {file_path}. Please run get_data.py first.")

            # Open the data file and parse through it while assigning it to nasa_data
            with open(data_path, 'r') as f:
                nasa_data = json.load(f)  

        except json.JSONDecodeError as e: 
            print(f"Error: Failed to parse JSON file at {file_path}.")
            raise 

        # Parse each asteroid from the JSON structure
        # The JSON has dates as top-level keys, each mapping to a list of asteroid dicts
        for date in nasa_data: 
            for neo in nasa_data[date]:
                # Extract fields from the nested NASA JSON structure
                name = neo["name"]
                diameter_min = neo["estimated_diameter"]["meters"]["estimated_diameter_min"]
                diameter_max = neo["estimated_diameter"]["meters"]["estimated_diameter_max"]
                # Velocity and miss_distance come as strings.
                velocity = float(neo["close_approach_data"][0]["relative_velocity"]["kilometers_per_hour"])
                miss_distance = float(neo["close_approach_data"][0]["miss_distance"]["kilometers"])
                is_hazardous = neo["is_potentially_hazardous_asteroid"]
                close_approach_date = neo["close_approach_data"][0]["close_approach_date"]

                # Create an Asteroid object and add it to our list
                asteroid = Asteroid(
                    name, diameter_min, diameter_max,
                    velocity, miss_distance, is_hazardous,
                    close_approach_date
                )
                self.asteroids.append(asteroid)

        # Compute dataset bounds for normalization using the utility function and makes sure that the list if not empty.
        if self.asteroids: 
            self.bounds = get_dataset_bounds(self.asteroids)
    
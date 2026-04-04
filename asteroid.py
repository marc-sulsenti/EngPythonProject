# Asteroid class of one single near Earth object
import json
from pathlib import Path

class Asteroid:
    """
    Represents a near-earth object from NASA's NEO API
    Stores key properties and provides risk assessment methods
    """
    def __init__(self, neo_data, close_approach_data):
        """
        Initializes Asteroid from NASA NEO API data
        Args:
            neo_data (dict): The asteroid's entry from NASA's near_earth_objects
            close_approach_data (dict): The specific close approach data entry
        """
        self.name = neo_data.get('name', 'Unknown')
        self.diameter_min = neo_data['estimated_diameter']['meters']['estimated_diameter_min']
        self.diameter_max = neo_data['estimated_diameter']['meters']['estimated_diameter_max']
        self.velocity = float(close_approach_data['relative_velocity']['kilometers_per_hour'])
        self.miss_distance = float(close_approach_data['miss_distance']['kilometers'])
        self.is_hazardous = neo_data.get('is_potentially_hazardous_asteroid', False)
        self.close_approach_date = close_approach_data['close_approach_date']
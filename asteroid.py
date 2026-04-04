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

    def calculate_risk_score(self):
        """
        Calculates risk score from 0-100 based on size, distance, and velocity
        Higher score indicates higher risk
        Returns:
            float: Calculated risk score
        """
        avg_diameter = (self.diameter_min + self.diameter_max) / 2
        size_score = min(40, (avg_diameter / 1000) * 40)
        distance_score = max(0, 35 * (1 - min(1, self.miss_distance / 1_000_000)))
        velocity_score = min(25, (self.velocity / 100000) * 25)
        hazardous_bonus = 15 if self.is_hazardous else 0
        return min(100, size_score + distance_score + velocity_score + hazardous_bonus)
    
    def get_risk_category(self):
        """
        Categorizes risk score into severity levels
        
        Returns:
            str: 'Extreme' (80-100), 'High' (60-79), 'Medium' (40-59), 'Low' (0-39)
        """
        score = self.calculate_risk_score()
        if score >= 80:
            return 'Extreme'
        elif score >= 60:
            return 'High'
        elif score >= 40:
            return 'Medium'
        else:
            return 'Low'
    
    def __str__(self):
        """
        Returns readable asteroid summary.
        """
        avg_diameter = (self.diameter_min + self.diameter_max) / 2
        risk_category = self.get_risk_category()
        return (f"Asteroid {self.name} | {avg_diameter:.0f}m | "
                f"{self.miss_distance/1_000_000:.1f}M km | Risk: {risk_category}")
    
    def __gt__(self, other):
        """
        Compares two asteroids by risk score
        
        Args:
            other (Asteroid): Another asteroid instance
            
        Returns:
            bool: True if this asteroid has higher risk than other
        """
        if not isinstance(other, Asteroid):
            return NotImplemented
        return self.calculate_risk_score() > other.calculate_risk_score()

def load_asteroids_from_data_file():
    """
    Loads asteroid data from the JSON file created by get_data.py
    
    Returns:
        list: List of Asteroid objects for all close approaches
    """
    data_path = Path('data/data.json')
    
    if not data_path.exists():
        raise FileNotFoundError(f"No data file found at {data_path}. Run get_data.py first.")
    
    with open(data_path, 'r') as f:
        nasa_data = json.load(f)
    
    asteroids = []
    for date, neo_list in nasa_data.items():
        for neo in neo_list:
            for approach in neo.get('close_approach_data', []):
                asteroid = Asteroid(neo, approach)
                asteroids.append(asteroid)
    
    return asteroids
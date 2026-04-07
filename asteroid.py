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
        self.name = neo_data.get('name', 'Unknown')  # Extracts asteroid name from data (default to 'Unknown')
        self.diameter_min = neo_data['estimated_diameter']['meters']['estimated_diameter_min']  # Gets minimum estimated diameter in meters
        self.diameter_max = neo_data['estimated_diameter']['meters']['estimated_diameter_max']  # Gets maximum estimated diameter in meters
        self.velocity = float(close_approach_data['relative_velocity']['kilometers_per_hour'])  # Converts relative velocity to float
        self.miss_distance = float(close_approach_data['miss_distance']['kilometers'])  # Converts miss distance to float
        self.is_hazardous = neo_data.get('is_potentially_hazardous_asteroid', False)  # Checks if asteroid is potentially hazardous
        self.close_approach_date = close_approach_data['close_approach_date']  # Gets the date of close approach

    def calculate_risk_score(self):
        """
        Calculates risk score from 0-100 based on size, distance, and velocity
        Higher score indicates higher risk
        Returns:
            float: Calculated risk score
        """
        avg_diameter = (self.diameter_min + self.diameter_max) / 2  # Computes average diameter
        size_score = min(40, (avg_diameter / 1000) * 40)  # Calculates size contribution to risk (max 40 points)
        distance_score = max(0, 35 * (1 - min(1, self.miss_distance / 1_000_000)))  # Calculates distance contribution (max 35 points)
        velocity_score = min(25, (self.velocity / 100000) * 25)  # Calculates velocity contribution (max 25 points)
        hazardous_bonus = 15 if self.is_hazardous else 0  # Adds bonus if hazardous
        return min(100, size_score + distance_score + velocity_score + hazardous_bonus)  # Return total risk score, capped at 100
    
    def get_risk_category(self):
        """
        Categorizes risk score into severity levels
        
        Returns:
            str: 'Extreme' (80-100), 'High' (60-79), 'Medium' (40-59), 'Low' (0-39)
        """
        score = self.calculate_risk_score()  # Gets the risk score
        if score >= 80:  # Checks for extreme risk
            return 'Extreme'
        elif score >= 60:  # Checks for high risk
            return 'High'
        elif score >= 40:  # Checks for medium risk
            return 'Medium'
        else:  # Determines low risk
            return 'Low'
    
    def __str__(self):
        """
        Returns readable asteroid summary.
        """
        avg_diameter = (self.diameter_min + self.diameter_max) / 2  # Calculates average diameter
        risk_category = self.get_risk_category()  # Gets risk category
        risk_score = self.calculate_risk_score()  # Gets risk score
        return (f"Asteroid {self.name} | {avg_diameter:.0f}m | "  # Formats the summary string
                f"{self.miss_distance/1_000_000:.1f}M km | "
                f"Risk: {risk_score:.1f}/100 ({risk_category})")
    
    def __gt__(self, other):
        """
        Compares two asteroids by risk score
        
        Args:
            other (Asteroid): Another asteroid instance
            
        Returns:
            bool: True if this asteroid has higher risk than other
        """
        if not isinstance(other, Asteroid):  # Checks if other is an Asteroid instance
            return NotImplemented
        return self.calculate_risk_score() > other.calculate_risk_score()  # Compares risk scores

def load_asteroids_from_data_file():
    """
    Loads asteroid data from the JSON file created by get_data.py
    
    Returns:
        list: List of Asteroid objects for all close approaches
    """
    data_path = Path('data/data.json')  # Defines path to data file
    
    if not data_path.exists():  # Checks if data file exists
        raise FileNotFoundError(f"No data file found at {data_path}. Run get_data.py first.")
    
    with open(data_path, 'r') as f:  # Open the data file for reading
        nasa_data = json.load(f)  # Load JSON data
    
    asteroids = []  # Initialize list for asteroids
    for date, neo_list in nasa_data.items():  # Iterate over dates and NEO lists
        for neo in neo_list:  # Iterate over NEOs
            for approach in neo.get('close_approach_data', []):  # Iterate over close approaches
                asteroid = Asteroid(neo, approach)  # Create Asteroid instance
                asteroids.append(asteroid)  # Add to list
    
    return asteroids  # Return the list of asteroids

if __name__ == "__main__":
    try:  # Tries to load and display asteroids
        asteroids = load_asteroids_from_data_file()  # Loads asteroids from file
        
        if not asteroids:  # Checks if any asteroids were loaded
            print("No asteroids found in data file.")
        else:  # Processes asteroids if they exist
            asteroids.sort(reverse=True)  # Sorts by risk score descending
            
            print(f"Loaded {len(asteroids)} asteroid approaches from data/data.json\n")  # Prints count
            print("=== TOP 5 MOST RISKY ASTEROIDS ===\n")  # Prints header
            
            for i, asteroid in enumerate(asteroids[:5], 1):  # Iterates over top 5
                print(f"{i}. {asteroid}")  # Prints asteroid summary
                print(f"   Risk Score: {asteroid.calculate_risk_score():.1f}/100")  # Prints risk score
                print(f"   Hazardous: {'Yes' if asteroid.is_hazardous else 'No'}")  # Prints hazardous status
                print(f"   Velocity: {asteroid.velocity:,.0f} km/h")  # Prints velocity
                print()  # Prints blank line
                
    except FileNotFoundError as e:  # Handles missing file error
        print(f"Error: {e}")  # Prints error message
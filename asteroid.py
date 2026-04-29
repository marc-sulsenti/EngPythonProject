# Asteroid class of one single near Earth object
from functions import calculate_risk_score as calc_risk

class Asteroid:
    """
    Represents a near-earth object from NASA's NEO API
    Stores key properties and provides risk assessment methods
    """
    def __init__(self, name, diameter_min, diameter_max, velocity, miss_distance, is_hazardous, close_approach_date):
        """
        Args:
            name (str): Asteroid name
            diameter_min (float): Minimum estimated diameter in meters
            diameter_max (float): Maximum estimated diameter in meters
            velocity (float): Relative velocity in km/h
            miss_distance (float): Miss distance in km
            is_hazardous (bool): NASA's potentially hazardous classification
            close_approach_date (str): Date of close approach (YYYY-MM-DD)
        """
        self.name = name
        self.diameter_min = diameter_min
        self.diameter_max = diameter_max
        self.velocity = velocity
        self.miss_distance = miss_distance
        self.is_hazardous = is_hazardous
        self.close_approach_date = close_approach_date

    def calculate_risk_score(self):
        """
        Calculates risk score from 0-100 based on size, distance, and velocity
        Higher score indicates higher risk
        Returns:
            float: Calculated risk score
        """
        avg_diameter = (self.diameter_min + self.diameter_max) / 2  # Computes average diameter
        return calc_risk(avg_diameter, self.velocity, self.miss_distance, self.is_hazardous)
    
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

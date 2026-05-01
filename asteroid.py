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
        self.bounds = None 

    def calculate_risk_score(self):
        """
        Calculates risk score from 0-10 based on size, distance, and velocity
        Higher score indicates higher risk
        Returns:
            float: Calculated risk score
        """
        avg_diameter = (self.diameter_min + self.diameter_max) / 2  # Computes average diameter
        return calc_risk(avg_diameter, self.velocity, self.miss_distance, self.bounds)  # Returns risk score
    
    def get_risk_category(self):
        """
        Categorizes risk score into severity levels
        
        Returns:
            str: 'Critical' (7.5-10), 'High' (5.0-7.5), 'Medium' (2.5-5.0), 'Low' (0-2.5)
        """
        score = self.calculate_risk_score()  # Gets the risk score
        if score >= 7.5:  # Checks for critical risk
            return 'Critical'
        elif score >= 5.0:  # Checks for high risk
            return 'High'
        elif score >= 2.5:  # Checks for medium risk
            return 'Medium'
        else:  # Determines low risk
            return 'Low'
    
    def __str__(self):
        """
        This method returns readable asteroid summary.
        """
        avg_diameter = (self.diameter_min + self.diameter_max) / 2  # Calculates average diameter
        risk_score = self.calculate_risk_score()  # Gets risk score
        risk_category = self.get_risk_category()  # Gets risk category
        return (f"Asteroid {self.name} | Diameter: {avg_diameter:.1f}m | "
                f"Miss: {self.miss_distance:.1f} km | Risk: {risk_score:.2f} ({risk_category})")  # Formats summary string
    
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

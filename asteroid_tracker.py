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
            # Resolve the path relative to this script's directory so it works regardless of CWD
            data_path = Path(__file__).parent / file_path
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
    def __len__(self):
        '''
        Returns the number of asteroids in the tracker.

        Returns:
            int: Total count of Asteroid objects.
        '''
        return len(self.asteroids)

    def get_hazardous(self):
        '''
        Returns a list of asteroids that NASA classified as potentially hazardous.

        Returns:
            list: Asteroid objects where is_hazardous is True.
        '''
        # Filter the list for only hazardous asteroids by checking the is_hazardous flag.
        hazardous = []
        for asteroid in self.asteroids: 
            if asteroid.is_hazardous:
                hazardous.append(asteroid)
        return hazardous

    def get_top_risks(self, n=10):
        '''
        Returns the top n riskiest asteroids sorted by risk score descending.

        Parameters:
            n: Integer of the top-risk asteroids to return. Defaults to 10.

        Returns:
            list: The n Asteroid objects with the highest risk scores.
        '''
        # Sort asteroids by risk score in descending order and return top n
        sorted_asteroids = sorted(self.asteroids, key=lambda a: a.calculate_risk_score(), reverse=True)
        return sorted_asteroids[:n]

    def get_summary_stats(self):
        '''
        Computes summary statistics across all asteroids in the tracker.

        Returns:
            dict: Dictionary containing:
                - 'total_count' (int): Total number of asteroids
                - 'hazardous_count' (int): Number of NASA-flagged hazardous asteroids
                - 'mean_risk' (float): Average risk score across all asteroids
                - 'max_risk' (float): Highest risk score in the dataset
                - 'min_risk' (float): Lowest risk score in the dataset
                - 'category_counts' (dict): Count of asteroids in each risk category
                - 'date_range' (tuple): Earliest and latest close approach dates
        '''
        # Check to see if the asteroids list is empty
        if not self.asteroids: 
            return {}

        # Compute all risk scores using a list comprehension
        scores = [a.calculate_risk_score() for a in self.asteroids]

        # Count asteroids in each risk category
        category_counts = {'Low': 0, 'Medium': 0, 'High': 0, 'Extreme': 0}
        for asteroid in self.asteroids:
            category = asteroid.get_risk_category()
            category_counts[category] += 1

        # Determine the date range from close approach dates
        dates = [a.close_approach_date for a in self.asteroids]
        date_range = (min(dates), max(dates))

        # Build and return the summary dictionary
        return {
            'total_count': len(self.asteroids),
            'hazardous_count': len(self.get_hazardous()),
            'mean_risk': sum(scores) / len(scores),
            'max_risk': max(scores),
            'min_risk': min(scores),
            'category_counts': category_counts,
            'date_range': date_range
        }

    def filter_by_date_range(self, start_date, end_date):
        '''
        Filters asteroids whose close approach date falls within a given range.

        Parameters:
            start_date: String start date. (YYYY-MM-DD' format)
            end_date: String end date. (YYYY-MM-DD' format)

        Returns:
            list: Asteroid objects within the specified date range.
        '''
        # Use datetime module to compare date strings properly
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")

        # Initialize list for matching asteroids and iterate through all asteroids to filter them out by date range.
        filtered = []
        for asteroid in self.asteroids:
            approach_date = datetime.strptime(asteroid.close_approach_date, "%Y-%m-%d")
            if start <= approach_date <= end:
                filtered.append(asteroid)
        return filtered

    def filter_by_risk_threshold(self, threshold):
        '''
        Returns asteroids with a risk score at or above the given threshold given the threshold value and a lambda function.

        Parameters:
            threshold: Minimum risk score to include.

        Returns:
            list: Asteroid objects whose risk score meets or exceeds the threshold.
        '''
        # Use filter() with a lambda to select asteroids above the threshold
        return list(filter(lambda a: a.calculate_risk_score() >= threshold, self.asteroids))

    def yield_high_risk(self, threshold=60):
        '''
        Generator function that yields one asteroid at a time that meet a risk score threshold.

        Parameters:
            threshold: Minimum risk score to yield. Defaults to 60.

        Yields:
            Asteroid: Each asteroid whose risk score meets or exceeds the threshold.
        '''
        # Yield asteroids one at a time if their risk score meets the threshold
        for asteroid in self.asteroids:
            if asteroid.calculate_risk_score() >= threshold:
                yield asteroid


if __name__ == "__main__":
    # Demo: load data and display summary stats
    try:
        tracker = AsteroidTracker('data/data.json')
        print(f"Loaded {len(tracker)} asteroids\n")

        # Display summary statistics
        stats = tracker.get_summary_stats()
        print("Summary:")
        print(f"  Total Asteroids:  {stats['total_count']}")
        print(f"  Hazardous Asteroids: {stats['hazardous_count']}")
        print(f"  Date Range:       {stats['date_range'][0]} to {stats['date_range'][1]}")
        print(f"  Mean Risk Score:  {stats['mean_risk']:.1f}/100")
        print(f"  Max Risk Score:   {stats['max_risk']:.1f}/100")
        print(f"  Min Risk Score:   {stats['min_risk']:.1f}/100")
        print(f"  Category counts:  {stats['category_counts']}\n")

        # Display top 5 riskiest asteroids
        print("Top 5 Riskiest Asteroids:")
        for i, asteroid in enumerate(tracker.get_top_risks(5), 1):
            print(f"  {i}. {asteroid}")

        # Demo the lambda function
        print(f"\nAsteroids With Risk >= 40:")
        high_risk = tracker.filter_by_risk_threshold(40)
        print(f"  Found {len(high_risk)} asteroids.")

        # Demo asteroid generator
        print(f"\nAsteroids With Risk >= 60:")
        for asteroid in tracker.yield_high_risk(60):
            print(f"  {asteroid}\n")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except json.JSONDecodeError as e:
        print(f"Error: {e}")
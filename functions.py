def normalize_value (value, min_value, max_value):
    '''
    This function takes a value and normalizes it to a range of 0 to 1 based on the provided minimum and maximum values.

    Parameters:
    value (float): The value to be normalized.
    min_value (float): The minimum value in the range.
    max_value (float): The maximum value in the range.

    Returns:
    float: The normalized value between 0 and 1.
    '''
    if max_value - min_value == 0:
        return 0.0  # We want to avoid any division by zero error
    return (value - min_value) / (max_value - min_value) # Return the normalized value.

def get_dataset_bounds(asteroids):
    '''
    Computes the min and max values for diameter, velocity, and miss_distance across a list of Asteroid objects.

    Parameters:
    asteroids (list): List of Asteroid objects.

    Returns:
    dict: Min and max values for diameter, velocity, and miss_distance.
    '''
    # Find all the diameters, velocities, and miss distances for every asteroid in the given list
    diameters = [(a.diameter_min + a.diameter_max) / 2 for a in asteroids]
    velocities = [a.velocity for a in asteroids]
    distances = [a.miss_distance for a in asteroids]
    # Return the min and max values for each of the three categories in a dictionary
    return {
        'diameter': (min(diameters), max(diameters)),
        'velocity': (min(velocities), max(velocities)),
        'miss_distance': (min(distances), max(distances))
    }

def calculate_risk_score(diameter, velocity, miss_distance, is_hazardous=False):
    '''
    Calculates a risk score from 0 to 100 for an asteroid based on its size, velocity, and miss distance.
    Larger diameter, higher velocity, and closer miss distance all increase the score.

    Parameters:
        diameter: Average estimated diameter in meters.
        velocity: Relative velocity in km/h.
        miss_distance: Miss distance in km.
        is_hazardous: Whether NASA flagged the asteroid as potentially hazardous. Defaults to False.

    Returns:
        float: Risk score from 0 to 100. Higher means more dangerous.
    '''
    # Size contribution: up to 40 points based on diameter relative to 1 km

    # Size is up to 40 points based on the diameter (1km), Distance is up to 35 points (Closer = Higher Score),
    # Velocity is up to 25 points (Relative to 100,000 km/h), and a bonus of 15 points if NASA flagged it as hazardous. X/100 score.
    size_score = min(40, (diameter / 1000) * 40)
    distance_score = max(0, 35 * (1 - min(1, miss_distance / 1_000_000)))
    velocity_score = min(25, (velocity / 100000) * 25)
    hazardous_bonus = 15 if is_hazardous else 0
    return min(100, size_score + distance_score + velocity_score + hazardous_bonus)
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

def calculate_risk_score(diameter, velocity, miss_distance, bounds):
    '''
    This method calculates a risk score from 0 to 10 for an asteroid based on its size, velocity, and miss distance.
    Each value is normalized against the full dataset so scores are relative to all loaded asteroids.
    Larger diameter, higher velocity, and closer miss distance all increase the score.

    Parameters:
        diameter (float): Average estimated diameter in meters.
        velocity (float): Relative velocity in km/h.
        miss_distance (float): Miss distance in km.
        bounds (dict): A Dictionary with 'diameter', 'velocity', and 'miss_distance' keys, each a (min, max) tuple.

    Returns:
        float: Risk score from 0 to 10. Higher means more dangerous relative to the dataset.
    '''
    # First we are going to normalize the diameter, then the velocity, and then the miss distance
    norm_diameter = normalize_value(diameter, bounds['diameter'][0], bounds['diameter'][1])
    norm_velocity = normalize_value(velocity, bounds['velocity'][0], bounds['velocity'][1])
    norm_distance = normalize_value(miss_distance, bounds['miss_distance'][0], bounds['miss_distance'][1])
    # We can then use the normalized variable to calculate a risk score
    # We want to weigh the diameter the most, the velocity the second most, and the miss distance the least, but factor all three in
    return (0.4 * norm_diameter + 0.3 * norm_velocity + 0.3 * (1 - norm_distance)) * 10
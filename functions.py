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
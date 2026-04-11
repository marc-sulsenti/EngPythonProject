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
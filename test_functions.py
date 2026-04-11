from functions import normalize_value
from asteroid import Asteroid

def test_asteroid_init():
    '''
    This method tests the Asteroid initialization with various test cases to ensure it works.
    '''
    a = Asteroid("Test Asteroid", 100.0, 200.0, 50000.0, 500000.0, False, "2026-04-11")
    assert a.name == "Test Asteroid"
    assert a.diameter_min == 100.0
    assert a.diameter_max == 200.0
    assert a.velocity == 50000.0
    assert a.miss_distance == 500000.0
    assert a.is_hazardous == False
    assert a.close_approach_date == "2026-04-11"
    # If we print this message than all the test cases have passed, and the asteroid initialization function should be all good
    print("Asteroid initialization test passed.")


def test_normalize_value():
    '''
    This method tests the normalize_value function with various test cases to ensure it works.
    '''
    assert normalize_value(5, 0, 10) == 0.5, "Test case 1 failed"
    assert normalize_value(0, 0, 10) == 0.0, "Test case 2 failed"
    assert normalize_value(10, 0, 10) == 1.0, "Test case 3 failed"
    assert normalize_value(5, 5, 5) == 0.0, "Test case 4 failed "
    assert normalize_value(15, 10, 20) == 0.5, "Test case 5 failed"
    assert normalize_value(-5, -10, 0) == 0.5, "Test case 6 failed"
    assert normalize_value(0.3, 0, 1) == 0.3, "Test case 7 failed"
    assert normalize_value(25, 0, 10) == 2.5, "Test case 8 failed"
    # If we print this message than all the test cases have passed, and the normalize_value function should be all good
    print("All normalize_value test cases have passed.")


if __name__ == "__main__":
    test_normalize_value()
    test_asteroid_init()
from functions import normalize_value, calculate_risk_score
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

def test_calculate_risk_score():
    '''
    This method tests the calculate_risk_score function with known inputs to verify expected outputs.
    Scores are on a 0-10 scale, normalized against dataset bounds.
    '''

    # First, we need to define the bounds for tesitng.
    # These will reflect the min and max values we expect to see from the dataset.
    bounds = {
        'diameter': (0, 1000),
        'velocity': (0, 100000),
        'miss_distance': (0, 50_000_000)
    }

    # The smallest, slowest, farthest asteroid in the dataset should score 0
    score_min = calculate_risk_score(0, 0, 50_000_000, bounds)
    assert score_min == 0.0, f"Expected 0.0, got {score_min}"

    # In this test the asteroids that are the largest, fastest, closest  should score 10
    score_max = calculate_risk_score(1000, 100000, 0, bounds)
    assert score_max == 10.0, f"Expected 10.0, got {score_max}"

    # In these tests  score for these  should always stay within 0-10
    assert 0.0 <= score_min <= 10.0, f"Score out of range: {score_min}"
    assert 0.0 <= score_max <= 10.0, f"Score out of range: {score_max}"

    # In these tests a mid-range asteroid should score around 5.0
    score_mid = calculate_risk_score(500, 50000, 25_000_000, bounds)
    assert abs(score_mid - 5.0) < 0.01, f"Expected ~5.0, got {score_mid}"

    print("All calculate_risk_score test cases have passed.")


if __name__ == "__main__":
    test_normalize_value()
    test_asteroid_init()
    test_calculate_risk_score()
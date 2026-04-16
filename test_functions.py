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
    '''
    # A small, slow, far asteroid should have a low risk score
    score_low = calculate_risk_score(50, 10000, 50_000_000, False)
    assert score_low < 20, f"Expected low score, got {score_low}"

    # A large, fast, close asteroid flagged hazardous should score high
    score_high = calculate_risk_score(1000, 100000, 100_000, True)
    assert score_high > 80, f"Expected high score, got {score_high}"

    # A zero-diameter, zero-velocity, max-distance asteroid should score near 0
    score_min = calculate_risk_score(0, 0, 10_000_000, False)
    assert score_min == 0.0, f"Expected 0.0, got {score_min}"

    # Score should never exceed 100
    score_cap = calculate_risk_score(5000, 500000, 0, True)
    assert score_cap <= 100, f"Expected <= 100, got {score_cap}"

    # Hazardous bonus should add 15 points
    score_no_haz = calculate_risk_score(500, 50000, 500_000, False)
    score_haz = calculate_risk_score(500, 50000, 500_000, True)
    assert score_haz - score_no_haz == 15, f"Expected 15 point difference, got {score_haz - score_no_haz}"

    print("All calculate_risk_score test cases have passed.")


if __name__ == "__main__":
    test_normalize_value()
    test_asteroid_init()
    test_calculate_risk_score()
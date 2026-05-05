# Engineering Python Project — Near-Earth Object Risk Analysis

_Project for CPE-551 | Engineering Programming: Python._

A Python project that gathers the data about the Near-Earth Objects (NEOs) from NASA's NeoWs API,
then computes a risk score for each asteroid, and provides filtering,
sorting, and a summary analysis.

---

## Team Members

| Name | Email | Student ID |
|------|--------|-------------|
| **Miguel Rodriguez** | [mrodri12@stevens.edu](mailto:mrodri12@stevens.edu) | 20010380 |
| **Marc Sulsenti** | [msulsent@stevens.edu](mailto:msulsent@stevens.edu) | 20010416 |
| **Max Ruiz** | [mruiz1@stevens.edu](mailto:mruiz1@stevens.edu) | 10475995 |

## Project Description

This project pulls live data from [NASA's NEO Web Service](https://api.nasa.gov/)
and analyzes the asteroids in a close radius to Earth. Each
asteroid is wrapped in an `Asteroid` object that collects the physical properties
and computes a **0–10 risk score** based on:

- **Diameter** (40% weight): larger asteroids carry more impact energy
- **Velocity** (30% weight):  faster asteroids are harder to deflect
- **Miss distance** (30% weight): closer approaches are riskier

The inputs are then normalized against the bounds of the dataset, so
scores are always relative to the current set of asteroids. Risk scores are
placed into four categories: **Low**, **Medium**, **High**, and **Critical**.

The `AsteroidTracker` class manages the full collection of Asteroids and supports filtering
by date range or risk threshold, listing top risks, generating
summary statistics, and a function that can diplay only the high-risk asteroids one at a
time.

## Project Structure

| File | Purpose |
|------|---------|
| [get_data.py](get_data.py) | Fetches NEO data from NASA's API and saves it to `data/data.json` |
| [asteroid.py](asteroid.py) | `Asteroid` class, single NEO with risk-score methods |
| [asteroid_tracker.py](asteroid_tracker.py) | `AsteroidTracker` class, collection management and analysis |
| [functions.py](functions.py) | Risk-score math: normalization, dataset bounds, scoring |
| [test_functions.py](test_functions.py) | Unit tests for the core functions and class init |
| [main.ipynb](main.ipynb) | Risk-analysis notebook showcasing the toolkit |
| [requirements.txt](requirements.txt) | Python dependencies |

## Contributions
| Team Member | Main Contributions |
|-------------|-------------------|
| **Miguel Rodriguez** | Helped construct the Main.ipynb. Constructed most of the AsteroidTracker class alongside any of the helper functions that are associated with it Also implemented in the calculate_risk_score() function in the asteroid.py file. |
| **Marc Sulsenti** | ... |
| **Max Ruiz** | ... |

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/marc-sulsenti/EngineeringProject.git
cd EngineeringProject/EngPythonProject
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up your NASA API key

Get a free key at [api.nasa.gov](https://api.nasa.gov/) and create a `.env`
file in the project root:

```
NASA_API_KEY=your_key_here
```

### 4. Fetch the asteroid data

```bash
python get_data.py
```

This populates `data/data.json` with the next 7 days of close-approach data.

### 5. Run the tracker demo

```bash
python asteroid_tracker.py
```

You'll see a summary of the loaded asteroids, the top 5 riskiest, and lists
filtered by risk threshold.

### 6. Run the notebook

Open [main.ipynb](main.ipynb) in Jupyter or VS Code for an interactive
walkthrough of the analysis.

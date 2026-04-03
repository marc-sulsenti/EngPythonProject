import requests
import json
import os
from dotenv import load_dotenv

# load the env, which is important because it contains our API key.
load_dotenv()

def fetch_asteroid_data():
    '''
    This method will fetch the data from the NASA NEO API and save it to a local JSON file at ./data/data.json.
    The data will be returned as a python dictionary.
    '''
    fpath = 'data/data.json'
    api_key = os.getenv('NASA_API_KEY')
    url = f'https://api.nasa.gov/neo/rest/v1/feed?api_key={api_key}'
    # fetch data from NEO API
    res = requests.get(url)
    if res.status_code == 200:
        # convert the response to a python dictionary to make it easier to work with
        data = res.json()
        neoData = data["near_earth_objects"]
        for _, asteroids in neoData.items():
            for asteroid in asteroids:
                # this line removes the links field and the sentry data, both of which contain the API key so make sure this is removed before dumping the data.
                asteroid.pop("links", None)
                asteroid.pop("sentry_data", None)
        # save the data to a local JSON file at ./data/data.json
        with open(fpath, 'w') as json_file:
            print(f"Saving data to {fpath}")
            json.dump(neoData, json_file, indent=4)
        print(f"Data has been fetched and saved to {fpath}")
        return neoData
    else:
        print(f"Error fetching data: {res.status_code}")
        return None


if __name__ == "__main__":
    fetch_asteroid_data()
    

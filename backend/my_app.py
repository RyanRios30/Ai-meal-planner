import os
import requests
from flask import Flask, jsonify, request
from dotenv import load_dotenv

print("script running")

load_dotenv()  # load .env variables

app = Flask(__name__)

GOOGLE_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
print("Loaded Google API Key:", GOOGLE_API_KEY)  # confirm it's loading correctly

@app.route('/')
def home():
    return jsonify({"message": "Hello from Flask"})


@app.route('/stores', methods=['GET'])
def get_stores():
    location = request.args.get('location')
    if not location:
        return jsonify({"error": "Missing ?location parameter"}), 400

    print(f"Searching Google Places for stores near: {location}")

    # Convert location (e.g. "98007") to coordinates
    geo_url = "https://maps.googleapis.com/maps/api/geocode/json"
    geo_params = {"address": location, "key": GOOGLE_API_KEY}
    geo_resp = requests.get(geo_url, params=geo_params).json()
    print("Geocoding response:", geo_resp)

    if not geo_resp.get('results'):
        return jsonify({"error": "Location not found"}), 404

    coords = geo_resp['results'][0]['geometry']['location']
    lat, lng = coords['lat'], coords['lng']

    # Search for grocery stores near the lat/lng
    places_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    places_params = {
        "location": f"{lat},{lng}",
        "radius": 5000,  # meters
        "type": "grocery_or_supermarket",
        "key": GOOGLE_API_KEY
    }

    places_resp = requests.get(places_url, params=places_params).json()

    # Parse and return relevant data
    stores = []
    for result in places_resp.get('results', []):
        stores.append({
            "name": result.get("name"),
            "address": result.get("vicinity"),
            "rating": result.get("rating"),
        })

    return jsonify(stores)

if __name__ == '__main__':
    print("Running app via __main__")
    app.run(debug=True)

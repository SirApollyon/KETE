from flask import Flask, render_template, jsonify, request
import json
import math

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('text.html')

@app.route('/filter_housing_ads')
def filter_housing_ads():
    nature_distance = float(request.args.get('nature_distance', 0))
    education_distance = float(request.args.get('education_distance', 0))
    transport_distance = float(request.args.get('transport_distance', 0))
    
    # Load housing ads, parks, schools, and transportation data
    with open('data/housing_ads.json') as f:
        housing_ads = json.load(f)
    
    with open('data/parks.json') as f:
        parks = json.load(f)
    
    with open('data/schools.json') as f:
        schools = json.load(f)

    with open('data/transportation.json') as f:
        transportation = json.load(f)

    filtered_housing_ads = []

    for ad in housing_ads:
        ad_latitude = ad['latitude']
        ad_longitude = ad['longitude']
        
        # Initialize criteria flags
        meets_nature_criteria = True
        meets_education_criteria = True
        meets_transport_criteria = True
        
        # Check for nature distance (parks) if nature_distance is > 0
        if nature_distance > 0:
            meets_nature_criteria = any(
                calculate_distance(ad_latitude, ad_longitude, park['latitude'], park['longitude']) <= nature_distance
                for park in parks
            )
        
        # Check for education distance (schools) if education_distance is > 0
        if education_distance > 0:
            meets_education_criteria = any(
                calculate_distance(ad_latitude, ad_longitude, school['latitude'], school['longitude']) <= education_distance
                for school in schools
            )
        
        # Check for transport distance (transportation) if transport_distance is > 0
        if transport_distance > 0:
            meets_transport_criteria = any(
                calculate_distance(ad_latitude, ad_longitude, transport['latitude'], transport['longitude']) <= transport_distance
                for transport in transportation
            )

        # Add ad if it meets all active criteria
        if meets_nature_criteria and meets_education_criteria and meets_transport_criteria:
            filtered_housing_ads.append(ad)

    return jsonify(filtered_housing_ads)

def calculate_distance(lat1, lon1, lat2, lon2):
    # Haversine formula to calculate distance between two points on the Earth
    R = 6371  # Radius of the Earth in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * 
         math.sin(dlon / 2) ** 2)
    c = 2 * math.asin(math.sqrt(a))
    return R * c

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
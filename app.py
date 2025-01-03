from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__, static_folder='static')

API_KEY = 'fa90ddbf05821a84addc3d5b0088f19b'

@app.route('/')
def home():
    """Render the home page."""
    return render_template('index.html')

@app.route('/get_weather', methods=['POST'])
def get_weather():
    """Endpoint to fetch weather data based on user input."""
    # Get the city from the POST request
    city = request.form['city']
    
    if city:
        # Construct the API request URL with the city and API key
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
        
        # Send a GET request to the OpenWeatherMap API
        response = requests.get(url)
        
        # Check if the response is successful (status code 200)
        if response.status_code == 200:
            # Parse JSON data from the response
            data = response.json()
            
            # Extract relevant weather information
            weather = {
                'city': data['name'],
                'temperature': data['main']['temp'],
                'temp_min': data['main']['temp_min'],
                'temp_max': data['main']['temp_max'],
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
            }
            
            # Return weather data as JSON response
            return jsonify(weather)
        else:
            # Return an error message if city is not found
            return jsonify({'error': 'City not found'})
    else:
        # Return an error message if no city is provided in the request
        return jsonify({'error': 'No city provided'})

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


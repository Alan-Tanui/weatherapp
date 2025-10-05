import requests
from flask import Flask, render_template, request
app = Flask(__name__)

API_BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

API_KEY = 'apikey'

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    error = None

    if request.method == 'POST':
        city = request.form['city']
        if city:
            # Construct the full API URL with the city and API key
            params = {
                'q': city,
                'appid': API_KEY,
                'units': 'metric'  # Use 'imperial' for Fahrenheit
            }
            try:
                response = requests.get(API_BASE_URL, params=params)
                response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

                data = response.json()
                
                # Extract the relevant weather information
                weather_data = {
                    'city': data['name'],
                    'temperature': f"{data['main']['temp']:.1f}", # Format to one decimal place
                    'description': data['weather'][0]['description'].title(),
                    'icon': data['weather'][0]['icon'],
                }
                
            except requests.exceptions.HTTPError as http_err:
                if response.status_code == 404:
                    error = f"Sorry, the city '{city}' could not be found."
                else:
                    error = f"An HTTP error occurred: {http_err}"
            except Exception as err:
                error = f"An unexpected error occurred: {err}"
        else:
            error = "Please enter a city name."

    return render_template('index.html', data=weather_data, error=error)

if __name__ == '__main__':
    app.run(debug=True)
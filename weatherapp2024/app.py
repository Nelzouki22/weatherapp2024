# app.py
import bottle
import os
import sys
import requests

# OpenWeatherMap API key and city
API_KEY = "5dcb3fa4c2554107b4f221801242409"
CITY = "Benghazi"

# Set up Bottle
app = bottle.Bottle()

@app.route('/')
def index():
    """Fetch weather data and return it as a response."""

    # URL for fetching weather data
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    
    # Sending the request and getting the response
    response = requests.get(base_url)

    # Check if the response is successful
    if response.status_code == 200:
        # Convert data to JSON
        data = response.json()
        
        # Extract required information
        main = data['main']
        temperature = main['temp']
        humidity = main['humidity']
        weather_description = data['weather'][0]['description']
        
        # Display information to the user
        return (f"<h1>الطقس في {CITY}</h1>"
                f"<p>درجة الحرارة: {temperature}°C</p>"
                f"<p>الرطوبة: {humidity}%</p>"
                f"<p>وصف الطقس: {weather_description}</p>")
    else:
        # If city not found or error occurred
        return "<p>تعذر جلب بيانات الطقس. تأكد من اسم المدينة وحاول مجددًا.</p>"

# Handle static files
@app.route('/static/<filepath:path>')
def server_static(filepath):
    """Handler for static files, used with the development server.
    When running under a production server such as IIS or Apache,
    the server should be configured to serve the static files."""
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static').replace('\\', '/')
    return bottle.static_file(filepath, root=STATIC_ROOT)

# Main entry point
if __name__ == '__main__':
    if '--debug' in sys.argv[1:] or 'SERVER_DEBUG' in os.environ:
        # Debug mode will enable more verbose output in the console window.
        # It must be set at the beginning of the script.
        bottle.debug(True)
    
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static').replace('\\', '/')
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555

    # Starts a local test server.
    bottle.run(app, server='wsgiref', host=HOST, port=PORT)

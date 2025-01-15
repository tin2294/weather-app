# WeatherApp

## Description

WeatherApp is a Django-based web application that provides real-time weather forecasts. The app fetches weather data from an external API (Weather API) and displays it to users based on their input city or their geolocation. Additionally, the user can also save temperatures based on the locations and date ranges they input (tech assessments 1, 2.1 and 2.3).

This application has been deployed on Heroku for easy access (also to test without having to set up a key since that is in the .env file).

## Features

- Fetches weather data from an external API based on user's geolocation or entered location.
- Fetches weather forecast for 5 days.
- Saves temperature data into database based on location and dates entered.
- Displays saved data
- Exports saved data
- Hosted on [Heroku](https://weathera-1c4f4371d9af.herokuapp.com/) for deployment.

### Dependencies

- Django==4.2.7
- requests==2.31.0
- gunicorn==20.1.0
- whitenoise==6.3.0
- django-heroku==0.3.1
- python-dotenv==1.0.0
- python-decouple==3.6

## How to Run Locally

Follow these steps to run the app on your local machine:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/tin2294/weather-app.git
   cd weatherapp

2. **Set up key**:
You would need to set up your key [here](https://www.weatherapi.com/) and add it to your .env file at the root of the repository like this:
    ```WEATHER_API_KEY=your_api_key

3. **Create a virtual environment**:
You can install the requirements in your virtual environment. To set up the environment:
    ```python -m venv venv
    source venv/bin/activate  # On macOS/Linux

Then, to install requirements:
    ```pip install -r requirements.txt

4. **Start server**:
    ```python manage.py runserver
Now you can run the app on http://127.0.0.1:8000/


On Heroku, the app has also been deployed so you can access this [link](https://weathera-1c4f4371d9af.herokuapp.com/) directly to run the app.


## DEMO

Here is a [loom](https://www.loom.com/share/e79cc8db66b443fbbea3b47c5350bf82?sid=8670580b-47a6-426f-8f8e-de7d4a23299a) with the demo of this app,
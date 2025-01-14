# WeatherApp

## Description

WeatherApp is a Django-based web application that provides real-time weather forecasts. The app fetches weather data from an external API and displays it to users based on their input city.

This application has been deployed on Heroku for easy access and scalability.

## Features

- Fetches weather data from an external API.
- Dynamic user interface that updates with current weather conditions.
- Hosted on Heroku for deployment.

## Requirements

To run this project, make sure you have the following installed:

- Python 3.x
- Pip (Python package manager)
- Virtualenv (optional but recommended)
- Heroku CLI (for deployment)

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
   git clone https://github.com/your-username/weatherapp.git
   cd weatherapp

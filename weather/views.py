import requests
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse

def weather_view(request):
    location = request.GET.get('location', '')
    geo_location = None
    weather_data = None
    forecast_data = None
    error_message = None

    api_key = settings.WEATHER_API_KEY

    if not location:
        geo_location = request.GET.get('geo_location')
        if geo_location:
            lat, lon = geo_location.split(',')
            location = f"{lat},{lon}"
        else:
            error_message = "Please provide a location or enable geolocation."

    if location:
        try:
            current_weather_url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}"
            current_response = requests.get(current_weather_url)

            forecast_url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={location}&days=5"
            forecast_response = requests.get(forecast_url)

            if current_response.status_code == 200 and forecast_response.status_code == 200:
                weather_data = current_response.json()
                forecast = forecast_response.json()
                forecast_data = forecast.get('forecast', {}).get('forecastday', [])
            else:
                error_message = "Unable to fetch weather data. Please try again."
        except Exception as e:
            error_message = f"Error: {str(e)}"

    context = {
        'location': location,
        'geo_location': geo_location,
        'weather_data': weather_data,
        'forecast': forecast_data,
        'error': error_message,
    }
    return render(request, 'weather/weather.html', context)

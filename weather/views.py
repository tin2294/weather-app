import requests
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from .models import WeatherData
from django.core.exceptions import ValidationError
from django.utils.dateparse import parse_date
from datetime import timedelta, date
from django.contrib import messages

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

def validate_date_range(start_date, end_date):
    if start_date > end_date:
        raise ValidationError("Start date must be earlier than or equal to end date.")

def fetch_temperature(location, query_date):
    """Fetch the temperature for a specific location and date using the weather API."""
    api_key = settings.WEATHER_API_KEY
    forecast_url = f"http://api.weatherapi.com/v1/history.json?key={api_key}&q={location}&dt={query_date.strftime('%Y-%m-%d')}"
    response = requests.get(forecast_url)
    if response.status_code == 200:
        data = response.json()
        return data['forecast']['forecastday'][0]['day']['avgtemp_f']
    else:
        raise Exception(f"Error fetching weather data: {response.text}")

def create_weather_data(request):
    if request.method == 'POST':
        location = request.POST.get('location')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        try:
            if not location:
                raise ValidationError("Location cannot be empty.")
            
            start_date = parse_date(start_date)
            end_date = parse_date(end_date)
            if not start_date or not end_date:
                raise ValidationError("Invalid date format.")
            
            validate_date_range(start_date, end_date)

            fetched_temperatures = []
            current_date = start_date
            while current_date <= end_date:
                try:
                    temperature = fetch_temperature(location, current_date)
                    weather_data = WeatherData(location=location, date=current_date, temperature=temperature)
                    weather_data.save()
                    fetched_temperatures.append({
                        'date': current_date.strftime('%Y-%m-%d'),
                        'temperature': temperature
                    })
                except Exception as e:
                    return JsonResponse({"error": f"Failed to fetch temperature for {current_date}: {e}"}, status=500)
                current_date += timedelta(days=1)

            return render(request, "create_weather.html", {
                "message": "Weather data created successfully for the entire range.",
                "fetched_temperatures": fetched_temperatures,
                "success": True
            })

        except ValidationError as e:
            return render(request, "create_weather.html", {"error": str(e)})
        except Exception as e:
            return render(request, "create_weather.html", {"error": str(e)})

    return render(request, "create_weather.html")

def list_weather_data(request):
    weather_data = WeatherData.objects.all()
    weather_data = weather_data.order_by('location', 'date')
    return render(request, "list_weather.html", {"weather_data": weather_data})

def update_weather_data(request, pk):
    weather_data = get_object_or_404(WeatherData, pk=pk)
    if request.method == 'POST':
        location = request.POST.get('location')
        date = request.POST.get('date')
        temperature = request.POST.get('temperature')

        try:
            if not location:
                raise ValidationError("Location cannot be empty.")

            date = parse_date(date)
            if not date:
                raise ValidationError("Invalid date format.")

            validate_date_range(date, date)

            weather_data.location = location
            weather_data.date = date
            weather_data.temperature = float(temperature)
            weather_data.save()

            messages.success(request, "Weather data updated successfully!")

            return redirect('list_weather')

        except ValidationError as e:
            messages.error(request, str(e))
            return redirect('update_weather_data', pk=pk)

    return render(request, "update_weather.html", {"weather_data": weather_data})

def delete_weather_data(request, pk):
    weather_data = get_object_or_404(WeatherData, pk=pk)

    if request.method == 'POST':
        weather_data.delete()
        messages.success(request, "Weather data deleted successfully!")
        return redirect('list_weather')

    return render(request, 'confirm_delete.html', {'weather_data': weather_data})

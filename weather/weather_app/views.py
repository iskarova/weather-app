import datetime
import requests
from django.shortcuts import render

# Create your views here.
def index(request):
  API_KEY = "68bb6d6735dd4afbae530224251405"

  current_weather_url = "http://api.weatherapi.com/v1/weather?q={}&appid={}"
  forecast_url = "http://api.weatherapi.com/v1/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}"
  
  
  if request.method == "POST":
    first_city = request.POST["first_city"]
    second_city = request.get("second_city", None)
    
    weather_data_1, daily_forecasts_1 = fetch_info(first_city, API_KEY, current_weather_url, forecast_url)
    
    if second_city:
      weather_data_2, daily_forecasts_2 = fetch_info(second_city, API_KEY, current_weather_url, forecast_url)
    else: 
      weather_data_2, daily_forecasts_2 = None, None
      
    context = {
      "weather_data_1": weather_data_1,
      "daily_forecasts_1": daily_forecasts_1,
      "weather_data_2": weather_data_2,
      "daily_forecasts_2": daily_forecasts_2
    }
    return render(request, "weather_app/index.html", context)
      
  else:
    return render(request, "weather_app/index.html")
  

def fetch_info(city, api_key, current_weather_url, forecast_url):
  curr_response = requests.get(current_weather_url.format(city, api_key)).json()
  lat, lon = curr_response["coord"]["lat"], curr_response["coord"]["lon"]
  forecast_response = requests.get(forecast_url.format(lat, lon, api_key) ).json()
  
  
  weather_data = {
    "city": city,
    "temperature": round(curr_response['main']['temp'] - 273.15, 2),
    "description": curr_response["weather"][0]["description"],
    "icon": curr_response["weather"][0]["icon"]
  }
  
  daily_forecasts = []
  for daily_data in forecast_response["daily"][:5]:
    daily_forecasts.append({
      "day": datetime.datetime.fromtimestamp(daily_data["dt"]).strftime("%A"),
      "min_temp": round(daily_data["temp"]['min'] - 273.15, 2),
      "max_temp": round(daily_data["temp"]['max'] - 273.15, 2),
      "description": daily_data['weather'][0]['description'],
      "icon": daily_data["weather"][0]['icon']
    })
    
    return weather_data, daily_forecasts
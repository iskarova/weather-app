import requests
import string
from django.shortcuts import render


def index(request):
  API_KEY = "key"

  current_weather_url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
  
  
  if request.method == "POST":
    first_city = request.POST["first_city"]
    second_city = request.POST.get("second_city", None)
    
    if valid_city(first_city) is False:
      first_city = None
    if valid_city(second_city) is False:
      second_city = None
    
    if first_city and second_city:
      weather_data_1 = fetch_info(first_city, API_KEY, current_weather_url)
      weather_data_2 = fetch_info(second_city, API_KEY, current_weather_url)
    elif first_city:
      weather_data_1 = fetch_info(first_city, API_KEY, current_weather_url)
      weather_data_2 = None
    elif second_city:
      weather_data_2 = fetch_info(second_city, API_KEY, current_weather_url)
      weather_data_1 = None
    else: 
      weather_data_1 = None
      weather_data_2 = None
      
    context = {
      "weather_data_1": weather_data_1,
      "weather_data_2": weather_data_2,
    }
    return render(request, "weather_app/index.html", context)   
  else:
    return render(request, "weather_app/index.html")
  

def fetch_info(city, api_key, current_weather_url):
  curr_response = requests.get(current_weather_url.format(city, api_key)).json()
  
  if curr_response['cod'] == '404':
    return None
  
  weather_data = {
    "city": city,
    "temperature": round(curr_response['main']['temp'] - 273.15, 2),
    "description": curr_response["weather"][0]["description"],
    "icon": curr_response["weather"][0]["icon"]
  }
  
  return weather_data

def valid_city(any_city):
  check_str = string.ascii_letters + '-'
  return all(char in check_str for char in any_city)

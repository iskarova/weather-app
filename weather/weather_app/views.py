import requests
from django.shortcuts import render


def index(request):
  API_KEY = "bf93b8b5def8cd901b298e9759de0a28"

  current_weather_url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
  
  
  if request.method == "POST":
    first_city = request.POST["first_city"]
    second_city = request.POST.get("second_city", None)
    
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
  
  weather_data = {
    "city": city,
    "temperature": round(curr_response['main']['temp'] - 273.15, 2),
    "description": curr_response["weather"][0]["description"],
    "icon": curr_response["weather"][0]["icon"]
  }
  
  return weather_data

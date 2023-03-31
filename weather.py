import requests
import json
import pickle
import os

class Weather:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5/"
        self.saved_locations_file = "saved_locations.pkl"


    def get_weather(self, location):
        url = f"{self.base_url}weather?q={location}&appid={self.api_key}&units=metric"
        response = requests.get(url)
        data = response.json()

        weather_data = {
            "location": f"{data['name']}, {data['sys']['country']}",
            "temp": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "lat": data["coord"]["lat"],
            "lon": data["coord"]["lon"],
        }

        return weather_data


    def get_extended_forecast(self, location):
    # Get the latitude and longitude of the location first
        current_weather_data = self.get_weather(location)
        lat = current_weather_data["lat"]
        lon = current_weather_data["lon"]

        url = f"{self.base_url}onecall?lat={lat}&lon={lon}&exclude=current,minutely,hourly,alerts&appid={self.api_key}&units=metric"
        response = requests.get(url)
        data = response.json()

        forecast_data = data["daily"]

        return forecast_data


    def convert_temperature(self, temp, unit):
        if unit == "F":
            return (temp * 9/5) + 32
        elif unit == "K":
            return temp + 273.15
        else:
            return temp

    def save_location(self, location):
        if os.path.exists(self.saved_locations_file):
            with open(self.saved_locations_file, "rb") as f:
                saved_locations = pickle.load(f)
        else:
            saved_locations = {}

        saved_locations[location] = True

        with open(self.saved_locations_file, "wb") as f:
            pickle.dump(saved_locations, f)

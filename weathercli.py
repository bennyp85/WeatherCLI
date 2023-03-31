# Import required libraries
import argparse
import json
import requests
from datetime import datetime
from weather import Weather

# Import Weather class from weather.py
from weather import Weather

# Import configuration settings from config.py
from config import API_KEY

# Define main() function
def main():
    # Parse command-line arguments using argparse
    parser = argparse.ArgumentParser(description="WeatherCLI: A command-line tool for fetching weather data")
    parser.add_argument("location", type=str, help="City name or zip code")
    parser.add_argument("-u", "--unit", choices=["C", "F", "K"], default="C", help="Temperature unit (Celsius, Fahrenheit, Kelvin)")
    parser.add_argument("-e", "--extended", action="store_true", help="Show extended forecast")
    parser.add_argument("-s", "--save", action="store_true", help="Save location for quick access")

    args = parser.parse_args()

    # Create an instance of the Weather class with the API key
    weather = Weather(API_KEY)

    # Get the weather data for the specified location
    current_weather = weather.get_weather(args.location)

    # Convert the temperature to the specified unit
    if args.unit != "C":
        current_weather["temp"] = weather.convert_temperature(current_weather["temp"], args.unit)

    # Get the extended forecast data if requested
    if args.extended:
        forecast_data = weather.get_extended_forecast(args.location)

    # Save the location if requested
    if args.save:
        weather.save_location(args.location)

    # Display the weather data using display_weather()
    display_weather(current_weather, args.unit, forecast_data if args.extended else None)

# Define display_weather() function
def display_weather(weather_data, unit, forecast_data=None):
    # Format and print weather data based on user's options
    unit_symbol = {"C": "°C", "F": "°F", "K": "K"}[unit]

    print(f"{weather_data['location']}:")
    print(f"Temperature: {weather_data['temp']}{unit_symbol}")
    print(f"Weather: {weather_data['description']}")
    print(f"Humidity: {weather_data['humidity']}%")
    print(f"Wind Speed: {weather_data['wind_speed']} m/s")

    if forecast_data:
        print("\nExtended forecast:")
        for day_data in forecast_data:
            day = datetime.fromtimestamp(day_data["dt"]).strftime("%A, %B %d")
            temp = day_data["temp"]["day"]
            if unit != "C":
                temp = Weather.convert_temperature(temp, unit)
            description = day_data["weather"][0]["description"]
            print(f"{day}: {temp}{unit_symbol}, {description}")


# Call the main() function to run the script
if __name__ == "__main__":
    main()

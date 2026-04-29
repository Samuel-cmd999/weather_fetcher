#!/usr/bin/env python3
"""
Weather Information Fetcher
A CLI tool to fetch current weather data from OpenWeatherMap API.
"""

import requests
import json
import os
from datetime import datetime

# You can get a free API key from: https://openweathermap.org/api
API_KEY_FILE = "weather_api_key.txt"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_api_key():
    """Get API key from file or prompt user."""
    if os.path.exists(API_KEY_FILE):
        with open(API_KEY_FILE, 'r') as f:
            return f.read().strip()
    return None

def save_api_key(key):
    """Save API key to file."""
    with open(API_KEY_FILE, 'w') as f:
        f.write(key.strip())
    print("✓ API key saved")

def kelvin_to_celsius(kelvin):
    """Convert Kelvin to Celsius."""
    return round(kelvin - 273.15, 1)

def kelvin_to_fahrenheit(kelvin):
    """Convert Kelvin to Fahrenheit."""
    return round((kelvin - 273.15) * 9/5 + 32, 1)

def get_weather(city, units="metric"):
    """Fetch weather data for a city."""
    api_key = get_api_key()
    
    if not api_key:
        print("No API key found. Set one with: python weather_fetcher.py setkey YOUR_KEY")
        print("Get a free API key at: https://openweathermap.org/api")
        return None
    
    params = {
        'q': city,
        'appid': api_key,
        'units': units
    }
    
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            print(f"City '{city}' not found")
        elif response.status_code == 401:
            print("Invalid API key. Get a new one at: https://openweathermap.org/api")
        else:
            print(f"HTTP Error: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")
        return None

def display_weather(data, units="metric"):
    """Display weather information in a formatted way."""
    if not data:
        return
    
    city = data.get('name', 'Unknown')
    country = data['sys'].get('country', '')
    temp = data['main']['temp']
    feels_like = data['main']['feels_like']
    humidity = data['main']['humidity']
    pressure = data['main']['pressure']
    description = data['weather'][0]['description'].title()
    wind_speed = data['wind']['speed']
    
    # Get additional info if available
    visibility = data.get('visibility', 'N/A')
    if visibility != 'N/A':
        visibility = f"{visibility/1000:.1f} km"
    
    unit_symbol = "°C" if units == "metric" else "°F" if units == "imperial" else "K"
    
    print("\n" + "="*50)
    print(f"WEATHER FOR {city.upper()}, {country}")
    print("="*50)
    print(f"  Condition:     {description}")
    print(f"  Temperature:   {temp}{unit_symbol}")
    print(f"  Feels Like:    {feels_like}{unit_symbol}")
    print(f"  Humidity:      {humidity}%")
    print(f"  Pressure:      {pressure} hPa")
    print(f"  Wind Speed:    {wind_speed} {'m/s' if units == 'metric' else 'mph'}")
    print(f"  Visibility:    {visibility}")
    print(f"  Data Time:      {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*50 + "\n")

def display_detailed(data, units="metric"):
    """Display detailed weather with all available info."""
    display_weather(data, units)
    
    if not data:
        return
    
    # Additional details
    print("DETAILED INFORMATION:")
    print("-"*50)
    
    # Sunrise/Sunset
    if 'sys' in data:
        sunrise = datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M')
        sunset = datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M')
        print(f"  Sunrise:       {sunrise}")
        print(f"  Sunset:        {sunset}")
    
    # Coordinates
    if 'coord' in data:
        print(f"  Coordinates:   {data['coord']['lat']}, {data['coord']['lon']}")
    
    # Clouds
    if 'clouds' in data:
        print(f"  Cloudiness:    {data['clouds']['all']}%")
    
    # Rain/Snow if available
    if 'rain' in data:
        print(f"  Rain (1h):     {data['rain'].get('1h', 'N/A')} mm")
    if 'snow' in data:
        print(f"  Snow (1h):     {data['snow'].get('1h', 'N/A')} mm")
    
    print("-"*50 + "\n")

def show_help():
    """Display help information."""
    print("""
Weather Fetcher Commands:
-------------------------
setkey <api_key>                 Save your OpenWeatherMap API key
get <city>                       Get current weather for city
get <city> --units imperial      Get weather in Fahrenheit
get <city> --units metric        Get weather in Celsius (default)
get <city> --detailed            Get detailed weather info
help                             Show this help message

Examples:
  python weather_fetcher.py setkey your_api_key_here
  python weather_fetcher.py get Johannesburg
  python weather_fetcher.py get "New York" --units imperial
  python weather_fetcher.py get London --detailed

Get a free API key at: https://openweathermap.org/api
""")

def main():
    """Main entry point."""
    import sys
    
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "setkey":
        if len(sys.argv) < 3:
            print("Usage: python weather_fetcher.py setkey YOUR_API_KEY")
            print("Get a free API key at: https://openweathermap.org/api")
            return
        save_api_key(sys.argv[2])
    
    elif command == "get":
        if len(sys.argv) < 3:
            print("Usage: python weather_fetcher.py get <city>")
            return
        
        city = sys.argv[2]
        units = "metric"
        detailed = False
        
        if "--units" in sys.argv:
            idx = sys.argv.index("--units")
            if idx + 1 < len(sys.argv):
                units = sys.argv[idx + 1]
        
        if "--detailed" in sys.argv:
            detailed = True
        
        data = get_weather(city, units)
        
        if data:
            if detailed:
                display_detailed(data, units)
            else:
                display_weather(data, units)
    
    elif command == "help":
        show_help()
    
    else:
        print(f"Unknown command: {command}")
        show_help()

if __name__ == "__main__":
    main()

# Weather Information Fetcher

A CLI tool to fetch current weather data using the OpenWeatherMap API.

## Features

- Fetch current weather for any city
- Temperature in Celsius (metric), Fahrenheit (imperial), or Kelvin
- Detailed weather information including sunrise/sunset
- Shows humidity, pressure, wind speed, visibility
- API key management (saved locally)

## Installation

```bash
pip install requests
```

## Setup

1. Get a free API key from [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for a free account
3. Copy your API key
4. Save it using the tool:

```bash
python weather_fetcher.py setkey your_api_key_here
```

## Usage

```bash
# Set your API key (first time setup)
python weather_fetcher.py setkey abc123yourapikey

# Get weather for a city (Celsius by default)
python weather_fetcher.py get Johannesburg

# Get weather in Fahrenheit
python weather_fetcher.py get "New York" --units imperial

# Get detailed weather info
python weather_fetcher.py get London --detailed

# Show help
python weather_fetcher.py help
```

## Example Output

```
==================================================
WEATHER FOR JOHANNESBURG, ZA
==================================================
  Condition:     Partly Cloudy
  Temperature:   22.5°C
  Feels Like:    21.8°C
  Humidity:      65%
  Pressure:      1013 hPa
  Wind Speed:    3.5 m/s
  Visibility:    10.0 km
  Data Time:      2024-01-15 14:30:00
==================================================
```

## Files

- `weather_fetcher.py` - Main application
- `weather_api_key.txt` - Saved API key (keep private!)

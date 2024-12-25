import requests
import json
from typing import Dict, Any, Union

def get_coordinates_from_zip(zip_code: str) -> Union[Dict[str, float], None]:
    """
    Convert a zip code to latitude and longitude using an external API (e.g., OpenCage Geocoder or similar).

    Args:
        zip_code (str): The zip code to convert.

    Returns:
        Dict[str, float]: A dictionary with latitude and longitude, or None if conversion fails.
    """
    # Example using a placeholder API (replace with a real geocoding API)
    geocoding_url = f"https://api.zippopotam.us/us/{zip_code}"
    response = requests.get(geocoding_url)
    if response.status_code == 200:
        data = response.json()
        return {"latitude": float(data['places'][0]['latitude']), "longitude": float(data['places'][0]['longitude'])}
    return None

def get_weather_data(input_data: Union[str, Dict[str, float]]) -> Dict[str, Any]:
    """
    Retrieve weather data for a given location using the Open-Meteo API.

    Args:
        input_data (Union[str, Dict[str, float]]): Either a zip code (str) or a dictionary with latitude and longitude.

    Returns:
        Dict[str, Any]: A dictionary containing weather data or an error message.
    """
    # Determine if input is a zip code or coordinates
    if isinstance(input_data, str):
        coordinates = get_coordinates_from_zip(input_data)
        if not coordinates:
            return {"error": "Invalid zip code or unable to fetch coordinates."}
        latitude = coordinates["latitude"]
        longitude = coordinates["longitude"]
    elif isinstance(input_data, dict) and "latitude" in input_data and "longitude" in input_data:
        latitude = input_data["latitude"]
        longitude = input_data["longitude"]
    else:
        return {"error": "Invalid input. Provide a zip code or a dictionary with latitude and longitude."}

    # Open-Meteo API endpoint
    url = "https://api.open-meteo.com/v1/forecast"

    # Parameters for the API request
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m,wind_speed_10m,relative_humidity_2m",
        "current_weather": True
    }

    # Make the API request
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to fetch data. Status code: {response.status_code}"}

# Example usage
if __name__ == "__main__":
    # Test with latitude and longitude
    # coordinates = {"latitude": 40.7128, "longitude": -74.0060}  # New York City
    # weather_data_coords = get_weather_data(coordinates)
    # print("Weather data for coordinates:")
    # print(json.dumps(weather_data_coords, indent=4))

    # Test with zip code
    zip_code = "20148"  # New Ashburn zip code
    weather_data_zip = get_weather_data(zip_code)
    print(f"\nWeather data for zip code: {zip_code}")
    print(json.dumps(weather_data_zip, indent=4))
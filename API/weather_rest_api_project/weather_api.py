import requests   #to call the weather API.
import json     #to handle JSON data.
from Config import API_KEY, BASE_URL, DEFAULT_CITY, UNITS  # imports your API key, base URL, default city, and units from a separate config file.
from datetime import datetime #to add a timestamp when data is fetched.


'''Defines a function get_weather_data(city):
Builds query parameters (q, appid, units).
Calls the API using requests.get.
Prints the full request URL for debugging.
If status code is 200 → returns JSON response
Otherwise prints error and returns None.'''

def get_weather_data(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": UNITS
    }
    response = requests.get(BASE_URL, params=params)
    print("Request URL:", response.url)  # Debugging: Print the full request URL    
    if response.status_code == 200:
        return response.json()
    else:
        print("API request failed with status code:", response.status_code)
        print("Response:", response.text)
        return None

'''Defines extract_weather_details(data):
Checks if data exists.
Extracts key info: city name, temperature, humidity, weather description.
Adds a timestamp.
Returns a dictionary with these details.
If no data → returns None.'''

def extract_weather_details(data):
    if data:
        weather_details = {
            "city": data.get("name"),
            "temperature": data.get("main", {}).get("temp"),
            "humidity": data.get("main", {}).get("humidity"),
            "weather": data.get("weather", [{}])[0].get("description"),
            "timestamp": datetime.now().isoformat()
        }
        return weather_details
    else:
        return None

'''Defines save_to_file(weather_details):
Opens a file (weather_output.json) in write mode.
Dumps the weather details into JSON format.
Prints confirmation.
If no details → prints a message.'''

def save_to_file(weather_details, filename="weather_output.json"):
    """Save weather details into a JSON file."""
    if weather_details:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(weather_details, f, indent=4)
        print(f"Weather details saved to {filename}")
    else:
        print("No weather details to save.")

'''Defines main():
Prompts user for a city name (defaults to DEFAULT_CITY if empty).
Calls get_weather_data(city) to fetch API data.
Extracts details with extract_weather_details.
Prints details and saves them to file.'''

def main():
    city = input(f"Enter city name or press Enter for default ({DEFAULT_CITY}): ") or DEFAULT_CITY
    weather_data = get_weather_data(city)
    weather_details = extract_weather_details(weather_data)

    if weather_details:
        print("Weather Details:", weather_details)
        save_to_file(weather_details)  # Save result to file

#Ensures the script runs main() only when executed directly, not when imported.
if __name__ == "__main__":
    main()

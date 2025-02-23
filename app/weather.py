import requests
import re 
from app.translator import translate_ru
def get_weather(city_name):
    api_key = "dddbea70c08a66f713e3b2d79b504ed6"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        main = data['main']
        weather = data['weather'][0]

        temperature = main['temp']
        humidity = main['humidity']
        weather_description = weather['description']

        return f"{translate_ru(city_name)}: {translate_ru(f"The temperature is: {temperature}°C")}, {translate_ru(f"The humidity: {humidity}%")}, {translate_ru(f"Weather Description: {weather_description.capitalize()}")}"
    else:
        return ("City not found or API key is invalid")


def get_city(sentence):
    match = re.search(r'in\s+([A-Za-z\s]+)', sentence)

    if match:
        city = match.group(1)
        return city
    else:
        print("City not found")

import requests
import gradio as gr
import subprocess


API_KEY = "" # Enter API Key Here

WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city):

	params = {
		'q': city,
		'appid': API_KEY,
		'units': 'imperial'
	}

	response = requests.get(WEATHER_URL, params=params)
	data = response.json()

	if response.status_code == 200:

		weather_description = data['weather'][0]['description']
		temp = data['main']['temp']
		location = data['name']

		return f'The weather in {location} is {weather_description} with a temperature of {temp} degrees farenheight'

	else:
		return f"Error Code {response.status_code}. Couldn't retrieve the data."


# TESTING IF THE API WORKS
city = input('Enter a City:')
print(get_weather(city))


def generate_creative_text(city, writing_stype):

	weather_summary = get_weather(city)

	prompt = 'Write a {writing_style} inspired by this weather description: {weather_summary}. Do not mention the city itself, it should only be based on the weather.'

	result = subprocess.run(

		['ollama', 'run', 'tinyllama'],
		input = prompt.encode(),
		capture_output = True

		)

	return result.stdout.decode().strip()


# TESTING IF AI PROMPT WORKS
# print(generate_creative_text(city,'very short poem'))
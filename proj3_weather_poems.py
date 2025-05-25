import requests
import gradio as gr
import subprocess
from dotenv import load_dotenv
import os
#load environment variables
load_dotenv()
API_KEY = os.getenv("api_key") # Enter API Key Here

if not API_KEY:
	print("Error: API_KEY not found")
	print("Please make a .env file with the api key given to you")

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


def generate_creative_text(city, writing_style):

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
with gr.Blocks() as demo:
	gr.Markdown("Weather Mood Writer")
	gr.Markdown("Type in a city and select a writing style. This AI with write creative text based on current weather conditions!")

	city_input = gr.Textbox(label="Enter a City", placeholder="Ex) New York City")

	style_dropdown = gr.Dropdown(

		choices = ["Poem", "Short Story", "Journal Entry"],
		label = "Choose a Writing Style"

	)

	output_box = gr.Textbox(label="Prompt Output")
	generate_button = gr.Button("Generate")

	generate_button.click(

		fn = generate_creative_text,
		inputs = [city_input, style_dropdown],
		outputs = output_box

		)


# RUNNING THE WHOLE PROGRAM
if __name__ == "__main__":
	demo.launch(share=True)

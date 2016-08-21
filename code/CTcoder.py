# encoding: utf-8
import os
import time
from slackclient import SlackClient
import urllib2
import json
import webbrowser

#starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")
SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')

#constants
AT_BOT = "<@" + BOT_ID + ">"
SHOW_COMMAND = "show"

#instantiate Slack & Twilio clients
slack_client = SlackClient(SLACK_BOT_TOKEN)

#id de cidades
id_aveiro = "2742611"
id_lisboa = "6458923"
id_porto = "2735943"

#open Weather API KEY
APIKEY = "f2a2184518b621bbd171e6c6cf9b518d"

# determines what to do
def handle_command(command, channel):
	"""
		Receives commands directed at the bot and determines if they are valid commands.
		If so, then acts on the commands. If not, returns back what it needs for clarification.
	"""

	response = ""
	words = len(command.split())
	if command.startswith(SHOW_COMMAND) and words > 1:
		if command.split(" ")[1].lower() == "weather":
			response = city_temp(command.split("/")[1])
		elif command.split(" ")[1].lower() == "forecast":
			response = city_forecast(command.split(" ")[2].lower())
		
	elif command.split(" ")[0].lower() == "hello":
		if command.split(" ")[1].lower() == "weather":
			response = city_temp("all")

	else :
		response = "Not sure what you mean. Use the *" + SHOW_COMMAND + "* command followed with the sub command, delimited by spaces."

	slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)	


# takes msg from slack and determines if they are directed at our StarterBot
def parse_slack_output(slack_rtm_output):
	"""
		The Slack Real Time Messaging API is an events firehose.
		This parsing function returns None unless a message is directed at the Bot, based on its ID.
	"""
	output_list = slack_rtm_output
	if output_list and len(output_list) > 0:
		for output in output_list:
			if output and 'text' in output and AT_BOT in output['text']:
				#return text after the @ mention, whitespace removed
				return output['text'].split(AT_BOT)[1].strip().lower(), output['channel']
	return None, None


#returns the weather(temperature) of the given city
def city_temp(city):
	if city == "all":
		#aveiro weather
		content = urllib2.urlopen("http://api.openweathermap.org/data/2.5/weather?id="+id_aveiro+"&units=metric&APPID="+APIKEY).read()
		parsed_content = json.loads(content)
		string_temp = "%.2f" % parsed_content['main']['temp']
		aveiro_temp = string_temp

		#porto weather
		content = urllib2.urlopen("http://api.openweathermap.org/data/2.5/weather?id="+id_porto+"&units=metric&APPID="+APIKEY).read()
		parsed_content = json.loads(content)
		string_temp = "%.2f" % parsed_content['main']['temp']
		porto_temp = string_temp

		#lisboa weather
		content = urllib2.urlopen("http://api.openweathermap.org/data/2.5/weather?id="+id_lisboa+"&units=metric&APPID="+APIKEY).read()
		parsed_content = json.loads(content)
		string_temp = "%.2f" % parsed_content['main']['temp']
		lisboa_temp = string_temp

		return "Bom dia CTcoder! \nEstá uma temperatura de "+aveiro_temp+"ºC em Aveiro. \nEstá uma temperatura de "+porto_temp+"ºC no Porto. \nEstá uma temperatura de "+lisboa_temp+"ºC em Lisboa. \n Have a nice day!"

	else:
		print city+"\n"
		city_tmp = city.split(",")[0]
		country = city.split(",")[1]
		print city_tmp +"; "+country+"\n" 
		content = urllib2.urlopen("http://api.openweathermap.org/data/2.5/weather?q="+city_tmp+","+country+"&units=metric&APPID="+APIKEY).read()
		parsed_content = json.loads(content)
		string_temp = "%.2f" % parsed_content['main']['temp']
		return "Está uma temperatura de "+string_temp+"ºC. \nHave a nice day."

def city_forecast(city):
	if city == "aveiro":
		#aveiro weather
		content = urllib2.urlopen("http://api.openweathermap.org/data/2.5/forecast?id="+id_aveiro+"&units=metric&APPID="+APIKEY).read()
		parsed_content = json.loads(content)
		lista = parsed_content['list']
		values = "Forecast para Aveiro: \n"
		for p in lista:
			#print ("date: "+p['dt_txt']+"; max_temp: "+ "%.2f" % p['main']['temp_max']+"; temp: "+ "%.2f" % p['main']['temp']+"; temp_min: "+ "%.2f" % p['main']['temp_min'])
			
			if p['dt_txt'].split(" ")[1] == "09:00:00" or p['dt_txt'].split(" ")[1] == "12:00:00" or p['dt_txt'].split(" ")[1] == "15:00:00":
				values+="date: "+p['dt_txt']+"; max_temp: "+ "%.2f" % p['main']['temp_max']+"; temp: "+ "%.2f" % p['main']['temp']+"; temp_min: "+ "%.2f" % p['main']['temp_min']+"\n"
				if p['dt_txt'].split(" ")[1] == "15:00:00":
					values+="\n"
		return values
	else:
		return ""



if __name__ == "__main__":
	READ_WEBSOCKET_DELAY = 1 #1 second delay between reading from firehose
	if slack_client.rtm_connect():
		print("StarterBot connected and running!")
		while True:
			command, channel = parse_slack_output(slack_client.rtm_read())
			if command and channel:
				handle_command(command, channel)
			time.sleep(READ_WEBSOCKET_DELAY)
	else:
		print("Connection failed. Invalid Slack token or bot ID?")
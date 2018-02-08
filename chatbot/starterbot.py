#Adopted with modifications from https://github.com/mattmakai/slack-starterbot/blob/master/starterbot.py
#Distributed under MIT license

#don't forget to set the environmental variable SLACK_BOT_TOKEN using
#export SLACK_BOT_TOKEN='xoxb-302972529057-XQvFAM4cU0jt0Tw9r6q18upM'
#or hardcode 

import os
import time
import re
from slackclient import SlackClient
from pprint import pprint
import requests
import json #used for debug printing


# instantiate Slack client
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None
weather_key = 'a3d2848b016e5b1f376098a55f215b55'


# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
COMMANDS = ['do', 'weather']

weather_data = json.load(open('city.list.json'))
#pprint(weather_data[1]['name'])

#for i in weather_data:
#    if i['name'] == 'Etobicoke':
#        pprint(i['id'])




MENTION_REGEX = "^<@(|[WU].+)>(.*)"

def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
    	#uncomment line below to debug print
    	#print json.dumps(event, indent = 2, sort_keys = True)
        
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            #uncomment line below to debug print
            #print user_id, " : ", message
            if user_id == starterbot_id:
                return message, event["channel"]
    return None, None

def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(command, channel):
    """
        Executes bot command if the command is known
    """
    # Default response is help text for the user
    default_response = "Not sure what you mean. Try *{}*.".format(COMMANDS[1])

    # Finds and executes the given command, filling in response
    response = None
    # This is where you start to implement more commands!

    split_command = command.split(' ')

    pprint(split_command)

    if split_command[0] == "weather":

        #print((command).strip("weather "))

        #response = get_weather(split_command[1])
        temp = command.split(' ', 1)[1]
        response = get_weather(command.split(' ', 1)[1])


    elif "?" in command:
        response = command 

    else:
        response = "Sure...write some more code then I can do that!"

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )

## FORMAT FOR WEATHER CALL IS: @starterbot weather City     (First letter Capital in City)

def get_weather(city):

    _id = ""

    #for i in weather_data:
    #    if (i['name']).lower() == city.lower():
    #        pprint(_id)
    #        _id = i['id']    

    pprint(_id)

    url = 'http://api.openweathermap.org/data/2.5/weather?q=' + city + '&APPID=' + weather_key + '&units=metric'
    #url = 'http://api.openweathermap.org/data/2.5/weather?id=' + str(_id) + '&APPID=' + weather_key + '&units=metric'
    #url = 'http://api.openweathermap.org/data/2.5/forecast/city?id=' + _id + '&APPID=' + weather_key   # full url


    r = requests.get(url)
    #pprint(r.json()['main']['temp_max'])

    #pprint(r.json()['message'])



    return("The temperature in " + city + " is " + (str)(r.json()['main']['temp_max']) + " degrees celsius.")


if __name__ == "__main__":
	# avm: connect is designed for larger teams, 
	# see https://slackapi.github.io/python-slackclient/real_time_messaging.html
	# for details
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")
#pip install slack client, flask, slackevents api
#get keys for slackclient, slackapi
#run ngrok, "ngrok http [local host port]"
#remember ngrok only transfers host, so you need to run locally first
#subscribe to slack events with ngrok URL + '/slack/events'

import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'],'/slack/events',app) #API param1, send events to param2, webserver param3

client = slack.WebClient(token=os.environ['SLACK_TOKEN']) #API
BOT_ID = client.api_call("auth.test")['user_id'] 

@slack_event_adapter.on('message') # if message is sent,
def message(payload): #take "payload" which is message data
    event = payload.get('event', {}) #if payload does not exist, return nothing
    channel_id = event.get('channel') #gets channel id from payload 
    user_id = event.get('user')
    text = event.get('text')

    if BOT_ID != user_id:
        client.chat_postMessage(channel=channel_id, text = text) 


#boilerplate, only runs code when on main module, otherwise acts like library
if __name__ == "__main__":
    app.run(debug=True)
#pip install slack client, flask, slackevents api
#get keys for slackclient, slackapi
#run ngrok, "ngrok http [local host port]"
#remember ngrok only transfers host, so you need to run locally first
#subscribe to slack events with ngrok URL + '/slack/events'

import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter
from werkzeug.wrappers import response

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'],'/slack/events',app) #API param1, send events to param2, webserver param3

client = slack.WebClient(token=os.environ['SLACK_TOKEN']) #API
BOT_ID = client.api_call("auth.test")['user_id'] 

message_counts = {'user_id': 0}
my_list = {'user_id': ' '}

@slack_event_adapter.on('message') # if message is sent,
def message(payload): #take "payload" which is message data
    event = payload.get('event', {}) #if payload does not exist, return nothing
    user_id = event.get('user')
    text = event.get('text')

    if BOT_ID != user_id:
        if user_id in my_list:
            my_list[user_id] += '\n'
            my_list[user_id] += text
        else:
            my_list[user_id] = 'List: '
            my_list[user_id] += '\n'
            my_list[user_id] += text

    if BOT_ID != user_id:
        if user_id in message_counts:
            message_counts[user_id] += 1
        else:
            message_counts[user_id] = 1


@app.route('/message-count', methods=['POST']) #message-count is the endpoint, POST is the permission to post something, you can also use GET
def message_count(): #now theres no payload, how do you get info?
    data = request.form
    user_id = data.get('user_id')
    user_name = data.get('user_name')
    channel_id = data.get('channel_id')
    message_count = message_counts.get(user_id, 0) # return 0 if not found
    mylist = my_list.get(user_id, 'list not found')
    client.chat_postMessage(channel=channel_id,text = f"{user_name}'s messages: {message_count}")
    client.chat_postMessage(channel=channel_id,text = mylist)
    return Response(), 200 #200 means ok, 404 means not ok




#boilerplate, only runs code when on main module, otherwise acts like library
if __name__ == "__main__":
    app.run(debug=True)
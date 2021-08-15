import os
import time
import json
import requests
from discord import Webhook, RequestsWebhookAdapter
from discord_webhook import DiscordWebhook, DiscordEmbed

#wekbook url variable, but hidden so u dont steal it lmfao
#for non replit users, use webhookurl = 'urlhere'
webhookurl = os.environ['webhookurl']
webhook = DiscordWebhook(url=webhookurl)

#table for how many visits are needed to send a notification
milestones = ['200000', '400000', '800000', '1000000']


#function to actually send the notification with the given visit count
def post(count):
    embed = DiscordEmbed(title='New milestone reached!',
                         description=str(count),
                         color='F55168')
    DiscordWebhook(title='@everyone')

    webhook.add_embed(embed)
    webhook.execute()

    ping = Webhook.from_url(webhookurl, adapter=RequestsWebhookAdapter())
    ping.send("@everyone")

    print("MILESTONE HIT:" + str(count))


#loop to check the visits every 10 seconds. if it matches anything in the milestones table, it runs the post notification function
while True:
    url = "https://games.roblox.com/v1/games?universeIds=2686191831"
    req = requests.get(url, stream=True)
    json_data = json.loads(req.text)
    visits = json_data['data'][0]['visits']
    string = str(round(visits, -3))
    print(string)
    if string in milestones:
        post(string)
        exit()
    time.sleep(10)

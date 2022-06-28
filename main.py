# from lib2to3.pgen2 import token
import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()

sad_words= ['Hopeless','Depressed','Mournful','Despairing','Miserable','Downcast','Gloomy','Heartbroken','Sorrowful','Glum','Dispirited','Dejected','Defeated','Woeful','Disheartened','Crushed','Crestfallen','Dismayed','Dismal','Dreary','sad']

encouraged_words = ["Hang in there.","Don't give up.","Keep pushing.","Keep fighting!","Stay strong.","Never give up.","Never say 'die'.","Come on! You can do it!.","Follow your dreams.","Reach for the stars.","Do the impossible.","Believe in yourself.","The sky is the limit."]

if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q']+" -"+json_data[0]['a']
  return (quote)

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragement(index):
  encouragements = db["encouragements"]
  if len(encouragements)>index:
    del encouragements[index]
    db["encouragements"] = encouragements

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    msg= message.content
    if message.author == client.user:
      return
    if msg.startswith('$inspire'):
      quote = get_quote()
      await message.channel.send(quote)

    if db["responding"]:
      options = encouraged_words
      if "encouragements" in db.keys():
        options = options + list(db["encouragements"])
    
      if any(word in msg for word in sad_words):
        await message.channel.send(random.choice(encouraged_words))

    if msg.startswith("$new"):
      encouraging_message = msg.split("$new ",1)[1]
      update_encouragements(encouraging_message)
      await message.channel.send("New Encouraging message added.")

    if msg.startswith("$del"):
      encouragements = []
      if "encouragements" in db.keys():
        index = int(msg.split("$del",1)[1])
        delete_encouragement(index)
        encouragements = db["encouragements"]
      await message.channel.send(encouragements)

    if msg.startswith("$list"):
      encouragements = []
      if "encouragements" in db.keys():
        encouragements = db["encouragements"]
      await message.channel.send(encouragements)

    if msg.startswith("$responding"):
      value = msg.split("$responding ",1)[1]
      if value.lower() == "true":
        db["responding"] = True
        await message.channel.send("Responding is on.")
      else:
        db["responding"] = False
        await message.channel.send("Responding is off.")
        
keep_alive()
client.run(os.getenv('token'))

from botconfig import Config
from minh import Minh

import discord

client = discord.Client()
minh = Minh(client)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    if message.content.startswith('+'):
        await minh.proc_cmd(message)


client.run(Config.bot_token)

from botconfig import bot_token
from botconfig import meme_list_file_name
from minh import Minh

import discord

minh = Minh(meme_list_file_name)
client = discord.Client()


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


client.run(bot_token)

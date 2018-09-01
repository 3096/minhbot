from botconfig import bot_token
from botconfig import meme_list_file_name

import discord
import asyncio
import os
import requests

def url_return_200(url):
    try:
        request = requests.get(url)
        return request.status_code == 200
    except:
        return False

meme_dict = {}
with open(meme_list_file_name, 'a+') as meme_list_file:
    meme_list_file.seek(0)
    for meme in meme_list_file:
        meme_entry = meme.split(' ', 1);
        if len(meme_entry) is 2:
            meme_dict[meme_entry[0]] = meme_entry[1]

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
        msg_tokens = message.content.split(' ')
        msg = ""
        memes_changed = False

        if message.content.startswith('+help'):
            msg = "Meme guide:\n"
            msg = msg + "+`memename` to send meme\n"
            msg = msg + "add: `+add name url` or `add name` with upload\n"
            msg = msg + "list: `+ls`\n"
            msg = msg + "rename: `+rename oldname newname`\n"
            msg = msg + "remove: `+rm name`\n"

            await client.send_message(message.channel, msg)

        elif message.content.startswith('+add'):
            url = ""
            if len(message.attachments) is not 0:
                url = message.attachments[0]['url']
            elif len(msg_tokens) >= 3:
                url = msg_tokens[2]

            msg_failed = "Mmmmh. Failed to add meme."
            if len(msg_tokens) >= 2 and len(url) > 0:
                meme_key = msg_tokens[1]
                if url_return_200(url):
                    meme_dict[meme_key] = url
                    msg = "Added \"" + meme_key + "\" to my spicy memes"
                    memes_changed = True
                else:
                    msg = msg_failed
            else:
                msg = msg_failed

            await client.send_message(message.channel, msg)

        elif message.content.startswith('+ls'):
            msg = "Total of " + str(len(meme_dict)) + " memes:\n"
            for meme_key in meme_dict:
                msg = msg + meme_key + "\n"
            await client.send_message(message.channel, msg)

        elif message.content.startswith('+rm'):
            if len(msg_tokens) < 2:
                msg = "What are you trying to remove?"
            else:
                remove_meme_key = msg_tokens[1]
                if remove_meme_key in meme_dict:
                    meme_dict.pop(remove_meme_key)
                    msg = "Goodbye meme, " + remove_meme_key
                    memes_changed = True
                else:
                    msg = "Didn't even find " + remove_meme_key

            await client.send_message(message.channel, msg)

        elif message.content.startswith('+rename'):
            if len(msg_tokens) < 3:
                msg = "`+rename oldname newname` pls"
            else:
                old_meme_key = msg_tokens[1]
                new_meme_key = msg_tokens[2]
                if old_meme_key in meme_dict:
                    meme_dict[new_meme_key] = meme_dict.pop(old_meme_key)
                    msg = "Renamed " + old_meme_key + " to " + new_meme_key
                    memes_changed = True
                else:
                    msg = "Didn't even find " + old_meme_key
                    
            await client.send_message(message.channel, msg)
        else:
            meme_key = msg_tokens[0][1:]
            if meme_key in meme_dict:
                msg = meme_dict[meme_key]
                await client.send_message(message.channel, msg)

        if memes_changed:
            with open(meme_list_file_name, 'w+') as meme_list_file:
                for meme_key in meme_dict:
                    meme_list_file.write(meme_key)
                    meme_list_file.write(' ')
                    meme_list_file.write(meme_dict[meme_key])
                    meme_list_file.write('\n')

client.run(bot_token)

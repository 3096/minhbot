from botconfig import Config

import requests


def url_return_200(url):
    try:
        request = requests.get(url)
        return request.status_code == 200
    except ConnectionError:
        return False


# noinspection PyMethodMayBeStatic
class Minh:
    meme_dict = {}

    def __init__(self, client):
        self.client = client

        with open(Config.meme_list_file_path, 'a+') as meme_list_file:
            meme_list_file.seek(0)
            for meme in meme_list_file:
                meme_entry = meme.split(' ', 1)
                if len(meme_entry) is 2:
                    self.meme_dict[meme_entry[0]] = meme_entry[1]

    def save_meme(self):
        with open(Config.meme_list_file_path, 'w+') as out_meme_list_file:
            for meme_key in self.meme_dict:
                out_meme_list_file.write(meme_key)
                out_meme_list_file.write(' ')
                out_meme_list_file.write(self.meme_dict[meme_key])
                out_meme_list_file.write('\n')

    async def send_msg(self, channel, msg):
        await channel.send(msg)

    async def cmd_help(self, message, msg_tokens):
        return "Meme guide:\n" \
               "`+memename` to send meme\n" \
               "`+add name url` or `+add name` with upload to add a meme\n" \
               "`+ls` to list all saved memes\n" \
               "`+rename oldname newname` to rename a meme\n" \
               "`+rm name` to remove a meme\n" \
               "`+help` to display this\n"

    async def cmd_add(self, message, msg_tokens):
        url = ""
        if len(message.attachments) is not 0:
            url = message.attachments[0]['url']
        elif len(msg_tokens) >= 3:
            url = msg_tokens[2]

        msg_failed = "Mmmmh. Failed to add meme."
        if len(msg_tokens) >= 2 and len(url) > 0:
            meme_key = msg_tokens[1]
            if url_return_200(url):
                self.meme_dict[meme_key] = url
                reply_msg = "Added \"" + meme_key + "\" to my spicy memes"
                self.save_meme()
            else:
                reply_msg = msg_failed
        else:
            reply_msg = msg_failed

        return reply_msg

    async def cmd_ls(self, message, msg_tokens):
        reply_msg = "Total of " + str(len(self.meme_dict)) + " memes:\n"
        for meme_key in self.meme_dict:
            reply_msg += meme_key + "\n"
        return reply_msg

    async def cmd_rm(self, message, msg_tokens):
        if len(msg_tokens) < 2:
            reply_msg = "What are you trying to remove?"
        else:
            remove_meme_key = msg_tokens[1]
            if remove_meme_key in self.meme_dict:
                self.meme_dict.pop(remove_meme_key)
                reply_msg = "Goodbye meme, " + remove_meme_key
                self.save_meme()
            else:
                reply_msg = "Didn't even find " + remove_meme_key

        return reply_msg

    async def cmd_rename(self, message, msg_tokens):
        if len(msg_tokens) < 3:
            reply_msg = "`+rename oldname newname` pls"
        else:
            old_meme_key = msg_tokens[1]
            new_meme_key = msg_tokens[2]
            if old_meme_key in self.meme_dict:
                self.meme_dict[new_meme_key] = self.meme_dict.pop(old_meme_key)
                reply_msg = "Renamed " + old_meme_key + " to " + new_meme_key
                self.save_meme()
            else:
                reply_msg = "Didn't even find " + old_meme_key

        return reply_msg

    async def admin_cmd_send(self, message, msg_tokens):
        print(message.author.id)
        if message.author.id not in Config.admin_id:
            return ""

        target_channel = self.client.get_channel(int(msg_tokens[1]))
        await self.send_msg(target_channel, " ".join(msg_tokens[2:]))

        return "sent"

    cmd_cb_dict = {
        "help": cmd_help,
        "add": cmd_add,
        "ls": cmd_ls,
        "rm": cmd_rm,
        "rename": cmd_rename,

        # admin commands
        "send": admin_cmd_send
    }

    async def proc_cmd(self, message):
        msg_tokens = message.content[1:].split(" ")
        try:
            reply_msg = await self.cmd_cb_dict[msg_tokens[0]](self, message, msg_tokens)
        except KeyError:
            try:
                reply_msg = self.meme_dict[msg_tokens[0]]
            except KeyError:
                return

        if len(reply_msg) > 0:
            await message.channel.send(reply_msg)

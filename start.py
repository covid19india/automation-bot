#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple Bot to reply to Telegram messages.

This is built on the API wrapper, see echobot2.py to see the same example built
on the telegram.ext bot framework.
This program is dedicated to the public domain under the CC0 license.
"""
import logging
import telegram
from telegram.error import NetworkError, Unauthorized
from time import sleep
import os
from time import time

BOT_TOKEN = os.environ["COVID_BOT_TOKEN"]
if os.environ["UPDATE_ID"]:
    update_id = int(os.environ["UPDATE_ID"])
else:
    update_id = None
print("this is the last update_id")
print(update_id)
# print(BOT_TOKEN)

start_time = int(time())
print("Start time: " + str(start_time))


def main():
    """Run the bot."""
    global update_id
    # Telegram Bot Authorization Token
    bot = telegram.Bot(BOT_TOKEN)

    # get the first pending update_id, this is so we can skip over it in case
    # we get an "Unauthorized" exception.
    # try:
    #     update_id = bot.get_updates()[0].update_id
    # except IndexError:
    #     update_id = 0

    logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    while True:
        try:
            echo(bot)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            update_id += 1
        if int(time()) - start_time > 60:
            print("enough for the day!")
            with open("/tmp/update_id", "w") as the_file:
                the_file.write(str(update_id))
            break
        else:
            print(int(time()) - start_time)


def echo(bot):
    """Echo the message the user sent."""
    global update_id
    # Request updates after the last update_id
    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1
        # print(update)

        if update.message:  # your bot can receive updates without messages
            # Reply to the message
            update.message.reply_text(update.message.text)


if __name__ == "__main__":
    main()

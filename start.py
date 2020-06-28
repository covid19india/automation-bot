#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import telegram
from telegram.error import NetworkError, Unauthorized
from time import sleep
import os
from time import time
from src.entry import entry

BOT_TOKEN = os.environ["COVID_BOT_TOKEN"]
try:
    update_id = int(os.environ["UPDATE_ID"])
except:
    update_id = 0

start_time = int(time())


def main():
    """Run the bot."""
    global update_id
    bot = telegram.Bot(BOT_TOKEN)

    logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    while True:
        try:
            for update in bot.get_updates(offset=update_id, timeout=60):
                update_id = update.update_id + 1
                entry(bot, update)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            update_id += 1
        if int(time()) - start_time > 3600:
            print("enough for the day!")
            with open("/tmp/update_id", "w") as the_file:
                the_file.write(str(update_id))
            break

if __name__ == "__main__":
    main()

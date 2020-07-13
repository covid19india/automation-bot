from os import stat
import telegram
from src.bulletin import Bulletin
import subprocess
import os
import shlex
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from src.util import build_menu, state_dict
from src.ocr_functions import ocr1, ocr2, pdf
import json


def entry(bot, update):
    try:
        res = bot.send_message(chat_id="-1001429652488", text=update.to_json())
        # print(json.dumps(update.to_dict(), indent=2))
        pass
    except Exception as e:
        print(e)
        bot.send_message(chat_id="-1001429652488", text=str(e))
        pass
    if update.callback_query:
        state_name = update.callback_query.data
        photo = update.callback_query.message.reply_to_message.photo[-1]
        is_translation_req = False
        if state_name == "Bihar" or state_name == "Uttar Pradesh":
            is_translation_req = True
        ocr1(
            bot,
            update.callback_query.message.chat.id,
            photo,
            state_name,
            "auto,auto",
            is_translation_req,
        )
        return
    if update.message:
        # Reply to the message
        if update.message.photo:
            button_list = []
            for key in state_dict:
                button_list.append(
                    InlineKeyboardButton(state_dict[key], callback_data=state_dict[key])
                )
            reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=3))
            bot.send_message(
                chat_id=update.message.chat.id,
                text="Which state bulletin is this?",
                reply_to_message_id=update.message.message_id,
                reply_markup=reply_markup,
            )
            return
        if not update.message.text:
            return
        message = None
        if update.message.text.startswith("/test"):
            message = "200 OK!"
        if update.message.reply_to_message and update.message.text.startswith("/"):
            bot.send_chat_action(
                chat_id=update.message.chat.id, action=telegram.ChatAction.TYPING
            )
            text_prev = update.message.text
            text_replaced = text_prev.replace("“", '"').replace("”", '"')
            text = shlex.split(text_replaced)
            if update.message.text.startswith("/ocr1"):
                if len(text) < 4:
                    return
                photo = update.message.reply_to_message.photo[-1]
                ocr1(bot, update.message.chat.id, photo, text[1], text[2], text[3])
            elif update.message.text.startswith("/ocr2"):
                if len(text) < 2:
                    return
                ocr2(
                    bot,
                    update.message.chat.id,
                    update.message.reply_to_message.text,
                    text[1],
                )
            elif update.message.text.startswith("/pdf"):
                if len(text) < 2:
                    return
                try:
                    if update.message.reply_to_message.entities[0].type == 'url':
                        text_prev = update.message.text
                        text_replaced = text_prev.replace("“", '"').replace("”", '"')
                        text = shlex.split(text_replaced)
                        url = update.message.reply_to_message.text
                        # Link passed. Call pdf automation
                        pdf(
                            bot,
                            update.message.chat.id,
                            url,
                            text[1],
                        )
                except KeyError:
                    update.message.reply_text("/pdf command need a downloadable link")
                    pass
            elif update.message.text.startswith("/test"):
                message = "200 OK!"
        else:
            # message = "Not a command!"
            pass
        if message:
            try:
                update.message.reply_text(
                    message,
                    parse_mode=telegram.ParseMode.MARKDOWN,
                    reply_markup=telegram.ReplyKeyboardRemove(),
                )
            except Exception as e:
                update.message.reply_text(str(e))


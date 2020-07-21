from os import stat
import telegram
from src.bulletin import Bulletin
import subprocess
import os
import shlex
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from src.util import build_menu, ocr_dict, pdf_dict, dash_dict
from src.ocr_functions import ocr1, ocr2, pdf, dashboard
import json


def entry(bot, update):
    try:
        # res = bot.send_message(chat_id="-1001429652488", text=update.to_json())
        # print(json.dumps(update.to_dict(), indent=2))
        pass
    except Exception as e:
        print(e)
        # bot.send_message(chat_id="-1001429652488", text=str(e))
        pass

    if update.callback_query:
        if update.callback_query.message.reply_to_message.photo:
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
        elif update.callback_query.message.reply_to_message.entities[0].type == 'url':
            state_name = update.callback_query.data
            url = update.callback_query.message.reply_to_message.text
            page_num = 2

            try:
                pdf(
                    bot, update.callback_query.message.chat.id, state_name, url, page_num
                )
            except Exception as e:
                bot.send_message(
                    chat_id=update.callback_query.message.chat.id,
                    text="PDF extraction failed",
                )
                print(e)
            
        elif update.callback_query.message.reply_to_message.text == '/dashboard':
            state_name = update.callback_query.data
            try:
                dashboard(
                    bot, update.callback_query.message.chat.id, state_name
                )
            except Exception as e:
                bot.send_message(
                    chat_id=update.callback_query.message.chat.id,
                    text="Dash fetch failed",
                )
                print(e)
            
            return
        
    if update.message:
        # Reply to the message
        if update.message.photo:
            button_list = []
            for key in ocr_dict:
                button_list.append(
                    InlineKeyboardButton(ocr_dict[key], callback_data=ocr_dict[key])
                )
            reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=3))
            bot.send_message(
                chat_id=update.message.chat.id,
                text="Which state bulletin is this?",
                reply_to_message_id=update.message.message_id,
                reply_markup=reply_markup,
            )
            return
        
        try:
            if update.message.entities[0].type == 'url':
                button_list = []
                for key in pdf_dict:
                    button_list.append(
                        InlineKeyboardButton(pdf_dict[key], callback_data=pdf_dict[key])
                    )
                reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=3))
                bot.send_message(
                    chat_id=update.message.chat.id,
                    text="Which state's PDF bulletin is this?",
                    reply_to_message_id=update.message.message_id,
                    reply_markup=reply_markup,
                )
                return
        except IndexError:
            pass

        if update.message.text.startswith("/dashboard"):
            bot.send_chat_action(
                chat_id=update.message.chat.id, action=telegram.ChatAction.TYPING
            )
            button_list = []
            for key in dash_dict:
                button_list.append(
                    InlineKeyboardButton(dash_dict[key], callback_data=dash_dict[key])
                )
            reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=3))
            bot.send_message(
                chat_id=update.message.chat.id,
                text="Which state's dashboard do you want to fetch?",
                reply_to_message_id=update.message.message_id,
                reply_markup=reply_markup,
            )
            return


        if update.message.text.startswith("/test"):
            update.message.reply_text(
                "200 OK!",
                parse_mode=telegram.ParseMode.MARKDOWN
                )
            return

        if update.message.text.startswith("/pdf"):
            update.message.reply_text(
                str('''Reply to a URL with \n`/pdf "Haryana" 3`'''),
                parse_mode=telegram.ParseMode.MARKDOWN
                )
            return            

        if update.message.text.startswith("/help") or update.message.text.startswith("/start"):
            help_text =f'''
            \n*OCR*
            - Send the bulletin image to do OCR
            - Errors and the results would be returned
            - If there are errors, copy the extracted text and make corrections.
            - Send it back to the text
            - Reply to the message with `/ocr2 "Madhya Pradesh"`
            \n*PDF*
            - Send the URL of the pdf bulletin
            - Choose the state. Default page number is 2.
            - For using different page number, use the command like below
            - `/pdf "Punjab" 3`
            \n*DASHBOARD*
            - `/dashboard`
            - Choose the state'''
            update.message.reply_text(
                str(help_text),
                parse_mode=telegram.ParseMode.MARKDOWN
                )
            return

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
                bot.send_chat_action(
                chat_id=update.message.chat.id, action=telegram.ChatAction.TYPING
                )
                text_prev = update.message.text
                text_replaced = text_prev.replace("“", '"').replace("”", '"')
                text = shlex.split(text_replaced)
                url = update.message.reply_to_message.text
                try:
                    pdf(
                        bot, update.message.chat.id, text[1], url, text[2]
                    )
                except Exception as e:
                    update.message.reply_text(
                        str('''Reply to the pdf URL with\n`/pdf <state name> <page number>`'''),
                        parse_mode=telegram.ParseMode.MARKDOWN)
                    print(e)
                    pass

                return

            elif update.message.text.startswith("/test"):
                message = "200 OK!"
                return
                
        # if message:
        #     try:
        #         update.message.reply_text(
        #             message,
        #             parse_mode=telegram.ParseMode.MARKDOWN,
        #             reply_markup=telegram.ReplyKeyboardRemove(),
        #         )
        #     except Exception as e:
        #         update.message.reply_text(str(e))


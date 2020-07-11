import telegram
from src.bulletin import Bulletin
import subprocess
import os
import shlex


def entry(bot, update):
    # print(update)
    message = None
    path = os.path.abspath("")
    path_ocr = path + "/webScraper/automation/ocr"
    path_automation = path + "/webScraper/automation"
    ocr_log_file = open("/tmp/ocr.log", "w+")
    try:
        res = bot.send_message(chat_id="-1001429652488", text=update.to_json())
        print(res)
    except Exception as e:
        print(e)
        bot.send_message(chat_id="-1001429652488", text=str(e))
        pass
    if update.message:
        # Reply to the message
        if not update.message.text:
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
                file_id = photo.file_id
                newFile = bot.get_file(file_id)
                newFile.download("/tmp/file.jpg")
                bot.send_chat_action(
                    chat_id=update.message.chat.id,
                    action=telegram.ChatAction.UPLOAD_PHOTO,
                )
                # ./ocr.sh /tmp/file.jpg Bihar Araria True
                subprocess.call(
                    ["bash", "ocr.sh", "/tmp/file.jpg", text[1], text[2], text[3]],
                    cwd=path_ocr,
                    stdout=ocr_log_file,
                    stderr=ocr_log_file,
                )
                bot.send_photo(
                    chat_id=update.message.chat.id,
                    photo=open(path_ocr + "/image.png", "rb"),
                )
                # reply_markup = telegram.ReplyKeyboardMarkup([["/ocr2 " + text[1]]])

                with open(path_ocr + "/output.txt") as f:
                    bot.send_message(
                        chat_id=update.message.chat.id,
                        text=f.read(),
                        # reply_markup=reply_markup,
                    )
                os.remove("/tmp/file.jpg")
                os.remove(path_ocr + "/output.txt")
                os.remove(path_ocr + "/image.png")
            elif update.message.text.startswith("/ocr2"):
                if len(text) < 2:
                    return
                output1 = update.message.reply_to_message.text
                state_name = text[1]
                print("Statename" + state_name)
                print(output1)
                with open(path_ocr + "/output.txt", "w+") as f:
                    f.write(output1)
                # ./ocr.sh ../../../b2.jpg Rajasthan AJMER False ocr,table
                subprocess.call(
                    ["bash", "ocr.sh", "", state_name, "", "", "ocr,table"],
                    cwd=path_ocr,
                    stdout=ocr_log_file,
                    stderr=ocr_log_file,
                )
                try:
                    with open(path_automation + "/output2.txt") as f:
                        output2 = f.read()
                        print(output2)
                        bot.send_message(chat_id=update.message.chat.id, text=output2)
                    os.remove(path_automation + "/output2.txt")
                except:
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
    ocr_log_file.close()
    with open("/tmp/ocr.log") as f:
        log_output = f.read()
        try:
            bot.send_message(chat_id="-1001429652488", text=log_output)
        except Exception as e:
            bot.send_message(chat_id="-1001429652488", text=str(e))

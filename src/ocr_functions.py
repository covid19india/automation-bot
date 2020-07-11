import subprocess
import telegram
import os

path = os.path.abspath("")
path_ocr = path + "/webScraper/automation/ocr"
path_automation = path + "/webScraper/automation"


def send_log_to_user(bot, chat_id):
    with open("/tmp/ocr.log") as f:
        log_output = f.read()
        try:
            bot.send_message(chat_id=chat_id, text=log_output)
        except Exception as e:
            bot.send_message(chat_id=chat_id, text=str(e))
    pass


def ocr1(bot, chat_id, photo, state_name, dist_name, is_translation_req=False):
    ocr_log_file = open("/tmp/ocr.log", "w+")
    file_id = photo.file_id
    newFile = bot.get_file(file_id)
    newFile.download("/tmp/file.jpg")
    bot.send_chat_action(
        chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO,
    )
    # ./ocr.sh /tmp/file.jpg Bihar Araria True
    subprocess.call(
        [
            "bash",
            "ocr.sh",
            "/tmp/file.jpg",
            state_name,
            dist_name,
            str(is_translation_req),
        ],
        cwd=path_ocr,
        stdout=ocr_log_file,
        stderr=ocr_log_file,
    )
    try:
        bot.send_photo(
            chat_id=chat_id, photo=open(path_ocr + "/image.png", "rb"),
        )
    except:
        pass

    try:
        with open(path_ocr + "/output.txt") as f:
            bot.send_message(
                chat_id=chat_id,
                text=f.read(),
                # reply_markup=reply_markup,
            )
        os.remove(path_ocr + "/output.txt")
        os.remove(path_ocr + "/image.png")
    except:
        print("File do not exist")
        bot.send_message(
            chat_id=chat_id,
            text="Picked the wrong state? :/",
            # reply_markup=reply_markup,
        )
    ocr_log_file.close()
    send_log_to_user(bot, chat_id)
    os.remove("/tmp/file.jpg")


def ocr2(bot, chat_id, text, state_name):
    ocr_log_file = open("/tmp/ocr.log", "w+")
    output1 = text
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
            bot.send_message(chat_id=chat_id, text=output2)
        os.remove(path_automation + "/output2.txt")
    except:
        pass
    ocr_log_file.close()
    send_log_to_user(bot, chat_id)
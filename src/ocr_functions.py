import subprocess
import telegram
import os
import logging

path = os.path.abspath("")
path_ocr = path + "/webScraper/automation/ocr"
path_automation = path + "/webScraper/automation"


def send_log_to_user(bot, chat_id, logname):
    with open(logname) as f:
        log_output = f.read()
        if len(log_output) > 4095:
            bot.send_document(chat_id=chat_id, document=open(logname, "rb"))
        else:
            bot.send_message(chat_id=chat_id, text=log_output)


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
            content = f.read()
            if len(content) > 4095:
                bot.send_document(chat_id=chat_id, document=open("/tmp/ocr.log", "rb"))
            else:
                bot.send_message(
                    chat_id=chat_id,
                    text=content,
                    # reply_markup=reply_markup,
                )
        os.remove(path_ocr + "/output.txt")
        os.remove(path_ocr + "/image.png")
    except:
        logging.info("File do not exist")
        bot.send_message(
            chat_id=chat_id,
            text="Picked the wrong state? :/",
            # reply_markup=reply_markup,
        )
    ocr_log_file.close()
    send_log_to_user(bot, chat_id, logname="/tmp/ocr.log")
    os.remove("/tmp/file.jpg")


def ocr2(bot, chat_id, text, state_name):
    with open("/tmp/ocr.log", "w+") as ocr_log_file:
        output1 = text
        try:
            with open(path_ocr + "/output.txt", "w+") as f:
                f.write(output1)
        except Exception as e:
            logging.error(e)
            pass
        # ./ocr.sh ../../../b2.jpg Rajasthan AJMER False ocr,table
        try:
            subprocess.run(
                ["bash", "ocr.sh", "", state_name, "", "", "ocr,table"],
                cwd=path_ocr,
                stdout=ocr_log_file,
                stderr=ocr_log_file,
                timeout=60
            )
        except subprocess.TimeoutExpired:
            e = 'Request timed out'
            logging.error(e)
            bot.send_message(chat_id=chat_id, text=e)
            return
        try:
            with open(path_automation + "/output2.txt") as f:
                output2 = f.read()
                if len(output2) > 4095:
                    bot.send_document(
                        chat_id=chat_id,
                        document=open(path_automation + "/output2.txt", "rb"),
                    )
                else:
                    bot.send_message(chat_id=chat_id, text=output2)
            os.remove(path_automation + "/output2.txt")
        except:
            pass
        send_log_to_user(bot, chat_id, logname="/tmp/ocr.log")


def pdf(bot, chat_id, url, state_name):
    """
    Run the pdf automation when pdf links are passed
    """
    pdf_log_file = "/tmp/pdf_output.txt"
    pdf_err_file = "/tmp/pdf_err.txt"
    # python3 automation.py Haryana full pdf=url
    logging.info(f"pdf={url}")
    with open(pdf_log_file,'w') as log_file:
        with open(pdf_err_file,'w') as err_file:
            p = subprocess.Popen(
                ["python3", "automation.py", state_name, "full", f"pdf={url}"],
                cwd=path_automation,
                stdout=log_file,
                stderr=err_file,
            )
            p.communicate()

    with open(pdf_log_file,'r') as log_file:
        with open(pdf_err_file,'r') as err_file:
            out = log_file.read()
            err = err_file.read()
            try:
                # Send the errata
                if (err is not None):
                    if len(err) > 4095:
                        bot.send_document(
                            chat_id=chat_id,
                            document=err_file
                        )
                    else:
                        bot.send_message(chat_id=chat_id, text=str(err))
                os.remove(pdf_err_file)
            except Exception as e:
                logging.error(e)
                pass
            
            try:
                # Send the results
                if (out is not None):
                    print(out)
                    if(len(out)>4095):
                        bot.send_document(
                            chat_id=chat_id,
                            document=log_file
                        )
                    else:
                        bot.send_message(chat_id=chat_id, text=str(out))
                    os.remove(pdf_log_file)
            except Exception as e:
                logging.error(e)
                pass

    # send_log_to_user(bot, chat_id, logname=pdf_log_file)

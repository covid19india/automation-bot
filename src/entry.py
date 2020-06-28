from src.bulletin import Bulletin

def entry(bot, update):
    print(update)
    if update.message: 
        # Reply to the message
        if update.message.text.find("Bihar") > -1:
            b = Bulletin(state="Bihar",type="individual")
            message = b.get_detailed()
        else:
            message = "Not there yet!"
        update.message.reply_text(message)

if __name__ == "__main__":
    entry()
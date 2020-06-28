def entry(bot, update):
    print(update)
    if update.message: 
        # Reply to the message
        update.message.reply_text(update.message.text)
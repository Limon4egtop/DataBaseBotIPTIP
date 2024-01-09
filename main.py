from funk import *

@bot.message_handler(content_types=['text'])
def getTextMessages(message):
    if message.text.lower() == "/start":
        startPutUserData(message)

bot.polling(none_stop=True, interval=0)
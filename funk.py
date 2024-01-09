import telebot
import datetime

from SQLWork import *

bot = telebot.TeleBot("BOT TOKEN")

def startPutUserData(message):
    putIdAndUsername(message.from_user.id, message.from_user.username)
    updateFirstAndLastName(message.from_user.id, message.from_user.first_name, message.from_user.last_name)
    bot.send_message(message.chat.id, text=f"Привет\nЯ бот-помощник, но пока я только собираю данные о тебе и ничего не даю взамен\nКое-что о тебе я уже знаю. Проверь пожалуйста актуальность своих данных:\nИмя: <code>{message.from_user.first_name}</code>\nФамилия: <code>{message.from_user.last_name}</code>\n",
                     parse_mode="HTML", reply_markup = generateRefreshNameDataKeyboard(True))

def generateRefreshNameDataKeyboard(isKnowActive):
    markupInline = telebot.types.InlineKeyboardMarkup()
    markupInline.add(telebot.types.InlineKeyboardButton(text="Исправить имя",
                                                        callback_data="refreshNameData"))
    markupInline.add(telebot.types.InlineKeyboardButton(text="Да, это я",
                                                        callback_data="refreshPhoneData"))
    if isKnowActive is True:
        markupInline.add(telebot.types.InlineKeyboardButton(text="Откуда ты знаешь мое имя?",
                                                            callback_data="whyYouKnowMyName"))
    return markupInline

@bot.callback_query_handler(func=lambda call: call.data == "refreshNameData")
def refreshNameData(call):
    msg = bot.send_message(call.message.chat.id, text="Введите ваше имя и фамилию через пробел")
    @bot.message_handler(content_types=['text'])
    def putFullName(message):
        if checkCorrectName(message.text) is True:
            firstName, lastName = formatName(message.text)
            updateFirstAndLastName(message.from_user.id, firstName, lastName)
            bot.send_message(call.message.chat.id,
                             f'Ваше имя: <code>{firstName}</code>\nФамилия: <code>{lastName}</code>',
                             parse_mode="HTML", reply_markup = generateRefreshPhoneKeyboard())
        else:
            bot.send_message(call.message.chat.id, "Это не похоже на имя")
            refreshNameData(call)
    bot.register_next_step_handler(msg, putFullName)

def formatName(fullName):
    return fullName.split()[0].title(), fullName.split()[1].title()

def checkCorrectName(fullName):
    if len(fullName.split()) == 2:
        return True
    else:
        return False

def generateRefreshPhoneKeyboard():
    markupInline = telebot.types.InlineKeyboardMarkup()
    markupInline.add(telebot.types.InlineKeyboardButton(text="Продолжить",
                                                        callback_data="refreshPhoneData"))
    markupInline.add(telebot.types.InlineKeyboardButton(text="Исправить",
                                                        callback_data="refreshNameData"))
    return markupInline

@bot.callback_query_handler(func=lambda call: call.data == "refreshPhoneData")
def refreshPhoneData(call):
    msgSendNumber = bot.send_message(call.message.chat.id, text="Отправьте свой номер телефона",
                           reply_markup=generateGetContactKeyboard())
    @bot.message_handler(func=lambda message: True, content_types=['contact'])
    def putPhoneNumber(message):
        if message.contact is not None:
            updatePhoneNumber(message.from_user.id, message.contact.phone_number)
            bot.send_message(call.message.chat.id,
                             f'Ваш номер: <code>+{message.contact.phone_number}</code>',
                             parse_mode="HTML")
            refreshGroupNumber(message)
        else:
            bot.send_message(call.message.chat.id, "Это не номер телефона")
            refreshPhoneData(call)
    bot.register_next_step_handler(msgSendNumber, putPhoneNumber)

def generateGetContactKeyboard():
    markup_replay = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup_replay.add(telebot.types.KeyboardButton(text="Отправить номер", request_contact=True))
    return markup_replay

@bot.callback_query_handler(func=lambda call: call.data == "whyYouKnowMyName")
def sendMesageWhyYouKnowMyName(call):
    bot.send_message(call.message.chat.id, "Это имя указано в профиле",
                     reply_markup=generateRefreshNameDataKeyboard(False))

def refreshGroupNumber(message):
    msgGroup = bot.send_message(message.chat.id,
                     "Отправь номер своей группы в формате\n<code>**БО-**-**</code>\nПримеры:\n<pre language=\"c++\">ЭФБО-03-23\nЭФБО-03-22\nЭЛБО-01-23</pre>",
                     parse_mode="HTML")
    @bot.message_handler(content_types=['text'])
    def putGroupNumber(message):
        if checkCorrectGroupFormat(message.text):
            groupName, groupNumber, groupYear = formatGroupeName(message.text)
            updateGroupeNumber(message.from_user.id, groupName, groupNumber, groupYear)
            bot.send_message(message.from_user.id, f"Номер группы: <code>{groupName}-{groupNumber}-{groupYear}</code>",
                             parse_mode="HTML")
            sendFullDataAboutUser(message)
        else:
            bot.send_message(message.from_user.id, "Номер группы не соответствует требованиям")
            refreshGroupNumber(message)
    bot.register_next_step_handler(msgGroup, putGroupNumber)

def checkCorrectGroupFormat(fullGroupNumber):
    if fullGroupNumber.count("-") == 2 and len(fullGroupNumber.split("-")) == 3:
        groupeName, groupNumber, groupYear = formatGroupeName(fullGroupNumber)
        if checkCorrectGroupName(groupeName) and checkCorrectGroupNumber(groupNumber) \
                and checkCorrectGroupYear(groupYear):
            return True
        else:
            return False
    else:
        return False

def formatGroupeName(fullGroupNumber):
    return (fullGroupNumber.split("-")[0].upper(),
            int(fullGroupNumber.split("-")[1]),
            int(fullGroupNumber.split("-")[2]))

def checkCorrectGroupName(name):
    if name[2:] == "БО":
        return True
    else:
        return False

def checkCorrectGroupNumber(number):
    if number <= 10:
        return True
    else:
        return False

def checkCorrectGroupYear(year):
    nowYear = datetime.date.today().year % 100
    if nowYear - year <= 7:
        return True
    else:
        return False

def sendFullDataAboutUser(message):
    userData = getAllDataAboutUser(message.from_user.id)
    bot.send_message(message.from_user.id, generateTextAboutUser(userData), parse_mode="HTML")

def generateTextAboutUser(userData):
    sendText = "Все что я смог собрать\n<pre language=\"c++\">"
    for key, value in userData.items():
        sendText += f"{str(key)}: {str(value)}\n"
    sendText += "</pre>"
    return sendText

import telebot
from telebot import types

with open("./dt.data", "r") as fl:
    file = fl.read().split("\n")
    token   = file[0]
    root    = file[1].split(' ')
    admin   = file[2].split(' ')
    blocked = file[4].split(' ')
    answer  = file[3]
    #admin = root
    print(root, admin, blocked)

def sniffer(message):
    print('id пользователя', message.chat.id)
    print('имя пользователя', message.from_user.first_name)
    print('фамилия пользователя', message.from_user.last_name)
    print('никнейм пользователя', message.from_user.username)
    print('сообщение пользователя', message.text, "\n")
    print("фото пользователя", message.photo)

bot=telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "чё надо?")
    sniffer(message)

@bot.message_handler(commands=['help'])
def help(message):
    res = ""
    if str(message.chat.id) == root:
        res += ("/shutdown     -- shutdown main script" + "\n"
                "" + "\n"
                "" 
                ""
                ""
                "")
    if str(message.chat.id) in admin:
        res += ("/rights userid role    -- gives the role to the user"+ "\n"
                "/userinfo  userid      -- gives info about this user"+ "\n"
                "/BE                    -- Ban Everyone on 5 minutes  "+ "\n"
                "/userid nickname       -- show his id"+ "\n"
                "/adminlist"+ "\n"
                "/send userid"+ "\n"
                "/editbot                -- edit "+ "\n"
                "/rights  "+ "\n"
                ""
                ""
                ""
                "")
    if str(message.chat.id) not in blocked:
        res += ("/help   -- this text" + "\n"
                "/bl     -- funny" + "\n"
                "/whoami -- shows u ur rights " + "\n"
                "/myid   -- shows u ur id" + "\n"
                "" + "\n"
                "" + "\n"
                "" + "\n"
                "")
    bot.send_message(message.chat.id, res)

@bot.message_handler(commands=['rights'])
def rights(message):
    if str(message.chat.id) in admin:
        with open('./dt.data', 'w+') as fl:
            data = fl.read().split("\n")
            print(data)
    if str(message.chat.id) not in blocked:
        bot.send_message(message.chat.id, "недостаточно прав")


@bot.message_handler(commands=['button'])
def button_message(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Pizda")
    markup.add(item1)
    bot.send_message(message.chat.id,'hui',reply_markup=markup)

@bot.message_handler(commands=['editbot'])
def editbot(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Pizda")
    markup.add(item1)
    bot.send_message(message.chat.id,'hui',reply_markup=markup)

@bot.message_handler(commands=['send'])
def send(message):
    if str(message.chat.id) in admin:
        try:
            bot.send_message(int(message.text[6:][:10]), message.text[21:])
            bot.send_message(message.chat.id, "готово")
        except Exception:
            bot.send_message(message.chat.id, "wrong id")
            print(message.text[6:][:10], "    ", message.text[16:], sep="\n")
    elif str(message.chat.id) not in blocked:
        bot.send_message(message.chat.id, "not enough rights")

@bot.message_handler(commands=['whoami'])
def whoami(message):
    if str(message.chat.id) == root:
        bot.send_message(message.chat.id, "u r root")
    elif str(message.chat.id) in admin:
        bot.send_message(message.chat.id, "u r admin")
    elif str(message.chat.id) not in blocked:
        bot.send_message(message.chat.id, "u r user")
    else:
        bot.send_message(message.chat.id, "u r nothing")

@bot.message_handler(commands=['myid'])
def myid(message):
    if message.chat.id not in blocked:
        bot.send_message(message.chat.id, message.chat.id)

@bot.message_handler(commands=['bl'])
def bl(message):
    if str(message.chat.id) not in blocked:
        bot.send_message(message.chat.id, "bl")

@bot.message_handler(content_types=['text', 'sticker', 'photo', "audio", "document"])
def message_reply(message):
    res = ""
    sniffer(message)
    if str(message.chat.id) not in blocked:
        if message.text=="hui":
            bot.send_message(message.chat.id,"pizda")
        try:
            markup = types.InlineKeyboardMarkup(row_width=2)
            button_foo = types.InlineKeyboardButton('ban', callback_data='ban')
            button_bar = types.InlineKeyboardButton('post', callback_data='post')
            markup.add(button_bar, button_foo)
            if message.text != None:
                res += message.text
            if message.photo != None:
                res += message.caption
            res += "\nid: " + str(message.chat.id)
            res += "\nnickname: " + str(message.chat.username)

            for i in admin:
                if message.photo != None:
                    fileID = message.photo[-1].file_id
                    file_info = bot.get_file(fileID)
                    downloaded_file = bot.download_file(file_info.file_path)
                    with open("image.jpg", 'wb') as new_file:
                        new_file.write(downloaded_file)
                    with open('image.jpg', 'rb') as photo:

                        bot.send_photo(message.chat.id, photo, caption=res, parse_mode="HTML", reply_markup=markup)
                else: bot.send_message(i, res, reply_markup=markup)


        except ValueError:
            bot.send_message(message.chat.id, "шо ты сделал блять?!")


        bot.send_message(message.chat.id, answer)
    else: print("this asshole trying to use me")

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == 'ban':
        idban = call.message.text.split("\n")[len(call.message.text.split("\n")) - 2][4:]
        if idban not in admin and idban not in blocked and idban not in root:
            blocked.append(idban)
            with open('./dt.data', 'a') as fl:
                pass #fl.write(' ' + idban)
            for i in admin:
                bot.send_message(i, "banned! but it`s still WIP")
            bot.send_message(idban, "ты забанен:)")
        elif idban in blocked:
            bot.send_message(call.from_user.id, "он уже забанен")
    if call.data == 'post':
        if call.message.photo == None:
            post = call.message.text.rsplit('\n', 2)[0]
            post += "\n" + "👤 "  + call.message.text.rsplit('\n', 2)[2][9:]
            bot.send_message("@test_for_coffeebot", post)
        else:
            post = call.message.caption.rsplit('\n', 2)[0]
            post += "\n" + "👤 " + call.message.caption.rsplit('\n', 2)[2][9:]
            with open('image.jpg', 'rb') as photo:
                bot.send_photo("@test_for_coffeebot", photo, caption=post)
        for i in admin:
            bot.send_message(i, "published! but it`s still WIP")
bot.infinity_polling()
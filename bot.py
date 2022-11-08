import telebot
from telebot import types
from database import Database

TOKEN = ''
db = Database('db.db')
bot = telebot.TeleBot(TOKEN)

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('👥 Söhbət Axtarmaq')
    markup.add(item1)
    return markup

def stop_dialog():
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('🗣 Profilimi demək')
    item2 = types.KeyboardButton('/stop')
    markup.add(item1, item2)
    return markup

def stop_search():
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('❌ Axtarmağı dayandırmaq')
    markup.add(item1)
    return markup

@bot.message_handler(commands = ['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('Mən Oğlanam ')
    item2 = types.KeyboardButton('Mən Qızam ')
    markup.add(item1, item2)

    bot.send_message(message.chat.id, 'Salam, {0.first_name}! Anonim söhbətə xoş gəlmisiniz! Zəhmət olmasa cinsinizi daxil edin! '.format(message.from_user), reply_markup = markup)

@bot.message_handler(commands = ['menu'])
def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('👥 Söhbət Axtarmaq')
    markup.add(item1)

    bot.send_message(message.chat.id, '📝 Menyu'.format(message.from_user), reply_markup = markup)

@bot.message_handler(commands = ['stop'])
def stop(message):
    chat_info = db.get_active_chat(message.chat.id)
    if chat_info != False:
        db.delete_chat(chat_info[0])
        markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
        item1 = types.KeyboardButton('✏️ Növbəti Dialoq')
        item2 = types.KeyboardButton('/menu')
        markup.add(item1, item2)

        bot.send_message(chat_info[1], '❌ Zəng edən söhbəti tərk etdi', reply_markup = markup)
        bot.send_message(message.chat.id, '❌ Siz Söhbəti tərk etdiz', reply_markup = markup)
    else:
        bot.send_message(message.chat.id, '❌ Siz söhbətə başlamamısınız!', reply_markup = markup)


@bot.message_handler(content_types = ['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == '👥 Söhbət Axtarmaq' or message.text == '✏️ Növbəti dialoq':
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = types.KeyboardButton('🔎 Oğlan')
            item2 = types.KeyboardButton('🔎 Qız')
            item3 = types.KeyboardButton('👩‍👨 Random')
            markup.add(item1, item2, item3)

            bot.send_message(message.chat.id, 'Kimi Axtarmaq?', reply_markup = markup)

            
        elif message.text == '❌ Axtarmağı dayandırmaq':
            db.delete_queue(message.chat.id)
            bot.send_message(message.chat.id, '❌ Axtarmaq dayandırıldı, yazın /menu', reply_markup = main_menu())

        
        elif message.text == '🔎 Oğlan':
            user_info = db.get_gender_chat('male')
            chat_two = user_info[0]
            if db.create_chat(message.chat.id, chat_two) == False:
                db.add_queue(message.chat.id, db.get_gender(message.chat.id))
                bot.send_message(message.chat.id, '👻 Söhbət Axtarmaq', reply_markup = stop_search())
            else:
                mess = 'Söhbət Tapıldı! Dialoqu dayandırmaq üçün yazın /stop'

                bot.send_message(message.chat.id, mess, reply_markup = stop_dialog())
                bot.send_message(chat_two, mess, reply_markup = stop_dialog())
        
        
        elif message.text == '🔎 Qız':
            user_info = db.get_gender_chat('female')
            chat_two = user_info[0]
            if db.create_chat(message.chat.id, chat_two) == False:
                db.add_queue(message.chat.id, db.get_gender(message.chat.id))
                bot.send_message(message.chat.id, '👻 Söhbət Axtarmaq', reply_markup = stop_search())
            else:
                mess = 'Söhbət Tapıldı! Dialoqu dayandırmaq üçün yazın /stop'

                bot.send_message(message.chat.id, mess, reply_markup = stop_dialog())
                bot.send_message(chat_two, mess, reply_markup = stop_dialog())
        

        elif message.text == '👩‍👨 Random':
            user_info = db.get_chat()
            chat_two = user_info[0]

            if db.create_chat(message.chat.id, chat_two) == False:
                db.add_queue(message.chat.id, db.get_gender(message.chat.id))
                bot.send_message(message.chat.id, '👻 Söhbət Axtarmaq', reply_markup = stop_search())
            else:
                mess = 'Söhbət Tapıldı! Dialoqu dayandırmaq üçün yazın /stop'

                bot.send_message(message.chat.id, mess, reply_markup = stop_dialog())
                bot.send_message(chat_two, mess, reply_markup = stop_dialog())
        
        elif message.text == '🗣 Profilimi demək':
            chat_info = db.get_active_chat(message.chat.id)
            if chat_info != False:
                if message.from_user.username:
                    bot.send_message(chat_info[1], '@' + message.from_user.username)
                    bot.send_message(message.chat.id, '🗣 Siz profilinizi dediz')
                else:
                    bot.send_message(message.chat.id, '❌ İstifadəçi adı hesabınızda qeyd edilməyib')
            else:
                bot.send_message(message.chat.id, '❌ Söhbətə başlamamısınız!')

        

        elif message.text == 'Mən Oğlanam':
            if db.set_gender(message.chat.id, 'male'):
                bot.send_message(message.chat.id, '✅ Cinsiyyətiniz uğurla əlavə edildi!', reply_markup = main_menu())
            else:
                bot.send_message(message.chat.id, '❌  Siz artıq cinsinizi daxil etmisiniz.')
        
        elif message.text == 'Mən Qızam':
            if db.set_gender(message.chat.id, 'female'):
                bot.send_message(message.chat.id, '✅ Cinsiyyətiniz uğurla əlavə edildi!', reply_markup = main_menu())
            else:
                bot.send_message(message.chat.id, '❌ Siz artıq cinsinizi daxil etmisiniz.')
        
        else:
            if db.get_active_chat(message.chat.id) != False:
                chat_info = db.get_active_chat(message.chat.id)
                bot.send_message(chat_info[1], message.text)
            else:
                bot.send_message(message.chat.id, '❌ Söhbətə başlamamısınız')


@bot.message_handler(content_types='stickers')
def bot_stickers(message):
    if message.chat.type == 'private':
        chat_info = db.get_active_chat(message.chat.id)
        if chat_info != False:
            bot.send_sticker(chat_info[1], message.sticker.file_id)
        else:
            bot.send_message(message.chat.id, '❌ Söhbətə başlamamısınız')

@bot.message_handler(content_types='voice')
def bot_voice(message):
    if message.chat.type == 'private':
        chat_info = db.get_active_chat(message.chat.id)
        if chat_info != False:
            bot.send_voice(chat_info[1], message.voice.file_id)
        else:
            bot.send_message(message.chat.id, '❌Söhbətə başlamamısınız')



bot.polling(none_stop = True)
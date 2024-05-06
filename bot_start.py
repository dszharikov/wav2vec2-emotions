import telebot
from model import get_emotion
import os
import gc

gc.collect()


API_KEY = os.getenv('VOICE_BOT_API_KEY')

bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['start'])
def hello(message):
    bot.send_message(message.chat.id, 'Здравствуйте, отправьте мне голосовое сообщение, а я определю Вашу эмоцию.')


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Я умею определять Ваши эмоции по голосовым сообщениям.\
    Пожалуйста, не отправляйте мне ничего, кроме голосовых сообщений, иначе я не скажу, какую эмоцию Вы испытываете сейчас.')
    

@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    try:
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open('voice.wav', 'wb') as voice:
            voice.write(downloaded_file)
        pred = get_emotion('voice.wav', 16000)
        bot.send_message(message.chat.id, f'Ваша эмоция: {pred}.')
    except:
        bot.send_message(message.chat.id, 'Я Вас не понял, повторите, пожалуйста.')
    

@bot.message_handler(content_types=['audio', 'photo', 'video', 'document',
    'text', 'location', 'contact', 'sticker'])
def message_proccessing(message):
    bot.send_message(message.chat.id, 'Я понимаю только голосовые сообщения, поговорите со мной.')


print('Polling...')
bot.infinity_polling()

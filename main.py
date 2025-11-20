import telebot
import requests

bot = telebot.TeleBot('ТОКЕН ЗДЕСЬ')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     "Привет! Я бот для поиска музыки. Просто отправь мне название песни или исполнителя, и я постараюсь найти треки для тебя.")


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id,
                     "Этот бот предназначен для поиска музыки. Просто отправьте мне название песни или исполнителя, и я постараюсь найти треки для вас.")


@bot.message_handler(commands=['great'])
def thumbs_up(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, '??')


@bot.message_handler(commands=['present'])
def flower(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, '??')


@bot.message_handler(commands=['cool'])
def cool(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, '??')


@bot.message_handler(func=lambda message: message.text[0] != '/' if message.text else False)
def search_music(message):
    query = message.text
    chat_id = message.chat.id

    api_url = f"https://itunes.apple.com/search?term={query.replace(' ', '+')}&media=music&entity=musicTrack&limit=5"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        tracks = data.get('results', [])

        if tracks:
            for track in tracks:
                track_name = track.get('trackName')
                artist_name = track.get('artistName')
                track_preview_url = track.get('previewUrl')

                if track_name and artist_name and track_preview_url:
                    bot.send_message(chat_id, f"{track_name} - {artist_name}")
                    bot.send_audio(chat_id, track_preview_url)
        else:
            bot.send_message(chat_id, "По вашему запросу ничего не найдено.")
    else:
        bot.send_message(chat_id, "Произошла ошибка при поиске музыки.")


bot.polling(none_stop=True)

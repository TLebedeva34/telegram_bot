import telebot
from config import keys, TOKEN
from extensions import APIException, Converter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start_help_start(message: telebot.types.Message):
    text = 'Привет! Чтобы ознакомиться со списком доступных валют, введите команду /values.\
\n Чтобы начать работу введите мне команду в формате: \n <имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Должно быть 3 параметра.')
    
        quote, base, amount = values
        total_base = Converter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обрабоотать команду.\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()

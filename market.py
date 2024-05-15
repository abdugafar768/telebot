import telebot
from currency_converter import CurrencyConverter
from telebot import types
bot = telebot.TeleBot('6933459637:AAGkXoOiW5Rq3B79K5_1S1LNxv62PqQgPcw')
currency = CurrencyConverter()
amount = 0

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,'Enter money amount')
    bot.register_next_step_handler(message,summa)

def summa(message):
    global amount
    try:
        amount = int(message.text.strip())

    except ValueError:
        bot.send_message(message.chat.id,'please write a number')
        bot.register_next_step_handler(message,summa)
        return
    
    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
        btn2 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
        btn3 = types.InlineKeyboardButton('USD/GBP', callback_data='usd/gbp')
        markup.add(btn1,btn2,btn3)
        bot.send_message(message.chat.id,'Select exchange rate',reply_markup=markup)

    else:
        bot.send_message(message.chat.id,'Enter a number greater than 0')
        bot.register_next_step_handler(message,summa)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != 'else':
        values = call.data.upper().split('/')
        res = currency.convert(amount, values[0],values[1])
        bot.send_message(call.message.chat.id, round(res,2))
        bot.register_next_step_handler(call.message,summa)

    else:
        bot.send_message(call.message.chat.id, "Please provide your custom currency pair.")
        bot.register_next_step_handler(call.message, my_currency)

def my_currency(message):
    try:
        values = message.text.upper().split('/')
        res = currency.convert(amount,values[0],values[1])
        bot.send_message(message.chat.id, round(res,2))
        bot.register_next_step_handler(message,summa)

    except Exception:
        bot.send_message(message.chat.id,'enter number')
        bot.register_next_step_handler(message,my_currency)



bot.polling(none_stop=True)

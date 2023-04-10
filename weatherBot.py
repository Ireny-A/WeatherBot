# This bot shows weather in any city

import json
import telebot
import requests
import math

token = '5509655822:AAFsCmgWiSmVe442hF1GiEAJ1Z16lQgVsU4'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def hello_Message(message):
    mess = f'Hi, {message.from_user.first_name}! I can tell you about the weather in any city. ' \
           f'Please, enter the name of the city.'
    bot.send_message(message.chat.id, mess)


@bot.message_handler(content_types='text')
def text(message):
    city_name = str(message.text.title())
    try:
        res = get_Weather(city_name)
        bot.send_message(message.chat.id, res)

    except requests.exceptions.RequestException:
        bot.send_message(message.chat.id, f'City "{city_name}" not found. Please enter a valid city name.')


def get_Weather(city_name):
    response = requests.get('https://api.openweathermap.org/data/2.5/weather?q=' + city_name+ '&appid=de67758d4936d6c1553e2b14a436e382&units=metric')
    response.raise_for_status()

    data = json.loads(response.text)
    rez = data.get('main')

    temp = math.ceil(rez.get('temp', 0))
    feel_like = math.ceil(rez.get('feels_like', 0))
    temp_min = math.ceil(rez.get('temp_min', 0))
    temp_max = math.ceil(rez.get('temp_max', 0))
    humidity = rez.get('humidity', 0)

    info = f'{city_name}\nThe air temperature now is : {temp}\nFeels like : {feel_like}\nMinimum air temperature : {temp_min}\n' \
          f'Maximum air temperature : {temp_max}\nHumidity : {humidity}'
    return info


bot.polling(none_stop=True)

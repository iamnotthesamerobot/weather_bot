#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  8 17:29:46 2019

"""
import os
from flask import Flask, request
import telebot
 
import requests
from bs4 import BeautifulSoup
import re
 
TOKEN = 'token'
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)
 
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)
    
@bot.message_handler(func=lambda message: True, regexp="Z")
def echo_message(message):
    bot.reply_to(message, message.text)
 
#@bot.message_handler(func=lambda message: True, content_types=['text'])

@bot.message_handler(func=lambda message: True, regexp="W")
def echo_message(message):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
      }

    page_w = requests.get("https://www.gismeteo.com/weather-amsterdam-1200/3-days/", headers=headers)
    soup_w = BeautifulSoup(page_w.content, 'html.parser')
 
    for i in range(0, 12):
        if i == 0:
            msg_0 = ('\n' + str(soup_w.select('a')[17].text))
            bot.send_message(message.chat.id, str(msg_0))
        if i == 4:
            msg_0 = ('\n' + str(soup_w.select('a')[18].text))
            bot.send_message(message.chat.id, str(msg_0))
        if i == 8:
            msg_0 = ('\n' + str(soup_w.select('a')[19].text))
            bot.send_message(message.chat.id, str(msg_0))
        day = soup_w.find_all(class_="time_of_day")[i].text
        tmpr = soup_w.find_all(class_="unit unit_temperature_c")[i].contents[0]
        cloudy = str(soup_w.find_all(class_="tooltip")[i])
        cloudy = re.sub(';|&', '$', cloudy, count=0).split(r'$')
        msg_1 = (str(day) + ' ' + str(tmpr) + ' ' + cloudy[4])  
        bot.send_message(message.chat.id, str(msg_1))
 
@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://HEROKU.herokuapp.com/' + TOKEN)
    return "!", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

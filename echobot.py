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
import time 

TOKEN = '709643552:AAHfwkI5IFT5i7QGjDDvdjW5nMVUolnKL4o'
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    page = requests.get("https://privatbank.ua")
    soup = BeautifulSoup(page.content, 'html.parser')
    extracted_data = soup.select("tbody tr td")
    bot.send_message(message.chat.id, 'Actual courses of exchange from The PRIVATBANK')
    eu = str(extracted_data[0].contents[0])
    eu_sell = str(extracted_data[2].contents[0]).strip()
    eu_buy = str(extracted_data[3].contents[0]).strip()
    euro = eu + ' ' + eu_sell + '/' + eu_buy
    bot.send_message(message.chat.id, str(euro))
    usd = str(extracted_data[4].contents[0])
    usd_sell = str(extracted_data[6].contents[0]).strip()
    usd_buy = str(extracted_data[7].contents[0]).strip()
    dollar = usd + ' ' + usd_sell + '/' + usd_buy
    bot.send_message(message.chat.id, str(dollar))
    rur = str(extracted_data[8].contents[0])
    rur_sell = str(extracted_data[10].contents[0]).strip()
    rur_buy = str(extracted_data[11].contents[0]).strip()
    rubl = rur + ' ' + rur_sell + '/' + rur_buy
    bot.send_message(message.chat.id, str(rubl))
    end_msg = str('The info is actual on ' + str(time.ctime()))
    bot.send_message(message.chat.id, end_msg)
    
@bot.message_handler(func=lambda message: True, regexp="Z")
def echo_message(message):
    bot.reply_to(message, message.text)


@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://botto8.herokuapp.com/' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

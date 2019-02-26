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

@bot.message_handler(func=lambda message: True, regexp="Z")
def echo_message(message):
    page = requests.get("https://privatbank.ua")
    soup = BeautifulSoup(page.content, 'html.parser')
    extracted_data = soup.select("tbody tr td")
    eu = str(extracted_data[0].contents[0])
    bot.reply_to(message, str(eu))
    bot.send_message(message.chat.id, str(eu))
    
@bot.message_handler(func=lambda message: True, content_types=['text'])
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

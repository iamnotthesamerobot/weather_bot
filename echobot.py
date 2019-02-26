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

TOKEN = '771254834:AAHwMQtxFeL4WUBTDNxWs4JvsTRA8ucIAHY'
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
      }

    page_w = requests.get("https://www.gismeteo.com/weather-dnipro-5077/", headers = headers)
    soup_w = BeautifulSoup(page_w.content, 'html.parser')
    filter_1 = soup_w.find(class_="tab tooltip").find("div")
    cur_date = filter_1.find(class_="date ").contents[0].strip()
    temp = filter_1.find_all(class_="unit unit_temperature_c")
    feelings = soup_w.select('a div span span')
    temp_now = feelings[0].contents[0].strip()
    temp_feel = feelings[2].contents[0].strip()
    filter_2 = soup_w.select('body section div div div')
    city = filter_2[0].contents[0]
    d_lenght = soup_w.find_all(class_="id_item title")[0].contents[0]
    sunrise = soup_w.find_all(class_="id_item")[1].contents[0]
    sunset = soup_w.find_all(class_="id_item")[2].contents[0]
    longer = soup_w.find_all(class_="txt")[0].contents[0].strip()
    f_moon = soup_w.find_all(class_="txt")[1].contents[0]
    moon_phase = soup_w.find_all(class_="id_item title")[1].contents[0].strip()
    road_cond_8 = soup_w.find_all(class_="w_roadcondition__description")[2].contents[0].strip()
    road_cond_20 = soup_w.find_all(class_="w_roadcondition__description")[6].contents[0].strip()
    moonrise = soup_w.find_all(class_="id_item")[4].contents[0]
    moonset = soup_w.find_all(class_="id_item")[5].contents[0]
    wind_km_h = soup_w.find_all(class_="unit unit_wind_km_h")[6].contents[0].strip()

    msg_1 = (str(city) + ' ' + str(cur_date))
    msg_2 = ('Actual ' + str(temp_now) + ' Feeling ' + str(temp_feel) + \
             '\nNight ' + str(temp[0].contents[0]) + ' Day ' + str(temp[1].contents[0]))
    msg_3 = ('Road condition by 8 A.M.: ' + str(road_cond_8) + \
             '\nRoad condition by 8 P.M.: ' + str(road_cond_20) + \
             '\nWind speed: ' + str(wind_km_h) + ' km/h')
    msg_4 = (str(sunrise) + ' ' + str(sunset) + '\n' + str(d_lenght) + '\n' + str(longer))
    msg_5 = ('Moon: ' + str(moonrise) + ' ' + str(moonset) + '\n' + str(f_moon) + '\n' + str(moon_phase))
          
    bot.send_message(message.chat.id, str(msg_1))
    bot.send_message(message.chat.id, str(msg_2))
    bot.send_message(message.chat.id, str(msg_3))
    bot.send_message(message.chat.id, str(msg_4))
    bot.send_message(message.chat.id, str(msg_5))
    
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

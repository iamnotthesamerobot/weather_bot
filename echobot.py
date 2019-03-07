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
 
TOKEN = '771254834:AAHwMQtxFeL4WUBTDNxWs4JvsTRA8ucIAHY'
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)
 
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)
    
@bot.message_handler(func=lambda message: True, regexp="Z")
def echo_message(message):
    bot.reply_to(message, message.text)
 
@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
      }

    page_w = requests.get("https://www.gismeteo.com/weather-dnipro-5077/3-days/", headers=headers)
    soup_w = BeautifulSoup(page_w.content, 'html.parser')

    print(soup_w.find_all('h1')[0].contents[0]) #weather in Dn


    def cloudy(i):
        aa = str(soup_w.find_all(class_="img")[i].find(class_="tooltip"))
        aa = re.sub(';|&', '#', aa, count=0).split(r'#')[4]
        return aa


    for i in range(1, 13):
        n = i - 1
        N = 2
        if i == 1:
            day = '\n' + str(soup_w.find_all(class_="link blue")[2].contents[0]) + '\nNight   '
        elif i == 5:
            day = '\n' + str(soup_w.find_all(class_="link blue")[3].contents[0]) + '\nNight   '
        elif i == 9:
            day = '\n' + str(soup_w.find_all(class_="link blue")[4].contents[0]) + '\nNight   '
        elif i == 2 or i == 6 or i == 10:
            day = 'Morning '
        elif i == 3 or i == 7 or i == 11:
            day = 'Day     '
        else:
            day = 'Evening '
        msg_1 = (day + str(soup_w.find_all(class_="unit unit_temperature_c")[n].contents[0]) + ' ' + str(cloudy(i)))
        bot.send_message(message.chat.id, str(msg_1))

    '''

    msg_1 = (str(city) + ' ' + str(cur_date))
    msg_2 = ('Actual ' + str(temp_now) + ' Feeling ' + str(temp_feel) + \
             '\nNight ' + str(temp[0].contents[0]) + ' Day ' + str(temp[1].contents[0]))
   # msg_3 = ('Road condition by 8 A.M.: ' + str(road_cond_8) + \
    #         '\nRoad condition by 8 P.M.: ' + str(road_cond_20) + \
     #        '\nWind speed: ' + str(wind_km_h) + ' km/h')
    msg_4 = (str(sunrise) + ' ' + str(sunset) + '\n' + str(d_lenght) + '\n' + str(longer))
    msg_5 = ('Moon: ' + str(moonrise) + ' ' + str(moonset) + '\n' + str(f_moon) + '\n' + str(moon_phase))
          
    bot.send_message(message.chat.id, str(msg_1))
    bot.send_message(message.chat.id, str(msg_2))
   # bot.send_message(message.chat.id, str(msg_3))
    bot.send_message(message.chat.id, str(msg_4))
    bot.send_message(message.chat.id, str(msg_5))
 
 '''
 
@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://botto20190226.herokuapp.com/' + TOKEN)
    return "!", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

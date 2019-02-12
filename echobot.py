#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  8 17:29:46 2019

@author: steve18
"""
#script for Get last update
 

TOKEN = '628611026:AAHrryBXhR5Y7OYjFEeQMFHo-KMVsuciBoY'
url = "https://api.telegram.org/bot628611026:AAHrryBXhR5Y7OYjFEeQMFHo-KMVsuciBoY/"


import requests  
import datetime

class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)
        print('def __init__')

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json
        print('def get_updates result_json' + str(result_json))

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp
        print(resp)

    def get_last_update(self):
        get_result = self.get_updates()
        print('get_result' + str( get_result))

        if len(get_result) > 0:
            last_update = get_result[-1]
            print('last_update' + str(last_update))
        else:
            last_update = get_result[len(get_result)]

        return last_update
        print(last_update)
    
greet_bot = BotHandler('628611026:AAHrryBXhR5Y7OYjFEeQMFHo-KMVsuciBoY')  
greetings = ('здравствуй', 'привет', 'ку', 'здорово')  
now = datetime.datetime.now()
print(now)


def main():  
    new_offset = None
    today = now.day
    hour = now.hour
    print('def main')

    while True:
        greet_bot.get_updates(new_offset)

        last_update = greet_bot.get_last_update()

        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']
        last_chat_name = last_update['message']['chat']['first_name']

        if last_chat_text.lower() in greetings and today == now.day and 6 <= hour < 12:
            greet_bot.send_message(last_chat_id, 'Доброе утро, {}'.format(last_chat_name))
            today += 1

        elif last_chat_text.lower() in greetings and today == now.day and 12 <= hour < 17:
            greet_bot.send_message(last_chat_id, 'Добрый день, {}'.format(last_chat_name))
            today += 1

        elif last_chat_text.lower() in greetings and today == now.day and 17 <= hour < 23:
            greet_bot.send_message(last_chat_id, 'Добрый вечер, {}'.format(last_chat_name))
            today += 1

        new_offset = last_update_id + 1

if __name__ == '__main__':  
    try:
        main()
    except KeyboardInterrupt:
        exit()
    

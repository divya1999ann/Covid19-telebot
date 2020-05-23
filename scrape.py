#import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl

from urllib.request import Request, urlopen
import requests
import datetime

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = Request('https://www.worldometers.info/coronavirus/country/india/', headers={'User-Agent': 'Mozilla/5.0'})
html = urlopen(req).read()
soup = BeautifulSoup(html, 'html.parser')
tags = soup('span')

tag1=tags[4].contents[0]
tag2=tags[5].contents[0]
tag3=tags[6].contents[0]
#print(tag.contents[0])
	
class BotHandler:
    def __init__(self, token):
            self.token = token
            self.api_url = "https://api.telegram.org/bot{}/".format(token)

    #url = "https://api.telegram.org/bot<token>/"

    def get_updates(self, offset=0, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_first_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[0]
        else:
            last_update = None

        return last_update


token = '1184438900:AAH5JIuB57-pJH5XC7t7VTyeWKpu6gW9B6M' #Token of your bot
magnito_bot = BotHandler(token) #Your bot's name



def main():
    new_offset = 0
    print('hi, now launching...')

    while True:
        all_updates=magnito_bot.get_updates(new_offset)

        if len(all_updates) > 0:
            for current_update in all_updates:
                print(current_update)
                first_update_id = current_update['update_id']
                if 'text' not in current_update['message']:
                    first_chat_text='New member'
                else:
                    first_chat_text = current_update['message']['text']
                first_chat_id = current_update['message']['chat']['id']
                if 'first_name' in current_update['message']:
                    first_chat_name = current_update['message']['chat']['first_name']
                elif 'new_chat_member' in current_update['message']:
                    first_chat_name = current_update['message']['new_chat_member']['username']
                elif 'from' in current_update['message']:
                    first_chat_name = current_update['message']['from']['first_name']
                else:
                    first_chat_name = "unknown"

                if first_chat_text == 'Hi':
                    magnito_bot.send_message(first_chat_id, 'Morning ' + first_chat_name+ 'What help do you want')
                    new_offset = first_update_id + 1
                elif first_chat_text == 'start':
                	magnito_bot.send_message(first_chat_id, 'Welocome Divya Bot. Get Covid 19 India live updates here...')
                	new_offset = first_update_id + 1
                elif 'India' in first_chat_text or 'india' in first_chat_text:
                    magnito_bot.send_message(first_chat_id, 'Total Coronana cases in India:'+tag1+' Deaths:'+tag2+' Recovered:'+tag3)
                    new_offset = first_update_id + 1
                else:
                	magnito_bot.send_message(first_chat_id, 'Sorry, I dont get you')
                	new_offset = first_update_id + 1


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()


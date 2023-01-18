import requests
import pprint

TOKEN = '5853898261:AAFg2jbzv1FFlvRaj0UfhKiDae99-0z8suA'
MAIN_URL = f'https://api.telegram.org/bot{TOKEN}'
# Информация о боте
url = f'{MAIN_URL}/getMe'

proxies = {
    'http':'http://104.223.135.178:10000',
    'https':'http://104.223.135.178:10000',
}

#result = requests.get(url,proxies=proxies)

#print(result.json())
# Обновления
url = f'{MAIN_URL}/getUpdates'
result = requests.get(url,proxies=proxies)

pprint.pprint(result.json())

messages = result.json()['result']
for message in messages:
    # Ответ на сообщение
    chat_id = message['message']['chat']['id']
    url = f'{MAIN_URL}/sendMessage'
    params = {
        'chat_id':chat_id,
        'text':'Привет User!'
    }
    result = requests.get(url, proxies=proxies,params=params)

import telebot
from telebot import apihelper
import requests
from bs4 import BeautifulSoup
import time

TOKEN = '5853898261:AAFg2jbzv1FFlvRaj0UfhKiDae99-0z8suA'
MAIN_URL = f'https://api.telegram.org/bot{TOKEN}'
proxies = {
    'http':'http://104.223.135.178:10000',
    'https':'http://104.223.135.178:10000',
}
apihelper.proxy = proxies
bot = telebot.TeleBot(TOKEN)

def parse_habr(filters,antifilters,pages=5):
    theme_articles = []
    for i in range(1,pages):
        time.sleep(0.4)
        url = f'https://habr.com/ru/flows/develop/page{i}/'
        response = requests.get(url)
        print(i, response.status_code)
        soup = BeautifulSoup(response.text,'html.parser')
        for ref in soup.find_all('a'):
            state_name = str(ref.string).lower()
            try:
                if ref['class'][0] == 'tm-article-snippet__title-link':
                    for filter in filters:
                        if filter in state_name:
                            is_break = False
                            for antifilter in antifilters:
                                if antifilter in state_name:
                                    is_break = True
                            if not is_break:
                                theme_articles.append(state_name + ' \n|\n')
                                break
            except:
                pass
    return theme_articles

@bot.message_handler(commands=['start','help'])
def send_welcome(message):
    bot.reply_to(message,'Привет, как настроение?')

@bot.message_handler(commands=['habr'])
def parser(message):
    text = message.text.lower()
    try:
        print(text.split(' ')[1])
        pages = int(text.split(' ')[1])
    except:
        pages = 5
    if pages > 30:
        bot.send_message(message.chat.id, 'Количество страниц урезано до 30')
        pages = 30

    filters = text.split(' ')[2:]
    antifilters = []
    id = 0
    for i in range(len(filters)):
        if filters[i] == 'del':
            id = i
            continue
        if id != 0:
            antifilters.append(filters[i])
    if id != 0:
        filters = filters[:id]

    print('Фильтры: ', filters)
    print('Исключающие фильтры:', antifilters)

    results = parse_habr(filters,antifilters,pages=pages)

    if len(results) > 0:
        print(str(''.join(results)))
        bot.send_message(message.chat.id,''.join(results))
    else:
        print('Не найдено ни одной похожей статьи')
        bot.send_message(message.chat.id, 'Не найдено ни одной похожей статьи')


@bot.message_handler(content_types='text')
def reverse_text(message):
    text = message.text
    bot.reply_to(message,text[::-1])

bot.polling()
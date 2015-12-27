#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'Asus'

import threading
import feedparser
import socket
import re
import os
import logging


logging.basicConfig(format = '%(filename)s |%(funcName)s| [LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level = logging.INFO, filename='/var/www/FlaskApp/FlaskApp/Debugging.txt')

socket.setdefaulttimeout(10.0)
url_selected = []
rss_current_rest = []
rss_dict = {'http://www.vedomosti.ru/newsline/out/rss.xml':'Ведомости',
        'http://apsny.ge/RSS.xml':'Грузия-онлайн',
        'http://itar-tass.com/rss/v2.xml':'ИТАР-ТАСС',
        'http://www.kavkaz-uzel.ru/articles.rss/':'Кавказский узел',
        'http://www.kommersant.ru/RSS/news.xml':'Коммерсант',
        'http://lenta.ru/rss':'Лента.ру',
        'http://www.mignews.com/export/mig_export3.html':'МигНьюс',
        'http://www.blackseanews.net/allnews/romania.rss':'BlackSeaNews',
        'http://www.blackseanews.net/allnews/bulgaria.rss':'BlackSeaNews',
        'http://www.blackseanews.net/allnews/turkey.rss':'BlackSeaNews',
        'http://www.blackseanews.net/allnews/georgia.rss':'BlackSeaNews',
        'http://feeds.feedburner.com/rosbalt?format=xml':'Росбалт',
        'http://www.trend.az/feeds/index.rss':'Тренд',
        'http://www.armstrade.org/export/news.xml':'ЦАМТО',
        'http://www.bbc.co.uk/russian/index.xml':'Би-Би-Си',
        'http://www.rbc.ua/static/rss/newsline.rus.rss.xml':'РБК-Украина',
        'http://www.ukrinform.ru/rss/':'Укринформ',
        'http://rian.com.ua/export/rss2/politics/index.xml':'РИА-Новости',
        'http://rss.unian.net/site/news_rus.rss':'УНИАН',
        'http://k.img.com.ua/rss/ru/ukraine.xml':'Корреспондент',
        'http://vpk-news.ru/feed':'ВПК',
        'http://www.news-asia.ru/rss/all':'News-Asia',
        'http://www.fergananews.com/rss.php':'Фергана',
        'http://ru.apa.az/rss':'APA.AZ',
        'http://static.feed.rbc.ru/rbc/internal/rss.rbc.ru/rbc.ru/mainnews.rss':'РБК',
        'http://newsgeorgia.ru/export/rss2/index.xml':'Спутник',
        'http://irna.ir//ru/rss.aspx?kind=701':'ИРНА',
        'http://russian.rt.com/rss/':'RussiaToday',
        'http://www.apsnypress.info/news/rss/':'Апсны-Пресс',
        'http://sana.sy/ru/?feed=rss2':'САНА',
        }

rss_func_dict = {'Лента.ру':'lenta', 'Кавказский узел':'kavuzel', 'Тренд':'trend', 'ВПК':'vpk', 'News-Asia':'news_asia',
                 'МигНьюс':'mignews', 'Коммерсант':'kommersant', 'Ведомости':'vedomosti', 'Фергана':'fergana',
                 'Грузия-онлайн':'georgiaonline', 'BlackSeaNews':'blacksea', 'ЦАМТО':'camto', 'ИТАР-ТАСС':'itartass',
                 'Росбалт':'rosbalt', 'Би-Би-Си':'bbc', 'РБК-Украина':'rbc_ukr', 'Укринформ':'ukrinform', 'РИА-Новости':'rian',
                 'УНИАН':'unian', 'Корреспондент':'korrespondent','РБК':'rbc_rus','APA.AZ':'apa_az','Спутник':'newsgeorgia',
                 'ИРНА':'irna','RussiaToday':'rustoday','Апсны-Пресс':'apsnypress','САНА':'sana'}


class PullFeeds:
    def __init__(self):
        self.data = [k for k in rss_dict.keys()]
    def pullfeed(self):
        global rss_current_rest
        rss_current_rest = []
        threads = []
        for i in range(2):
            for url in self.data:
                 t = RssParser(url)
                 threads.append(t)
            for thread in threads:
                 thread.start()
            for thread in threads:
                 thread.join()
            if not rss_current_rest:
                break
            self.data = rss_current_rest
            if i == 1:
                rss_current_rest = []
            threads = []
            logging.info('!!!RSS second ROUND!!!')
        if rss_current_rest:
            msg = "FAILED RSS:\n"
            for r in rss_current_rest:
                msg += rss_dict[r] + '\n'
            logging.info(msg)

class RssParser(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url
    def run(self):
        global rss_current_rest
        print ("Starting: ", self.name, rss_dict[self.url])
        rss_current_rest.append(self.url)
        count = 0
        logging.info("Starting: {} {}".format(self.name, rss_dict[self.url]))
        rss_data = feedparser.parse(self.url)
        if len(rss_data['entries']):
            logging.info("{}: TOTAL - {}".format(rss_dict[self.url],len(rss_data['entries'])))
            for entry in rss_data.get('entries'):
                if self.add_to_selected_or_not(entry):
                    count += 1
            print ("Exiting: ", self.name, rss_dict[self.url])
            rss_current_rest.remove(self.url)
            print ("Осталось: {}".format(len(rss_current_rest)))
            logging.info("{}: Selected - {}".format(rss_dict[self.url], count))
        else:
            logging.info("{}: FAILED!!!".format(rss_dict[self.url]))
        # logging.info("Exiting: {} {}".format(self.name, rss_dict[self.url]))

    def add_to_selected_or_not(self, rss_item):
        global url_selected
        rss_item.link = rss_item.link.replace('http://az.apa','http://ru.apa')
        if is_in_history(rss_item) == True:
            return False
        stop_words = ['боксер','боксёр','хоккеист','Бессмертн','Звездные войны','Звездных войн','Войнов','Путин',
                      'велик[а-я]{2} отечествен','втор[а-я]{2} миров']
        for word in stop_words:
            p = re.compile(word)
            if p.search(rss_item.title.lower()) or p.search(rss_item.title):
                # print(rss_item.title, file=open("корзина.txt",'a',encoding='utf-8'))
                return False
        keywords_text = keywords_extract()
        for word in keywords_text:  # перебираем ключевые слова
            p = re.compile(word)
            if p.search(rss_item.title.lower()) or p.search(rss_item.title):
                print(rss_item.title)
                print(rss_item.link)
                print (rss_item.published_parsed)
                url_selected.append((rss_item.link,                      # link
                                    rss_item.title,                      # title of article
                                    rss_dict[self.url],                  # IA name
                                    rss_func_dict[rss_dict[self.url]],   # func name
                                    rss_item.published_parsed             # time
                                     ))
                return True


def keywords_extract():
    with open('/var/www/FlaskApp/FlaskApp/keywords_militar.txt','r',encoding='utf-8') as f:
        lines = f.readlines()
        lines = [l.strip() for l in lines]
    return lines

def is_in_history(rss_item):
    if not os.path.isfile('/var/www/FlaskApp/FlaskApp/history.txt'): create_history_file() # если файла нет, добавляем его и вписываем лимит-счетчик
    with open('/var/www/FlaskApp/FlaskApp/history.txt', 'r') as history_txt: # открываем файл с уникальными url
        history_txt.seek(0)                     # переводим курсор в начало файла
        history_list = history_txt.readlines()  # копируем оттуда весь текст
    if any(rss_item.link in line for line in history_list):  #преверяем наличие текущей статьи в файле history.txt. Если есть то пропускаем.
        return True
    try:
        if 'http://www.blackseanews.net/read/' + rss_item.link.split('/')[8] + '\n' in history_list: # отдельно проверяется для blackseanews, возможна ошибка в rss_item.link.split('/')[8]
            return True
    except IndexError:
        pass
    return False

def create_history_file():
    with open('/var/www/FlaskApp/FlaskApp/history.txt', 'w+') as history_txt:
        history_txt.write('0b1100100\n')

if __name__ == '__main__':
    pf = PullFeeds()
    pf.pullfeed()
    print(len(url_selected))
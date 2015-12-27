#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'Asus'

from bs4 import BeautifulSoup
from datetime import date, datetime,timedelta
import logging

logging.basicConfig(format = '%(filename)s |%(funcName)s| [LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level = logging.INFO, filename='/var/www/FlaskApp/FlaskApp/Debugging.txt')

class NEWSAGENCY():
    def __init__(self,item):
        self.main_text_class = ''
        self.url = item[4]
        self.rss_name = item[2]
        self.soup = BeautifulSoup(item[0])
        for script in self.soup.findAll('script'):   # Delete all js scripts from soup
            script.decompose()
        for style in self.soup.findAll('style'):     # Delete all css styles from soup
            style.decompose()

    def get_time(self, datetime_format):
        month_names = ['января','февраля','марта','апреля','мая','июня','июля','августа','сентября','октября','ноября','декабря']
        self.month_name = month_names[datetime_format.month - 1]
        self.date_final = '{} {} {} г.'.format(str(datetime_format.day).lstrip("0"),self.month_name,str(datetime_format.year))
        self.time_final = datetime_format.strftime("%H.%M")
        return self.date_final, self.time_final
    def strip_texts(self):
        self.main_text_class = "\n".join([line.strip() for line in self.main_text_class.split('\n') if line.strip()])

    def korrespondent(self):
        try:
            self.main_text_class = self.soup.find('div', {'class': 'post-item__text'}).text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.main_text_class.\n{}\n'.format(self.url, e))
            return False
        return 'Ok'
    def unian(self):
        try:
            self.main_text_class = ''
            for everyitem in self.soup.find('div', {'class': 'article_body'}).findAll('p',recursive=False):
                if "Читайте также" not in everyitem.text:
                    self.main_text_class = self.main_text_class + '\n' + everyitem.text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.main_text_class.\n{}\n'.format(self.url, e))
            return False
        return 'Ok'
    def ukrinform(self):
        try:
            self.main_text_class = ''
            for everyitem in self.soup.find('div',{'class':'newsText'}).findAll('p',recursive=False):
                if "Читайте также:" not in everyitem.text:
                    self.main_text_class = self.main_text_class + '\n' + everyitem.text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.main_text_class.\n{}\n'.format(self.url, e))
            return False
        return 'Ok'
    def rbc_ukr(self):
        try:
            self.main_text_class = self.soup.find('div', {'class':'text'}).text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.main_text_class.\n{}\n'.format(self.url, e))
            return False
        return 'Ok'
    def rbc_rus(self):
        try:
            self.main_text_class = ''
            for everyitem in self.soup.find('div',{'class':'article__text'}).findAll('p'):
                self.main_text_class = self.main_text_class + '\n' + everyitem.text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.main_text_class.\n{}\n'.format(self.url, e))
            return False
        return 'Ok'
    def bbc(self):
        main_div = self.soup.find('div', {'class': 'story-body__inner'})
        if not main_div: main_div = self.soup.find('div', {'class': 'map-body'})
        if not main_div: return
        try:
            self.main_text_class = ''
            for everyitem in main_div.findAll('p'):
                self.main_text_class = self.main_text_class + '\n' + everyitem.text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.main_text_class.\n{}\n'.format(self.url, e))
            return False
        return 'Ok'
    def lenta(self):
        try:
            self.main_text_class = ''
            for everyitem in self.soup.find('div', {'itemprop': 'articleBody'}).findAll('p'):
                self.main_text_class = self.main_text_class + '\n' + everyitem.text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.main_text_class.\n{}\n'.format(self.url, e))
            return False
        return 'Ok'
    def rian(self):
        for everyitem in self.soup.findAll('p', {'style': 'text-align: center;'}):
            everyitem.replaceWith('')
        try:
            self.main_text_class = ''
            for everyitem in self.soup.find('div', {'itemprop': 'articleBody'}).findAll('p'):
                self.main_text_class = self.main_text_class + '\n' + everyitem.text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.main_text_class.\n{}\n'.format(self.url, e))
            return False
        return 'Ok'
    def trend(self):
        try:
            self.main_text_class = ''
            for everyitem in self.soup.find('div', {'itemprop': 'articleBody'}).findAll('p'):
                if "@www_Trend_Az" not in everyitem.text and "agency@trend.az" not in everyitem.text:
                    self.main_text_class = self.main_text_class + '\n' + everyitem.text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.main_text_class.\n{}\n'.format(self.url, e))
            return False
        return 'Ok'
    def mignews(self):
        for everyitem in self.soup.findAll('noindex', recursive=False):
            everyitem.replaceWith('')
        for everyitem in self.soup.findAll('iframe'):
            everyitem.replaceWith('')
        for everyitem in self.soup.findAll('div', {'class': 'addthis_toolbox addthis_default_style pad2'}):
            everyitem.replaceWith('')
        for everyitem in self.soup.findAll('ul'):
            everyitem.replaceWith('')
        for everyitem in self.soup.findAll('h5'):
            everyitem.replaceWith('')
        try:
            if self.soup.find('div', {'class': 'textnews'}):
                self.main_text_class = self.soup.find('div', {'class': 'textnews'}).text + '\n\n'
            elif self.soup.find('div', {'id': 'leftc'}):
                self.main_text_class = self.soup.find('div', {'id': 'leftc'}).text + '\n\n'
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.main_text_class.\n{}\n'.format(self.url, e))
            return False
        return 'Ok'
    def kavuzel(self):
        for everyitem in self.soup.findAll('div', {'class': 'lt-feedback_banner pull-right hidden-phone'}):
                everyitem.replaceWith('')
        try:
            self.main_text_class = ''
            for everyitem in self.soup.find('div', {'class': 'articles-body'}).findAll('p',recursive=False):
                self.main_text_class = self.main_text_class + '\n' + everyitem.text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.main_text_class.\n{}\n'.format(self.url, e))
            return False
        return 'Ok'
    def kommersant(self):
        try:
            self.main_text_class = ''
            for everyitem in self.soup.findAll('p', {'class': 'b-article__text'}):
                self.main_text_class = self.main_text_class + '\n' + everyitem.text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.main_text_class.\n{}\n'.format(self.url, e))
            return False
        return 'Ok'
    def vedomosti(self):
        try:
            self.main_text_class = ''
            for everyitem in self.soup.find('div', {'class': 'b-news-item__text b-news-item__text_one'}).findAll('p'):
                self.main_text_class = self.main_text_class + '\n' + everyitem.text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.main_text_class.\n{}\n'.format(self.url, e))
            return False
        return 'Ok'
    def georgiaonline(self):
        try:
            self.main_text_class = ''
            for everyitem in self.soup.find('td', {'class': 'newsbody'}).findAll('div', {'class': 'txt-item-news'}):
                self.main_text_class = self.main_text_class + '\n' + everyitem.text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.main_text_class.\n{}\n'.format(self.url, e))
            return False
        return 'Ok'
    def blacksea(self):
        if 'Attention Required!' in self.soup.html.head.title.text:
            return False
        # ИЗВЛЕЧЕНИЕ ВРЕМЕНИ, ЗАГОЛОВКА И ТЕКСТА ПО HTML ТЭГАМ
        for everyitem in self.soup.findAll('a', {'class': 'icon comment'}):
            everyitem.replaceWith('')
        for everyitem in self.soup.findAll('a', {'class': ' flagLinks-moldova'}):
            everyitem.replaceWith('')
        try:
            self.main_text_class = ''
            for everyitem in self.soup.findAll('div', {'id': 'contentText'}):
                self.main_text_class = self.main_text_class + '\n' + everyitem.text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.main_text_class.\n{}\n'.format(self.url, e))
            return False
        return 'Ok'
    def camto(self):
        if '401' in self.soup.html.head.title.text:
            logging.warning('%%%%%Платная статья.\n')
            self.main_text_class = 'ПЛАТНАЯ СТАТЬЯ'
            self.vremya_class = 'Empty'
            return
        try:
            self.main_text_class = ''
            for everyitem in self.soup.find('div', {'class': 'content'}).find('div', {'class': 'mainnews'}).findAll('div'):
                self.main_text_class = self.main_text_class + '\n' + everyitem.text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.main_text_class.\n{}\n'.format(self.url, e))
            return False
        return 'Ok'
    def itartass(self):
        for everyitem in self.soup.findAll('div', {'class': 'b-gallery-widget-item'}):
            everyitem.replaceWith('')
        for everyitem in self.soup.findAll('div', {'class': 'b-links printHidden'}):
            everyitem.replaceWith('')
        for everyitem in self.soup.findAll('div', {'class': 'b-links b-links_mini b-links_right printHidden'}):
            everyitem.replaceWith('')
        for everyitem in self.soup.findAll('a', {'target': '_blank'}):
            everyitem.replaceWith('')
        try:
            self.main_text_class = ''
            for everyitem in self.soup.find('div', {'class': 'b-material-text__l'}).findAll('p'):
                self.main_text_class = self.main_text_class + '\n' + everyitem.text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.main_text_class.\n{}\n'.format(self.url, e))
            return False
        return 'Ok'
    def rosbalt(self):
        try:
            self.main_text_class = ''
            # mat_cont = self.soup.find('div', {'id': 'mat_cont'})
            for everyitem in self.soup.find('article').findAll('p'):
                self.main_text_class = self.main_text_class + '\n' + everyitem.text
            if not self.main_text_class:
                self.main_text_class = self.soup.find('article').text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.main_text_class.\n{}\n'.format(self.url, e))
            return False
        return 'Ok'
    def vpk(self):
        try:
            self.main_text_class = ''
            for everyitem in self.soup.find('div',{'class':'field-item even','property':'content:encoded'}).findAll('p'):
                self.main_text_class = self.main_text_class + '\n' + everyitem.text
            if len(self.main_text_class) > 4000:
                logging.warning('%%%%%Скорее всего это был анализ.УДАЛЕНО.\n')
                return 'no_interest'
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.main_text_class.\n{}\n'.format(self.url, e))
            return False
        return 'Ok'
    def news_asia(self):
        try:
            self.main_text_class = ''
            for everyitem in self.soup.findAll('div',{'class':'content'}):
                self.main_text_class = self.main_text_class + '\n' + everyitem.text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.main_text_class.\n{}\n'.format(self.url, e))
            return False
        return 'Ok'
    def fergana(self):
        try:
            self.main_text_class = ''
            for everyitem in self.soup.findAll('div',{'id':'text'}):
                self.main_text_class = self.main_text_class + '\n' + everyitem.text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.main_text_class.\n{}\n'.format(self.url, e))
            return False
        return 'Ok'
    def apa_az(self):
        try:
            self.main_text_class = ''
            for everyitem in self.soup.find('div',{'class':'content'}).findAll('p'):
                self.main_text_class = self.main_text_class + '\n' + everyitem.text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.main_text_class.\n{}\n'.format(self.url, e))
            return False
        return 'Ok'
    def newsgeorgia(self):
        try:
            self.main_text_class = ''
            for everyitem in self.soup.find('div', {'class': 'b-article__text'}).findAll('p'):
                self.main_text_class = self.main_text_class + '\n' + everyitem.text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.main_text_class.\n{}\n'.format(self.url, e))
            return False
        return 'Ok'
    def irna(self):
        try:
            self.main_text_class = ''
            self.main_text_class = self.main_text_class + '\n' + self.soup.find('h3', {'id': 'ctl00_ctl00_ContentPlaceHolder_ContentPlaceHolder_NewsContent1_H1'}).text
            self.main_text_class = self.main_text_class + '\n' + self.soup.find('p', {'id': 'ctl00_ctl00_ContentPlaceHolder_ContentPlaceHolder_NewsContent1_BodyLabel'}).text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.main_text_class.\n{}\n'.format(self.url, e))
            return False
        return 'Ok'
    def rustoday(self):
        try:
            self.main_text_class = ''
            for everyitem in self.soup.find('article', {'id': 'content'}).findAll('p'):
                self.main_text_class = self.main_text_class + '\n' + everyitem.text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.main_text_class.\n{}\n'.format(self.url, e))
            return False
        return 'Ok'
    def apsnypress(self):
        try:
            self.main_text_class = self.soup.find('div', {'class': 'detail_text'}).text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.main_text_class.\n{}\n'.format(self.url, e))
            return False
        return 'Ok'
    def sana(self):
        try:
            self.main_text_class = ''
            for everyitem in self.soup.find('div', {'class': 'entry'}).findAll('p'):
                self.main_text_class = self.main_text_class + '\n' + everyitem.text
        except Exception as e:
            logging.warning('%%%%%В {} не найдено self.main_text_class.\n{}\n'.format(self.url, e))
            return False
        return 'Ok'

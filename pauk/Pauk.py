#!/usr/bin/python3
# -*- coding: utf-8 -*- 

__author__ = 'Asus'
# TODO: Вынести фильтрацию по ключемым словам в файл Pauk
from datetime import datetime, date, timedelta
import asyncio
import aiohttp
import logging
# import shutil
# import glob

import rss_threading
import bs4_processing
import output


logging.basicConfig(format = '%(filename)s |%(funcName)s| [LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level = logging.INFO, filename='/var/www/FlaskApp/FlaskApp/Debugging.txt')


def get_rss_data():
    # RSS threading
    rss_threading.url_selected = []
    pf = rss_threading.PullFeeds()
    pf.pullfeed()

def time_correction(url_selected):
    today_url_selected = []
    for i in url_selected:
        old_time = i[4]
        new_time = datetime(old_time.tm_year, old_time.tm_mon, old_time.tm_mday, old_time.tm_hour,old_time.tm_min,
                            old_time.tm_sec)
        if i[2] == 'ИРНА':
            new_time = new_time - timedelta(hours=0.5)
        elif i[2] == 'Спутник':
            new_time = new_time + timedelta(hours=2)
        else:
            new_time = new_time + timedelta(hours=3)
        today_url_selected.append((i[0],i[1],i[2],i[3],new_time))
    print("Было: {}, Стало: {}".format(len(url_selected), len(today_url_selected)))
    return today_url_selected

class Async():
    def __init__(self, url_selected):
        self.data_current = url_selected[:]
        self.data_changable = url_selected[:]
        self.final_list_of_articles = []

    @asyncio.coroutine
    def download_HTMLs_to_HTMLlist(self,url,title,rss,func,atime):
        print('Start downloading {}'.format(url))
        logging.info('Start downloading {}'.format(url))
        response = yield from asyncio.wait_for(aiohttp.request('GET', url), 30)  # With timeout
        body = yield from response.read_and_close()
        try:
            if rss in ['News-Asia', 'МигНьюс', 'Коммерсант', 'Грузия-онлайн', 'ЦАМТО']:
                body = body.decode(encoding='cp1251')
            else:
                body = body.decode(encoding='utf-8')
        except Exception as e:
            logging.info('Кодировка: {}'.format(e))
        self.final_list_of_articles.append([body,title,rss,func,url,atime])
        try:
            self.data_changable.remove((url,title,rss,func,atime))
        except:
            pass
        print('Finished {}'.format(url))
        logging.info('Finished {}'.format(url))


    def start_async(self):
        for i in range(3):
            print("ROUND {}".format(i))
            if self.data_changable:
                self.data_current = self.data_changable[:]
                loop = asyncio.get_event_loop()
                aw = asyncio.wait([self.download_HTMLs_to_HTMLlist(item[0],item[1],item[2],item[3],item[4])
                                   for item in self.data_current])
                loop.run_until_complete(aw)
        return self.final_list_of_articles

def bs4_and_output(final_list_of_articles):
    count = len(final_list_of_articles)
    recieved = 0
    for html_item in final_list_of_articles:        # consist of body,title,rss,func,url,atime
        count -= 1
        NA_obj = bs4_processing.NEWSAGENCY(html_item)
        func_result = getattr(NA_obj,html_item[3])()
        if func_result != False:       # Parse by IA name
            output.add_url_to_history(html_item[4])
            if func_result != 'no_interest':
                NA_obj.strip_texts()
                rss_a = html_item[2]
                title_a = html_item[1]
                dtformat = html_item[5]
                date_a,time_a = NA_obj.get_time(dtformat)
                maintext_a = NA_obj.main_text_class
                output.country = "Другие"
                output.define_country_by_zagolovok(title_a)
                if output.country == "Другие":
                    maintext_a = output.define_country_by_mtext(maintext_a)
                recieved += 1
                if output.country != "Другие":
	                try:
	                    output.output_to_sql(title_a, maintext_a, dtformat,rss_a,output.country)
	                    print('Добавлено в БД')
	                except Exception as e:
	                    logging.warning('sqlite PROBLEM\n{}'.format(e))
    return recieved


def main():
    total_len = 0

    get_rss_data()
    today_urls = time_correction(rss_threading.url_selected)

    async_instance = Async(today_urls)
    final_list = async_instance.start_async()

    recieved = bs4_and_output(final_list)
    total = len(rss_threading.url_selected)
    downloaded = len(async_instance.final_list_of_articles)
    total_len += downloaded
    print('Total: {}'.format(total))
    logging.info('Total: {}'.format(total))
    print('Downloaded: {}'.format(downloaded))
    logging.info('Downloaded: {}'.format(downloaded))
    print("LEFT:")
    bad_url = ""
    for u in async_instance.data_changable:
        bad_url += '\n' + u[0]
    logging.info('Не скачаны следующие статьи:{}'.format(bad_url))




if __name__ == "__main__":

    main()

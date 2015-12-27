# -*- coding: utf-8 -*-
import datetime

from flask import Flask, render_template, request, url_for, redirect, flash, send_file, jsonify
import sqlite_connect
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from app import views, models

rss_dict = {u'Би-Би-Си': 'http://www.bbc.co.uk/russian/', 
			u'APA.AZ': 'http://ru.apa.az/', 
			u'Тренд': 'http://www.trend.az/', 
			u'РБК': 'http://www.rbc.ru/', 
			u'Корреспондент': 'http://korrespondent.net/', 
			u'ЦАМТО': 'http://www.armstrade.org/', 
			u'ВПК': 'http://vpk-news.ru/', 
			u'BlackSeaNews': 'http://www.blackseanews.net/', 
			u'Укринформ': 'http://www.ukrinform.ua/rus/', 
			u'RussiaToday': 'http://russian.rt.com/', 
			u'МигНьюс': 'http://www.mignews.com/', 
			u'Лента.ру': 'http://lenta.ru/', 
			u'УНИАН': 'http://www.unian.net/', 
			u'Росбалт': 'http://www.rosbalt.ru/', 
			u'Ведомости': 'http://www.vedomosti.ru/', 
			u'РИА-Новости': 'http://rian.com.ua/', 
			u'News-Asia': 'http://www.news-asia.ru/', 
			u'РБК-Украина': 'http://www.rbc.ua/', 
			u'ИРНА': 'http://irna.ir//ru/', 
			u'Спутник': 'http://newsgeorgia.ru/', 
			u'ИТАР-ТАСС': 'http://itar-tass.com/', 
			u'Коммерсант': 'http://www.kommersant.ru/', 
			u'Фергана': 'http://www.fergananews.com/', 
			u'Апсны-Пресс': 'http://www.apsnypress.info/', 
			u'Кавказский узел': 'http://www.kavkaz-uzel.ru/', 
			u'Грузия-онлайн': 'http://apsny.ge/'}




@app.route('/')
def homepage():
    return render_template("main.html")

@app.route('/map/')		
def map_page():
	return render_template("my_map.html")

@app.route('/<country>/')		
def find_country(country):
	NEWS = sqlite_connect.GetbyCountry(country)
	return render_template("news.html", NEWS=NEWS)

@app.route('/news_body/<url>/<id>/')		
def news_body(id, url):
	ARTICLE = sqlite_connect.Getbyid(id)
	source_url = rss_dict[ARTICLE[2]]
	return render_template("news_body.html", ARTICLE=ARTICLE, URL=url, SOURCE_URL=source_url)

@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html")

@app.route('/download_articles/', methods=['GET','POST'])
def download_articles():
	try:
		articles_ids = request.form.getlist("selected")
		# all_selected = ''
		all_selected_web = ''
		for id in articles_ids:
			ARTICLE = sqlite_connect.Getbyid(id)
			# all_selected = all_selected + '\n'.join(ARTICLE) + '\n\n'
			all_selected_web = all_selected_web + '<br>'.join(ARTICLE) + '<br><br>'
		return all_selected_web
	except Exception as e:
		return (str(e))


# EDIT
@app.route('/main_edit/')
def main_edit():
    return render_template("main_edit.html")


# GET FILE

@app.route('/get_file/')
def get_file():
    return send_file('static/download/Паук 3.1.rar', as_attachment=True)



# СНГ
@app.route('/news_az/')		
def news_page_az():
	NEWS = sqlite_connect.GetbyWordsExercises(u'''mylower(article_title) like {}'''.format(u'"%азербайдж%"'))
	return render_template("news.html", NEWS=NEWS)

@app.route('/news_ge/')		
def news_page_ge():
	NEWS = sqlite_connect.GetbyWordsExercises(u'''mylower(article_title) like {}'''.format(u'"%грузи%"'))
	return render_template("news.html", NEWS=NEWS)

@app.route('/news_ua/')		
def news_page_ua():
	NEWS = sqlite_connect.GetbyWordsExercises(u'''mylower(article_title) like {}'''.format(u'"%украин%"'))
	return render_template("news.html", NEWS=NEWS)

# НАТО
@app.route('/news_na/')		
def news_page_na():
	NEWS = sqlite_connect.GetbyWordsExercises(u'''mylower(article_title) like {}'''.format(u'"%нато%"'))
	return render_template("news.html", NEWS=NEWS)

@app.route('/news_po/')		
def news_page_po():
	NEWS = sqlite_connect.GetbyWordsExercises(u'''(mylower(article_title) like {} or mylower(article_title) like {})'''.format(u'"%польш%"',u'"% польск%"'))
	return render_template("news.html", NEWS=NEWS)

@app.route('/news_la/')
def news_page_la():
	NEWS = sqlite_connect.GetbyWordsExercises(u'''(mylower(article_title) like {} or mylower(article_title) like {} or mylower(article_title) like {} 
		or mylower(article_title) like {})'''.format(u'"%латви%"', u'"%эстон%"', u'"%литва%"', u'"%прибалти%"'))
	return render_template("news.html", NEWS=NEWS)

@app.route('/news_tr/')		
def news_page_tr():
	NEWS = sqlite_connect.GetbyWordsExercises(u'''(mylower(article_title) like {} or mylower(article_title) like {})'''.format(u'"%турци%"',u'"%турецк%"'))
	return render_template("news.html", NEWS=NEWS)

# Регионы
@app.route('/news_bl/')		
def news_page_bl():
	NEWS = sqlite_connect.GetbyWords(u'''mylower(article_title) like {} or 
		(mylower(article_title) like {} and mylower(article_title) like {})'''.format(u'"%черноморск%"',	u'"%черн%"', u'"%мор%"'))
	return render_template("news.html", NEWS=NEWS)

@app.route('/news_md/')		
def news_page_md():
	NEWS = sqlite_connect.GetbyWords(u'''mylower(article_title) like {}'''.format(u'"%средиземно%"'))
	return render_template("news.html", NEWS=NEWS)

@app.route('/news_mu/')		
def news_page_mu():
	NEWS = sqlite_connect.GetbyWords(u'''mylower(article_title) like {} and (mylower(article_title) like {} or mylower(article_title) like {})'''.format(
		u'"%украин%"', u'"%чехи%"', u'"%чешск%"'))
	return render_template("news.html", NEWS=NEWS)



def ConvertTimeFormat(bad_time_format):
    good_time = datetime.datetime.strptime(bad_time_format, "%Y-%m-%d %H:%M:%S")
    return good_time.strftime('%d.%m.%Y %H.%M')
if __name__ == "__main__":
	app.run(debug=True)

# def row2dict(row):
#     d = {}
#     for column in row.__table__.columns:
#         d[column.name] = str(getattr(row, column.name))
#     return d
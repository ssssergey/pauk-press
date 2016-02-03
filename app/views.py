# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, session, url_for, request, g, send_file
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from .forms import LoginForm, RegistrationForm, FeedbackForm
from .models import User, Main

from passlib.handlers.sha2_crypt import sha256_crypt
from sqlalchemy import func, or_, and_
import datetime

from emails import feedback_notification, download_notification, registration_notification

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
			u'Новости-Грузия': 'http://newsgeorgia.ru/',
			u'САНА': 'http://sana.sy/ru/',
			u'РИА Новости': 'http://ria.ru/',
			u'Грузия-онлайн': 'http://apsny.ge/',
			u'ДАН':'http://dan-news.info/',
			u'Анадолу':'http://aa.com.tr/ru/',
			u'Арменпресс':'http://armenpress.am/rus/'
			}


@app.route('/')
@app.route('/index')
def index():
	query = Main.query.order_by("article_time desc").limit(100).all()
	posts = []
	for row in query:
		new_row = [row.article_title, ConvertTimeFormat(row.article_time),row.rss_source,row.id]
		posts.append(new_row)
	return render_template("main.html", NEWS=posts)

@app.route('/main_edit/')
def main_edit():
	return render_template("main_edit.html")

@app.route('/register', methods=["GET","POST"])
def register():
	form = RegistrationForm(request.form)

	if form.is_submitted():
		print "submitted"
	if form.validate():
		print "valid"
	print form.errors

	if request.method == "POST" and form.validate():
		nickname  = form.username.data
		email = form.email.data
		password = sha256_crypt.encrypt((str(form.password.data)))

		user = User.query.filter_by(nickname=nickname).first()
		if user != None:
			flash(u"Этот ник уже занят, попробуйте другой")
			return render_template('register.html', form=form)
		else:
			user = User(nickname=nickname, email=email, password=password)
			db.session.add(user)
			db.session.commit()
			registration_notification(nickname, 'is registered!')
			flash(u"Вы успешно зарегистрировались!")
			login_user(user)
			return redirect(request.args.get('next') or url_for('index'))
	return render_template("register.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
	if g.user is not None and g.user.is_authenticated:
		flash(u"Вы уже вошли")
		return redirect(url_for('index'))
	form = LoginForm(request.form)

	if form.is_submitted():
		print "submitted"
	if form.validate():
		print "valid"
	print form.errors

	if request.method == "POST" and form.validate_on_submit():
		nickname  = form.username.data
		password = str(form.password.data)

		user = User.query.filter_by(nickname=nickname).first()
		if user != None and sha256_crypt.verify(password, user.password):
			session['remember_me'] = form.remember_me.data
			remember_me = False

			if 'remember_me' in session:
				remember_me = session['remember_me']
				session.pop('remember_me', None)
			login_user(user, remember = remember_me)
			flash(u"Поздравляю, {}, Вы успешно вошли.".format(user.nickname))
			return redirect(request.args.get('next') or url_for('index'))
		else:
			flash(u"Нерправильный логин или пароль")
	if request.method == "POST":
		flash(u"Неправильно заполнены поля")
	return render_template('login.html',
						   title='Sign In',
						   form=form
						   )

@app.before_request
def before_request():
	g.user = current_user

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@lm.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.route('/user/<nickname>')
@login_required
def user(nickname):
	user = User.query.filter_by(nickname=nickname).first()
	if user == None:
		flash(u'Пользователь %s не найден.' % nickname)
		return redirect(url_for('index'))
	posts = [
		{'author': user, 'body': 'Test post #1'},
		{'author': user, 'body': 'Test post #2'}
	]
	return render_template('user.html',
						   user=user,
						   posts=posts)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
	form = FeedbackForm(request.form)

	if form.is_submitted():
		print "submitted"
	if form.validate():
		print "valid"
	print form.errors

	if request.method == "POST" and form.validate():
		nickname  = form.username.data
		message = form.message.data
		import os
		basedir = os.path.abspath(os.path.dirname(__file__))
		feedback_path = os.path.join(basedir, 'feedback.txt')
		with open(feedback_path, 'a') as history_txt:
			history_txt.write('{} | {}\n{}\n\n'.format(datetime.datetime.utcnow(),
                                                       nickname.encode('utf8'),message.encode('utf8')))
		flash(u"Ваше сообщение получено!")
		feedback_notification(nickname, message)
		return redirect(request.args.get('next') or url_for('index'))
	if g.user.is_authenticated:
		form.username.data = g.user.nickname
	return render_template("feedback.html", form=form)


#########################################################################

@app.route('/news_search/', methods=['GET','POST'])
@login_required
def news_search():
	if request.method == 'POST':
		words = request.form['word1'],request.form['word2'],request.form['word3']
		bunch = []
		for i in words:
			if i:
				bunch.append((("%" + i + "%"),("%" + i.capitalize() + "%")))
		args = []
		for pair in bunch:
			args.append(or_(Main.article_title.like(pair[0]),
							Main.article_title.like(pair[1]),
							Main.article_text.like(pair[0]),
							Main.article_text.like(pair[1]),
							))
		print(pair)
		query = Main.query.filter(and_(*[i for i in args])).order_by("article_time desc").all()
		posts = []
		for row in query:
			new_row = [row.article_title, ConvertTimeFormat(row.article_time),row.rss_source,row.id]
			posts.append(new_row)
		return render_template("news.html", NEWS=posts)
	else:
		return render_template("news_search.html")

@app.route('/<country>')
def find_country(country):
	query = Main.query.filter(Main.country == country).order_by("article_time desc").limit(1500).all()
	posts = []
	for row in query:
		new_row = [row.article_title, ConvertTimeFormat(row.article_time),row.rss_source,row.id]
		posts.append(new_row)
	return render_template("news.html", NEWS=posts, country=country)

@app.route('/news_body/<id>')
def news_body(id):
	query_row = Main.query.filter(Main.id == int(id)).first()
	posts = (query_row.article_title,ConvertTimeFormat(query_row.article_time),query_row.rss_source,query_row.article_text.replace('\n','<br>'))
	source_url = rss_dict[posts[2]]
	return render_template("news_body.html", ARTICLE=posts, SOURCE_URL=source_url)


@app.route('/news_az/')
def news_page_az():
	NEWS = exercises_help_function(u"азербайдж")
	return render_template("news.html", NEWS=NEWS)

@app.route('/news_ge/')
def news_page_ge():
	NEWS = exercises_help_function(u"грузи")
	return render_template("news.html", NEWS=NEWS)

@app.route('/news_ua/')
def news_page_ua():
	NEWS = exercises_help_function(u"украин")
	return render_template("news.html", NEWS=NEWS)

# НАТО
@app.route('/news_na/')
def news_page_na():
	NEWS = exercises_help_function(u"НАТО")
	return render_template("news.html", NEWS=NEWS)

@app.route('/news_po/')
def news_page_po():
	NEWS = exercises_help_function(u"польш",u'польск')
	return render_template("news.html", NEWS=NEWS)

@app.route('/news_la/')
def news_page_la():
	NEWS = exercises_help_function(u"латви",u'эстон',u'литва',u'прибалти')
	return render_template("news.html", NEWS=NEWS)

@app.route('/news_tr/')
def news_page_tr():
	NEWS = exercises_help_function(u"турци",u'турецк')
	return render_template("news.html", NEWS=NEWS)

# Регионы
@app.route('/news_bl/')
def news_page_bl():
	NEWS = sea_help_function(u"черн")
	return render_template("news.html", NEWS=NEWS)

@app.route('/news_md/')
def news_page_md():
	NEWS = sea_help_function(u"средиземно")
	return render_template("news.html", NEWS=NEWS)

@app.route('/pers_gulf/')
def news_pers_gulf():
	NEWS = sea_help_function(u"персидск")
	return render_template("news.html", NEWS=NEWS)

def exercises_help_function(*args):
	bunch = []
	for i in args:
		bunch.append("%" + i + "%")
		bunch.append("%" + i.capitalize() + "%")
	query = Main.query.filter(or_(Main.article_title.like(u'%учени%'),
										Main.article_title.like(u'%Учени%'),
										Main.article_title.like(u'%отраб%'),
										Main.article_title.like(u'%Отраб%'),
										Main.article_title.like(u'%трениров%'),
										Main.article_title.like(u'%Трениров%'),
								   ))
	query = query.filter(or_(*[Main.article_title.like(i) for i in bunch])).order_by("article_time desc")
	posts = []
	for row in query:
		new_row = [row.article_title, ConvertTimeFormat(row.article_time),row.rss_source,row.id]
		posts.append(new_row)
	return posts

def sea_help_function(*args):
	bunch = []
	for i in args:
		bunch.append("%" + i + "%")
		bunch.append("%" + i.capitalize() + "%")
	query = Main.query.filter(or_(Main.article_title.like(u'%морск%'),
									Main.article_title.like(u'%море%'),
									Main.article_title.like(u'%акватори%'),
									Main.article_title.like(u'%залив%'),
							   ))
	query = query.filter(or_(*[Main.article_title.like(i) for i in bunch])).order_by("article_time desc")
	posts = []
	for row in query:
		new_row = [row.article_title, ConvertTimeFormat(row.article_time),row.rss_source,row.id]
		posts.append(new_row)
	return posts

@app.route('/download_articles/', methods=['GET','POST'])
def download_articles():
	try:
		articles_ids = request.form.getlist("selected")
		all_selected_web = ''
		for id in articles_ids:
			query_row = Main.query.filter(Main.id == int(id)).first()
			ARTICLE = (query_row.article_title,ConvertTimeFormat(query_row.article_time),
					   query_row.rss_source,query_row.article_text)
			all_selected_web = all_selected_web + '<br>'.join(ARTICLE) + '<br><br>'
		return all_selected_web
	except Exception as e:
		return (str(e))

@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html")

# GET FILE
@app.route('/get_file/')
def get_file():
	download_notification('Somebody','downloaded')
	return send_file('static/download/Паук 3.5.rar', as_attachment=True)

def ConvertTimeFormat(utc_format):
	try:
		good_time = datetime.datetime.strptime(utc_format, "%Y-%m-%d %H:%M:%S").strftime('%d.%m.%Y %H.%M')
	except (ValueError, TypeError):
		good_time = "None"
	return good_time
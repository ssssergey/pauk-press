# -*- coding: utf-8 -*-
import datetime

from flask import Flask, render_template, request, url_for, redirect, flash,  jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

lm = LoginManager()
lm.login_message = u"Сначала войдите на сайт под своим паролем"
lm.init_app(app)
lm.login_view = 'login'

from app import views, models

if __name__ == "__main__":
	app.run(debug=True)

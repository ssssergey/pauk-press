# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField, TextAreaField
from wtforms.validators import DataRequired,Length,EqualTo

class LoginForm(Form):
    username = StringField(u'Имя', validators=[DataRequired(message=u'Обязательное поле')])
    password = PasswordField(u'Пароль', validators=[DataRequired(message=u'Обязательное поле')])
    remember_me = BooleanField(u'remember_me', default=False)

class RegistrationForm(Form):
    username = StringField(u'Имя', validators=[DataRequired(message=u'Обязательное поле')])
    email = StringField(u'Email', validators=[DataRequired(message=u'Обязательное поле')])
    password = PasswordField(u'Пароль', validators=[
        DataRequired(u'Обязательное поле'),
        EqualTo('confirm', message=u'Пароли должны совпадать')
    ])
    confirm = PasswordField(u'Повторить пароль')

class FeedbackForm(Form):
    username = StringField(u'Имя', default=u'Аноним')
    message = TextAreaField(u'Ваше сообщение', validators=[DataRequired(u'Обязательное поле')])
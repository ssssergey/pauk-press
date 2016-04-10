# -*- coding: utf-8 -*-
from flask.ext.mail import Message
from app import mail
from flask import render_template
from config import ADMINS
from .decorators import async
from app import app

@async
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.html = html_body
    send_async_email(app, msg)

def feedback_notification(nickname, message):
    send_email(u"Еще один отзыв на сайте!",
               ADMINS[0],
               ADMINS,
               render_template("feedback_email.html",
                               nickname=nickname, message=message))
def download_notification(nickname, message):
    send_email(u"Очередное скачивание Паука!",
               ADMINS[0],
               ADMINS,
               render_template("feedback_email.html",
                               nickname=nickname, message=message))

def registration_notification(nickname, message):
    send_email(u"Кто-то зарегистрировался!",
               ADMINS[0],
               ADMINS,
               render_template("feedback_email.html",
                               nickname=nickname, message=message))
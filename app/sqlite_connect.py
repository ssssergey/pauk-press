# -*- coding: utf-8 -*-
import sqlite3
import datetime

def lower_case_func(s):
    return s.lower()

sqlite_path = "c:\Users\Asus\Coding_Lee\_pauk-press\pauk\pauk_db.db"

def GetbyWords(tail):
    query = u'''select article_title, article_time, rss_source, id from main where {} order by article_time desc;'''.format(tail)
    conn = sqlite3.connect(sqlite_path)
    conn.create_function("mylower", 1, lower_case_func) 
    cur = conn.cursor()
    cur.execute(query)
    DB = cur.fetchall()
    conn.close()
    posts = []
    for row in DB:
        new_row = []
        for i, item in enumerate(row):
            if item:
                if i==1:
                    item = ConvertTimeFormat(item.encode('utf-8').decode('utf-8'))
                elif i==3:
                    item = item
                else:
                    item = item.encode('utf-8').decode('utf-8')
            else:
                item = u"Пусто"
            new_row.append(item)
        posts.append(new_row)
    return posts

def GetbyWordsExercises(tail):
    query = u'''select article_title, article_time, rss_source, id from main where (mylower(article_title) like "%учени%" or 
        mylower(article_title) like "%отраб%" or mylower(article_title) like "%трениров%") and {} order by article_time desc;'''.format(tail)
    conn = sqlite3.connect(sqlite_path)
    conn.create_function("mylower", 1, lower_case_func) 
    cur = conn.cursor()
    cur.execute(query)
    DB = cur.fetchall()
    conn.close()
    posts = []
    for row in DB:
        new_row = []
        for i, item in enumerate(row):
            if item:
                if i==1:
                    item = ConvertTimeFormat(item.encode('utf-8').decode('utf-8'))
                elif i==3:
                    item = item
                else:
                    item = item.encode('utf-8').decode('utf-8')
            else:
                item = u"Пусто"
            new_row.append(item)
        posts.append(new_row)
    return posts

def GetbyCountry(strana):
    query2 = u'''select article_title, article_time, rss_source, id from main where country like "%{}%" order by article_time desc limit 100;'''.format(strana.encode('utf-8').decode('utf-8'))
    conn = sqlite3.connect(sqlite_path)
    cur = conn.cursor()
    cur.execute(query2)
    DB = cur.fetchall()
    conn.close()
    posts = []
    for row in DB:
        new_row = []
        for i, item in enumerate(row):
            if item:
                if i==1:
                    item = ConvertTimeFormat(item.encode('utf-8').decode('utf-8'))
                elif i==3:
                    item = item
                else:
                    item = item.encode('utf-8').decode('utf-8')
            else:
                item = u"Пусто"
            new_row.append(item)
        posts.append(new_row)
    return posts

def Getbyid(id):
    query = u'''select article_title, article_time, rss_source, article_text from main where id = {};'''.format(id)
    conn = sqlite3.connect(sqlite_path)
    cur = conn.cursor()
    cur.execute(query)
    row = cur.fetchone()
    conn.close()
    new_time_format = ConvertTimeFormat(row[1].encode('utf-8').decode('utf-8'))
    posts = (row[0].encode('utf-8').decode('utf-8'), 
        new_time_format, 
        row[2].encode('utf-8').decode('utf-8'), 
        row[3].encode('utf-8').decode('utf-8'))
    return posts

def ChangeCountryByid(country, id):
    # country = country.decode('utf-8-sig').encode('utf-8')
    conn = sqlite3.connect(sqlite_path)
    cur = conn.cursor()
    cur.execute(u'''update main set country=? where id=?;''', (country, id))
    conn.commit()
    conn.close()

def ConvertTimeFormat(bad_time_format):
    try:
        good_time = datetime.datetime.strptime(bad_time_format, "%Y-%m-%d %H:%M:%S")
        return good_time.strftime('%d.%m.%Y %H.%M')
    except:
        return bad_time_format



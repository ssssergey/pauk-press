WTF_CSRF_ENABLED = True
SECRET_KEY = 'jsjgidgs8etjgnxg9a3wgsklgj'



import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'pauk/pauk_db.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
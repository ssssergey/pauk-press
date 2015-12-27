from app import db

class Main(db.Model):
    rss_source = db.Column(db.TEXT)
    article_title = db.Column(db.TEXT)
    article_text = db.Column(db.TEXT)
    article_time = db.Column(db.TEXT)
    extraction_time = db.Column(db.TEXT)
    country = db.Column(db.TEXT)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    def __repr__(self):
        return '<Main %r>' % (self.article_title)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(100))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<User %r>' % (self.nickname)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)
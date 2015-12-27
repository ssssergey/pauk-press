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

from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
#import pylint_flask
from iearn import db, login_manager, app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))


class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'admin_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            admin_id = s.loads(token)['admin_id']
        except:
            return None
        return Admin.query.get(admin_id)

    # How the object is printed 
    def __repr__(self):
        return f"Admin('{ self.email }', '{ self.password }')"

class TeamMembers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(20), nullable=False)
    profile_image_file = db.Column(db.String(20), nullable=False, default='default-profile.jpg')
    image_path = db.Column(db.String(200), nullable=True)
    # How the object is print
    def __repr__(self):
        return f"TeamMembers('{ self.id }', '{ self.name }', '{ self.description }', '{ self.profile_image_file }')"


class AboutPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(600), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default-image.jpg')
    image_path = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f"AboutPost('{ self.id }', '{ self.content }', '{ self.image_file }')"

class ProjectPost(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    thumbnail = db.Column(db.String(20), nullable=False, default='default-image.jpg')
    thumbnail_path = db.Column(db.String(200), nullable=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(300), nullable=False)

    article_body = db.Column(db.String(1000), nullable=False)
    article_images = db.relationship('ArticleImages', backref='article', lazy=True)

    is_posted = db.Column(db.Boolean, default=False, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return  f"ProjectPost('{ self.id }', '{ self.title }', '{ self.is_posted }', '{ self.date_posted }')"

class ArticleImages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_file = db.Column(db.String(20), nullable=False, default='default-image.jpg')
    image_path = db.Column(db.String(200), nullable=True)
    article_id = db.Column(db.Integer, db.ForeignKey('project_post.id'), nullable=False)

    def __repr__(self):
        return f"ArticleImages('{ self.id }', '{ self.image_file }', '{ self.image_path }')"

class TemporaryImg(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_file = db.Column(db.String(20), nullable=False, default='default-image.jpg')
    image_path = db.Column(db.String(200), nullable=True)
    

    def __repr__(self):
        return f"TemporaryImg('{ self.id }', '{ self.image_file }', '{ self.image_path }')"

class MediaLinks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    web_name = db.Column(db.String(20), nullable=False)
    web_link = db.Column(db.String(250), nullable=False)
    
    def __repr__(self):
        return  f"MediaLinks('{ self.id }', '{ self.web_name }', '{ self.web_link }')"

class Contacts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(50), nullable=False)
    
    def __repr__(self):
        return  f"Contacts('{ self.id }', '{ self.content }')"

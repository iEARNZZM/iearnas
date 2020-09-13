import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#import pymysql                            # Database
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail

app = Flask(__name__)

app.config['SECRET_KEY'] = '3a4ca2f2d90e63d9449024d768d189ed'
# enable CSRF protection for article images
app.config['CKEDITOR_ENABLE_CSRF'] = True
# Connect to the database (dialect+driver://username:password@host:port/database(schema))
#app.config['SQLALCHEMY_DATABASE_URI'] = 'pymysql+mysql://root:iearnroot@localhost/website_db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# Configuration for CKEditor
app.config['CKEDITOR_FILE_UPLOADER'] = 'upload'
app.config['CKEDITOR_SERVE_LOCAL'] = True
# Configuration for Mail
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'just.kaulakis@gmail.com'
app.config['MAIL_PASSWORD'] = 'Justas.3.Kaulakis'





# SQLAlchemy Database and other instances
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
ckeditor = CKEditor(app)
csrf = CSRFProtect(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = u"Prašome prisijungti, norint pasiekti šį puslapį."
login_manager.login_message_category = "info"
mail = Mail(app)


from iearn import routes
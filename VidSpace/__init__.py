from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)

# main app configs
app.config['SECRET_KEY'] = 'a88d5845a420df12486e8d1e4e917a44'

# mysql config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'ashutosh'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'vidspace'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# upload configs
# UPLOAD_FOLDER = '/home/ashutosh/PycharmProjects/VidSpace/VidSpace/uploads/videos/'
UPLOAD_FOLDER = '/home/ashking/Documents/VidSpace/VidSpace/static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 4096 * 1024 * 1024

from VidSpace import routes
from VidSpace import misc
from VidSpace import client
from VidSpace import comments
from VidSpace import misc_adv

def get_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute('''SELECT first_name FROM users WHERE _uid = %s''', [user_id])
    data = cur.fetchone()
    return data


app.jinja_env.globals.update(get_user=get_user)
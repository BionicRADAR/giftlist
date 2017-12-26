from flask import Flask, request, url_for, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test/db'
db = SQLAlchemy(app)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/bye')
def goodbye_cruel_world():
    return 'Goodbye, cruel world!'

@app.route('/add', methods=['POST'])
def add_user():
    return 'Weclome, %s' % request.form['username']

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    
    def __repr__(self):
        return '<User %r>' % self.username

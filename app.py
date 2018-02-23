from flask import Flask, request, url_for, render_template, redirect, flash, session, make_response
from flask_sqlalchemy import SQLAlchemy
from hashlib import sha256
from functools import wraps
import random

app = Flask(__name__)

POSTGRES = {
    'user': 'postgres',
    'pw': 'password',
    'db': 'giftlistdb',
    'host': 'localhost',
    'port': '5432'
}
app.config['DEBUG'] = True
app.secret_key = 'secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

salt = "ADGHi3298h2f2h@#%@(awhg9"
cookiename = 'gift_list_session_cookie'

#Here is stuff that could go in models.py
db = SQLAlchemy()
#end models.py


db.init_app(app)

def check_session(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if Session.query.filter_by(hashid=request.cookies.get(cookiename)).all():
            return f(*args, **kwargs)
        flash("Error: not logged in")
        return redirect(url_for('login'))
    return decorated

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/bye')
def goodbye_cruel_world():
    resp = make_response('Goodbye, cruel world!')
    resp.set_cookie(cookiename, expires=0)
    return resp

@app.route('/add', methods=['POST'])
def add_user():
    #if user not in table, add the user to the users table
    if not User.query.filter_by(username=request.form['username']).all():
        newUser = User(username=request.form['username'], password=sha256(salt + request.form['password']).hexdigest())
        db.session.add(newUser)
        db.session.commit()
        return make_session(newUser.id)
    else:
        flash('Error: user with that name already exists.')
        return redirect(url_for('login'))

def make_session(userid):
    hashid = hex(random.getrandbits(128))[2:-1]
    newSession = Session(hashid=hashid, user_id=userid)
    db.session.add(newSession)
    db.session.commit()
    resp = make_response(redirect(url_for('user_list')))
    resp.set_cookie(cookiename, hashid)
    return resp

@app.route('/add_session', methods=['POST'])
def add_session():
    user = User.query.filter_by(username=request.form['username']).first()
    if user:
        if user.password == sha256(salt + request.form['password']).hexdigest():
            return make_session(user.id)
        else:
            flash('Error: incorrect password')
            return redirect(url_for('login'))
    else:
        flash('Error: no user exists with that name.')
        return redirect(url_for('login'))

@app.route('/user/<int:userid>')
@check_session
def user_page(userid):
    user = User.query.filter_by(id=userid).first()
    return render_template('userpage.html', lists=user.lists, userid=userid, username=user.username)

@app.route('/user/<int:userid>/addedlist', methods=['POST'])
@check_session
def add_list(userid):
    user = User.query.filter_by(id=userid).first()
    newList = Wishlist(name=request.form['newlist'],user_id=user.id)
    db.session.add(newList)
    db.session.commit()
    return redirect(url_for('list_page', userid=userid, listid=newList.id), code=302, Response=None)

@app.route('/user/<int:userid>/removedlist', methods=['POST'])
@check_session
def remove_list(userid):
    user = User.query.filter_by(id=userid).first()
    listId = request.args.get('id', '')
    removedList = Wishlist.query.filter_by(id=listId).first()
    db.session.delete(removedList)
    db.session.commit()
    return redirect(url_for('user_page', userid=userid), code=302, Response=None)

@app.route('/user/<int:userid>/list/<int:listid>')
@check_session
def list_page(userid, listid):
    wishlist = Wishlist.query.filter_by(id=listid).first()
    return render_template('listpage.html', items=wishlist.items, listid=listid, userid=userid, wishlist=wishlist)

@app.route('/user/<int:userid>/list/<int:listid>/addeditem', methods=['POST'])
@check_session
def add_item(userid, listid):
    wishlist = Wishlist.query.filter_by(id=listid).first()
    newItem = Item(name=request.form['newitem'],list_id=wishlist.id)
    db.session.add(newItem)
    db.session.commit()
    return redirect(url_for('list_page', userid=userid, listid=listid), code=302, Response=None)

@app.route('/user/<int:userid>/list/<int:listid>/removeditem', methods=['POST'])
@check_session
def remove_item(userid, listid):
    wishlist = User.query.filter_by(id=listid).first()
    itemId = request.args.get('id', '')
    removedItem = Item.query.filter_by(id=itemId).first()
    db.session.delete(removedItem)
    db.session.commit()
    return redirect(url_for('list_page', userid=userid, listid=listid), code=302, Response=None)

@app.route('/users')
@check_session
def user_list():
    return render_template('users.html', users=User.query.all())

def get_username(user):
    return user.username

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    lists = db.relationship('Wishlist', backref='users', lazy=True, cascade="all, delete-orphan")
    password = db.Column(db.String(64), nullable=False)
    
    def __repr__(self):
        return '<User %r>' % self.username

class Wishlist(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), nullable=False)
	items = db.relationship('Item', backref='wishlist', lazy=True, cascade="all, delete-orphan")
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
			nullable=False)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    list_id = db.Column(db.Integer, db.ForeignKey('wishlist.id'),
            nullable=False)

class Session(db.Model):
    hashid = db.Column(db.String(64), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

if __name__ == '__main__':
    app.run()

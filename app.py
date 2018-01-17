from flask import Flask, request, url_for, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

POSTGRES = {
    'user': 'postgres',
    'pw': 'password',
    'db': 'giftlistdb',
    'host': 'localhost',
    'port': '5432'
}
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

#Here is stuff that could go in models.py
db = SQLAlchemy()

class BaseModel(db.Model):
    """Base data model for all objects"""
    __abstract__ = True
    #define here __repr__ and json methods or any common method
    #that you need for all your models

class User(BaseModel):
    """model for one of your tables"""
    __tablename__ = 'users'
    #define your model
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)

#end models.py


db.init_app(app)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/bye')
def goodbye_cruel_world():
    return 'Goodbye, cruel world!'

@app.route('/add', methods=['POST'])
def add_user():
    #if user not in table, add the user to the users table
    print('%s') % User.query.filter_by(username=request.form['username']).all()
    if not User.query.filter_by(username=request.form['username']).all():
        newUser = User(username=request.form['username'])
        db.session.add(newUser)
        db.session.commit()
        return 'Weclome, new user %s' % request.form['username']
    else:
        return 'Weclome back, %s' % request.form['username']

@app.route('/userpage')
def user_page():
    user = User.query.filter_by(username='one').first()
    return render_template('userpage.html', items=user.items)

@app.route('/addeditem', methods=['POST'])
def add_item():
    user = User.query.filter_by(username='one').first()
    newItem = Item(name=request.form['newitem'],user_id=user.id)
    db.session.add(newItem)
    db.session.commit()
    return redirect('/userpage', code=302, Response=None)

@app.route('/userlist')
def user_list():
    #list all users
    return '%s' % map(get_username, User.query.all());

def get_username(user):
    return user.username;

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    items = db.relationship('Item', backref='user', lazy=True)
    
    def __repr__(self):
        return '<User %r>' % self.username

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
            nullable=False)

if __name__ == '__main__':
    app.run()

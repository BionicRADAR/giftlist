from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/bye')
def goodbye_cruel_world():
    return 'Goodbye, cruel world!'

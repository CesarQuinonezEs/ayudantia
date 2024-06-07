from flask import Flask

app = Flask(__name__)

@app.route('/hola')
def running():
    return 'Hello from flask'


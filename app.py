from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/teste")
def teste():
    return render_template('teste.html')

if __name__ == '__main__':
    app.run()



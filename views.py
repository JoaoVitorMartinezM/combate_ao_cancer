from flask import render_template

from app import app


@app.route('/formulario')
def cadastraJogo():
    return render_template("index.html"), 200

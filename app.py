from datetime import date

from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Session
from sqlalchemy.sql.operators import exists
from flask_mail import Mail, Message

from models import *

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='justdatascientist@gmail.com',
    MAIL_PASSWORD='ailz zlai icxk quko'
)
mail = Mail(app)
mail.connect()


@app.route("/enviado")
def hello():
    return render_template("index.html")


@app.route('/formulario')
def formulario():
    return render_template("index.html"), 200


@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == "POST":
        full_name = request.form["full_name"]
        age = request.form["date"]
        sex = request.form["sexo"]
        ano = age.split("-")
        age = date.today().year - int(ano[0])
        user_mail = request.form["email"]
        listDiseases = ["diabetes", "hipotirioidismo", "hipertensao", "outro", "HIV", "lupus"]
        has_disease = ""
        for disease in listDiseases:
            try:
                has_disease += request.form[disease] + " "
            except:
                print(disease + " não selecionado pelo usuário.")
        smoke = True if request.form["habitos-sociais-1"].__eq__("fuma") else False
        quit_smoking = True if not smoke and request.form["habitos-sociais-1"].__eq__("jah-fumou") else False
        drink = True if request.form["habitos-sociais-2"].__eq__("sim-frequentemente") else False
        drink_rarely = True if not drink and request.form["habitos-sociais-2"].__eq__("bebe-raramente") else False
        have_cancer = True if request.form["historico-cancer-1"].__eq__("sim") else False
        history_of_cancer = True if request.form["historico-cancer-2"].__eq__("sim") else False
        went_dentist = True if request.form["lesoes-boca-1"].__eq__("sim") else False
        consume_mate = True if request.form["lesoes-boca-2"].__eq__("sim") else False
        sunscreen = True if request.form["lesoes-pele-1"].__eq__("sim") else False
        sunstroke = True if request.form["lesoes-pele-2"].__eq__("sim") else False
        skin_lesion = True if request.form["lesoes-pele-3"].__eq__("sim") else False

        user = User(user_mail, full_name, age, sex)
        form = Form(has_disease, smoke, quit_smoking, drink_rarely,
                    drink, have_cancer, history_of_cancer, went_dentist,
                    consume_mate, sunscreen, sunstroke, skin_lesion, user.email)

        query = db.session.query(User).filter(User.email == user.email).first()
        if not query:
            db.session.add(user)
            db.session.commit()
        db.session.add(form)
        db.session.commit()
        db.session.close()

        send_mail("hdasid", "!isdajsd")

        print(request.form)

        return redirect(url_for("formulario")), 200
    else:
        return "Método GET não permitido", 405


def send_mail(sender, recepients):
    msg = Message("Teste",
                  sender="justdatascientist@gmail.com",
                  recipients=["2002joao2002@gmail.com"])
    msg.html = "<b>TESTE 1</b>"
    mail.send(msg)
    print()
    return 'foi o email'


if __name__ == '__main__':
    app.run()

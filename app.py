from datetime import date
from enums import Score_Enum

from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from templates import replaces

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
                continue

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
        list_score = {
            'smoke-2': smoke, 'quit_smoking-1': quit_smoking, 'drink_rarely-1': drink_rarely,
            'drink-2': drink, 'have_cancer-2': have_cancer, 'history_of_cancer-1': history_of_cancer,
            'went_dentist': went_dentist,
            'consume_mate-2': consume_mate, 'sunscreen': sunscreen, 'sunstroke-2': sunstroke,
            'skin_lesion-2': skin_lesion
        }

        data_dict = {'full_name': full_name,
                     'age': age,
                     'sex': sex,
                     'has_disease': has_disease}

        query = db.session.query(User).filter(User.email == user.email).first()
        if not query:
            db.session.add(user)
            db.session.commit()
        db.session.add(form)
        db.session.commit()
        response = db.get_or_404(Form, form.id)
        db.session.close()

        data_dict.update(list_score)

        score_dict = score(response)


        send_mail("2002joao2002@gmail.com", data_dict)

        print(request.form)

        return render_template("index.html"), 200
    else:
        return "Método GET não permitido", 405


def send_mail(recipient, data):
    msg = Message("Teste",
                  sender="justdatascientist@gmail.com",
                  recipients=[recipient])

    msg.html = replaces(data)
    mail.send(msg)


def score(data):
    mouth_multiplier = 0
    mouth_multiplier += 1 if data.drink or data.drink_rarely else 0
    mouth_multiplier += 1 if data.smoke or data.quit_smoking else 0
    mouth_multiplier += 1 if data.consume_mate else 0
    cancer_multiplier = (1 if data.have_cancer else 0) + (1 if data.history_of_cancer else 0)
    skin_multiplier = (1 if data.sunstroke else 0) + (1 if data.skin_lesion else 0)
    mouth_score = (
                      Score_Enum.SMOKE.value * mouth_multiplier if data.drink or data.drink_rarely or data.smoke or data.consume_mate else 0) + \
                  (
                      Score_Enum.HAVE_CANCER.value * cancer_multiplier if data.have_cancer or data.history_of_cancer else 0) + \
                  (Score_Enum.WENT_DENTIST.value if data.went_dentist else 0)
    skin_score = (Score_Enum.SKIN_LESION.value * skin_multiplier if data.skin_lesion or data.sunstroke else 0) + \
                 (
                     Score_Enum.SUNSCREEN.value if data.sunscreen else 0) + Score_Enum.HAVE_CANCER.value * cancer_multiplier
    # base = 100
    # result = base
    # for key in iterable.keys():
    #     if key[-1] == '2' and iterable[key]:
    #         result -= base * 0.1
    #     elif key[-1] == '1' and iterable[key]:
    #         result -= base * 0.05
    #     elif iterable[key]:
    #         continue
    #     elif key[-1] != '1' and key[-1] != '2' and not iterable[key]:
    #         result -= base * 0.025
    return {
        'skin_score': skin_score,
        'mouth_score': mouth_score
    }


if __name__ == '__main__':
    app.run()

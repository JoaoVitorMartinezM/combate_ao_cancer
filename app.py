import datetime
from datetime import date

from sqlalchemy import update
from sqlalchemy.orm import backref

from enums import Score_Enum
from flask_cors import CORS, cross_origin
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from templates import replaces

from waitress import serve

app = Flask(__name__)
app.config.from_pyfile('config.py')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
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


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False)
    sex = db.Column(db.String(20), nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)

    def __init__(self, email, fullname, birthday, sex):
        self.email = email
        self.full_name = fullname
        self.birthday = birthday
        self.sex = sex


class Form(db.Model):
    __tablename__ = 'form'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=backref("user", uselist=False))
    date = db.Column(db.DateTime, nullable=False)
    has_disease = db.Column(db.String(100), nullable=True)
    smoke = db.Column(db.Boolean, nullable=False)
    quit_smoking = db.Column(db.Boolean, nullable=False)
    drink_rarely = db.Column(db.Boolean, nullable=False)
    drink = db.Column(db.Boolean, nullable=False)
    have_cancer = db.Column(db.Boolean, nullable=False)
    history_of_cancer = db.Column(db.Boolean, nullable=False)
    went_dentist = db.Column(db.Boolean, nullable=False)
    consume_mate = db.Column(db.Boolean, nullable=False)
    sunscreen = db.Column(db.Boolean, nullable=False)
    sunstroke = db.Column(db.Boolean, nullable=False)
    skin_lesion = db.Column(db.Boolean, nullable=False)

    def __init__(self, has_disease, smoke, quit_smoking, drink_rarely,
                 drink, have_cancer, history_of_cancer, went_dentist,
                 consume_mate, sunscreen, sunstroke, skin_lesion, user_mail):
        self.date = datetime.datetime.now()
        self.has_disease = has_disease
        self.smoke = smoke
        self.quit_smoking = quit_smoking
        self.drink_rarely = drink_rarely
        self.drink = drink
        self.have_cancer = have_cancer
        self.history_of_cancer = history_of_cancer
        self.went_dentist = went_dentist
        self.consume_mate = consume_mate
        self.sunscreen = sunscreen
        self.sunstroke = sunstroke
        self.skin_lesion = skin_lesion
        self.user_id = user_mail


with app.app_context():
    db.create_all()


@app.route('/formulario')
@cross_origin()
def formulario():
    return render_template("index.html"), 200


@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == "POST":
        full_name = request.form["full_name"]
        birthday = request.form["date"]
        birthday = birthday.split("-")
        sex = request.form["sexo"]
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

        user = User(user_mail, full_name, date(month=int(birthday[1]), day=int(birthday[2]), year=int(birthday[0])),
                    sex)

        list_score = {
            'smoke-2': smoke, 'quit_smoking-1': quit_smoking, 'drink_rarely-1': drink_rarely,
            'drink-2': drink, 'have_cancer-2': have_cancer, 'history_of_cancer-1': history_of_cancer,
            'went_dentist': went_dentist,
            'consume_mate-2': consume_mate, 'sunscreen': sunscreen, 'sunstroke-2': sunstroke,
            'skin_lesion-2': skin_lesion
        }

        data_dict = {'full_name': full_name,
                     'age': birthday,
                     'sex': sex,
                     'has_disease': has_disease}

        db.session.add(user)
        db.session.commit()
        query = db.session.query(User).filter_by(email=user.email, full_name=full_name).first()
        print(query.id)

        form = Form(has_disease, smoke, quit_smoking, drink_rarely,
                    drink, have_cancer, history_of_cancer, went_dentist,
                    consume_mate, sunscreen, sunstroke, skin_lesion, query.id)
        db.session.add(form)
        db.session.commit()
        response = db.get_or_404(Form, form.id)

        print(form.date)
        db.session.close()

        data_dict.update(list_score)

        score_dict = score(response)

        send_mail(user_mail, score_dict)

        print(form.user_id)

        return render_template("sucessfull.html", id=form.id), 200
    else:
        return "Método GET não permitido", 405


@app.route('/formulario/<int:id>', methods=['POST'])
def editar(id):
    if request.method == "POST":
        form = Form.query.filter_by(id=id).first()
        birthday = date.__format__(form.user.birthday, "%Y-%m-%d")
        sex = form.user.sex.__eq__("masculino")
        teste = ["diabetes", "hipertensao", "hipotirioidismo", "HIV", "lupus"]
        diseases = form.has_disease.split(" ")
        diabetes = diseases.__contains__("diabetes")
        hipertensao = diseases.__contains__("hipertensao")
        hipotirioidismo = diseases.__contains__("hipotirioidismo")
        HIV = diseases.__contains__("HIV")
        lupus = diseases.__contains__("lupus")
        outro = [elemento for elemento in diseases if elemento not in teste]
        have_other = True if len(outro) > 0 else False


        return render_template("edit_form.html", form=form, birthday=birthday, sex=sex, diabetes=diabetes,
                               hipertensao=hipertensao, hipotirioidismo=hipotirioidismo,
                               lupus=lupus, HIV=HIV, outro=outro[0], have_other=have_other)
    else:
        "Metodo não permitido"


@app.route('/atualizar', methods=['GET', 'POST'])
def atualizar():
    if request.method == "POST":
        birthday = request.form["date"]
        birthday = birthday.split("-")
        listDiseases = ["diabetes", "hipotirioidismo", "hipertensao", "outro", "HIV", "lupus"]
        has_disease = ""
        for disease in listDiseases:
            try:
                has_disease += request.form[disease] + " "
            except:
                continue
        form = Form.query.filter_by(id=request.form['form_id']).first()
        form.user.full_name = request.form["full_name"]
        form.user.birthday = date(month=int(birthday[1]), day=int(birthday[2]), year=int(birthday[0]))
        form.user.email = request.form["email"]
        form.user.sex = request.form["sexo"]

        form.has_disease = has_disease
        form.smoke = True if request.form["habitos-sociais-1"].__eq__("fuma") else False
        form.quit_smoking = True if not form.smoke and request.form["habitos-sociais-1"].__eq__("jah-fumou") else False
        form.drink = True if request.form["habitos-sociais-2"].__eq__("sim-frequentemente") else False
        form.drink_rarely = True if not form.drink and request.form["habitos-sociais-2"].__eq__(
            "bebe-raramente") else False
        form.have_cancer = True if request.form["historico-cancer-1"].__eq__("sim") else False
        form.went_dentist = True if request.form["lesoes-boca-1"].__eq__("sim") else False
        form.consume_mate = True if request.form["lesoes-boca-2"].__eq__("sim") else False
        form.sunscreen = True if request.form["lesoes-pele-1"].__eq__("sim") else False
        form.skin_lesion = True if request.form["lesoes-pele-3"].__eq__("sim") else False
        form.sunstroke = True if request.form["lesoes-pele-2"].__eq__("sim") else False
        db.session.add(form)

        response = db.get_or_404(Form, form.id)

        list_score = {
            'smoke-2': form.smoke, 'quit_smoking-1': form.quit_smoking, 'drink_rarely-1': form.drink_rarely,
            'drink-2': form.drink, 'have_cancer-2': form.have_cancer, 'history_of_cancer-1': form.history_of_cancer,
            'went_dentist': form.went_dentist,
            'consume_mate-2': form.consume_mate, 'sunscreen': form.sunscreen, 'sunstroke-2': form.sunstroke,
            'skin_lesion-2': form.skin_lesion
        }

        data_dict = {'full_name': form.user.full_name,
                     'age': birthday,
                     'sex': form.user.sex,
                     'has_disease': has_disease}

        data_dict.update(list_score)

        score_dict = score(response)

        send_mail(form.user.email, score_dict)

        db.session.commit()
        db.session.close()

        return render_template("sucessfull.html", id=request.form['form_id']), 200
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

    return {
        'skin_score': skin_score,
        'mouth_score': mouth_score
    }


if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=8080)
    app.run()

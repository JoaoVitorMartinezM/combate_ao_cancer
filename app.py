import datetime
from datetime import date
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
    email = db.Column(db.String(100), primary_key=True, autoincrement=False)
    sex = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)

    def __init__(self, email, fullname, age, sex):
        self.email = email
        self.full_name = fullname
        self.age = age
        self.sex = sex


class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, nullable=False)
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

    user_mail = db.Column(db.String(100), db.ForeignKey('user.email'), nullable=False)

    def __init__(self, has_disease, smoke, quit_smoking, drink_rarely,
                 drink, have_cancer, history_of_cancer, went_dentist,
                 consume_mate, sunscreen, sunstroke, skin_lesion, user_mail):
        self.date = datetime.date.today()
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
        self.user_mail = user_mail


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

        send_mail(user_mail, score_dict)

        print(form.user_mail)


        return render_template("sucessfull.html", id=form.id), 200
    else:
        return "Método GET não permitido", 405


@app.route('/formulario/<int:id>', methods=['POST'])
def editar(id):
    if request.method == "POST":
        form = Form.query.filter_by(id=id).first()
        print(form.have_cancer)
        return render_template("edit_form.html", form=form)
    else:
        "Metodo não permitido"


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

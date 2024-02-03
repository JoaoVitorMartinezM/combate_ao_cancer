import datetime

from app import db, app


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
        self.date = datetime.date.today().strftime('%d/%m/%y %H:%M:%S')
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
        self. sunstroke = sunstroke
        self.skin_lesion = skin_lesion
        self.user_mail = user_mail



with app.app_context():
    db.create_all()

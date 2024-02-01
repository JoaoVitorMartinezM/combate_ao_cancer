from app import db, app


class User(db.Model):
    email = db.Column(db.String(100), primary_key=True, autoincrement=False)
    sex = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)

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


with app.app_context():
    db.create_all()

from app import db, app


class User(db.Model):
    email = db.Column(db.String(100), primary_key=True, autoincrement=False)
    sex = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)


with app.app_context():
    db.create_all()

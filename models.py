from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app=Flask(__name__)
db = SQLAlchemy()
migrate = Migrate(app, db)


class Workers(db.Model):
    __tablename__ = 'workers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    surname = db.Column(db.String())
    birth_date = db.Column(db.Integer)
    
    def format(self):
       return {
      'id': self.id,
      'name': self.name,
      'surname': self.surname,
      'birth_date': self.birth_date
    }
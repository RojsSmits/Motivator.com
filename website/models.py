from . import db
from flask_login import UserMixin
from sqlalchemy import PrimaryKeyConstraint, func
#izvedo datu bāzes izkārtojumu nosaka galveno lielumu un ievades formu
class Note(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    data=db.Column(db.String(200000))
    #izveidoju funkciju kas ievietos lietāja id ziņu tabulā
    use_id=db.Column(db.Integer, db.ForeignKey('user.id'))
#izvedo datu bāzes izkārtojumu nosaka galveno lielumu un ievades formu 
class User(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(200),unique=True)
    password=db.Column(db.String(200))
    #izveido savienojumu un pievienu litotāja piezīmes
    notes=db.relationship('Note')
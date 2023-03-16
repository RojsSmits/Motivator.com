from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db=SQLAlchemy()
#izveido datubāzi
DB_NAME="database.db"
#izveido aplikāciju
def create_app():
 app=Flask(__name__)
 app.config['SECRET_KEY']='qfefwff23 qdd3ffq3'
 #norādu kur atrodas mana datubāze
 app.config['SQLALCHEMY_DATABASE_URI']=f'sqlite:///{DB_NAME}'
 #norāda kur db strādās
 db.init_app(app)


 from .views import views
 #definē kā izskatīsie un kur atrodamas adreses
 app.register_blueprint(views, url_prefix='/')

 from .models import User, Note
 from . import models
 #izveido datubāzi dokumentos
 with app.app_context():
    db.create_all()
#izveido funkciju kas atļaus login funkcija strādāt ,norāda kurā dokumentā un kurā aplikācijā viss strādās
 login_manager=LoginManager()
 login_manager.login_view='views.login_page'
 login_manager.init_app(app)

 @login_manager.user_loader
 #parādā kā tiek lādēts lietotājs
 def load_user(id):
    return User.query.get(int(id))

 return app

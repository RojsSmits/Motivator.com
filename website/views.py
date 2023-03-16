#vajadzīgie importi
from . import db
from flask import Blueprint, render_template,request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from.models import User, Note
from flask_login import login_required, login_user, logout_user, current_user
#šis imports sniedz iespēju paslēpt paroli un saglabāt to apslēptā formā datubāzē
from werkzeug.security import generate_password_hash, check_password_hash
#izveidoju ceļus uz dažādām adresēm
views=Blueprint("views",__name__)
@views.route("/")
@views.route("/home")
#nosaka to, ka logins nepieciešams
@login_required
def home():
    #parāda mājas adreses izdevi
    return render_template ("index.html")
@views.route('/music')
#nosaka to, ka logins nepieciešams
@login_required
def music_page():
    #parāda mūzikas adreses izdevi
    return render_template('music.html')
#sniedz iespēju no funkcijas nolasīt informāciju
@views.route('/info', methods=['GET','POST'])
#nosaka to, ka logins nepieciešams
@login_required
def info_page():
    #nosaka mainīgu lielumu
    word=""
    #nosaka vai informācija no lapas tiek sūtīta
    if request.method=='POST':
        #saņem vajadzīgo lielumu
        note=request.form.get('note')
        #pārbauda vai lielums ievadīts pareizi
        if len(note)<4:
            word='Message is too short!'
        #aizsūta iegūto informāciju uz datu bāzi, maina izvadīto mainīgo lielumu
        else:
            new_note=Note(data=note, use_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            word='Thank you for your input!'
    #izvada adreses izkārtojumu un mainīgo lielumu
    return render_template('info.html',notemessage=word)
#izveidoj loginin adrese norādu, ka no tās var tikt nosūtīta informācija
@views.route('/login',methods=['GET','POST'])
def login_page():
    #nosaka mainīgu lielumu
    word=""
    #nosaka vai informācija no lapas tiek sūtīta
    if request.method=='POST':
        #saņem vajadzīgo lielumus
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()
        #pārbauda stubāzē ir ievadītai lielums
        if user:
            #nolasa paslēpto paroli nosaka tās pareizumu
            if check_password_hash(user.password, password):
                #maina mainīgo lielumu
                word='Logged in successfully!'
                login_user(user, remember=True)
                #lietājs tiek aizsūtīts uz citu adresi
                return redirect(url_for('views.home'))
            else:
                #maina mainīgo lielumu
                word='Incorect password, try again!'
        #maina mainīgo lielumu
        else:
            word='Email dose not exist'
    #izvada adreses izkārtojumu un mainīgo lielumu
    return render_template('login.html',loginmessage=word)
#izveidoju sigin adrese norādu, ka no tās var tikt nosūtīta informācija
@views.route('/singin',methods=['GET','POST'])
def singin_page():
    #nosaka mainīgu lielumu
    word=""
    #nosaka vai informācija no lapas tiek sūtīta
    if request.method=='POST':
        #saņem vajadzīgo lielumus
        email=request.form.get('email')
        password1=request.form.get('password1')
        password2=request.form.get('password2')
        #pārbauda ievadītās informācijas pareizumu, maina mainīgo lilumu
        user=User.query.filter_by(email=email).first()
        if user:
            word='Email already exists!'
        elif len(email)<6:
            word='Email must contain atleast 6 characters. '
        elif password1!=password2 :
            word='Passwords do not match '
        elif len(password1)<4:
            word='Password must contain atleast 4 characters. '
        else:
            #izveido jaunu lietotāju
            new_user=User(email=email, password=generate_password_hash(password2, method="sha256"))
            #izveidotā lietotāja dati tiek aizsūtīti uz datu bāzi
            db.session.add(new_user)
            db.session.commit()
            #litotājs tie reģistrēts
            login_user(new_user, remember=True)
            word='Account created!'
            #lietājs tiek aizsūtīts uz citu adresi
            return redirect(url_for('views.home'))
    #izvada adreses izkārtojumu un mainīgo lielumu
    return render_template('signin.html', singupmessage=word)
@views.route('/logout')
#nosaka, login ir nepieciešams
@login_required
#izveido funkciju, kura izmet lietotāju no vi'ba profila
def logout():
    logout_user()
    #lietājs tiek aizsūtīts uz citu adresi
    return redirect(url_for('views.login_page'))



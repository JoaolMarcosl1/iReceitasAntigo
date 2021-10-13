from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user
from app import app, db
from app.models import User

#from  flask.ext.bcrypt  import  generate_password_hash
#pw_hash  =  generate_password_hash ( 'hunter2' ,  10 )
#from  flask  import  Flask
#from  flask.ext.bcrypt  import  Bcrypt
#app  =  Flask ( __name__ )
#bcrypt  =  Bcrypt ( app )

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        pwd = request.form['password']

        user = User(name, email, pwd)
        db.session.add(user) #inserir
        db.session.commit()  #atualiza

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        pwd = request.form['password']

        user = User.query.filter_by(email=email).first()

        if not user or not user.verify_password(pwd):
            return redirect(url_for('login'))

        login_user(user)
        return redirect(url_for('home'))

    return render_template('login.html')

#sair da conta
#from flask_login import logout_user
#@app.route("/logout")
#def logout():
  #  logout_user()
   # return redirect(somewhere)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)

from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user
from app import app, db
from app.models import User


#from  flask.ext.bcrypt  import  generate_password_hash
#pw_hash  =  generate_password_hash ( 'hunter2' ,  10 )
#from  flask  import  Flask
#from  flask.ext.bcrypt  import  Bcrypt
#app  =  Flask ( __name__ )
#bcrypt  =  Bcrypt ( app )

@app.route('/home')
@app.route('/')
def home():
    return render_template("home.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        pwd = request.form['password']

        user = User(name, email, pwd)
        db.session.add(user) #inserir
        db.session.commit()  #atualiza

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        pwd = request.form['password']

        user = User.query.filter_by(email=email).first()

        if not user or not user.verify_password(pwd):
            flash("Email ou senha inválidos!")
            return redirect(url_for('login'))

        login_user(user)
        flash('You were successfully logged in')
        return redirect(url_for('home'))

    return render_template('login.html')

#####
#@app.route("/lista")
#@login_manager.user_loader
#def load_user(id):


 #   return render_template("lista.html")
#@login_manager.user_loader
#def load_user(user_id):
  #  try:
 #       return User.query.get(user_id)
  #  except:
   #     return None

#####

#Alteração de dados
@app.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    user = User.query.get(id)
    if request.method == 'POST':
        user.name = request.form['name']
        user.email = request.form['email']
        db.session.commit()

        return redirect(url_for('home'))
    return render_template("edit.html", user=user)
#Deletar conta
@app.route("/delete/<int:id>", methods=['GET', 'POST'])
def delete(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return redirect(url_for("home"))

#@app.route("/alterar_senha/<int:id>", methods=['GET', 'POST'])
#def alterar_senha(id):
  #  user = User.query.get(id)
  #  if request.method == 'POST':
        #if not user or not user.verify_password(pwd):
         #   flash("Email ou senha inválidos!")
         #   return redirect(url_for('login'))


       # return redirect(url_for('login'))




@app.get('/usuario/<email>')
def usu_email(email):
    return str(User.query.filter_by(email=email).first())

#@app.route('/perfil/<id>')
#def perfil(id):
  #  return render_template("perfil_user.html")

@app.errorhandler(404)#Caso usuário acesse uma pagina que não existe
def not_found(e):
  return render_template("404.html")

@app.route('/topicos')
def topicos():
    return render_template("topicos.html")

@app.route('/contato')
def contato():
    return render_template("contato.html")

@app.route('/perfil')
def perfil():
    return render_template("perfil_user.html")


@app.route('/logout')
def logout():
    logout_user()
    flash('You were logged out')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)

from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from app import app, db
from app.models import User
from flask_mail import Mail, Message
from sqlalchemy.exc import IntegrityError

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL']= True
app.config['MAIL_USE_TLS']= False
app.config['MAIL_USERNAME'] = 'receitasprojetoint@gmail.com'
app.config['MAIL_PASSWORD'] = 'receitas2021proj'

mail = Mail(app)


#from  flask.ext.bcrypt  import  generate_password_hash
#pw_hash  =  generate_password_hash ( 'hunter2' ,  10 )
#from  flask  import  Flask
#from  flask.ext.bcrypt  import  Bcrypt
#app  =  Flask ( __name__ )
#bcrypt  =  Bcrypt ( app )
@app.route('/home')
@app.route('/')
#@login_manager

def home():
    if not current_user.is_authenticated:
        flash("\nVocê não esta logado.")
    else:
        flash(f"\n\nOlá {current_user.name}, seja bem vindo(a).")

    return render_template("home.html")

@app.route('/massas')
def massas():
    return render_template("MassasCarrossel.html")

@app.route('/comidasfit')
def comidasfit():
    return render_template("ComidasFitnessCarrossel.html")

@app.route('/sobremesas')
def sobremesas():
    return render_template("SobremesasCarrossel.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        pwd = request.form['password']
        sobre = ""


        jatem = User.query.filter_by(email=email).first()

        if jatem is not None:
            flash('Já existe uma conta com esse e-mail. Insira outro e-mail')
            return redirect(url_for('register'))

        else:
            user = User(name, email, pwd, sobre)
            db.session.add(user) #inserir
            db.session.commit()  #atualiza
            flash('Conta criada com sucesso!')
            return redirect(url_for('login'))


    return render_template('register.html')

@app.route('/contato', methods=['GET', 'POST'])
def contato():
    if request.method == 'POST':
        tittle = request.form.get('tittle')
        message = request.form.get('message')

        #message = message+f"\nReperquilson se garante mais que o {current_user.name}"

        msg = Message(subject=f"Help {current_user.name}: {tittle}", body=f"\n{current_user.name}: {message}",
                      sender="joaobastos716@gmail.com", recipients=["receitasprojetoint@gmail.com"])

        mail.send(msg)
        flash("Sua mensagem foi enviada com sucesso!")

        #msg = Message("Olá, Estou precisando da ajuda de vocês.", sender="joaobastos716@gmail.com", recipients=["receitasprojetoint@gmail.com"])
        #msg.body = "Enviando uma duvida, testando"
        #mail.send(msg)
        return redirect(url_for('home'))


    return render_template("contato.html")

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
        flash('Você foi logado com sucesso :)\n')
        return redirect(url_for('home'))

    return render_template('login.html')

#Alteração de dados

@app.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    user = User.query.get(id)
    if request.method == 'POST':

        user.name = request.form['name']
        user.email = request.form['email']
        user.sobre = request.form['sobre']

        try:
            db.session.commit()
            flash("Alteração feita com sucesso!")
            return redirect(url_for('home'))

        except IntegrityError:
            flash("Opa! Esse e-mail ja esta sendo utilizado.")
            return redirect(url_for('perfil'))

            #return "E-mail existe"
            #db.session.commit()
           # return "Deu certo, você mudou o e-mail"
       # db.session.commit()
       # return redirect(url_for('home'))
        #jatem = User.query.filter_by(email=user.email).first()
       # if jatem is not None:
           # return "E-mail existe"
      #  else:
    return render_template("edit.html", user=user)


#Deletar conta
@app.route("/delete/<int:id>", methods=['GET', 'POST'])
def delete(id):
    user = User.query.get(id)

    db.session.delete(user)
    db.session.commit()

    return redirect(url_for("home"))


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

@app.route('/perfil')
def perfil():
    if not current_user.is_authenticated:
        flash("\nSomente quem esta logado pode acessar o seu perfil.")
    else:
        flash(".")
    return render_template("perfil_user.html")


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)

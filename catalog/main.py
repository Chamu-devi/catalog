from flask import Flask,redirect,url_for,render_template,request,flash
from flask_mail import Mail,Message
from random import randint
from project_database import Register,Base,User
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from flask_login import LoginManager,login_user,current_user,logout_user,login_required,UserMixin


engine=create_engine('sqlite:///iii.db')
engine=create_engine('sqlite:///iii.db',connect_args={'check_same_thread':False},echo=True)
Base.metadata.bind=engine
DBsession=sessionmaker(bind=engine)
session=DBsession()


app=Flask(__name__)

login_manager=LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category='info'


app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']='venkatapavani.vegi@gmail.com'
app.config['MAIL_PASSWORD']='pavanigrace'
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True

app.secret_key='abc'

mail=Mail(app)
otp=randint(000000,999999)

@app.route("/sample")
def demo():
	return "Hello World welcome iiit"

@app.route("/demo")
def dem():
	return"<h1>Hello Demo Page</h1>"

@app.route("/info/details")
def det():
	return"hello details"

@app.route("/details/<name>/<int:age>/<float:salary>")
def info(name,age,salary):
	return" Nmae: {} age: {} salary: {}".format(name,age,salary)

@app.route("/student")
def s():
	return "hello student"

@app.route("/admin")
def a():
	return "Hello Admin"

@app.route("/staff")
def st():
	return "Hello satff"

@app.route("/infos/<name>")
def admin_info(name):
	if name=="admin":
		return redirect(url_for("a"))
	elif name=="student":
		return redirect(url_for("s"))
	elif name=="staff":
		return redirect(url_for("st"))
	else:
		return "NO URL"

		
@app.route("/data/<name>/<int:age>/<float:sal>")
def demo_html(name,age,sal):
	return render_template("sample.html",n=name,a=age,s=sal)

@app.route("/infotable")
def tab():
	sno=28
	name="pavani"
	branch="trainer"
	dept="cse"
	return render_template("table.html",s=sno,n=name,b=branch,d=dept)
#reading multiple records

data=[{'sno':123,'name':'pavani','branch':'cse','dept':'trainer'},
{'sno':12,'name':'Avani','branch':'it','dept':'developer'}]
@app.route("/dummy_data")
def dummy():
	return render_template("data.html",multiple=data)

#table printing
@app.route("/table/<int:no>")
def table(no):
	return render_template("five.html",n=no)

#file upload
@app.route("/file_upload",methods=['GET','POST'])
def file_upload():
	return render_template("file_upload.html")
@app.route("/success",methods=['GET','POST'])
def success():
	if request.method=='POST':
		f=request.files['file']
		f.save(f.filename)

		return render_template("success.html", f_name=f.filename)

@app.route("/email", methods=['POST','GET'])
def email_send():
	return render_template("email.html")

@app.route("/email_verify",methods=['POST','GET'])
def verify_email():
	email=request.form['email']
	msg=Message("one Time Password",sender="venkatapavani.vegi@gmail.com",recipients=[email])
	msg.body=str(otp)
	mail.send(msg)
	return render_template("v_email.html")

@app.route("/email_success",methods=['POST','GET'])
def success_email():
	user_otp=request.form['otp']
	if otp==int(user_otp):
		return render_template("email_success.html")
	return "invalid otp"

@app.route("/page")
def index():
	return render_template("index1.html")


@app.route("/show")
@login_required
def showdata():
	register=session.query(Register).all()
	return render_template('show.html',reg=register)

@app.route("/new",methods=['POST','GET'])
def adddata():
	if request.method=='POST':
		newData=Register(name=request.form['name'],
			sur_name=request.form['sur_name'],
			mobile=request.form['mobile'],
			email=request.form['email'],
			branch=request.form['branch'],
			role=request.form['role'])
		session.add(newData)
		session.commit()
		flash("New Data Added...")
		return redirect(url_for('showdata'))
	else:
		return render_template('new.html')


@app.route("/edit/<int:register_id>",methods=['POST','GET'])
def editdata(register_id):
	editedData=session.query(Register).filter_by(id=register_id).one()
	if request.method=='POST':
		editedData.name=request.form['name']
		editedData.sur_name=request.form['sur_name']
		editedData.mobile=request.form['mobile']
		editedData.email=request.form['email']
		editedData.branch=request.form['branch']
		editedData.role=request.form['role']

		session.add(editedData)
		session.commit()
		flash("Data is Edited...{}".format(editedData.name))

		return redirect(url_for('showdata'))
	else:
		return render_template('edit.html',register=editedData)

@app.route("/delete/<int:register_id>",methods=['POST','GET'])
def deletedata(register_id):
	deletedData=session.query(Register).filter_by(id=register_id).one()
	if request.method=='POST':
		session.delete(deletedData)
		session.commit()
		flash("Data Deleted Successfully....{}".format(deletedData.name))

		return redirect(url_for('showdata'))
	else:
		return render_template('delete.html',register=deletedData)

@app.route("/account",methods=['POST','GET'])
@login_required
def account():
	return render_template("account.html")

@app.route("/register",methods=['POST','GET'])
def register():
	if request.method=='POST':
		userData=User(name=request.form['name'],
			email=request.form['email'],
			password=request.form['password'])
		session.add(userData)
		session.commit()
		return redirect(url_for('index'))
	else:
		return render_template('register.html')

@login_required
@app.route("/login",methods=['POST','GET'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('showdata'))
	try:
		if request.method=='POST':
			user=session.query(User).filter_by(email=request.form['email'],password=request.form['password']).first()
		
			if user:
				login_user(user)
				return redirect(url_for('showdata'))
			else:
				flash("Inavalid Login...")
		else:
			return render_template('login.html',title='login')
	except Exception as e:
		flash("Login Failed...")

	else:
		return render_template('login.html',title='login')

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('index'))

@login_manager.user_loader
def load_user(user_id):
	return session.query(User).get(int(user_id))

if __name__=='__main__':
	app.run(debug=True)
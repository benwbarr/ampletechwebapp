from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_bootstrap import Bootstrap
from flaskext.mysql import MySQL
import sys
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import babel
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, login_manager, login_required, logout_user, current_user, LoginManager
from flask_mail import Mail, Message
from datetime import datetime
import os
from webforms import (LoginForm, UserForm, WDForm, PostAuditDismantleForm, WholesaleEWasteReceivingForm,
					WholesaleClientShippingForm, EWasteClientShippingForm, PasswordForm, RequestResetForm, ResetPasswordForm,
					  pickForm, auditForm, preauditForm, ITADSortForm, InventoryWSForm)
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
sys.setrecursionlimit(2000)




#Flask Instance
app = Flask(__name__)

#add database
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://benwebwd:w8TBX&MsZvC&F92Qc9Fa9c@10.104.1.52/wd"
#secret key
app.config['SECRET_KEY'] = "super secret key"
#Initialize the database
Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
app.config['MAIL_SERVER'] = 'smtp.sendgrid.net'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'apikey'
app.config['MAIL_PASSWORD'] = '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'
app.config['MYSQL_USERNAME'] = 'apikey'
app.config['MYSQL_PASSWORD'] = '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'
mail = Mail(app)


app.config['MYSQL_DATABASE_USER'] = 'benwebwd'
app.config['MYSQL_DATABASE_PASSWORD'] = 'w8TBX&MsZvC&F92Qc9Fa9c'
app.config['MYSQL_DATABASE_DB'] = 'wd'
app.config['MYSQL_DATABASE_HOST'] = '10.104.1.52'
mail = Mail(app)

mysql = MySQL()
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
	return Users.query.get(int(user_id))



class Users(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), nullable=False, unique=True)
	name = db.Column(db.String(200), nullable=False)
	email = db.Column(db.String(120), nullable=False, unique=True)
	department = db.Column(db.String(200), nullable=False)
	level = db.Column(db.String(50), nullable=True)
	password_hash = db.Column(db.String(128))

	def get_reset_token(self, expires_sec=1800):
		s = Serializer(app.config['SECRET_KEY'], expires_sec)
		return s.dumps({'user_id': self.id}).decode('utf-8')

	@staticmethod
	def verify_reset_token(token):
		s = Serializer(app.config['SECRET_KEY'])
		try:
			user_id = s.loads(token)['user_id']
		except:
			return None
		return Users.query.get(user_id)

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute!')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return '<Name %r>' % self.Name



class WD(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	Company_Name = db.Column(db.String(100), nullable=False)
	SO = db.Column(db.String(50), nullable=False)
	Pallet = db.Column(db.Integer, nullable=False)
	Shipping = db.Column(db.String(50), nullable=False)
	Length = db.Column(db.Integer, nullable=False)
	Width = db.Column(db.Integer, nullable=False)
	Height = db.Column(db.Integer, nullable=False)
	Weight = db.Column(db.Integer, nullable=False)
	Total_Weight = db.Column(db.Integer, nullable=False)
	Status = db.Column(db.String(50), nullable=False)
	date = db.Column(db.Date, nullable=True)
	date_added = db.Column(db.DateTime, default=datetime.utcnow)

	#Create A String
	def __repr__(self):
		return 'WD %r>' % self.Company_Name



@app.route('/login', methods =['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = Users.query.filter_by(username= form.username.data).first()
		if user:
			if check_password_hash(user.password_hash, form.password.data):
				login_user(user)
				flash("Login Succesfull!")
				return redirect(url_for('dashboard'))
			else:
				flash("Wrong Password - Try Again!")
		else:
			flash("That User Doesn't Exist! Try Again!")


	return render_template('login.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
	logout_user()
	flash("You Have Logged Out!")
	return redirect(url_for('login'))

@app.route('/dashboard', methods =['GET', 'POST'])
@login_required
def dashboard():

	return render_template('dashboard.html')





@app.route('/User_update/<int:id>', methods=['GET', 'POST'])
@login_required
def User_update(id):
	form= UserForm()
	name_to_update = Users.query.get_or_404(id)
	if request.method == "POST":
		name_to_update.name = request.form['name']
		name_to_update.email = request.form['email']
		name_to_update.username = request.form['username']
		try:
			db.session.commit()
			flash("User Updated")
			return render_template("dashboard.html",
								   form = form,
								   name_to_update = name_to_update,
								   id=id)
		except:
			flash("Error User Not Updated")
			return render_template("User_update.html",
								   form=form,
								   name_to_update=name_to_update,
								   id=id)
	else:
		return render_template("User_update.html",
							   form=form,
							   name_to_update=name_to_update,
							   id=id)







@app.route('/WD_update/<int:id>', methods=['GET', 'POST'])
@login_required
def WD_update(id):
	Company_Name = None
	SO = None
	Pallet = None
	Shipping = None
	Length = None
	Width = None
	Height = None
	Weight = None,
	Total_Weight = None
	Status = None
	Date = None
	form = WDForm()
	WD_to_update = WD.query.get_or_404(id)
	if form.validate_on_submit():
		Company_Name = form.Company_Name.data
		SO = form.SO.data
		Pallet = form.Pallet.data
		Shipping = form.Shipping.data
		Length = form.Length.data
		Width = form.Width.data
		Height = form.Height.data
		Weight = form.Weight.data
		Total_Weight = form.Total_Weigh.data
		Status = form.Status.data
		Date = form.Date.data
		form.Company_Name.data = ""
		form.SO.data = ""
		form.Status.data = ""
		form.Pallet = ""
		form.Shipping = ""
		form.Length = ""
		form.Width = ""
		form.Height = ""
		form.Total_Weigh = ""
		form.Status = ""
		form.Date = ""
	if request.method == "POST":
		WD_to_update.Company_Name = request.form['Company_Name']
		WD_to_update.SO = request.form['SO']
		WD_to_update.Pallet = request.form['Pallet']
		WD_to_update.Shipping = request.form['Shipping']
		WD_to_update.Length = request.form['Length']
		WD_to_update.Width = request.form['Width']
		WD_to_update.Height = request.form['Height']
		WD_to_update.Total_Weight = request.form['Total_Weight']
		WD_to_update.Status = request.form['Status']
		WD_to_update.Date = request.form['Date']
		try:
			db.session.commit()
			flash(" Updated Successfuly!")
			return render_template("WD_update.html",
				form=form,
				Company_Name=Company_Name,
				SO = SO,
				Pallet= Pallet,
				Shipping = Shipping,
				Length = Length,
				Width = Width,
				Height = Height,
				Weight = Weight,
				Total_Weight = Total_Weight,
				Status= Status,
				Date= Date,
				WD_to_update = WD_to_update)

		except:
			flash("ERROR!! W&D Not Updated")
			return render_template("WD_update.html",
				form=form,
				Company_Name=Company_Name,
				SO=SO,
				Pallet=Pallet,
				Shipping=Shipping,
				Length=Length,
				Width=Width,
				Height=Height,
				Weight=Weight,
				Total_Weight=Total_Weight,
				Status=Status,
				Date=Date,
				WD_to_update=WD_to_update)

	else:
		return render_template("WD_update.html",
			   form=form,
			   Company_Name=Company_Name,
			   SO=SO,
			   Pallet=Pallet,
			   Shipping=Shipping,
			   Length=Length,
			   Width=Width,
			   Height=Height,
			   Weight=Weight,
			   Total_Weight=Total_Weight,
			   Status=Status,
			   Date=Date,
			   WD_to_update=WD_to_update)


@app.route('/delete/<int:id>')
def delete(id):
	wd_to_delete = WD.query.get_or_404(id)
	Company_Name = None
	SO = None
	Pallet = None
	Shipping = None
	Length = None
	Width = None
	Height = None
	Weight = None
	Total_Weight = None
	date = None
	Status = None
	form = WDForm()
	try:
		db.session.delete(wd_to_delete)
		db.session.commit()
		flash("Deleted Successfully")

		our_wds = WD.query.order_by(WD.date_added)
		return render_template("add_WD.html",
	    form=form,
	    Company_Name=Company_Name,
	    SO=SO,
	    Pallet=Pallet,
	    Shipping=Shipping,
	    Length=Length,
	    Width=Width,
	    Height=Height,
	    Weight=Weight,
	    Total_Weight=Total_Weight,
	    date=date,
	    Status=Status,
	    our_wds=our_wds)

	except:
		flash("Error Could Not Delete!")
		return render_template("add_WD.html",
							   form=form,
							   Company_Name=Company_Name,
							   SO=SO,
							   Pallet=Pallet,
							   Shipping=Shipping,
							   Length=Length,
							   Width=Width,
							   Height=Height,
							   Weight=Weight,
							   Total_Weight=Total_Weight,
							   date=date,
							   Status=Status,
							   our_wds=our_wds)





#Route decorator
@app.route('/WD/add', methods=['GET','POST'])
@login_required
def add_WD():
	Company_Name = None
	SO = None
	Pallet = None
	Shipping = None
	Length = None
	Width = None
	Height = None
	Weight = None
	Total_Weight = None
	date = None
	Status = None
	form = WDForm()
	if form.validate_on_submit():
		wd = WD(Company_Name=form.Company_Name.data,
				SO=form.SO.data,
				Pallet=form.Pallet.data,
				Shipping=form.Shipping.data,
				Length=form.Length.data,
				Width=form.Width.data,
				Height=form.Height.data,
				Weight=form.Weight.data,
				Total_Weight=form.Total_Weight.data,
				date=form.date.data,
				Status=form.Status.data)
		db.session.add(wd)
		db.session.commit()
	Company_Name = form.Company_Name.data
	form.Company_Name.data = ''
	SO = form.SO.data
	form.SO.data = ''
	Pallet = form.Pallet.data
	form.Pallet.data = ''
	Shipping = form.Shipping.data
	form.Shipping.data = ''
	Length = form.Length.data
	form.Length.data = ''
	Width = form.Width.data
	form.Width.data = ''
	Height = form.Height.data
	form.Height.data = ''
	Weight = form.Weight.data
	form.Weight.data = ''
	Total_Weight = form.Total_Weight.data
	form.Total_Weight.data = ''
	date = form.date.data
	form.date.data = ''
	Status = form.Status.data
	form.Status.data = ''
	our_wds =WD.query.order_by(WD.date_added)
	if Shipping == "Domestic" and Height >= 71:
		flash("Domestic Sipping Height Can't Be Over 72!!!")
	if Shipping == "International" and Height >= 91:
		flash("International Sipping Height Can't Be Over 90!!!")
	return render_template("add_WD.html",
						   form = form,
						   Company_Name=Company_Name,
						   SO=SO,
						   Pallet=Pallet,
						   Shipping=Shipping,
						   Length=Length,
						   Width=Width,
						   Height=Height,
						   Weight=Weight,
						   Total_Weight=Total_Weight,
						   date=date,
						   Status=Status,
						   our_wds=our_wds)

@app.route('/CompleteWD', methods=['GET','POST'])
@login_required
def CompleteWD():
	#Grab all W&Ds from DB
	page = request.args.get('page',1, type=int)
	WDs = WD.query.order_by(WD.date_added.desc(), WD.SO.desc()).paginate(page=page, per_page=10)
	return render_template("CompleteWD.html", WDs=WDs)


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == "POST":
        WD = request.form['book']
        # search by author or book
        cursor.execute("SELECT id, Company_Name, SO, Shipping, date, Pallet, Length, Width, Height, Weight, Total_Weight, Status "
					   "from WD WHERE id LIKE %s OR Company_Name LIKE %s OR SO LIKE %s OR Shipping LIKE %s OR date LIKE %s"
						"OR Pallet LIKE %s OR Length LIKE %s OR Width LIKE %s OR Height LIKE %s OR Weight LIKE %s OR Total_Weight LIKE %s OR Status LIKE %s",

					   (WD, WD, WD, WD, WD, WD, WD, WD, WD, WD, WD, WD))
        conn.commit()
        data = cursor.fetchall()

        # all in the search box will return all the tuples
        if len(data) == 0 and WD == 'all':
            cursor.execute("SELECT id, Company_Name, SO, Shipping, date, Pallet, Length, Width, Height, Weight, Total_Weight, Status from WD")
            conn.commit()
            data = cursor.fetchall()
        return render_template('search.html', data=data)
    return render_template('search.html')



@app.route('/')
def index():
	return render_template("index.html")



@app.route('/InventoryRec', methods=['GET', 'POST'])
@login_required
def InventoryRec():
	JobbNumber = None
	BatchNumber = None
	PoNumber = None
	Commodity = None
	Dimms = None
	Dimms2 = None
	Dimms3 = None
	QTY = None
	NetWeight = None
	GrossWeight = None
	TareWeight = None
	Data = None
	Evaluated = None
	Date = None
	form = PostAuditDismantleForm()
	#Validate Form
	if form.validate_on_submit():
		JobbNumber = form.JobbNumber.data
		form.JobbNumber.data = ""
		BatchNumber = form.BatchNumber.data
		form.LotNumber.data = ""
		PoNumber = form.PoNumber.data
		form.PoNumber.data = ""
		QTY = form.QTY.data
		form.QTY.data = ""
		Commodity = form.Commodity.data
		form.Commodity.data = ""
		Dimms = form.Dimms.data
		form.Dimms.data = ''
		Dimms2 = form.Dimms2.data
		form.Dimms2.data = ''
		Dimms3 = form.Dimms3.data
		form.Dimms3.data = ''
		NetWeight = form.NetWeight.data
		form.NetWeight.data = ''
		GrossWeight = form.GrossWeight.data
		form.GrossWeight.data = ''
		TareWeight = form.TareWeight.data
		form.TareWeight.data = ''
		Data = form.Data.data
		form.Data.data = ""
		Evaluated = form.Evaluated.data
		form.Evaluated.data = ""
		Date = form.Date.data
		form.Data.data = ""
		return redirect(url_for('PostAuditDismantle'))

	return render_template("InventoryRec.html",
		JobbNumber=JobbNumber,
		BatchNumber=BatchNumber,
		PoNumber = PoNumber,
		Commodity = Commodity,
		Dimms=Dimms,
		Dimms2=Dimms,
		Dimms3=Dimms,
		NetWeight=NetWeight,
		GrossWeight=GrossWeight,
		TareWeight=TareWeight,
		QTY=QTY,
		Data = Data,
		Evaluated=Evaluated,
		Date = Date,
		form = form)

@app.route('/IRPrint', methods= ["POST"])

def IRPrint():
	JobNumber = request.form.get("JobNumber")
	BatchNumber = request.form.get("BatchNumber")
	PoNumber = request.form.get("PoNumber")
	Commodity = request.form.get("Commodity")
	Dimms = request.form.get("Dimms")
	Dimms2 = request.form.get("Dimms2")
	Dimms3 = request.form.get("Dimms3")
	NetWeight = request.form.get("NetWeight")
	GrossWeight = request.form.get("GrossWeight")
	TareWeight = request.form.get("TareWeight")
	QTY = request.form.get("QTY")
	Data = request.form.get("Data")
	Evaluated = request.form.get("Evaluated")
	Date = request.form.get("Date")

	return render_template("IRPrint.html",
		JobNumber=JobNumber,
		BatchNumber=BatchNumber,
		PoNumber=PoNumber,
		Commodity=Commodity,
		Dimms=Dimms,
		Dimms2=Dimms,
		Dimms3=Dimms,
		NetWeight=NetWeight,
		GrossWeight=GrossWeight,
		TareWeight=TareWeight,
		QTY=QTY,
		Data=Data,
		Evaluated=Evaluated,
		Date=Date)


@app.route('/InventoryWS', methods=['GET', 'POST'])
@login_required
def InventoryWS():
	JobbNumber = None
	BatchNumber = None
	PoNumber = None
	Commodity = None
	Dimms = None
	Dimms2 = None
	Dimms3 = None
	QTY = None
	NetWeight = None
	GrossWeight = None
	TareWeight = None
	Data = None
	Evaluated = None
	Date = None
	form = InventoryWSForm()
	#Validate Form
	if form.validate_on_submit():
		JobbNumber = form.JobbNumber.data
		form.JobbNumber.data = ""
		BatchNumber = form.BatchNumber.data
		form.LotNumber.data = ""
		PoNumber = form.PoNumber.data
		form.PoNumber.data = ""
		QTY = form.QTY.data
		form.QTY.data = ""
		Commodity = form.Commodity.data
		form.Commodity.data = ""
		Dimms = form.Dimms.data
		form.Dimms.data = ''
		Dimms2 = form.Dimms2.data
		form.Dimms2.data = ''
		Dimms3 = form.Dimms3.data
		form.Dimms3.data = ''
		NetWeight = form.NetWeight.data
		form.NetWeight.data = ''
		GrossWeight = form.GrossWeight.data
		form.GrossWeight.data = ''
		TareWeight = form.TareWeight.data
		form.TareWeight.data = ''
		Data = form.Data.data
		form.Data.data = ""
		Evaluated = form.Evaluated.data
		form.Evaluated.data = ""
		Date = form.Date.data
		form.Data.data = ""
		return redirect(url_for('PostAuditDismantle'))

	return render_template("InventoryWS.html",
		JobbNumber=JobbNumber,
		BatchNumber=BatchNumber,
		PoNumber = PoNumber,
		Commodity = Commodity,
		Dimms=Dimms,
		Dimms2=Dimms,
		Dimms3=Dimms,
		NetWeight=NetWeight,
		GrossWeight=GrossWeight,
		TareWeight=TareWeight,
		QTY=QTY,
		Data = Data,
		Evaluated=Evaluated,
		Date = Date,
		form = form)

@app.route('/IWSPrint', methods= ["POST"])

def IWSPrint():
	JobNumber = request.form.get("JobNumber")
	BatchNumber = request.form.get("BatchNumber")
	PoNumber = request.form.get("PoNumber")
	Commodity = request.form.get("Commodity")
	Dimms = request.form.get("Dimms")
	Dimms2 = request.form.get("Dimms2")
	Dimms3 = request.form.get("Dimms3")
	NetWeight = request.form.get("NetWeight")
	GrossWeight = request.form.get("GrossWeight")
	TareWeight = request.form.get("TareWeight")
	QTY = request.form.get("QTY")
	Data = request.form.get("Data")
	Evaluated = request.form.get("Evaluated")
	Date = request.form.get("Date")

	return render_template("IWSPrint.html",
		JobNumber=JobNumber,
		BatchNumber=BatchNumber,
		PoNumber=PoNumber,
		Commodity=Commodity,
		Dimms=Dimms,
		Dimms2=Dimms,
		Dimms3=Dimms,
		NetWeight=NetWeight,
		GrossWeight=GrossWeight,
		TareWeight=TareWeight,
		QTY=QTY,
		Data=Data,
		Evaluated=Evaluated,
		Date=Date)


@app.route('/ITADSort', methods=['GET', 'POST'])
@login_required
def ITADSort():
	Commodity = None
	TareWeight = None
	Data = None
	Evaluated = None
	form = ITADSortForm()
	#Validate Form
	if form.validate_on_submit():
		Commodity = form.Commodity.data
		form.Commodity.data = ""
		TareWeight = form.TareWeight.data
		form.TareWeight.data = ''
		Data = form.Data.data
		form.Data.data = ""
		Evaluated = form.Evaluated.data
		form.Evaluated.data = ""
		return redirect(url_for('ITADSort'))

	return render_template("ITADSort.html",
		Commodity = Commodity,
		TareWeight=TareWeight,
		Data = Data,
		Evaluated=Evaluated,
		form = form)

@app.route('/ITADSortPrint', methods= ["POST"])

def ITADSortPrint():
	Commodity = request.form.get("Commodity")
	TareWeight = request.form.get("TareWeight")
	Data = request.form.get("Data")
	Evaluated = request.form.get("Evaluated")

	return render_template("ITADSortPrint.html",
		Commodity=Commodity,
		TareWeight=TareWeight,
		Data=Data,
		Evaluated=Evaluated)




@app.route('/WholesaleEWasteReceiving', methods=['GET', 'POST'])
@login_required
def  WholesaleEWasteReceiving():
	JobNumber = None
	PoNumber = None
	Weight = None
	CurrentPallet = None
	TotalPallets = None
	Data = None
	Date = None
	form = WholesaleEWasteReceivingForm()
	#Validate Form
	if form.validate_on_submit():
		JobNumber = form.JobNumber.data
		PoNumber = form.PoNumber.data
		Weight = form.Weight.data
		CurrentPallet = form.CurrentPallet.data
		TotalPallets = form.TotalPallets.data
		Data = form.Data.data
		Date = form.Date.data
		form.Client.data = ''
		form.PoNumber.data = ''
		form.Weight.data = ''
		form.CurrentPallet.data = ''
		form.TotalPallets.data = ''
		form.Data.data = ''
		form.Date.data = ''


	return render_template("WholesaleEWasteReceiving.html",
		JobNumber = JobNumber,
		PoNumber = PoNumber,
		Weight = Weight,
		CurrentPallet = CurrentPallet,
		TotalPallets = TotalPallets,
		Data=Data,
		Date = str(Date),
		form = form)

@app.route('/WEWRPrint', methods= ["POST"])



def WEWRPrint():
	JobNumber = request.form.get("JobNumber")
	PoNumber = request.form.get("PoNumber")
	Weight = request.form.get("Weight")
	CurrentPallet = request.form.get("CurrentPallet")
	TotalPallets = request.form.get("TotalPallets")
	Data = request.form.get("Data")
	Date = request.form.get("Date")

	return render_template("WEWRPrint.html",
		JobNumber =JobNumber,
		PoNumber=PoNumber,
		Weight=Weight,
		CurrentPallet=CurrentPallet,
		TotalPallets=TotalPallets,
		Data=Data,
		Date=Date)


@app.route('/WholesaleClientShipping ', methods=['GET', 'POST'])
@login_required
def  WholesaleClientShipping():
	JobNumber = None
	SoNumber = None
	Weight = None
	Dimms = None
	Dimms2 = None
	Dimms3 = None
	CurrentPallet = None
	TotalPallets = None
	Data = None
	QA = None
	UECM = None
	UDM = None
	ECTR = None
	FMCEC = None
	FM = None
	NECUO = None
	NEE = None
	NFM = None
	PREC = None
	Date = None
	form = WholesaleClientShippingForm()
	#Validate Form
	if form.validate_on_submit():
		JobNumber = form.JobNumber.data
		form.JobNumber.data = ''
		SoNumber = form.SoNumber.data
		form.SoNumber.data = ''
		Weight = form.Weight.data
		form.Weight.data = ''
		Dimms = form.Dimms.data
		form.Dimms.data = ''
		Dimms2 = form.Dimms2.data
		form.Dimms2.data = ''
		Dimms3 = form.Dimms3.data
		form.Dimms3.data = ''
		CurrentPallet = form.CurrentPallet.data
		form.CurrentPallet.data = ''
		TotalPallets = form.TotalPallets.data
		form.TotalPallets.data = ''
		Data = form.Data.data
		form.Data.data = ''
		QA = form.QA.data
		form.QA.data = ''
		UECM = form.UECM.data
		form.UECM.data = ''
		UDM = form.UDM.data
		form.UDM.data = ''
		ECTR = form.ECTR.data
		form.ECTR.data = ''
		FMCEC = form.FMCEC.data
		form.FMCEC.data = ''
		FM = form.FM.data
		form.FM.data = ''
		NECUO = form.NECUO.data
		form.NECUO.data = ''
		NEE = form.NEE.data
		form.NEE.data = ''
		NFM = form.NFM.data
		form.NFM.data = ''
		PREC = form.PREC.data
		form.PREC.data = ''
		Date = form.Date.data
		form.Date.data = ''


	return render_template("WholesaleClientShipping.html",
		JobNumber = JobNumber,
		SoNumber = SoNumber,
		Weight = Weight,
		Dimms = Dimms,
		Dimms2=Dimms,
		Dimms3=Dimms,
		CurrentPallet=CurrentPallet,
		TotalPallets=TotalPallets,
		Data =Data,
		QA =QA,
		UECM =UECM,
		UDM=UDM,
		ECTR=ECTR,
		FMCEC=FMCEC,
		FM =FM,
		NECUO =NECUO,
		NEE =NEE,
		NFM =NFM,
		PREC =PREC,
		Date=Date,
		form =form)

@app.route('/WCSPrint', methods= ["POST"])

def WCSPrint():
	JobNumber = request.form.get("JobNumber")
	SoNumber = request.form.get("SoNumber")
	Weight = request.form.get("Weight")
	Dimms = request.form.get("Dimms")
	Dimms2 = request.form.get("Dimms2")
	Dimms3 = request.form.get("Dimms3")
	CurrentPallet = request.form.get("CurrentPallet")
	TotalPallets = request.form.get("TotalPallets")
	Data = request.form.get("Data")
	QA = request.form.get("QA")
	UECM = request.form.get("UECM")
	UDM = request.form.get("UDM")
	ECTR = request.form.get("ECTR")
	FMCEC = request.form.get("FMCEC")
	FM = request.form.get("FM")
	NECUO = request.form.get("NECUO")
	NEE = request.form.get("NEE")
	NFM = request.form.get("NFM")
	PREC = request.form.get("PREC")
	Date = request.form.get("Date")

	return render_template("WCSPrint.html",
		JobNumber =JobNumber,
		SoNumber=SoNumber,
		Weight=Weight,
		Dimms=Dimms,
		Dimms2=Dimms2,
		Dimms3=Dimms3,
		CurrentPallet=CurrentPallet,
		TotalPallets=TotalPallets,
		Data=Data,
		QA=QA,
		UECM=UECM,
		UDM=UDM,
		ECTR=ECTR,
		FMCEC=FMCEC,
		FM=FM,
		NECUO=NECUO,
		NEE=NEE,
		NFM=NFM,
		PREC=PREC,
		Date=Date)

@app.route('/EWasteClientShipping ', methods=['GET', 'POST'])
@login_required
def  EWasteClientShipping():
	JobNumber = None
	SoNumber = None
	Weight = None
	Dimms = None
	Dimms2 = None
	Dimms3 = None
	Commodity = None
	Category = None
	CurrentPallet = None
	TotalPallets = None
	Evaluated = None
	Data = None
	QA = None
	UECM = None
	UDM = None
	ECTR = None
	FMCEC = None
	FM = None
	NECUO = None
	NEE = None
	NFM = None
	PREC = None
	Date = None
	form = EWasteClientShippingForm()
	#Validate Form
	if form.validate_on_submit():
		JobNumber = form.JobNumber.data
		form.JobNumber.data = ''
		SoNumber = form.SoNumber.data
		form.SoNumber.data = ''
		Weight = form.Weight.data
		form.Weight.data = ''
		Dimms = form.Dimms.data
		form.Dimms.data = ''
		Dimms2 = form.Dimms2.data
		form.Dimms2.data = ''
		Dimms3 = form.Dimms3.data
		form.Dimms3.data = ''
		Commodity = form.Commodity.data
		form.Commodity.data = ''
		Category = form.Category.data
		form.Category.data = ''
		CurrentPallet = form.CurrentPallet.data
		form.CurrentPallet.data = ''
		TotalPallets = form.TotalPallets.data
		form.TotalPallets.data = ''
		Evaluated = form.Evaluated.data
		form.Evaluated.data = ''
		Data = form.Data.data
		form.Data.data = ''
		QA = form.QA.data
		form.QA.data = ''
		UECM = form.UECM.data
		form.UECM.data = ''
		UDM = form.UDM.data
		form.UDM.data = ''
		ECTR = form.ECTR.data
		form.ECTR.data = ''
		FMCEC = form.FMCEC.data
		form.FMCEC.data = ''
		FM = form.FM.data
		form.FM.data = ''
		NECUO = form.NECUO.data
		form.NECUO.data = ''
		NEE = form.NEE.data
		form.NEE.data = ''
		NFM = form.NFM.data
		form.NFM.data = ''
		PREC = form.PREC.data
		form.PREC.data = ''
		Date = form.Date.data
		form.Date.data = ''


	return render_template("EWasteClientShipping.html",
		JobNumber = JobNumber,
		SoNumber = SoNumber,
		Weight = Weight,
		Dimms = Dimms,
		Dimms2=Dimms,
		Dimms3=Dimms,

		Commodity=Commodity,
		Category=Category,
		CurrentPallet=CurrentPallet,
		TotalPallets=TotalPallets,
		Evaluated=Evaluated,
		Data =Data,
		QA =QA,
		UECM =UECM,
		UDM=UDM,
		ECTR=ECTR,
		FMCEC=FMCEC,
		FM =FM,
		NECUO =NECUO,
		NEE =NEE,
		NFM =NFM,
		PREC =PREC,
		Date=Date,
		form =form)

@app.route('/EWCSPrint', methods= ["POST"])

def EWCSPrint():
	JobNumber = request.form.get("JobNumber")
	SoNumber = request.form.get("SoNumber")
	Weight = request.form.get("Weight")
	Dimms = request.form.get("Dimms")
	Dimms2 = request.form.get("Dimms2")
	Dimms3 = request.form.get("Dimms3")
	Commodity = request.form.get("Commodity")
	Category = request.form.get("Category")
	CurrentPallet = request.form.get("CurrentPallet")
	TotalPallets = request.form.get("TotalPallets")
	Evaluated = request.form.get("Evaluated")
	Data = request.form.get("Data")
	QA = request.form.get("QA")
	UECM = request.form.get("UECM")
	UDM = request.form.get("UDM")
	ECTR = request.form.get("ECTR")
	FMCEC = request.form.get("FMCEC")
	FM = request.form.get("FM")
	NECUO = request.form.get("NECUO")
	NEE = request.form.get("NEE")
	NFM = request.form.get("NFM")
	PREC = request.form.get("PREC")
	Date = request.form.get("Date")

	return render_template("EWCSPrint.html",
		JobNumber =JobNumber,
		SoNumber=SoNumber,
		Weight=Weight,
		Dimms=Dimms,
		Dimms2=Dimms2,
		Dimms3=Dimms3,
		Commodity=Commodity,
		Category=Category,
		CurrentPallet=CurrentPallet,
		TotalPallets=TotalPallets,
		Evaluated=Evaluated,
		Data=Data,
		QA=QA,
		UECM=UECM,
		UDM=UDM,
		ECTR=ECTR,
		FMCEC=FMCEC,
		FM=FM,
		NECUO=NECUO,
		NEE=NEE,
		NFM=NFM,
		PREC=PREC,
		Date=Date)

@app.route('/pick', methods=['GET', 'POST'])
@login_required
def  pick():
	JobNumber = None
	SO = None
	Data = None
	Evaluated = None
	Date = None
	form = pickForm()
	#Validate Form
	if form.validate_on_submit():
		JobNumber = form.JobNumber.data
		SO = form.SO.data
		Data = form.Data.data
		Evaluated = form.Evaluated.data
		Date = form.Date.data
		form.SO.data = ''
		form.Data.data = ''
		form.Evaluated.data = ''
		form.Date.data = ''


	return render_template("pick.html",
		JobNumber = JobNumber,
		SO = SO,
		Data = Data,
		Evaluated = Evaluated,
		Date = Date,
		form = form)

@app.route('/pickPrint', methods= ["POST"])
def pickPrint():
	JobNumber = request.form.get("JobNumber")
	SO = request.form.get("SO")
	Data = request.form.get("Data")
	Evaluated = request.form.get("Evaluated")
	Date = request.form.get("Date")

	return render_template("pickPrint.html",
		JobNumber =JobNumber,
		SO =SO,
		Data=Data,
		Evaluated=Evaluated,
		Date=Date)

@app.route('/audit', methods=['GET', 'POST'])
@login_required
def  audit():
	JobNumber = None
	PO = None
	Data = None
	Evaluated = None
	Date = None
	form = auditForm()
	#Validate Form
	if form.validate_on_submit():
		JobNumber = form.JobNumber.data
		PO = form.PO.data
		Data = form.Data.data
		Evaluated = form.Evaluated.data
		Date = form.Date.data
		form.JobNumber.data = ''
		form.PO.data = ''
		form.Data.data = ''
		form.Evaluated.data = ''
		form.Date.data = ''


	return render_template("audit.html",
		JobNumber = JobNumber,
		PO = PO,
		Data = Data,
		Evaluated = Evaluated,
		Date = Date,
		form = form)

@app.route('/auditPrint', methods= ["POST"])
def auditPrint():
	JobNumber = request.form.get("JobNumber")
	PO = request.form.get("PO")
	Data = request.form.get("Data")
	Evaluated = request.form.get("Evaluated")
	Date = request.form.get("Date")

	return render_template("auditPrint.html",
		JobNumber = JobNumber,
		PO = PO,
		Data=Data,
		Evaluated=Evaluated,
		Date=Date)

@app.route('/PreAudit', methods=['GET', 'POST'])
@login_required
def  PreAudit():
	JobNumber = None
	Data = None
	form = preauditForm()
	#Validate Form
	if form.validate_on_submit():
		JobNumber = form.JobNumber.data
		Data = form.Data.data
		form.JobNumber.data = ''
		form.Data.data = ''


	return render_template("PreAudit.html",
		JobNumber = JobNumber,
		Data = Data,
		form = form)

@app.route('/PAPrint', methods= ["POST"])
def PAPrint():
	JobNumber = request.form.get("JobNumber")
	PO = request.form.get("PO")
	Data = request.form.get("Data")
	Evaluated = request.form.get("Evaluated")
	Date = request.form.get("Date")

	return render_template("PAPrint.html",
		JobNumber = JobNumber,
		PO =PO,
		Data=Data,
		Evaluated=Evaluated,
		Date=Date)



@app.route('/sort', methods=['GET', 'POST'])
@login_required
def  sort():
	JobNumber = None
	Data = None
	Evaluated = None
	Date = None
	form = auditForm()
	#Validate Form
	if form.validate_on_submit():
		JobNumber = form.JobNumber.data
		Data = form.Data.data
		Evaluated = form.Evaluated.data
		Date = form.Date.data
		form.JobNumber.data = ''
		form.PO.data = ''
		form.Data.data = ''
		form.Evaluated.data = ''
		form.Date.data = ''


	return render_template("sort.html",
		JobNumber = JobNumber,
		Data = Data,
		Evaluated = Evaluated,
		Date = Date,
		form = form)

@app.route('/sortPrint', methods= ["POST"])
def sortPrint():
	JobNumber = request.form.get("JobNumber")
	Data = request.form.get("Data")
	Evaluated = request.form.get("Evaluated")
	Date = request.form.get("Date")

	return render_template("sortPrint.html",
		JobNumber = JobNumber,
		Data=Data,
		Evaluated=Evaluated,
		Date=Date)



@app.route('/count', methods=['GET', 'POST'])
@login_required
def  count():
	JobNumber = None
	Data = None
	Evaluated = None
	Date = None
	form = auditForm()
	#Validate Form
	if form.validate_on_submit():
		JobNumber = form.JobNumber.data
		Data = form.Data.data
		Evaluated = form.Evaluated.data
		Date = form.Date.data
		form.JobNumber.data = ''
		form.PO.data = ''
		form.Data.data = ''
		form.Evaluated.data = ''
		form.Date.data = ''


	return render_template("count.html",
		JobNumber = JobNumber,
		Data = Data,
		Evaluated = Evaluated,
		Date = Date,
		form = form)

@app.route('/countPrint', methods= ["POST"])
def countPrint():
	JobNumber = request.form.get("JobNumber")
	Data = request.form.get("Data")
	Evaluated = request.form.get("Evaluated")
	Date = request.form.get("Date")

	return render_template("countPrint.html",
		JobNumber = JobNumber,
		Data=Data,
		Evaluated=Evaluated,
		Date=Date)



@app.route('/data_destruction', methods=['GET', 'POST'])
@login_required
def  data_destruction():
	JobNumber = None
	Data = None
	Evaluated = None
	Date = None
	form = auditForm()
	#Validate Form
	if form.validate_on_submit():
		JobNumber = form.JobNumber.data
		Data = form.Data.data
		Evaluated = form.Evaluated.data
		Date = form.Date.data
		form.JobNumber.data = ''
		form.PO.data = ''
		form.Data.data = ''
		form.Evaluated.data = ''
		form.Date.data = ''


	return render_template("data_destruction.html",
		JobNumber = JobNumber,
		Data = Data,
		Evaluated = Evaluated,
		Date = Date,
		form = form)

@app.route('/data_destructionPrint', methods= ["POST"])
def data_destructionPrint():
	JobNumber = request.form.get("JobNumber")
	Data = request.form.get("Data")
	Evaluated = request.form.get("Evaluated")
	Date = request.form.get("Date")

	return render_template("data_destructionPrint.html",
		JobNumber = JobNumber,
		Data=Data,
		Evaluated=Evaluated,
		Date=Date)

@app.route('/users/add', methods=['GET', 'POST'])
def add_user():
	name = None
	form = UserForm()
	if form.validate_on_submit():
		user = Users.query.filter_by(email=form.email.data).first()
		if user is None:
			hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
			user = Users(username =form.username.data, name=form.name.data, email=form.email.data, department=form.department.data,  password_hash=hashed_pw)
			db.session.add(user)
			db.session.commit()
		name = form.name.data
		form.name.data = ''
		form.username.data = ''
		form.email.data = ''
		form.department.data = ''
		form.password_hash.data = ''

		flash("User Added")
	our_users = Users.query.order_by()
	return render_template("add_user.html", form=form, name=name, our_users = our_users)


@app.route('/user', methods=['GET', 'POST'])
def user():
	name = None
	form = UserForm()
	if form.validate_on_submit():
		user = Users.query.filter_by(email=form.email.data).first()
		if user is None:
			hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
			user = Users(username=form.username.data, name=form.name.data, email=form.email.data,
						 department=form.department.data, password_hash=hashed_pw)
			db.session.add(user)
			db.session.commit()
		name = form.name.data
		form.name.data = ''
		form.username.data = ''
		form.email.data = ''
		form.department.data = ''
		form.password_hash.data = ''

		flash("User Added")
	our_users = Users.query.order_by()
	return render_template("user.html", form=form, name=name, our_users=our_users)

@app.route('/delete_user/<int:id>')
def delete_user(id):
	user_to_delete = Users.query.get_or_404(id)
	name = None
	form = UserForm()
	try:
		db.session.delete(user_to_delete)
		db.session.commit()
		flash("User Deleted")
		our_users = Users.query
		return render_template("add_user.html",
							   form=form,
							   name=name,
							   our_users=our_users)

	except:
		flash("ERROR User Not Deleted!")
		return render_template("add_user.html",
							   form=form,
							   name=name,
							   our_users=our_users)

@app.route('/test_pw', methods=['GET','POST'])
def test_pw():
	email = None
	password = None
	pw_to_check = None
	passed = None
	form= PasswordForm()

	if form.validate_on_submit():
		email= form.email.data
		password = form.password_hash.data
		form.email.data = ''
		form.password_hash.data = ''

		pw_to_check = Users.query.filter_by(email=email).first()

		passed = check_password_hash(pw_to_check.password_hash, password)

	return render_template("test_pw.html",
						   email=email,
						   password= password,
						   pw_to_check=pw_to_check,
						   passed = passed,
						   form = form)

def send_reset_email(Users):
	token = Users.get_reset_token()
	msg = Message('Password Reset Request', sender='noreply@ampletechrefresh.com', recipients=[Users.email])
	msg.body = f''' To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then ignore this email.
'''
	mail.send(msg)

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RequestResetForm()
	if form.validate_on_submit():
		user = Users.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		flash('An email has been sent with instructions to reset your password.', 'info')
		return redirect(url_for('login'))
	return render_template('reset_request.html', title="Reset Password",form=form)

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	user = Users.verify_reset_token(token)
	if user is None:
		flash('Invalid or expired token', 'warning')
		return redirect(url_for('reset_request'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
		user.password = hashed_pw
		db.session.commit()
		flash("Password has been updated!")
		return redirect(url_for('login'))
	return render_template('reset_token.html', title="Reset Password",form=form)

@app.template_filter('datetimeformat')
def datetimeformat(value, format ='%d-%m-%Y'):
    return value.strftime(format)

#app.jinja_env.filters['datetimeformat'] = datetimeformat


if __name__ == "__main__":
    app.run(debug=True)


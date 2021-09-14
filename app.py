from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, DateField, validators, BooleanField, DateTimeField
from wtforms.fields.html5 import DateField, DateTimeField
from wtforms.validators import DataRequired
from flask_mysqldb import MySQL, MySQLdb
from flaskext.mysql import MySQL
import pymysql
import sys
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from jinja2 import environment, filters
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




app.config['MYSQL_DATABASE_USER'] = 'benwebwd'
app.config['MYSQL_DATABASE_PASSWORD'] = 'w8TBX&MsZvC&F92Qc9Fa9c'
app.config['MYSQL_DATABASE_DB'] = 'wd'
app.config['MYSQL_DATABASE_HOST'] = '10.104.1.52'

mysql = MySQL()
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()


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



#create form class
class WDForm(FlaskForm):
	Company_Name = StringField("Company Name", validators=[DataRequired()])
	SO = StringField("Sales Order", validators=[DataRequired()])
	Pallet = IntegerField("Pallet", validators=[DataRequired()])
	Shipping = SelectField("Shipping", choices=[('Domestic', 'Domestic'), ('International', 'International')] ,validators=[DataRequired()])
	Length = IntegerField("Length", validators=[DataRequired()])
	Width = IntegerField("Width", validators=[DataRequired()])
	Height = IntegerField("Height", validators=[DataRequired()])
	Weight = IntegerField("Weight", validators=[DataRequired()])
	Total_Weight = IntegerField("Total Weight", validators=[DataRequired()])
	Status = SelectField("Status", choices=[('Not Complete', 'Not Complete'), ('Complete', 'Complete')] ,validators=[DataRequired()])
	date = DateField("Date", validators=[DataRequired()])
	Submit = SubmitField("Submit")



@app.route('/WD_update/<int:id>', methods=['GET', 'POST'])
def WD_update(id):
	Company_Name = None
	SO = None
	Status = None
	form = WDForm()
	WD_to_update = WD.query.get_or_404(id)
	if form.validate_on_submit():
		Company_Name = form.Company_Name.data
		SO = form.SO.data
		Status = form.Status.data
		form.Company_Name.data = ""
		form.SO.data = ""
		form.Status.data = ""
	if request.method == "POST":
		WD_to_update.Company_Name = request.form['Company_Name']
		WD_to_update.SO = request.form['SO']
		WD_to_update.Status = request.form['Status']
		try:
			db.session.commit()
			flash(" Updated Successfuly!")
			return render_template("WD_update.html",
			   form=form,
			   Company_Name=Company_Name,
			   SO = SO,
				Status=Status,
			   WD_to_update = WD_to_update)

		except:
			flash("ERROR!! W&D Not Updated")
			return render_template("WD_update.html",
			   form=form,
			   Company_Name=Company_Name,
			   Status=Status,
			   WD_to_update=WD_to_update)

	else:
		return render_template("WD_update.html",
			   form=form,
			   Company_Name=Company_Name,
			   SO=SO,
			   Status=Status,
			   WD_to_update=WD_to_update)

class PostAuditDismantleForm(FlaskForm):
	PoNumber = IntegerField("PO Number", validators=[DataRequired()])
	Commodity = StringField("Commodity", validators=[DataRequired()])
	Data = SelectField("Data", choices=[('YES', 'YES'), ('NO', 'NO')])
	Submit = SubmitField("Print")

#create form class
class WholesaleEWasteReceivingForm(FlaskForm):
	Client = StringField("Client", validators=[DataRequired()])
	PoNumber = IntegerField("PO Number", validators=[DataRequired()])
	Weight = IntegerField("Weight", validators=[DataRequired()])
	Date = DateField("Date", format='%m-%d-%Y', validators=[DataRequired()])
	Submit = SubmitField("Print")

class WholesaleClientShippingForm(FlaskForm):
	Client = StringField("Client", validators=[DataRequired()])
	SoNumber = IntegerField("SO Number", validators=[DataRequired()])
	Weight = IntegerField("Weight", validators=[DataRequired()])
	Dimms = StringField("Dimms", validators=[DataRequired()])
	Dimms2 = StringField("Dimms", validators=[DataRequired()])
	Dimms3 = StringField("Dimms", validators=[DataRequired()])
	CurrentPallet = StringField("Current Pallet", validators=[DataRequired()])
	TotalPallets = StringField("Total Pallets", validators=[DataRequired()])
	Data = SelectField("Data", choices=[('YES', 'YES'), ('NO', 'NO')])
	QA = SelectField("QA Checked By", choices=[('Adan J', 'Adan J'), ('Corey G', 'Corey G'), ('Jesus G', 'Jesus G'), ('Scott G', 'Scott G'),('Mike V', 'Mike V')])
	UECM = BooleanField("Unevaluated Equipment, Components & Materials")
	UDM = BooleanField("Unsanitized Devices/Media")
	ECTR = BooleanField("Equipment/Components for Test & Repair")
	FMCEC = BooleanField("FM Containing Equipment/Components")
	FM = BooleanField("Focus materials")
	NECUO = BooleanField("New Equipment/Components in Unopened, Original OEM Packaging")
	NEE = BooleanField("Non-Electronics Equipment")
	NFM = BooleanField("Non-focus materials")
	PREC = BooleanField("Planned Return Equipment/Components")
	Submit = SubmitField("Print")


class EWasteClientShippingForm(FlaskForm):
	Client = StringField("Client", validators=[DataRequired()])
	SoNumber = IntegerField("SO Number", validators=[DataRequired()])
	Weight = IntegerField("Weight", validators=[DataRequired()])
	Dimms = StringField("Dimms", validators=[DataRequired()])
	Dimms2 = StringField("Dimms", validators=[DataRequired()])
	Dimms3 = StringField("Dimms", validators=[DataRequired()])
	Commodity = StringField("Commodity", validators=[DataRequired()])
	Category = SelectField("Category", choices=[('C0', 'C0'), ('C1', 'C1'), ('C2', 'C2')])
	CurrentPallet = StringField("Current Pallet", validators=[DataRequired()])
	TotalPallets = StringField("Total Pallets", validators=[DataRequired()])
	Evaluated = SelectField("Evaluated", choices=[('YES', 'YES'), ('NO', 'NO')])
	Data = SelectField("Data", choices=[('YES', 'YES'), ('NO', 'NO')])
	QA = SelectField("QA Checked By", choices=[('Adan J', 'Adan J'), ('Corey G', 'Corey G'), ('Jesus G', 'Jesus G'), ('Scott G', 'Scott G'),('Mike V', 'Mike V')])
	UECM = BooleanField("Unevaluated Equipment, Components & Materials")
	UDM = BooleanField("Unsanitized Devices/Media")
	ECTR = BooleanField("Equipment/Components for Test & Repair")
	FMCEC = BooleanField("FM Containing Equipment/Components")
	FM = BooleanField("Focus materials")
	NECUO = BooleanField("New Equipment/Components in Unopened, Original OEM Packaging")
	NEE = BooleanField("Non-Electronics Equipment")
	NFM = BooleanField("Non-focus materials")
	PREC = BooleanField("Planned Return Equipment/Components")
	Submit = SubmitField("Print")



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
def CompleteWD():
	#Grab all W&Ds from DB
	page = request.args.get('page',1, type=int)
	WDs = WD.query.order_by(WD.date_added.desc()).paginate(page=page, per_page=10)
	return render_template("CompleteWD.html", WDs=WDs)


@app.route('/search', methods=['GET', 'POST'])
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



@app.route('/PostAuditDismantle', methods=['GET', 'POST'])

def PostAuditDismantle():
	PoNumber = None
	Commodity = None
	Data = None
	form = PostAuditDismantleForm()
	#Validate Form
	if form.validate_on_submit():
		PoNumber = form.PoNumber.data
		form.PoNumber.data = ""
		Commodity = form.Commodity.data
		form.Commodity.data = ""
		Data = form.Data.data
		form.Data.data = ""
		return redirect(url_for('PostAuditDismantle'))

	return render_template("PostAuditDismantle.html",
		PoNumber = PoNumber,
		Commodity = Commodity,
		Date = Data,
		form = form)

@app.route('/PADPrint', methods= ["POST"])

def PADPrint():
	PoNumber = request.form.get("PoNumber")
	Commodity = request.form.get("Commodity")
	Data = request.form.get("Data")

	return render_template("PADPrint.html",
		PoNumber=PoNumber,
		Commodity=Commodity,
		Data=Data)



@app.route('/WholesaleEWasteReceiving', methods=['GET', 'POST'])

def  WholesaleEWasteReceiving():
	Client = None
	PoNumber = None
	Weight = None
	Date = None
	form = WholesaleEWasteReceivingForm()
	#Validate Form
	if form.validate_on_submit():
		Client = form.Client.data
		PoNumber = form.PoNumber.data
		Weight = form.Weight.data
		Date = form.Date.data
		form.Client.data = ''
		form.PoNumber.data = ''
		form.Weight.data = ''
		form.Date.data = ''


	return render_template("WholesaleEWasteReceiving.html",
		Client = Client,
		PoNumber = PoNumber,
		Weight = Weight,
		Date = Date,
		form = form)

@app.route('/WEWRPrint', methods= ["POST"])



def WEWRPrint():
	Client = request.form.get("Client")
	PoNumber = request.form.get("PoNumber")
	Weight = request.form.get("Weight")
	Date = request.form.get("Date")

	return render_template("WEWRPrint.html",
		Client =Client,
		PoNumber=PoNumber,
		Weight=Weight,
		Date=Date)


@app.route('/WholesaleClientShipping ', methods=['GET', 'POST'])

def  WholesaleClientShipping():
	Client = None
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
	form = WholesaleClientShippingForm()
	#Validate Form
	if form.validate_on_submit():
		Client = form.Client.data
		form.Client.data = ''
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


	return render_template("WholesaleClientShipping.html",
		Client = Client,
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
		form =form)

@app.route('/WCSPrint', methods= ["POST"])

def WCSPrint():
	Client = request.form.get("Client")
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

	return render_template("WCSPrint.html",
		Client =Client,
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
		PREC=PREC)

@app.route('/EWasteClientShipping ', methods=['GET', 'POST'])

def  EWasteClientShipping():
	Client = None
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
	form = EWasteClientShippingForm()
	#Validate Form
	if form.validate_on_submit():
		Client = form.Client.data
		form.Client.data = ''
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


	return render_template("EWasteClientShipping.html",
		Client = Client,
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
		form =form)

@app.route('/EWCSPrint', methods= ["POST"])

def EWCSPrint():
	Client = request.form.get("Client")
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

	return render_template("EWCSPrint.html",
		Client =Client,
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
		PREC=PREC)



if __name__ == "__main__":
    app.run(debug=True)


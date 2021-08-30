from flask import Flask, render_template, request, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, DateField, validators, BooleanField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
import sys
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
sys.setrecursionlimit(2000)



#Flask Instance
app = Flask(__name__)

#add database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///wd.db"
#secret key
app.config['SECRET_KEY'] = "super secret key"
#Initialize the database
db= SQLAlchemy(app)

#create model

class WD(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	Company_Name = db.Column(db.String(50), nullable=False)
	SO = db.Column(db.String(50), nullable=False)
	Pallet = db.Column(db.Integer, nullable=False)
	Length = db.Column(db.Integer, nullable=False)
	Width = db.Column(db.Integer, nullable=False)
	Height = db.Column(db.Integer, nullable=False)
	Weight = db.Column(db.Integer, nullable=False)
	Status = db.Column(db.String(50), nullable=False)
	date_added = db.Column(db.DateTime, default=datetime.utcnow)

	#Create A String
	def __repr__(self):
		return 'Name %r>' % self.name



#create form class
class WDForm(FlaskForm):
	Company_Name = StringField("Company Name", validators=[DataRequired()])
	SO = StringField("Sales Order", validators=[DataRequired()])
	Pallet = IntegerField("Pallet", validators=[DataRequired()])
	Length = IntegerField("Length", validators=[DataRequired()])
	Width = IntegerField("Width", validators=[DataRequired()])
	Height = IntegerField("Height", validators=[DataRequired()])
	Weight = IntegerField("Weight", validators=[DataRequired()])
	Status = SelectField("Status", choices=[('Complete', 'Complete'), ('Not Complete', 'Not Complete')] ,validators=[DataRequired()])
	Submit = SubmitField("Print")






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


#Route decorator
@app.route('/WD/add', methods=['Get','POST'])
def add_WD():
	form = WDForm()
	if form.validate_on_submit():
		wd = WD(Company_Name=form.Company_Name.data,
				)
	return render_template("add_WD.html" ,form = form)



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
		form.PoNumber.data = ''
		Commodity = form.Commodity.data
		form.Commodity.data = ''
		Data = form.Data.data
		form.Data.data = ''


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
		form.Client.data = ''
		PoNumber = form.PoNumber.data
		form.PoNumber.data = ''
		Weight = form.Weight.data
		form.Weight.data = ''
		Date = form.Date.data
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






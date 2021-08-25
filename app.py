from flask import Flask, render_template, request, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, DateField
from wtforms.validators import DataRequired


#Flask Instance
app = Flask(__name__)
app.config['SECRET_KEY'] = "super secret key"

#create form class
class PostAuditDismantleForm(FlaskForm):
	PoNumber = IntegerField("PO Number", validators=[DataRequired()])
	Commodity = StringField("Commodity", validators=[DataRequired()])
	Data = SelectField("Data", choices=[('YES', 'YES'), ('NO', 'NO')])
	Submit = SubmitField("Print")

#create form class
class WholesaleEWasteReceivingForm(FlaskForm):
	Client = IntegerField("PO Number", validators=[DataRequired()])
	PoNumber = IntegerField("PO Number", validators=[DataRequired()])
	Weight = IntegerField("Weight", validators=[DataRequired()])
	Date = DateField("Date", validators=[DataRequired()])
	Submit = SubmitField("Print")


#Route decorator
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

	return render_template("PADPrint.html",
		Client =Client,
		PoNumber=PoNumber,
		Weight=Weight,
		Date=Date)




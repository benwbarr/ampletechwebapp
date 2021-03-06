
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, DateField, validators, BooleanField, DateTimeField, PasswordField, ValidationError
from wtforms.fields.html5 import DateField, DateTimeField
from wtforms.validators import DataRequired, EqualTo, Length

from wtforms.widgets import TextArea

Commodity = [('Desktops', 'Desktops'), ('Laptops', 'Laptops'), ('Keyboards and Mice', 'Keyboards and Mice'),
							('Docking Stations above cutline', 'Docking Stations above cutline'), ('Docking Stations below cutline', 'Docking Stations below cutline'),
												  ('Mixed wires', 'Mixed wires'), ('Adapters', 'Adapters'), ('Batteries','Batteries'), ('Ram', 'Ram'),
												  ('Networking', 'Networking'), ('Headsets', 'Headsets'), ('CAT 5', 'CAT 5'), ('LCDs', 'LCDs'),
												('Green board', 'Green board'), ('IP Phones Below Cut Line', 'IP Phones Below Cut Line'), ('IP Phones Above Cut Line', 'IP Phones Above Cut Line'), ('Scrap servers','Scrap servers'),
												  ('UPS/APC’s', 'UPS/APC’s'), ('Aluminum', 'Aluminum'),('Plastic', 'Plastic'), ('Steel','Steel'),
												  ('Cardboard', 'Cardboard'), ('Trash', 'Trash'), ('Projectors', 'Projectors'), ('Media Players', 'Media Players'),
			 ('Power Strips','Power Strips'),('Fans', 'Fans'), ('Speakers', 'Speakers'), ('Printers & Scanners', 'Printers & Scanners'), ('Copper','Copper')]

Commodity.sort()


QAs = [('Ruben G','Ruben G'),('Martin ','Martin'), ('Michael C', 'Michael C'), ('Scott G', 'Scott G'),('Mike V', 'Mike V')]

class LoginForm(FlaskForm):
	username = StringField("Username", validators=[DataRequired()])
	password= PasswordField("Password", validators=[DataRequired()])
	submit = SubmitField("Submit")

class UserForm(FlaskForm):
	name = StringField("Name", validators=[DataRequired()])
	username = StringField("User Name", validators=[DataRequired()])
	email = StringField("Email", validators=[DataRequired()])
	department = SelectField("Department", choices=[('Audit', 'Audit'),('CleanPack', 'Clean & Pack'), ('HR', 'HR'), ('IT', 'IT'),
													('Itad', 'ITAD'), ('Management', 'Management'), ('Refurb', 'Refurb'), ('Sales', 'Sales'),
													('ShippingReceiving', 'Shipping/Receiving'), ('Sort', 'Sort')])

	password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2',message='Passwords Must Match!')])
	password_hash2 = PasswordField('Confirm Password',validators=[DataRequired()])
	submit = SubmitField("Submit")

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

class PostAuditDismantleForm(FlaskForm):
	JobNumber = IntegerField("Job Number", validators=[DataRequired()])
	BatchNumber = StringField("Batch Number", validators=[DataRequired()])
	PoNumber = IntegerField("PO Number", validators=[DataRequired()])
	Commodity = SelectField("Commodity", choices=Commodity)
	Dimms = StringField("Dimms", validators=[DataRequired()])
	Dimms2 = StringField("Dimms", validators=[DataRequired()])
	Dimms3 = StringField("Dimms", validators=[DataRequired()])
	NetWeight = IntegerField("Net Weight", validators=[DataRequired()])
	GrossWeight = IntegerField("Gross Weight", validators=[DataRequired()])
	TareWeight = IntegerField("Tare Weight", validators=[DataRequired()])
	Data = SelectField("Data", choices=[('YES', 'YES'), ('NO', 'NO')])
	Evaluated = SelectField("Evaluated", choices=[('YES', 'YES'), ('NO', 'NO')])
	Date = DateField("Date", format='%m-%d-%Y', validators=[DataRequired()])
	Submit = SubmitField("Print")

class InventoryWSForm(FlaskForm):
	JobNumber = IntegerField("Job Number", validators=[DataRequired()])
	BatchNumber = StringField("Batch Number", validators=[DataRequired()])
	PoNumber = IntegerField("PO Number", validators=[DataRequired()])
	Commodity = SelectField("Commodity", choices=Commodity)
	Dimms = StringField("Dimms", validators=[DataRequired()])
	Dimms2 = StringField("Dimms", validators=[DataRequired()])
	Dimms3 = StringField("Dimms", validators=[DataRequired()])
	NetWeight = IntegerField("Net Weight", validators=[DataRequired()])
	GrossWeight = IntegerField("Gross Weight", validators=[DataRequired()])
	TareWeight = IntegerField("Tare Weight", validators=[DataRequired()])
	Data = SelectField("Data", choices=[('YES', 'YES'), ('NO', 'NO')])
	Evaluated = SelectField("Evaluated", choices=[('YES', 'YES'), ('NO', 'NO')])
	Date = DateField("Date", format='%m-%d-%Y', validators=[DataRequired()])
	Submit = SubmitField("Print")

class ITADSortForm(FlaskForm):
	Commodity = SelectField("Commodity", choices=Commodity)
	Data = SelectField("Data", choices=[('YES', 'YES'), ('NO', 'NO')])
	Evaluated = SelectField("Evaluated", choices=[('NO', 'NO'), ('YES', 'YES')])
	TareWeight = IntegerField("Tare Weight", validators=[DataRequired()])
	Submit = SubmitField("Print")

#create form class
class WholesaleEWasteReceivingForm(FlaskForm):
	JobNumber = IntegerField("Job Number", validators=[DataRequired()])
	PoNumber = IntegerField("PO Number", validators=[DataRequired()])
	Weight = IntegerField("Weight", validators=[DataRequired()])
	Date = DateField("Date", format='%m-%d-%Y', validators=[DataRequired()])
	Data = SelectField("Data", choices=[('YES', 'YES'), ('NO', 'NO')])
	CurrentPallet = StringField("Current Pallet", validators=[DataRequired()])
	TotalPallets = StringField("Total Pallets", validators=[DataRequired()])
	Submit = SubmitField("Print")

class pickForm(FlaskForm):
	JobNumber = IntegerField("Job Number", validators=[DataRequired()])
	SO = IntegerField("SO Number", validators=[DataRequired()])
	Data = SelectField("Data", choices=[('YES', 'YES'), ('NO', 'NO')])
	Evaluated = SelectField("Evaluated", choices=[('YES', 'YES'), ('NO', 'NO')])
	Date = DateField("Date", format='%m-%d-%Y', validators=[DataRequired()])
	Submit = SubmitField("Print")

class auditForm(FlaskForm):
	JobNumber = IntegerField("Job Number", validators=[DataRequired()])
	PO = IntegerField("PO Number", validators=[DataRequired()])
	Data = SelectField("Data", choices=[('YES', 'YES'), ('NO', 'NO')])
	Evaluated = SelectField("Evaluated", choices=[('YES', 'YES'), ('NO', 'NO')])
	Date = DateField("Date", format='%m-%d-%Y', validators=[DataRequired()])
	Submit = SubmitField("Print")

class preauditForm(FlaskForm):
	JobNumber = IntegerField("Job Number", validators=[DataRequired()])
	Data = SelectField("Data", choices=[('YES', 'YES'), ('NO', 'NO')])
	Submit = SubmitField("Print")

class sortForm(FlaskForm):
	JobNumber = IntegerField("Job Number", validators=[DataRequired()])
	Data = SelectField("Data", choices=[('YES', 'YES'), ('NO', 'NO')])
	Evaluated = SelectField("Evaluated", choices=[('NO', 'NO'), ('YES', 'YES')])
	Date = DateField("Date", format='%m-%d-%Y', validators=[DataRequired()])
	Submit = SubmitField("Print")

class countForm(FlaskForm):
	JobNumber = IntegerField("Job Number", validators=[DataRequired()])
	Data = SelectField("Data", choices=[('YES', 'YES'), ('NO', 'NO')])
	Evaluated = SelectField("Evaluated", choices=[('NO', 'NO'), ('YES', 'YES')])
	Date = DateField("Date", format='%m-%d-%Y', validators=[DataRequired()])
	Submit = SubmitField("Print")

class data_destructiontForm(FlaskForm):
	JobNumber = IntegerField("Job Number", validators=[DataRequired()])
	Data = SelectField("Data", choices=[('YES', 'YES'), ('NO', 'NO')])
	Evaluated = SelectField("Evaluated", choices=[('NO', 'NO'), ('YES', 'YES')])
	Date = DateField("Date", format='%m-%d-%Y', validators=[DataRequired()])
	Submit = SubmitField("Print")


class WholesaleClientShippingForm(FlaskForm):
	JobNumber = IntegerField("Batch Number", validators=[DataRequired()])
	SoNumber = IntegerField("SO Number", validators=[DataRequired()])
	Weight = IntegerField("Weight", validators=[DataRequired()])
	Dimms = StringField("Dimms", validators=[DataRequired()])
	Dimms2 = StringField("Dimms", validators=[DataRequired()])
	Dimms3 = StringField("Dimms", validators=[DataRequired()])
	CurrentPallet = StringField("Current Pallet", validators=[DataRequired()])
	TotalPallets = StringField("Total Pallets", validators=[DataRequired()])
	Data = SelectField("Data", choices=[('YES', 'YES'), ('NO', 'NO')])
	QA = SelectField("QA Checked By", choices=QAs)
	UECM = BooleanField("Unevaluated Equipment, Components & Materials")
	UDM = BooleanField("Unsanitized Devices/Media")
	ECTR = BooleanField("Equipment/Components for Test & Repair")
	FMCEC = BooleanField("FM Containing Equipment/Components")
	FM = BooleanField("Focus materials")
	NECUO = BooleanField("New Equipment/Components in Unopened, Original OEM Packaging")
	NEE = BooleanField("Non-Electronics Equipment")
	NFM = BooleanField("Non-focus materials")
	PREC = BooleanField("Planned Return Equipment/Components")
	Date = DateField("Date", format='%m-%d-%Y', validators=[DataRequired()])
	Submit = SubmitField("Print")


class EWasteClientShippingForm(FlaskForm):
	JobNumber = IntegerField("Batch Number", validators=[DataRequired()])
	SoNumber = IntegerField("SO Number", validators=[DataRequired()])
	Weight = IntegerField("Weight", validators=[DataRequired()])
	Dimms = StringField("Dimms", validators=[DataRequired()])
	Dimms2 = StringField("Dimms", validators=[DataRequired()])
	Dimms3 = StringField("Dimms", validators=[DataRequired()])
	Commodity = SelectField("Commodity", choices=Commodity)
	Category = SelectField("Category", choices=[('C0', 'C0'), ('C1', 'C1'), ('C2', 'C2')])
	CurrentPallet = StringField("Current Pallet", validators=[DataRequired()])
	TotalPallets = StringField("Total Pallets", validators=[DataRequired()])
	Evaluated = SelectField("Evaluated", choices=[('YES', 'YES'), ('NO', 'NO')])
	Data = SelectField("Data", choices=[('YES', 'YES'), ('NO', 'NO')])
	QA = SelectField("QA Checked By", choices=QAs)
	UECM = BooleanField("Unevaluated Equipment, Components & Materials")
	UDM = BooleanField("Unsanitized Devices/Media")
	ECTR = BooleanField("Equipment/Components for Test & Repair")
	FMCEC = BooleanField("FM Containing Equipment/Components")
	FM = BooleanField("Focus materials")
	NECUO = BooleanField("New Equipment/Components in Unopened, Original OEM Packaging")
	NEE = BooleanField("Non-Electronics Equipment")
	NFM = BooleanField("Non-focus materials")
	PREC = BooleanField("Planned Return Equipment/Components")
	Date = DateField("Date", format='%m-%d-%Y', validators=[DataRequired()])
	Submit = SubmitField("Print")


class PasswordForm(FlaskForm):
	email = StringField("What's Your Email?", validators=[DataRequired()])
	password_hash = PasswordField("What's Your Password?", validators=[DataRequired()])
	submit = SubmitField("Submit")

class RequestResetForm(FlaskForm):
	email = StringField("Email", validators=[DataRequired()])
	submit = SubmitField("Request Password Reset")



class ResetPasswordForm(FlaskForm):
	password = PasswordField('Password', validators=[DataRequired(),
													 EqualTo('password_hash2', message='Passwords Must Match!')])
	password2 = PasswordField('Confirm Password', validators=[DataRequired()])
	submit = SubmitField("Reset Password")
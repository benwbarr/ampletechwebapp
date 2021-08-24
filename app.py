from flask import Flask, render_template

#Flask Instance
app = Flask(__name__)

#Route decorator
#pp.route('/')

@app.route('/')

def index():
	return render_template("index.html")


@app.route('/WholesaleEWaste/')

def WholesaleEWaste():
	return render_template("WholesaleEWaste.html")

@app.route('/PostAuditDismantle/')

def PostAuditDismantle():
	return render_template("PostAuditDismantle.html")

@app.route('/WholesaleClientShipping/')

def WholesaleClientShipping():
	return render_template("WholesaleClientShipping.html")

@app.route('/WWasteClientShipping/')

def EWasteClientShipping():
	return render_template("EWasteClientShipping.html")
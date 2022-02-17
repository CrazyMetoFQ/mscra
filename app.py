from flask import Flask, render_template, url_for
from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, IntegerField, BooleanField, SelectField
from wtforms.fields import IntegerRangeField
from wtforms.validators import DataRequired, NumberRange

import os
import json

from pprint import pprint


base_path = "C:/Users/Ali Hussain/flaskwtf_tri"
stuffes_path = base_path+"/stuffes"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'


class basicForm(FlaskForm):
	raw_name = StringField("Name  ", validators=[DataRequired()])
	sumbit = SubmitField("Submit")


def confirur(_path = None):
	"""
	return json as dict from path
	"""

	if _path == None:
		_path = stuffes_path+"/stuff/main_stuff.json" 
	else:
		_path = _path

	with open(_path) as f:
		st = json.load(f)

	return st


def base_form_gen(_path = None):
	"""
	converts stuff from the json specified in path 
	to wtforms field

	return dict --> {raw_+key: wtforms.field}
	"""

	cofn = confirur(_path)

	da = {}
	for k in cofn:

		fk = f"{k}:  ".replace("_"," ").title()
		ga = cofn[k]

		if ga["type"] == "string":
			da["raw_"+k] = StringField(fk)

		elif ga["type"] == "number":
			da["raw_"+k] = IntegerField(fk)

		elif ga["type"] == "boolean":
			da["raw_"+k] = BooleanField(fk)

		elif ga["type"] == "dropdown":
			da["raw_"+k] = SelectField(fk, choices=ga["options"])

		elif ga["type"] == "slider":

			da["raw_"+k] = IntegerRangeField(fk,
							 [NumberRange(min = ga["min"], max=ga["max"])])

	return da


def get_da_attr(form_class):
	"""
	gets da usefull class atrributes
	"""

	da = {}
	for i in dir(form_class):
		
		if not i.startswith("_") and i.startswith("raw_"):	
			da[i] = getattr(form_class, i)

	return da



class mainForm(FlaskForm):

	cofn = base_form_gen()
	sumbit = SubmitField("Submit")

	for k in cofn:
		vars()[k] = cofn.get(k) 


class advForm(FlaskForm):
    
    adv_path = stuffes_path+"/stuff/adv_stuff.json"
    cofn =  base_form_gen(adv_path)

    sumbit = SubmitField("Sumbit")
    for k in cofn:
    	vars()[k] = cofn.get(k)

class homeUrlForm(FlaskForm):
    
	homeUrl_path = stuffes_path+"/stuff/homeUrl_stuff.json"
	cofn =  base_form_gen(homeUrl_path)

	sumbit = SubmitField("Sumbit")
	for k in cofn:
		vars()[k] = cofn.get(k)




@app.route('/', methods=["GET"])
def home():
	return render_template("index.html")


@app.route('/<ty>_form', methods=['GET', 'POST'])
def supa_form(ty):

	dd = \
	{
	"basic":{"cls":basicForm,
			 "tt":"Basic Form",
			 "ht":"Basic Thing"},
	 "main": {"cls":mainForm,
			  "tt":"Main Form",
			 "ht":"Main Form"},
	 "adv":  {"cls":advForm,
			  "tt":"Advanced Form",
			 "ht":"Advanced Configurations"},
	 "homeUrl": {"cls":homeUrlForm,
		 		 "tt":"homeUrl config Form",
			 	 "ht":"Configurate Home Url"}
	 }
	
	if ty in dd:
		aform = dd.get(ty)['cls']()

	else:
		return render_template("error.html", error = "bad url")


	al = get_da_attr(aform)

	if ty != "basic":
		cofn = confirur(stuffes_path+f"/stuff/{ty}_stuff.json")
	else:
		cofn = {"name":{"content":"Joe"}}

	# Validate Form
	if aform.validate_on_submit():
		
		with open(stuffes_path+f"/stuffed/{ty}_stuffed.json", "w") as f:
			json.dump({ k:v.data  for k,v in al.items()}, f)
	else:
		pass

	return render_template("/apptrial/supaForm.html", aform = aform,
													atz = al,
													cofn = cofn,
											 		title_text = dd.get(ty)['tt'],
											 		header_text = dd.get(ty)['ht'])


# main for it
@app.route("/ty")
def gso_main():


	l = os.listdir(stuffes_path+"/stuffed/")
	l = [i.replace(".json","") for i in l]

	return render_template("ty_main.html", ls = l)


# da outpts of forms 
@app.route("/<ty>_gso")
def gso(ty):

	with open(stuffes_path+f"/stuffed/{ty}.json") as f:
			st = json.load(f)

	return render_template("ty.html", title = ty, ars = st)



if __name__ == '__main__':
    app.run(debug=True)
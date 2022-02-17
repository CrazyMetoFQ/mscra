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
	return render_template("/apptrial/findex.html")


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

# da outpts of forms 
@app.route("/<ty>_gso")
def gso(ty):

	with open(stuffes_path+f"/stuffed/{ty}_stuffed.json") as f:
			st = json.load(f)
	return str(st.items())

# @app.route('/basic_form', methods=['GET', 'POST'])
# def basic_form():

# 	name = None
# 	form = basicForm()

# 	# Validate Form
# 	if form.validate_on_submit():
# 		name = form.name.data
# 		form.name.data = '' ## clear
# 	else:
# 		pass

# 	return render_template("/forms/form_page.html", form = form,
# 											 name = name)


# @app.route("/main_form", methods=["GET", "POST"])
# def main_form():

# 	aform = mainForm()
# 	al = get_da_attr(aform)

# 	# Validate Form
# 	if aform.validate_on_submit():
		
# 		with open(stuffes_path+"/stuffed/main_stuffed.json", "w") as f:
# 			json.dump({ k:v.data  for k,v in al.items()}, f)

# 	else:
# 		pass

	
# 	dl = [(k, v.data) for k,v in al.items()]


# 	return render_template("/forms/main_form.html", aform = aform,
# 											 atls = al,
# 											 dls = dl)


# @app.route("/adv_form", methods=["GET", "POST"])
# def adv_form():

# 	name = None
# 	aform = advForm()

# 	al = get_da_attr(aform)

# 	# Validate Form
# 	if aform.validate_on_submit():
		
# 		with open(stuffes_path+"/stuffed/adv_stuffed.json", "w") as f:
# 			json.dump({ k:v.data  for k,v in al.items()}, f)

# 	else:
# 		pass

	
# 	dl = [(k, v.data) for k,v in al.items()]


# 	return render_template("/forms/adv_form.html", aform = aform,
# 											 atls = al,
# 											 dls = dl)



# @app.route("/homeUrl_form", methods=["GET", "POST"])
# def homeUrl_form():

# 	name = None
# 	aform = homeUrlForm()

# 	al = get_da_attr(aform)

# 	# Validate Form
# 	if aform.validate_on_submit():
		
# 		with open(stuffes_path+"/stuffed/homeUrl_stuffed.json", "w") as f:
# 			json.dump({ k:v.data  for k,v in al.items()}, f)

# 	else:
# 		pass

	
# 	dl = [(k, v.data) for k,v in al.items()]


# 	return render_template("/forms/homeUrl_form.html", aform = aform,
# 											 atls = al,
# 											 dls = dl)








if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask
from flask import request
from flask import render_template
import database

app = Flask(__name__)
app.config["TRAP_HTTP_EXCEPTIONS"]=True
app.config["DEBUG"]= True
property_names = ("open","name","pause","close")

def format(openkg, name, pause):
	return '[Open: %s][Name: %s][Pause: %s]' % (bool(openkg), name, bool(pause))


@app.route('/', methods=["GET"])
def home():
	if request.args:
		if "clearall" in request.args:
			init()
		else:
			modify(request.args)
			
	dbobj = database.Database()
	properties = dbobj.acquire_properties(*property_names)
	dbobj.release()
	return render_template("home.html",
		status=format(properties[0],properties[1],properties[2]),
		togglestatus=properties[0],
		pausestatus=properties[2]
		)
	
@app.route('/raw',methods=["GET"])
def raw():
	dbobj = database.Database()
	properties = dbobj.acquire_properties(*property_names)
	dbobj.release()
	return format(properties[0],properties[1],properties[2])

def modify(args):
	property_dic = {}
	for key in args:
		property_dic[key] = args[key]
	dbobj = database.Database()
	dbobj.modify_properties(**property_dic)
	dbobj.release()

def init():
	property_dic = {"open":0,"name":"","pause":0}
	dbobj = database.Database()
	dbobj.modify_properties(**property_dic)
	dbobj.release()

if __name__ == "__main__":
	app.run()

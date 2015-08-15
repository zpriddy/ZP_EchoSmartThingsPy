#! /usr/bin/python
#################################################
#			EchoPy Alexa API					#
#################################################
# Zachary Priddy - 2015 						#
# me@zpriddy.com 								#
#												#
# Features: 									#
#									 			#
#												#
#################################################
#################################################


#################################################
# TO DO:
# Move smartthings_settings to echopy_settings
# chage myApp to stApp and add nestApp

###############################################################################
# IMPORTS
###############################################################################

import echopy_app
import echopy_doc
import echopy_smartthings as myApp
import echopy_nest as nestApp
import smartthings_lib as st
import nest_lib as nest
import smartthings_settings as settings
import logger
from flask import Flask, render_template, Response, send_from_directory, request, current_app, redirect, jsonify, json
from flask_mail import Mail, Message


app = Flask(__name__)
mail=Mail(app)

app.config.update(
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = settings.mail_username,
	MAIL_PASSWORD = settings.mail_password
	)
mail=Mail(app)


###############################################################################
# BASE PAGES
###############################################################################

@app.route("/")
def home():
	count = myApp.get_st_user_count()
	return echopy_doc.main_page(count).format(settings.full_root_url)


@app.route(settings.url_root)
def main():
	count = myApp.get_st_user_count()
	return echopy_doc.main_page(count).format(settings.full_root_url)



@app.route(settings.url_root + "/privacy")
def privacy():
	return echopy_doc.privacy_policy.format(settings.full_root_url)

@app.route(settings.url_root + "/email_test")
def email():
	msg = Message(
			  'ZPriddy - Alexa Support',
		   sender='alexa@zpriddy.com',
		   recipients=
			   ['me@zpriddy.com'])
	msg.body = "This is the email body"
	mail.send(msg)
	return redirect(settings.url_root)


###############################################################################
# SMARTTHINGS PAGES
###############################################################################

@app.route(settings.url_root + "/EchoPyAPI",methods = ['POST'])
def apicalls():
	if request.method == 'POST':
		data = request.get_json()
		print "POST"
		sessionId = myApp.data_handler(data)
		return sessionId + "\n"

@app.route(settings.url_root + "/auth",methods = ['GET','POST'])
def auth():
	if request.method == 'GET':
		return echopy_doc.auth_page

	if request.method == 'POST':
		alexaId=request.form['AlexaID'].replace(' ','')
		clientId=request.form['SmartThingsClientID'].replace(' ','')
		clientSecret=request.form['SmartThingsClientSecret'].replace(' ','')
		clientEmail=request.form['Email'].replace(' ','')

		auth_uri = myApp.STAlexaAuth(alexaId,clientId,clientSecret,clientEmail)
		return redirect(auth_uri)


@app.route(settings.url_root + "/oauth2/<path:alexaId>",methods = ['GET'])
def authcode(alexaId):

	code = request.args.get('code')
	userId = myApp.getUserIdFromAlexaId(alexaId)

	if st.smartThingsToken(alexaId, userId,code):

		print "authed..."
		#print st.stData.getUser(userId).getClientInfo().token

		myApp.genNewAlexaId(userId,100)
		sendWelcomeEmail(userId)

	return redirect(settings.url_root)


@app.route(settings.url_root + "/samples",methods = ['GET','POST'])
def samples():
	if request.method == 'GET':
		return echopy_doc.samples_page.format(settings.full_root_url)

	if request.method == 'POST':
		try:
			alexaId=request.form['AlexaID']
			userId = myApp.getUserIdFromAlexaId(alexaId)
			samples = st.getSamples(userId)
			myApp.genNewAlexaId(userId,100)
			return echopy_doc.samples_results.replace('RESULTS',samples.replace('\n','&#13;&#10;')).format(settings.full_root_url)
		except:
			return echopy_doc.samples_results.replace('RESULTS',"AN ERROR HAS ACCRUED").format(settings.full_root_url)


###############################################################################
# NEST PAGES
###############################################################################

@app.route("/nest/")
def nest_page():
	return echopy_doc.nest_page.format(settings.full_root_url)

@app.route(settings.url_root + "/nest/EchoPyAPI",methods = ['POST'])
def nest_apicalls():
	if request.method == 'POST':
		data = request.get_json()
		print "POST"
		sessionId = nestApp.data_handler(data)
		return sessionId + "\n"

@app.route(settings.url_root + "/nest/auth",methods = ['GET','POST'])
def nest_auth():
	if request.method == 'GET':
		return echopy_doc.nest_auth_page(nestApp.get_nest_user_count())

	if request.method == 'POST':
		alexaId=request.form['AlexaID'].replace(' ','')
		clientEmail=request.form['Email'].replace(' ','')

		auth_uri = nestApp.nestAuth(alexaId)
		#auth_uri = myApp.STAlexaAuth(alexaId,clientId,clientSecret,clientEmail)
		return redirect(auth_uri)
		
@app.route(settings.url_root + "/nest/oauth2",methods = ['GET'])
def nest_authcode():
	alexaId = request.args.get('state')
	code = request.args.get('code')

	print alexaId, code

	if nestApp.nestToken(alexaId,code):
		print "authed.."
		userId = nestApp.getUserIdFromAlexaId(alexaId)
		nestApp.genNewAlexaId(userId,100)

	return redirect(settings.url_root)


###############################################################################
# OTHER
###############################################################################

def sendWelcomeEmail(userId):
	userEmail = myApp.getUserEmail(userId)
	msg = Message(
			  'ZPriddy - Alexa Support',
		   sender='alexa@zpriddy.com',
		   recipients=
			   [userEmail])
	msg.body = '''
	Welcome to ZPriddy Alexa SmartThings! This is a conformation that your account has been created and is linked to your SmartThings account! 

	Comming Soon: Better Support! :) 
	'''
	mail.send(msg)

def run_echopy_app():
	import SocketServer
	#SocketServer.BaseServer.handle_error = close_stream
	SocketServer.ThreadingTCPServer.allow_reuse_address = True
	echopy_app.run(app)



if __name__ == "__main__":
	st.smartThingsMongoDBInit()
	nest.nestDBInit()
	logger.init_logging()
	myApp.data_init()
	nestApp.data_init()
	run_echopy_app()

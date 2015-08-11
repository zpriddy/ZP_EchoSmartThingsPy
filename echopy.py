import os
import echopy_app
import echopy_doc
import echopy_smartthings as myApp
import smartthings_lib as st
import smartthings_settings as settings
import logger
from flask import Flask, render_template, Response, send_from_directory, request, current_app, redirect, jsonify, json


app = Flask(__name__)

@app.route("/")
def home():
	return echopy_doc.main_page


@app.route(settings.url_root)
def main():
	return echopy_doc.main_page

@app.route("/nest/")
def nest():
	return echopy_doc.nest_page


@app.route(settings.url_root + "/EchoPyAPI",methods = ['GET','POST'])
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
		alexaId=request.form['AlexaID']
		clientId=request.form['SmartThingsClientID']
		clientSecret=request.form['SmartThingsClientSecret']
		#userId = myApp.getUserIdFromAlexaId(alexaId)

		auth_uri = myApp.STAlexaAuth(alexaId,clientId,clientSecret)
		return redirect(auth_uri)


@app.route(settings.url_root + "/oauth2/<path:alexaId>",methods = ['GET'])
def authcode(alexaId):

	code = request.args.get('code')
	userId = myApp.getUserIdFromAlexaId(alexaId)

	if st.smartThingsToken(alexaId, userId,code):

		print "authed..."
		#print st.stData.getUser(userId).getClientInfo().token

		myApp.genNewAlexaId(userId,100)

	return redirect("/alexa")


@app.route(settings.url_root + "/samples",methods = ['GET','POST'])
def samples():
	if request.method == 'GET':
		return echopy_doc.samples_page

	if request.method == 'POST':
		try:
			alexaId=request.form['AlexaID']
			userId = myApp.getUserIdFromAlexaId(alexaId)
			samples = st.getSamples(userId)
			myApp.genNewAlexaId(userId,100)
			return echopy_doc.samples_results.replace('RESULTS',samples.replace('\n','&#13;&#10;'))
		except:
			return echopy_doc.samples_results.replace('RESULTS',"AN ERROR HAS ACCRUED")





def run_echopy_app():
	import SocketServer
	#SocketServer.BaseServer.handle_error = close_stream
	SocketServer.ThreadingTCPServer.allow_reuse_address = True
	echopy_app.run(app)


if __name__ == "__main__":
	st.smartThingsMongoDBInit()
	logger.init_logging()
	myApp.data_init()
	run_echopy_app()

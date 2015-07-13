import os
import echopy_app
import echopy_doc
import echopy_smartthings as myApp
import smartthings_lib as st
import smartthings_settings as settings
from flask import Flask, render_template, Response, send_from_directory, request, current_app, redirect, jsonify, json


app = Flask(__name__)


@app.route("/alexa/")
def main():
	return echopy_doc.main_page


@app.route("/alexa/EchoPyAPI",methods = ['GET','POST'])
def apicalls():
	if request.method == 'POST':
		data = request.get_json()
		print "POST"
		sessionId = myApp.data_handler(data)
		return sessionId + "\n"

@app.route("/alexa/auth/<path:userId>/<path:clientId>/<path:clientSecret>",methods = ['GET'])
def auth(userId,clientId,clientSecret):

	auth_uri = st.smartThingsAuth(userId,clientId,clientSecret)
	return redirect(auth_uri)

@app.route("/alexa/oauth2/<path:userId>",methods = ['GET'])
def authcode(userId):

	code = request.args.get('code')

	if st.smartThingsToken(userId,code):

		print st.stData.getUser(userId).getClientInfo().token

	return redirect("/alexa")


@app.route("/alexa/test/<path:userId>")
def test(userId):
	return str(st.stData.getUser(userId).getClientInfo().token) + "<br>" +  str(st.stData.getUser(userId).getClientInfo().url)

@app.route("/alexa/switch/<path:userId>/<path:deviceId>/<path:state>")
def switch(userId, deviceId, state):

	return str(st.st_switch(userId, deviceId, state))




def run_echopy_app():
	import SocketServer
	#SocketServer.BaseServer.handle_error = close_stream
	SocketServer.ThreadingTCPServer.allow_reuse_address = True
	echopy_app.run(app)


if __name__ == "__main__":
	st.smartThingsDataStoreInit()
	myApp.data_init()
	run_echopy_app()

import os
import echopy_app
import echopy_doc
import smartthings_doc as st_doc
import smartthings_lib as st
import smartthings_settings as settings
from flask import Flask, render_template, Response, send_from_directory, request, current_app, redirect, jsonify, json


appVersion = 1.0

debug = settings.debug


def data_init():
	global MyDataStore
	MyDataStore = DataStore()


def data_handler(rawdata):
	global MyDataStore
	currentSession = MyDataStore.getSession(rawdata['session'])
	currentUser = MyDataStore.getUser(rawdata['session'])
	currentRequest = rawdata['request']
	response = request_handler(currentSession, currentUser, currentRequest)


	if debug: print json.dumps({"version":appVersion,"response":response},sort_keys=True,indent=4)

	return json.dumps({"version":appVersion,"response":response},indent=2,sort_keys=True)


def request_handler(session, user, request):
	requestType = request['type']
	
	if requestType == "LaunchRequest":
		return launch_request(session, user, request)
	elif requestType == "IntentRequest":
		return intent_request(session, user, request)


def launch_request(session, user, request):
	if not st.isValidStUser(user.getUserId()):
		output_speech = "Current user is not a valid smart things user. Please look at the Echo app for help"
		output_type = "PlainText"

		card_type = "Simple"
		card_title = "SmartThings Control"
		card_content = "Current user is not a valid SmartThings user. Please authenticate user with userId: " + user.getUserId() + " to SmartThings as instructed in the README"

		response = {"outputSpeech": {"type":output_type,"text":output_speech},"card":{"type":card_type,"title":card_title,"content":card_content},'shouldEndSession':True}


		return response
	else:
		output_speech = "Welcome to Smart Things Control App. Please say a command."
		output_type = "PlainText"

		card_type = "Simple"
		card_title = "SmartThings Control - Welcome"
		card_content = "Welcome to SmartThings Control App. Please say a command."

		response = {"outputSpeech": {"type":output_type,"text":output_speech},"card":{"type":card_type,"title":card_title,"content":card_content},'shouldEndSession':False}

		return response

def intent_request(session, user, request):
	print "intent_request"

	if not st.isValidStUser(user.getUserId()):
		output_speech = "Current user is not a valid smart things user. Please look at the Echo app for help"
		output_type = "PlainText"

		card_type = "Simple"
		card_title = "SmartThings Control"
		card_content = "Current user is not a valid SmartThings user. Please authenticate user with userId: " + user.getUserId() + " to SmartThings as instructed in the README"

		response = {"outputSpeech": {"type":output_type,"text":output_speech},"card":{"type":card_type,"title":card_title,"content":card_content},'shouldEndSession':True}


		return response

	else:

		if request['intent']['name'] ==  "STSetMode":
			mode = request['intent']['slots']['mode']['value']
			output_speech = "Setting Smart Things to " + mode + " mode"
			output_type = "PlainText"

			card_type = "Simple"
			card_title = "SmartThings Control - Setting Mode"
			card_content = "Setting Smart Things to " + mode + " mode"

			response = {"outputSpeech": {"type":output_type,"text":output_speech},"card":{"type":card_type,"title":card_title,"content":card_content},'shouldEndSession':True}

			result = st.set_mode(user.getUserId(), mode)

			if mode == result:
				return response
			else:
				st_doc.generateError(result, "Setting Mode")

		elif request['intent']['name'] ==  "STSwitch":
			switchId = request['intent']['slots']['switch']['value']
			switchState = request['intent']['slots']['state']['value']

			result = st.set_mode(user.getUserId(), mode)

			output_speech = "Telling " + switchId + " to turn " + result
			output_type = "PlainText"

			card_type = "Simple"
			card_title = "SmartThings Control - Switch"
			card_content = "Telling " + switchId + " to turn " + result

			response = {"outputSpeech": {"type":output_type,"text":output_speech},"card":{"type":card_type,"title":card_title,"content":card_content},'shouldEndSession':True}

			if switchState == 'toggle':
				if result.lower() != 'on' and result.lower() != 'off':
					return st_doc.generateError(result, "Switch")
				else:
					return response

			elif state == result.lower():
				return response
			else:
				st_doc.generateError(result, "Switch")

		else:
			return launch_request(session, user, request) ##Just do the same thing as launch request





class Session:
	def __init__(self,sessionData):
		self.sessionId = sessionData['sessionId']


	def getSessionID(self):
		return self.sessionId

class User:
	def __init__(self,userId):
		self.userId = userId
		self.settings = {}

	def getUserId(self):
		return self.userId

class DataStore:
	def __init__(self):
		self.sessions = {}
		self.users = {}

	def getSession(self,session):
		if session['new'] is True or session['sessionId'] not in self.sessions:
			self.sessions[session['sessionId']] = Session(session)

		return self.sessions[session['sessionId']]

	def getUser(self,session):
		userId = session['user']['userId']
		if userId not in self.users:
			self.users[userId] = User(userId)

		return self.users[userId]


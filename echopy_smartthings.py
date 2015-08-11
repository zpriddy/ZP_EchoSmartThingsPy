import os
import echopy_app
import echopy_doc
import smartthings_doc as st_doc
import smartthings_lib as st
import smartthings_settings as settings
import date_check as dc
import random
import logger
import string
from flask import Flask, render_template, Response, send_from_directory, request, current_app, redirect, jsonify, json
import pymongo
from pymongo import MongoClient


appVersion = 1.0

debug = settings.debug


def STAlexaAuth(alexaId, clientId, clientSecret,clientEmail):
	global mongoST
	clientInfo = mongoST.find_one({'alexaId':alexaId.upper()})
	userId = clientInfo['st_amazonEchoID']

	auth_uri = st.smartThingsAuth(alexaId, userId, clientId, clientSecret, clientEmail)
	return auth_uri


def data_init():
	global mongoST
	mongoClient = MongoClient()
	mongoClient = MongoClient('localhost', 27017)
	mongoDB = mongoClient['AlexaSmartThingsDB']
	mongoST = mongoDB['ST']

	st.initAllSwitches()



def data_handler(rawdata):
	global mongoST
	logger.write_log(str(json.dumps(rawdata,sort_keys=True,indent=4)))
# Session will come later
#	currentSession = MyDataStore.getSession(rawdata['session'])
#	currentUser = MyDataStore.getUser(rawdata['session'])
	sessionId = rawdata['session']['sessionId']
	userId = rawdata['session']['user']['userId']
	currentRequest = rawdata['request']


	if len([a for a in mongoST.find({'st_amazonEchoID':userId})]) == 0:
		print "Need to add user into database"
		currentUser = {'_id':userId,'st_amazonEchoID':userId,'authenticated':False}
		mongoST.update({'st_amazonEchoID':userId},currentUser,True)


	timestamp = currentRequest['timestamp']


	if dc.datecheck(timestamp,5):
		response = request_handler(sessionId, userId, currentRequest)
	else:
		response = AlexaInvalidDate()

	if response is None:
		response = AlexaDidNotUnderstand()


	if debug: print json.dumps({"version":appVersion,"response":response},sort_keys=True,indent=4)
	logger.write_log(str(json.dumps({"version":appVersion,"response":response},sort_keys=True,indent=4)))

	return json.dumps({"version":appVersion,"response":response},indent=2,sort_keys=True)


def request_handler(sessionId, userId, request):
	global mongoST
	requestType = request['type']
	
	if requestType == "LaunchRequest":
		return launch_request(sessionId, userId, request)
	elif requestType == "IntentRequest":
		return intent_request(sessionId, userId, request)
	else:
		return AlexaDidNotUnderstand()


def launch_request(sessionId, userId, request):
	global mongoST
	if not st.isValidStUser(userId):
		genNewAlexaId(userId,10)
		alexaId = getAlexaIdFormUserID(userId)
		output_speech = "Current user is not a valid smart things user. Please look at the Echo app for help. New Alexa ID has been generated."
		output_type = "PlainText"

		card_type = "Simple"
		card_title = "SmartThings Control"
		card_content = "Current user is not a valid SmartThings user. Please authenticate user with Alexa ID: " + alexaId + " to SmartThings as instructed in the README"

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

def intent_request(sessionId, userId, request):
	print "intent_request"
	if debug: print json.dumps(request,sort_keys=True,indent=4)
	logger.write_log(str(json.dumps(request,sort_keys=True,indent=4)))
	if not st.isValidStUser(userId):
		genNewAlexaId(userId,10)
		alexaId = getAlexaIdFormUserID(userId)
		output_speech = "Current user is not a valid smart things user. Please look at the Echo app for help. New Alexa ID has been generated."
		output_type = "PlainText"

		card_type = "Simple"
		card_title = "SmartThings Control"
		card_content = "Current user is not a valid SmartThings user. Please authenticate user with Alexa ID: " + alexaId + " to SmartThings as instructed in the README"

		response = {"outputSpeech": {"type":output_type,"text":output_speech},"card":{"type":card_type,"title":card_title,"content":card_content},'shouldEndSession':True}


		return response

	else:
		try:
			if request['intent']['name'] ==  "STSetMode":
				mode = request['intent']['slots']['mode']['value']
				output_speech = "Setting Smart Things to " + mode + " mode"
				output_type = "PlainText"

				card_type = "Simple"
				card_title = "SmartThings Control - Setting Mode"
				card_content = "Setting Smart Things to " + mode + " mode"

				response = {"outputSpeech": {"type":output_type,"text":output_speech},"card":{"type":card_type,"title":card_title,"content":card_content},'shouldEndSession':True}

				result = st.set_mode(userId, mode)

				if mode == result:
					return response
				else:
					st_doc.generateError(result, "Setting Mode")

			elif request['intent']['name'] ==  "STPhrase":
				genNewAlexaId(userId,100)
				phrase = request['intent']['slots']['phrase']['value']
				output_speech = "Telling Smart Things to say " + phrase 
				output_type = "PlainText"

				card_type = "Simple"
				card_title = "SmartThings Control - HelloHome"
				card_content = "Telling Smart Things to say " + phrase 

				response = {"outputSpeech": {"type":output_type,"text":output_speech},"card":{"type":card_type,"title":card_title,"content":card_content},'shouldEndSession':True}

				result = st.set_phrase(userId, phrase)

				if phrase == result:
					return response
				else:
					st_doc.generateError(result, "Setting Phrase")

			elif request['intent']['name'] ==  "STSwitch":
				genNewAlexaId(userId,100)
				switchId = request['intent']['slots']['switch']['value']
				switchState = request['intent']['slots']['state']['value']

				result = st.st_switch(userId, switchId, switchState)

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

				elif switchState == result.lower():
					return response
				else:
					st_doc.generateError(result, "Switch")

			elif request['intent']['name'] ==  "STSamples":
				genNewAlexaId(userId,10)
				alexaId = getAlexaIdFormUserID(userId)
				output_speech = "Requesting new samples. New Alexa ID has been generated. Please see the Echo App."
				output_type = "PlainText"

				card_type = "Simple"
				card_title = "SmartThings Control"
				card_content = "New samples have been requested. Please authenticate user with Alexa ID: " + alexaId + " to https://alexa.zpriddy.com/alexa/samples"

				response = {"outputSpeech": {"type":output_type,"text":output_speech},"card":{"type":card_type,"title":card_title,"content":card_content},'shouldEndSession':True}


				return response

			else:
				output_speech = "Smart Things app did not understand your request. Please say it again."
				output_type = "PlainText"

				card_type = "Simple"
				card_title = "SmartThings Control - Welcome"
				card_content = "Welcome to SmartThings Control App. Please say a command."

				response = {"outputSpeech": {"type":output_type,"text":output_speech},"card":{"type":card_type,"title":card_title,"content":card_content},'shouldEndSession':False}

				return response
		except:
			return AlexaDidNotUnderstand()



def alexaIdGenerator(N):
	return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N))

def getUserIdFromAlexaId(alexaId):
	global mongoST
	currentUser = mongoST.find_one({'alexaId':alexaId})
	return currentUser['st_amazonEchoID']

def genNewAlexaId(userId,size):
	global mongoST
	currentUser = mongoST.find_one({'st_amazonEchoID':userId})
	newAlexaId = alexaIdGenerator(size)
	while len([a for a in mongoST.find({'alexaId':newAlexaId})]) > 0:
			newAlexaId = alexaIdGenerator(size)
	currentUser['alexaId'] = newAlexaId
	mongoST.update({'st_amazonEchoID':userId},currentUser,True)

def getAlexaIdFormUserID(userId):
	global mongoST
	currentUser = mongoST.find_one({'st_amazonEchoID':userId})
	return currentUser['alexaId']


def AlexaDidNotUnderstand():
	output_speech = "Smart Things app did not understand your request. Please say it again."
	output_type = "PlainText"

	card_type = "Simple"
	card_title = "SmartThings Control - Welcome"
	card_content = "Welcome to SmartThings Control App. Please say a command."

	response = {"outputSpeech": {"type":output_type,"text":output_speech},"card":{"type":card_type,"title":card_title,"content":card_content},'shouldEndSession':False}

	return response

def AlexaInvalidDate():
	output_speech = "The date and or time of the request does not match the durrent date."
	output_type = "PlainText"

	card_type = "Simple"
	card_title = "SmartThings Control - Error"
	card_content = "The date and or time of the request does not match the durrent date."

	response = {"outputSpeech": {"type":output_type,"text":output_speech},"card":{"type":card_type,"title":card_title,"content":card_content},'shouldEndSession':True}

	return response

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
		self.alexaIds = {}

	def getSession(self,session):
		if session['new'] is True or session['sessionId'] not in self.sessions:
			self.sessions[session['sessionId']] = Session(session)

		return self.sessions[session['sessionId']]

	def getUser(self,session):
		userId = session['user']['userId']
		if userId not in self.users:
			self.users[userId] = User(userId)
			alexaId = alexaIdGenerator(100)
			while alexaId in self.alexaIds.values():
				alexaId = alexaIdGenerator(100)
			self.alexaIds[userId] = alexaId


		return self.users[userId]

	def getAlexaUser(self,alexaId):

		userId = [a for a, alexa in self.alexaIds.items() if alexa == alexaId][0]
		return userId


	def getAlexaId(self, userId):
		return self.alexaIds[userId]

	def genNewAlexaId(self,userId, size):
		alexaId = alexaIdGenerator(size)
		while alexaId in self.alexaIds.values():
			alexaId = alexaIdGenerator(size)
		self.alexaIds[userId] = alexaId




#! /usr/bin/python
#################################################
#			NEST and Alexa Python API			#
#################################################
# Zachary Priddy - 2015 						#
# me@zpriddy.com 								#
#												#
# Features: 									#
#	- Read and Write capabilities with 			#
#		Amazon Echo and Nest 					#
#################################################
#################################################


#################################################
# TO DO:


###############################################################################
# IMPORTS
###############################################################################

import json
import echopy_doc
import nest_lib as nest
import echopy_settings as settings
import logger

import alexa_utils as utils
from flask import Flask, render_template, Response, send_from_directory, request, current_app, redirect, jsonify, json
import pymongo
from pymongo import MongoClient


appVersion = 1.0

debug = settings.debug



def nestAuth(alexaId):
	return nest.nestAuth(alexaId)

def nestToken(alexaId,authCode):
	return nest.nestToken(alexaId,authCode)

###############################################################################
# DATABASE INIT
###############################################################################

def data_init():
	global mongoNEST
	mongoClient = MongoClient()
	mongoClient = MongoClient('localhost', 27017)
	mongoDB = mongoClient['AlexaNestDB']
	mongoNEST = mongoDB['NEST']


###############################################################################
# INITAL DATA HANDLER
#
# Processes raw data from Alexa
###############################################################################
def data_handler(rawdata):
	global mongoNEST
	#currentSession = MyDataStore.getSession(rawdata['session'])
	#currentUser = MyDataStore.getUser(rawdata['session'])
	sessionId = rawdata['session']['sessionId']
	userId = rawdata['session']['user']['userId']
	currentRequest = rawdata['request']

	#Check for user in database
	if len([a for a in mongoNEST.find({'nest_amazonEchoID':userId})]) == 0:
		print "Need to add user into database"
		currentUser = {'_id':userId,'nest_amazonEchoID':userId,'authenticated':False}
		mongoNEST.update({'nest_amazonEchoID':userId},currentUser,True)


	#Check Timestamp of Request
	timestamp = currentRequest['timestamp']
	if utils.datecheck(timestamp,5):
		response = request_handler(sessionId, userId, currentRequest)
	else:
		response = utils.alexaInvalidDate('Nest Control')

	if response is None:
		response = utils.alexaDidNotUnderstand('Nest Control')

	if debug: print json.dumps({"version":appVersion,"response":response},sort_keys=True,indent=4)
	logger.write_log(str(json.dumps({"version":appVersion,"response":response},sort_keys=True,indent=4)))

	return json.dumps({"version":appVersion,"response":response},indent=2,sort_keys=True)

###############################################################################
# REQUEST HANDLERs
#
# Checks for the kind of request and pushes it to the correct handler
#
# intent_handler is where all requests are processed
###############################################################################

def request_handler(session, userId, request):
	requestType = request['type']

	if requestType == "LaunchRequest":
		return launch_request(session, userId, request)
	elif requestType == "IntentRequest":
		return intent_request(session, userId, request)
	else:
		return utils.alexaDidNotUnderstand('Nest Control') 


def launch_request(session, userId, request):
	if not nest.isValidNestUser(userId):
		alexaId = genNewAlexaId(userId,10)
		output_speech = "Current user is not a valid nest user. Please look at the Echo app for help"
		output_type = "PlainText"

		card_type = "Simple"
		card_title = "Nest Control - Setting Nest Temp"
		card_content = "Current user is not a valid nest user. Please authenticate user with userId: " + alexaId + " to Nest as instructed in the README"

		response = {"outputSpeech": {"type":output_type,"text":output_speech},"card":{"type":card_type,"title":card_title,"content":card_content},'shouldEndSession':True}


		return response
	else:
		output_speech = "Welcome to Nest Control App. Please say a command."
		output_type = "PlainText"

		card_type = "Simple"
		card_title = "Nest Control - Welcome"
		card_content = "Welcome to Nest Control App. Please say a command."

		response = {"outputSpeech": {"type":output_type,"text":output_speech},"card":{"type":card_type,"title":card_title,"content":card_content},'shouldEndSession':False}

		return response

def intent_request(session, userId, request):
	print "intent_request"

	if not nest.isValidNestUser(userId):
		alexaId = genNewAlexaId(userId,10)
		output_speech = "Current user is not a valid nest user. Please look at the Echo app for help"
		output_type = "PlainText"

		card_type = "Simple"
		card_title = "Nest Control - Setting Nest Temp"
		card_content = "Current user is not a valid nest user. Please authenticate user with userId: " + alexaId + " to Nest as instructed in the README"

		response = {"outputSpeech": {"type":output_type,"text":output_speech},"card":{"type":card_type,"title":card_title,"content":card_content},'shouldEndSession':True}


		return response

	else:

		if request['intent']['name'] ==  "NestSetTempIntent":
			nestTempValue = request['intent']['slots']['temp']['value']
			output_speech = "Setting Nest to " + str(nestTempValue) + " degrees fahrenheit"
			output_type = "PlainText"

			card_type = "Simple"
			card_title = "Nest Control - Setting Nest Temp"
			card_content = "Telling Nest to set to " + str(nestTempValue) + " degrees fahrenheit."

			response = {"outputSpeech": {"type":output_type,"text":output_speech},"card":{"type":card_type,"title":card_title,"content":card_content},'shouldEndSession':True}

			if int(nestTempValue) <= 90:
				nest.setTemperatureTargetAll(userId,int(nestTempValue))

			return response

		else:
			return launch_request(session, user, request) ##Just do the same thing as launch request
'''
		elif request['intent']['name'] ==  "NestCoolDownIntent":
			setTemp = nest.setTurnDownTemperatureAll(user.getUserId())
			output_speech = "Turning down the Nest"
			output_type = "PlainText"

			card_type = "Simple"
			card_title = "Nest Control - Setting Nest Temp"
			card_content = "Telling Nest to set to " + "str(setTemp+2)" + " degrees fahrenheit."

			response = {"outputSpeech": {"type":output_type,"text":output_speech},"card":{"type":card_type,"title":card_title,"content":card_content},'shouldEndSession':True}

			

			return response

		elif request['intent']['name'] ==  "NestWarmUpIntent":
			setTemp = nest.setTurnUpTemperatureAll(user.getUserId())
			output_speech = "Turning up the Nest"
			output_type = "PlainText"

			card_type = "Simple"
			card_title = "Nest Control - Setting Nest Temp"
			card_content = "Telling Nest to set to " + "str(setTemp+2)" + " degrees fahrenheit."

			response = {"outputSpeech": {"type":output_type,"text":output_speech},"card":{"type":card_type,"title":card_title,"content":card_content},'shouldEndSession':True}

			

			return response
		
		elif request['intent']['name'] ==  "HelpIntent":
			output_speech = "This is the Nest control app. You can tell me to set temperature to 74 degrees fahrenheit. You can also say that you are too hot or too cold and I will adjust the temperature by two degrees."
			output_type = "PlainText"

			card_type = "Simple"
			card_title = "Nest Control - Help"
			card_content = "This is the Nest control app. You can tell me to set temperature to 74 degrees. You can also say that you are too hot or too cold and I will adjust the temperature by two degrees."

			response = {"outputSpeech": {"type":output_type,"text":output_speech},"card":{"type":card_type,"title":card_title,"content":card_content},'shouldEndSession':False}


			return response
'''
		




def genNewAlexaId(userId,size):
	global mongoNEST
	currentUser = mongoNEST.find_one({'nest_amazonEchoID':userId})
	newAlexaId = utils.alexaIdGenerator(size)
	while len([a for a in mongoNEST.find({'alexaId':newAlexaId})]) > 0:
			newAlexaId = utils.alexaIdGenerator(size)
	currentUser['alexaId'] = newAlexaId
	mongoNEST.update({'nest_amazonEchoID':userId},currentUser,True)
	return newAlexaId

def getUserIdFromAlexaId(alexaId):
	global mongoNEST
	currentUser = mongoNEST.find_one({'alexaId':alexaId})
	return currentUser['nest_amazonEchoID']

###############################################################################
# TO BE DELETED
###############################################################################

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


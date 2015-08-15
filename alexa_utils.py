#! /usr/bin/python
#################################################
#			Alexa Utils							#
#################################################
# Zachary Priddy - 2015 						#
# me@zpriddy.com 								#
#												#
# Features: 									#
#												#
#################################################
#################################################


#################################################
# TO DO:

import datetime
import random
import string
from dateutil import parser


def datecheck(utcTimestamp,okaySecondsOffset):
	now = datetime.datetime.utcnow()
	print now
	ts = parser.parse(utcTimestamp.replace('Z','.00'))
	print ts
	offset = now - ts
	print offset
	if offset.seconds <= okaySecondsOffset: 
		return True
	else: 
		return False

def alexaInvalidDate(appName):
	output_speech = "The date and or time of the request does not match the durrent date."
	output_type = "PlainText"

	card_type = "Simple"
	card_title = appName + " - Error"
	card_content = "The date and or time of the request does not match the durrent date."

	response = {"outputSpeech": {"type":output_type,"text":output_speech},"card":{"type":card_type,"title":card_title,"content":card_content},'shouldEndSession':True}

	return response

def alexaDidNotUnderstand(appName):
	output_speech = appName + " app did not understand your request. Please say it again."
	output_type = "PlainText"

	card_type = "Simple"
	card_title = appName + " - Welcome"
	card_content = "Welcome to " + appName + " Control App. Please say a command."

	response = {"outputSpeech": {"type":output_type,"text":output_speech},"card":{"type":card_type,"title":card_title,"content":card_content},'shouldEndSession':False}

	return response

def alexaIdGenerator(N):
	return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N))
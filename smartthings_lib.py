#! /usr/bin/python
#################################################
#			SmartThings Python API				#
#################################################
# Zachary Priddy - 2015 						#
# me@zpriddy.com 								#
#												#
# Features: 									#
#	- Read and Write capabilities with 			#
#		SmartThings	using RESTapi				#
#################################################
#################################################


#################################################
# TO DO:
# -Add Thermostat Control
# -Add HUE Intagration


import json
import requests
import pickle
import smartthings_settings as settings
import sampleUtterances_generator as sampleGen
import logger
import os.path
import pymongo
from pymongo import MongoClient

from urllib import quote

debug = settings.debug
loadSettings = settings.smartthings_load_pickle
initUserData = settings.init_user_data
picklefile = 'smartthings_settings.pickle'



def smartThingsMongoDBInit():
	global mongoST
	mongoClient = MongoClient()
	mongoClient = MongoClient('localhost', 27017)
	mongoDB = mongoClient['AlexaSmartThingsDB']
	mongoST = mongoDB['ST']




def smartThingsAuth(altId, userId, clientId, clientSecret,clientEmail):
	global mongoST
	clientInfo = mongoST.find_one({'st_amazonEchoID':userId})

	clientInfo['st_clientId'] = clientId
	clientInfo['st_clientSecret'] = clientSecret
	clientInfo['st_clientEmail'] = clientEmail

	if debug: print 'ST Auth: ' + userId
	logger.write_log('ST Auth: ' + userId)
	auth_uri = settings.auth_uri_1.replace('CLIENTID',clientId).replace('CALLBACK',quote(settings.callback_url + altId))
	if debug: print 'Auth URL: ' + auth_uri
	logger.write_log('Auth URL: ' + auth_uri)

	mongoST.update({'st_amazonEchoID':userId},clientInfo,True)


	return auth_uri


def smartThingsToken(altId, userId, authCode):
	global mongoST
	clientInfo = mongoST.find_one({'st_amazonEchoID':userId})

	if debug: print 'ST Token: ' + userId
	logger.write_log('ST Token: ' + userId)
	token_uri = settings.auth_uri_2.replace('CODE',authCode).replace('CLIENTID',clientInfo['st_clientId']).replace('CLIENTSECRET',clientInfo['st_clientSecret']).replace('CALLBACK',quote(settings.callback_url + altId))
	if debug: print 'Token URL: ' + token_uri
	logger.write_log('Token URL: ' + token_uri)
	response = requests.get(token_uri).json()
	print response
	#clientInfo.setFromOauth(response)
	oauthResponse = response
	clientInfo['st_access_token'] = oauthResponse['access_token']
	clientInfo['st_token_type'] = oauthResponse['token_type']
	clientInfo['st_scope'] = oauthResponse['scope']
	clientInfo['st_expires_in'] = oauthResponse['expires_in']
	clientInfo['st_api'] = settings.api.replace('CLIENTID',str(clientInfo['st_clientId']))
	clientInfo['st_api_location'] = settings.api_location

	if debug: print "Response: " + str(response)
	logger.write_log("Response: " + str(response))

	#Get Endpoints
	endpoints_params = {
		"access_token": clientInfo['st_access_token']
	}
	if debug: print "Endpoints URL: " + str(clientInfo['st_api'])
	logger.write_log("Endpoints URL: " + str(clientInfo['st_api']))
	response = requests.get(clientInfo['st_api'], params=endpoints_params).json()  #[0]['url']
	print "Response: "
	print response
	response = response[0]['url']
	if debug: print "Endpoints: " + str(response)
	logger.write_log("Endpoints: " + str(response))
	clientInfo['st_url'] = response
	clientInfo['authenticated'] = True

	mongoST.update({'st_amazonEchoID':userId},clientInfo,True)

	return True





###############################################################################
# Mode
###############################################################################

def st_update_users_modes(userId):
	'''
	This is used to update the database of users modes
	'''
	if debug: print "Updating users modes"
	global mongoST
	clientInfo = mongoST.find_one({'st_amazonEchoID':userId})
	mode_uri = clientInfo['st_api_location'] + clientInfo['st_url'] + "/mode"
	mode_header = {
		"Authorization": clientInfo['st_token_type'] + " " + clientInfo['st_access_token']
	}
	clientInfo['st_modes'] = requests.get(mode_uri, headers=mode_header).json()

	if debug: print clientInfo['st_modes']

	mongoST.update({'st_amazonEchoID':userId},clientInfo,True)

	return True

def set_mode(userId,modeId):
	'''
	This is used to chnage current mode
	'''
	global mongoST
	clientInfo = mongoST.find_one({'st_amazonEchoID':userId})

	if 'st_modes' not in clientInfo:
		st_update_users_modes(userId)
		clientInfo = mongoST.find_one({'st_amazonEchoID':userId})

	modes = clientInfo['st_modes']
	selectedMode = [a for a in modes if a.lower().replace('!','') == modeId.lower()]

	if len(selectedMode) < 1:
		st_update_users_modes(userId)
		selectedMode = [a for a in modes if a.lower().replace('!','') == modeId.lower()]

	if len(selectedMode) > 1:
		return "Too many modes matched the mode name I heard: " + modeId
	if len(selectedMode) < 1:
		return "No modes matched the mode name I heard: " + modeId
	else:
		selectedMode = selectedMode[0]
		if debug: print selectedMode

		mode_json = {
			"mode":selectedMode
		}
		mode_header = {
				"Authorization": clientInfo['st_token_type'] + " " + clientInfo['st_access_token']
			}

		mode_uri = clientInfo['st_api_location'] + clientInfo['st_url'] + "/mode"

		response = requests.post(mode_uri, headers=mode_header, json=mode_json)
		response = requests.post(mode_uri, headers=mode_header, json=mode_json)

		if debug: print "Mode Response: " + str(response.json())
		logger.write_log("Mode Response: " + str(response.json()))

		return modeId if response.json()['error'] == 0 else "Unknown Error. See Logs"

###############################################################################
# Phrases
###############################################################################

def st_update_users_phrases(userId):
	'''
	This is used to update the database of users phrases
	'''
	if debug: print "Updating users phrases"
	global mongoST
	clientInfo = mongoST.find_one({'st_amazonEchoID':userId})
	phrase_uri = clientInfo['st_api_location'] + clientInfo['st_url'] + "/phrase"
	phrase_header = {
		"Authorization": clientInfo['st_token_type'] + " " + clientInfo['st_access_token']
	}
	clientInfo['st_phrases'] = requests.get(phrase_uri, headers=phrase_header).json()

	if debug: print clientInfo['st_phrases']

	mongoST.update({'st_amazonEchoID':userId},clientInfo,True)

	return True

def set_phrase(userId,phraseId):
	'''
	This is used to chnage current phrase
	'''
	global mongoST
	clientInfo = mongoST.find_one({'st_amazonEchoID':userId})

	if 'st_phrases' not in clientInfo:
		st_update_users_phrases(userId)
		clientInfo = mongoST.find_one({'st_amazonEchoID':userId})

	phrases = clientInfo['st_phrases']
	selectedPhrase = [a for a in phrases if a.lower().replace('!','') == phraseId.lower()]

	if len(selectedPhrase) < 1:
		st_update_users_phrases(userId)
		selectedPhrase = [a for a in phrases if a.lower().replace('!','') == phraseId.lower()]

	if len(selectedPhrase) > 1:
		return "Too many phrases matched the phrase name I heard: " + phraseId
	if len(selectedPhrase) < 1:
		return "No phrase matched the phrase name I heard: " + phraseId
	else:
		selectedPhrase = selectedPhrase[0]
		if debug: print "Phrase: " + selectedPhrase

		## Push chnages to REST API
		phrase_json = {
			"phrase":selectedPhrase
		}
		phrase_header = {
				"Authorization": clientInfo['st_token_type'] + " " + clientInfo['st_access_token']
		}

		phrase_uri = clientInfo['st_api_location'] + clientInfo['st_url'] + "/phrase"

		response = requests.post(phrase_uri, headers=phrase_header, json=phrase_json)

		if debug: print "Phrase Response: " + str(response.json())
		logger.write_log("Phrase Response: " + str(response.json()))

		return phraseId if response.json()['error'] == 0 else "Unknown Error. See Logs"


###############################################################################
# SWITCHES
###############################################################################

def st_update_users_switches(userId):
	'''
	This is used to update the database of users switches
	'''
	if debug: print "Updating users switches"
	global mongoST
	clientInfo = mongoST.find_one({'st_amazonEchoID':userId})
	switch_uri = clientInfo['st_api_location'] + clientInfo['st_url'] + "/switch"
	switch_header = {
		"Authorization": clientInfo['st_token_type'] + " " + clientInfo['st_access_token']
	}
	st_switches = requests.get(switch_uri, headers=switch_header).json()
	switches = []
	for switch in st_switches:
		switches.append(switch.replace(".","$$"))
	clientInfo['st_switches'] = switches

	if debug: print clientInfo['st_switches']

	mongoST.update({'st_amazonEchoID':userId},clientInfo,True)

	return True

def st_switch(userId, switchId, state):
	'''
	This is used to chnage the state of a switch from SmartThings. State = "ON" or "OFF" ot "TOGGLE"
	'''
	print "SWITCH"
	global mongoST
	clientInfo = mongoST.find_one({'st_amazonEchoID':userId})
	selectedSwitch = []


	if 'st_switches' not in clientInfo:
		st_update_users_switches(userId)
		clientInfo = mongoST.find_one({'st_amazonEchoID':userId})
	
	switches = clientInfo['st_switches']
	selectedSwitch = [a for a in switches if a.lower().replace('$$','.') == switchId.lower()]
	if len(selectedSwitch) < 1:
		st_update_users_switches(userId)
		selectedSwitch = [a for a in switches if a.lower().replace('$$','.') == switchId.lower()]

	if len(selectedSwitch) < 1:
		return "No switches matched the switch name I heard: " + switchId
	if len(selectedSwitch) > 1:
		return "Too many switches matched the switch name I heard: " + switchId
	else:
		selectedSwitch = selectedSwitch[0]
		if debug: print "Switching" + selectedSwitch
		return switch(userId,selectedSwitch,state)

def switch(userId,deviceId,state):
	'''
	This is used to chnage the state of a switch. State = "ON" or "OFF" ot "TOGGLE"
	'''
	global mongoST
	clientInfo = mongoST.find_one({'st_amazonEchoID':userId})

	if state.lower() == "toggle":
		state = "OFF" if getSwitchState(clientInfo, deviceId) == "on" else "ON"

	switch_uri = clientInfo['st_api_location'] + clientInfo['st_url'] + "/switch"
	switch_json = {
		"deviceId":deviceId,
		"command":state.lower()
	}
	switch_header = {
		"Authorization": clientInfo['st_token_type'] + " " + clientInfo['st_access_token']
	}

	response = requests.post(switch_uri, headers=switch_header, json=switch_json)
	if debug: print "Switch Response: " + str(response.json())
	logger.write_log("Switch Response: " + str(response.json()))

	return state if response.json()['error'] == 0 else "Unknown Error. See Logs"

def getSwitchState(clientInfo, deviceId):
	switch_uri = clientInfo['st_api_location'] + clientInfo['st_url'] + "/switch"
	switch_json = {
		"deviceId":deviceId
	}
	switch_header = {
		"Authorization": clientInfo['st_token_type'] + " " + clientInfo['st_access_token']
	}

	response = requests.get(switch_uri, headers=switch_header, json=switch_json).json()
	print response
	if debug: print "Switch Response: " + str(response)
	logger.write_log("Switch Response: " + str(response))

	return response['switch']

###############################################################################
# samples
###############################################################################

def getSamples(userId):
	global mongoST
	
	clientInfo = mongoST.find_one({'st_amazonEchoID':userId})

	mode_uri = clientInfo['st_api_location'] + clientInfo['st_url'] + "/mode"
	
	mode_header = {
		"Authorization": clientInfo['st_token_type'] + " " + clientInfo['st_access_token']
	}

	#get list of modes
	modeList = requests.get(mode_uri, headers=mode_header).json()

	switch_uri = clientInfo['st_api_location'] + clientInfo['st_url'] + "/switch"
	switch_header = {
		"Authorization": clientInfo['st_token_type'] + " " + clientInfo['st_access_token']
	}

	switchList = requests.get(switch_uri, headers=switch_header).json()


	phrase_uri = clientInfo['st_api_location'] + clientInfo['st_url'] + "/phrase"
	phrase_header = {
		"Authorization": clientInfo['st_token_type'] + " " + clientInfo['st_access_token']
	}

	phraseList = requests.get(phrase_uri, headers=phrase_header).json()


	return sampleGen.gen_all(modeList,switchList, phraseList)





def isValidStUser(userId):
	global mongoST
	if(mongoST.find_one({'st_amazonEchoID':userId})):
		if(mongoST.find_one({'st_amazonEchoID':userId})['authenticated']):
			return True
		else:
			return False
	else:
		return False


def initAllSwitches():
	global mongoST
	all_users = [a['_id'] for a in mongoST.find({})]
	print all_users

	for user in all_users:
		try:
			clientInfo = mongoST.find_one({'st_amazonEchoID':user})
			switch_uri = clientInfo['st_api_location'] + clientInfo['st_url'] + "/switch"
			switch_header = {
				"Authorization": clientInfo['st_token_type'] + " " + clientInfo['st_access_token']
			}

			st_switches = requests.get(switch_uri, headers=switch_header).json()
			switches = []
			for switch in st_switches:
				switches.append(switch.replace(".","$$"))
			clientInfo['st_switches'] = switches

			if debug: print clientInfo['st_switches']

			mongoST.update({'st_amazonEchoID':user},clientInfo,True)

		except:
			print "Error getting Switches"

	


def initAllPhrases():
	global mongoST
	all_users = [a['_id'] for a in mongoST.find({})]

	for user in all_users:
		try:
			clientInfo = mongoST.find_one({'st_amazonEchoID':user})
			phrase_uri = clientInfo['st_api_location'] + clientInfo['st_url'] + "/phrase"
			phrase_header = {
				"Authorization": clientInfo['st_token_type'] + " " + clientInfo['st_access_token']
			}
			clientInfo['phrases'] = requests.get(phrase_uri, headers=phrase_header).json()

			if debug: print clientInfo['phrases']

			mongoST.update({'st_amazonEchoID':user},clientInfo,True)

		except:
			print "Error getting Phrases"



def initAllModes():
	global mongoST
	all_users = [a['_id'] for a in mongoST.find({})]

	for user in all_users:
		try:
			clientInfo = mongoST.find_one({'st_amazonEchoID':user})
			mode_uri = clientInfo['st_api_location'] + clientInfo['st_url'] + "/mode"
			mode_header = {
				"Authorization": clientInfo['st_token_type'] + " " + clientInfo['st_access_token']
			}
			clientInfo['modes'] = requests.get(mode_uri, headers=mode_header).json()

			if debug: print clientInfo['modes']

			mongoST.update({'st_amazonEchoID':user},clientInfo,True)

		except:
			print "Error getting Modes"






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

from urllib import quote

debug = settings.debug
loadSettings = settings.smartthings_load_pickle
initUserData = settings.init_user_data
picklefile = 'smartthings_settings.pickle'


def smartThingsDataStoreInit():
	global stData

	if debug: print 'Datastore Init'

	if loadSettings and os.path.isfile(picklefile):
		stData = pickle.load(open(picklefile,'rb'))
		#del stData.stUsers['amzn1.account.AHVHAI2CGQGGRTBNSUQ5RGYHUYVA']
		#print stData.stUsers
		#print "Deleted Bruce"
	else:
		stData = STDataStore()

	if initUserData:
		#initAllSwitches()
		#initAllModes()
		initAllPhrases()


def smartThingsAuth(altId, userId, clientId, clientSecret):
	global stData
	currentClientUserId = userId
	currentClient = stData.getUser(userId)
	clientInfo = currentClient.getClientInfo()
	clientInfo.clientId = clientId
	clientInfo.clientSecret = clientSecret

	if debug: print 'ST Auth: ' + currentClientUserId
	logger.write_log('ST Auth: ' + currentClientUserId)
	auth_uri = settings.auth_uri_1.replace('CLIENTID',clientId).replace('CALLBACK',quote(settings.callback_url + altId))
	if debug: print 'Auth URL: ' + auth_uri
	logger.write_log('Auth URL: ' + auth_uri)

	return auth_uri


def smartThingsToken(altId, userId, authCode):
	global stData
	currentClient = stData.getUser(userId)
	clientInfo = currentClient.getClientInfo()

	if debug: print 'ST Token: ' + userId
	logger.write_log('ST Token: ' + userId)
	token_uri = settings.auth_uri_2.replace('CODE',authCode).replace('CLIENTID',clientInfo.clientId).replace('CLIENTSECRET',clientInfo.clientSecret).replace('CALLBACK',quote(settings.callback_url + altId))
	if debug: print 'Token URL: ' + token_uri
	logger.write_log('Token URL: ' + token_uri)
	response = requests.get(token_uri).json()
	clientInfo.setFromOauth(response)
	if debug: print "Response: " + str(response)
	logger.write_log("Response: " + str(response))

	#Get Endpoints
	endpoints_params = {
		"access_token": clientInfo.token
	}
	if debug: print "Endpoints URL: " + str(clientInfo.api)
	logger.write_log("Endpoints URL: " + str(clientInfo.api))
	response = requests.get(clientInfo.api, params=endpoints_params).json()  #[0]['url']
	print "Response: "
	print response
	print response[0]
	if debug: print "Endpoints: " + str(response)
	logger.write_log("Endpoints: " + str(response))
	clientInfo.url = response

	pickle.dump(stData,open(picklefile,"wb"))

	return True

def switch(userId,deviceId,state):
	'''
	This is used to chnage the state of a switch. State = "ON" or "OFF" ot "TOGGLE"
	'''
	global stData
	currentClient = stData.getUser(userId)
	clientInfo = currentClient.getClientInfo()

	if state.lower() == "toggle":
		state = "OFF" if getSwitchState(clientInfo, deviceId) == "on" else "ON"

	switch_uri = clientInfo.api_location + clientInfo.url + "/switch"
	switch_json = {
		"deviceId":deviceId,
		"command":state.lower()
	}
	switch_header = {
		"Authorization": clientInfo.token_type + " " + clientInfo.token
	}

	response = requests.post(switch_uri, headers=switch_header, json=switch_json)
	if debug: print "Switch Response: " + str(response.json())
	logger.write_log("Switch Response: " + str(response.json()))

	return state if response.json()['error'] == 0 else "Unknown Error. See Logs"

def getSwitchState(clientInfo, deviceId):
	switch_uri = clientInfo.api_location + clientInfo.url + "/switch"
	switch_json = {
		"deviceId":deviceId
	}
	switch_header = {
		"Authorization": clientInfo.token_type + " " + clientInfo.token
	}

	response = requests.get(switch_uri, headers=switch_header, json=switch_json).json()
	print response
	if debug: print "Switch Response: " + str(response)
	logger.write_log("Switch Response: " + str(response))

	return response['switch']

def set_mode(userId,modeId):
	'''
	This is used to chnage current mode
	'''
	global stData
	currentClient = stData.getUser(userId)
	clientInfo = currentClient.getClientInfo()

	modes = clientInfo.modes

	selectedMode = [a for a in modes if a.lower() == modeId.lower()]


	if len(selectedMode) < 1:
		mode_uri = clientInfo.api_location + clientInfo.url + "/mode"
		
		mode_header = {
			"Authorization": clientInfo.token_type + " " + clientInfo.token
		}

		#get list of modes
		clientInfo.modes = requests.get(mode_uri, headers=mode_header).json()
		modes = clientInfo.modes
		if debug: print modes
		logger.write_log(userId + " - Modes: " +  str(modes))


		selectedMode = [a for a in modes if a.lower() == modeId.lower()]

	if len(selectedMode) > 1:
		return "Too many modes matched the mode name I heard: " + modeId
	if len(selectedMode) < 1:
		return "No modes matched the mode name I heard: " + modeId

	selectedMode = selectedMode[0]

	mode_json = {
		"mode":selectedMode
	}
	mode_header = {
			"Authorization": clientInfo.token_type + " " + clientInfo.token
		}

	mode_uri = clientInfo.api_location + clientInfo.url + "/mode"

	response = requests.post(mode_uri, headers=mode_header, json=mode_json)
	response = requests.post(mode_uri, headers=mode_header, json=mode_json)

	if debug: print "Mode Response: " + str(response.json())
	logger.write_log("Mode Response: " + str(response.json()))

	return modeId if response.json()['error'] == 0 else "Unknown Error. See Logs"


def set_phrase(userId,phraseId):
	'''
	This is used to chnage current phrase
	'''
	global stData
	currentClient = stData.getUser(userId)
	clientInfo = currentClient.getClientInfo()

	phrases = clientInfo.phrases

	selectedPhrase = [a for a in phrases if a.lower() == phraseId.lower()]


	if len(selectedPhrase) < 1:
		phrase_uri = clientInfo.api_location + clientInfo.url + "/phrase"
		
		phrase_header = {
			"Authorization": clientInfo.token_type + " " + clientInfo.token
		}

		#get list of phrases
		clientInfo.phrases = requests.get(phrase_uri, headers=phrase_header).json()
		phrases = clientInfo.phrases
		if debug: print phrases
		logger.write_log(userId + " - Phrases: " +  str(phrases))


		selectedPhrase = [a for a in phrases if a.lower() == phraseId.lower()]

	if len(selectedPhrase) > 1:
		return "Too many phrases matched the phrase name I heard: " + phraseId
	if len(selectedPhrase) < 1:
		return "No phrase matched the phrase name I heard: " + phraseId

	selectedPhrase = selectedPhrase[0]

	phrase_json = {
		"phrase":selectedPhrase
	}
	phrase_header = {
			"Authorization": clientInfo.token_type + " " + clientInfo.token
		}

	phrase_uri = clientInfo.api_location + clientInfo.url + "/phrase"

	response = requests.post(phrase_uri, headers=phrase_header, json=phrase_json)


	if debug: print "Phrase Response: " + str(response.json())
	logger.write_log("Phrase Response: " + str(response.json()))

	return phraseId if response.json()['error'] == 0 else "Unknown Error. See Logs"

def st_switch(userId, switchId, state):
	'''
	This is used to chnage the state of a switch from SmartThings. State = "ON" or "OFF" ot "TOGGLE"
	'''
	global stData
	currentClient = stData.getUser(userId)
	clientInfo = currentClient.getClientInfo()

	switches = clientInfo.switches

	selectedSwitch = [a for a in switches if a.lower() == switchId.lower()]

	if len(selectedSwitch) < 1:

		switch_uri = clientInfo.api_location + clientInfo.url + "/switch"
		switch_header = {
			"Authorization": clientInfo.token_type + " " + clientInfo.token
		}

		clientInfo.switches = requests.get(switch_uri, headers=switch_header).json()
		switches = clientInfo.switches
		if debug: print "Switchs: " + str(switches)
		logger.write_log(userId + ' - Switches: ' + str(switches))

		selectedSwitch = [a for a in switches if a.lower() == switchId.lower()]

	if len(selectedSwitch) > 1:
		return "Too many switches matched the switch name I heard: " + switchId
	if len(selectedSwitch) < 1:
		return "No switches matched the switch name I heard: " + switchId

	selectedSwitch = selectedSwitch[0]

	return switch(userId,selectedSwitch,state)


def getSamples(userId):
	global stData
	currentClient = stData.getUser(userId)
	clientInfo = currentClient.getClientInfo()

	mode_uri = clientInfo.api_location + clientInfo.url + "/mode"
	
	mode_header = {
		"Authorization": clientInfo.token_type + " " + clientInfo.token
	}

	#get list of modes
	modeList = requests.get(mode_uri, headers=mode_header).json()

	switch_uri = clientInfo.api_location + clientInfo.url + "/switch"
	switch_header = {
		"Authorization": clientInfo.token_type + " " + clientInfo.token
	}

	switchList = requests.get(switch_uri, headers=switch_header).json()

	phrase_uri = clientInfo.api_location + clientInfo.url + "/phrase"
	phrase_header = {
		"Authorization": clientInfo.token_type + " " + clientInfo.token
	}

	phraseList = requests.get(phrase_uri, headers=phrase_header).json()


	return sampleGen.gen_all(modeList,switchList, phraseList)





def isValidStUser(userId):
	global stData
	return stData.isValidUser(userId)


def initAllSwitches():
	global stData
	all_users = stData.getAllUsers()

	for user in all_users:
		try:
			currentClient = stData.getUser(user)
			clientInfo = currentClient.getClientInfo()

			switch_uri = clientInfo.api_location + clientInfo.url + "/switch"
			switch_header = {
				"Authorization": clientInfo.token_type + " " + clientInfo.token
			}

			clientInfo.switches = requests.get(switch_uri, headers=switch_header).json()

			print clientInfo.switches

		except:
			pass

	pickle.dump(stData,open(picklefile,"wb"))


def initAllPhrases():
	global stData
	all_users = stData.getAllUsers()

	for user in all_users:
		try:
			currentClient = stData.getUser(user)
			clientInfo = currentClient.getClientInfo()

			phrase_uri = clientInfo.api_location + clientInfo.url + "/phrase"
			phrase_header = {
				"Authorization": clientInfo.token_type + " " + clientInfo.token
			}

			clientInfo.phrases = requests.get(phrase_uri, headers=phrase_header).json()

			print clientInfo.phrases

		except:
			pass

	pickle.dump(stData,open(picklefile,"wb"))

def initAllModes():
	global stData
	all_users = stData.getAllUsers()

	for user in all_users:
		try:
			currentClient = stData.getUser(user)
			clientInfo = currentClient.getClientInfo()

			mode_uri = clientInfo.api_location + clientInfo.url + "/mode"
			print mode_uri
		
			mode_header = {
				"Authorization": clientInfo.token_type + " " + clientInfo.token
			}

			#get list of modes
			clientInfo.modes = requests.get(mode_uri, headers=mode_header).json()

			print clientInfo.modes

		except:
			pass

	pickle.dump(stData,open(picklefile,"wb"))











###############################
# CLASSSES AND DATASTRUCTUE 
###############################

class STUser(object):
	def __init__(self,userId):
		self.userId = userId
		self.clientInfo = STClientInfo()
		#Use this to build out a list of all available devices and device types
		self.deviceList = None

	def getClientInfo(self):
		return self.clientInfo

class STClientInfo(object):
	def __init__(self):

		self._access_token = None
		self._expires_in = None
		self._client_id = None
		self._client_secret = None
		self._api = settings.api
		self._api_location = settings.api_location
		self._token_type = None 
		self._scope = None
		self._url = None 
		self._switches = {}
		self._modes = {}

	@property
	def token(self):
		return self._access_token

	@token.setter
	def token(self,value):
		self._access_token = value

	@property
	def api(self):
		return self._api

	@api.setter
	def api(self, value):
		self._api = value

	@property
	def api_location(self):
		return self._api_location

	@property
	def token_type(self):
		return self._token_type

	@property
	def url(self):
		return self._url

	@url.setter
	def url(self, value):
		self._url = value

	@property
	def clientId(self):
		return self._client_id
	
	@clientId.setter
	def clientId(self, value):
		print "SETTING CLIENT ID"
		self._client_id = value

	@property
	def clientSecret(self):
		return self._client_secret

	@clientSecret.setter
	def clientSecret(self, value):
		self._client_secret = value

	@property
	def switches(self):
		return self._switches

	@switches.setter
	def switches(self, value):
		self._switches = value

	@property
	def modes(self):
		return self._modes

	@modes.setter
	def modes(self, value):
		self._modes = value 

	def setFromOauth(self, oauthResponse):
		self._access_token = oauthResponse['access_token']
		self._token_type = oauthResponse['token_type']
		self._scope = oauthResponse['scope']
		self._expires_in = oauthResponse['expires_in']
		print self._api
		print self._client_id
		self._api = self._api.replace('CLIENTID',str(self._client_id))





class STDataStore(object):
	def __init__(self):
		self.stUsers = {}

	def getAllUsers(self):
		print self.stUsers
		return self.stUsers

	def addUser(self, userId, stUser):
		if not self.isValidUser(userId):
			self.stUsers[userId] = stUser

	def getUser(self, userId):
		if not self.isValidUser(userId):
			self.addUser(userId,STUser(userId))

		return self.stUsers[userId]

	def isValidUser(self, userId):
		if userId in self.stUsers:
			return True
		else:
			return False



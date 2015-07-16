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
import os.path

from urllib import quote

debug = settings.debug
loadSettings = True
picklefile = 'smartthings_settings.pickle'

def smartThingsDataStoreInit():
	global stData

	if debug: print 'Datastore Init'

	if loadSettings and os.path.isfile(picklefile):
		stData = pickle.load(open(picklefile,'rb'))
	else:
		stData = STDataStore()


def smartThingsAuth(altId, userId, clientId, clientSecret):
	global stData
	currentClientUserId = userId
	currentClient = stData.getUser(userId)
	clientInfo = currentClient.getClientInfo()
	clientInfo.clientId = clientId
	clientInfo.clientSecret = clientSecret

	if debug: print 'ST Auth: ' + currentClientUserId
	auth_uri = settings.auth_uri_1.replace('CLIENTID',clientId).replace('CALLBACK',quote(settings.callback_url + altId))
	if debug: print 'Auth URL: ' + auth_uri

	return auth_uri


def smartThingsToken(altId, userId, authCode):
	global stData
	currentClient = stData.getUser(userId)
	clientInfo = currentClient.getClientInfo()

	if debug: print 'ST Token: ' + userId
	token_uri = settings.auth_uri_2.replace('CODE',authCode).replace('CLIENTID',clientInfo.clientId).replace('CLIENTSECRET',clientInfo.clientSecret).replace('CALLBACK',quote(settings.callback_url + altId))
	if debug: print 'Token URL: ' + token_uri
	response = requests.get(token_uri).json()
	clientInfo.setFromOauth(response)
	if debug: print "Response: " + str(response)

	#Get Endpoints
	endpoints_params = {
		"access_token": clientInfo.token
	}
	if debug: print "Endpoints URL: " + str(clientInfo.api)
	response = requests.get(clientInfo.api, params=endpoints_params).json()[0]['url']
	if debug: print "Endpoints: " + str(response)
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

	return response['switch']

def set_mode(userId,modeId):
	'''
	This is used to chnage current mode
	'''
	global stData
	currentClient = stData.getUser(userId)
	clientInfo = currentClient.getClientInfo()

	mode_uri = clientInfo.api_location + clientInfo.url + "/mode"
	
	mode_header = {
		"Authorization": clientInfo.token_type + " " + clientInfo.token
	}

	#get list of modes
	modes = requests.get(mode_uri, headers=mode_header).json()
	if debug: print modes


	selectedMode = [a for a in modes if a.lower() == modeId.lower()]
	if len(selectedMode) > 1:
		return "Too many modes matched the mode name I heard: " + modeId
	if len(selectedMode) < 1:
		return "No modes matched the mode name I heard: " + modeId

	selectedMode = selectedMode[0]

	mode_json = {
		"mode":selectedMode
	}

	response = requests.post(mode_uri, headers=mode_header, json=mode_json)
	response = requests.post(mode_uri, headers=mode_header, json=mode_json)

	if debug: print "Mode Response: " + str(response.json())

	return modeId if response.json()['error'] == 0 else "Unknown Error. See Logs"


def st_switch(userId, switchId, state):
	'''
	This is used to chnage the state of a switch from SmartThings. State = "ON" or "OFF" ot "TOGGLE"
	'''
	global stData
	currentClient = stData.getUser(userId)
	clientInfo = currentClient.getClientInfo()

	switch_uri = clientInfo.api_location + clientInfo.url + "/switch"
	switch_header = {
		"Authorization": clientInfo.token_type + " " + clientInfo.token
	}

	switches = requests.get(switch_uri, headers=switch_header).json()
	if debug: print "Switchs: " + str(switches)

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


	return sampleGen.gen_all(modeList,switchList)





def isValidStUser(userId):
	global stData
	return stData.isValidUser(userId)








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



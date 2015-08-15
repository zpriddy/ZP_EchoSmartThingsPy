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
import requests

from bson.binary import Binary
import pickle 


import pymongo
from pymongo import MongoClient

import echopy_settings as settings

###############################################################################
# DB INIT
###############################################################################

def nestDBInit():
	global mongoNEST
	mongoClient = MongoClient()
	mongoClient = MongoClient('localhost', 27017)
	mongoDB = mongoClient['AlexaNestDB']
	mongoNEST = mongoDB['NEST']


###############################################################################
# NEST AUTH
###############################################################################

def nestAuth(alexaId):
	auth_uri = settings.nest_auth_uri_1.replace('STATE',alexaId)
	return auth_uri

def nestToken(alexaId,authCode):
	global mongoNEST
	clientInfo = mongoNEST.find_one({'alexaId':alexaId})
	clientInfo['nest_authcode'] = authCode
	userId = clientInfo['nest_amazonEchoID']

	token_uri = settings.nest_auth_uri_2.replace('AUTHORIZATION_CODE',authCode)
	usertoken = requests.post(token_uri).json()['access_token']

	clientInfo['nest_usertoken'] = usertoken

	mongoNEST.update({'nest_amazonEchoID':userId},clientInfo,True)

	getStructures(userId)
	getThermostats(userId)


	clientInfo = mongoNEST.find_one({'alexaId':alexaId})
	clientInfo['authenticated'] = True
	mongoNEST.update({'nest_amazonEchoID':userId},clientInfo,True)

	return True

###############################################################################
# READ DATA FROM NEST
###############################################################################

def getStructures(userId):
	global mongoNEST
	clientInfo = mongoNEST.find_one({'nest_amazonEchoID':userId})

	access_token = clientInfo['nest_usertoken']
	structures_uri = "https://developer-api.nest.com/structures?auth=" + access_token

	structures_raw = requests.get(structures_uri).json()
	clientInfo['structures'] = objectToData(NestStructure(structures_raw))

	print dataToObject(clientInfo['structures'])._structures

	mongoNEST.update({'nest_amazonEchoID':userId},clientInfo,True)


def getThermostats(userId):
	global mongoNEST
	clientInfo = mongoNEST.find_one({'nest_amazonEchoID':userId})

	access_token = clientInfo['nest_usertoken']
	thermostats_uri = "https://developer-api.nest.com/devices/thermostats?auth=" + access_token

	thermostats_raw = requests.get(thermostats_uri).json()
	clientInfo['thermostats'] = objectToData(NestThermostats(thermostats_raw))

	print dataToObject(clientInfo['thermostats'])._thermostats

	mongoNEST.update({'nest_amazonEchoID':userId},clientInfo,True)

###############################################################################
# SET ALL THERMOSTATS
###############################################################################

def setTemperatureTargetAll(userId,temp):
	global mongoNEST
	clientInfo = mongoNEST.find_one({'nest_amazonEchoID':userId})

	access_token = clientInfo['nest_usertoken']
	thermostats = dataToObject(clientInfo['thermostats']).getThermostatIds()

	command = {"target_temperature_f":int(temp)}

	commandSucessfull = True

	for device in thermostats:
		print "Device:" + device
		command_uri = 'https://developer-api.nest.com/devices/thermostats/' + device + "?auth=" + access_token
		print command_uri
		response = requests.put(url=command_uri, data=command, json=command)
		print response
		print response.text
		if response.status_code != 200:
			commandSucessfull = False

	return commandSucessfull


###############################################################################
# Turn down temp by 2 degress
###############################################################################

def setTurnDownTemperatureAll(userId):
	print "Turn Down Temp"
	global mongoNEST
	clientInfo = mongoNEST.find_one({'nest_amazonEchoID':userId})

	access_token = clientInfo['nest_usertoken']
	commandSucessfull = True
	
	getThermostats(userId)
	thermostats = dataToObject(clientInfo['thermostats']).getThermostats()

	temps = []

	for device in thermostats:
		print "Setting Temp for: " + device
		currentTemp = thermostats[device]['status']['target_temperature_f']
		deviceId = thermostats[device]['id']
		temps.append(int(currentTemp)-2)
		command = {"target_temperature_f":int(currentTemp)-2}
		command_uri = 'https://developer-api.nest.com/devices/thermostats/' + deviceId + "?auth=" + access_token
		response = requests.put(url=command_uri, data=command, json=command)
		if response.status_code != 200:
			commandSucessfull = False
			return False

	return sum(temps)/len(temps)

###############################################################################
# NEST TEMP UP
###############################################################################


def setTurnUpTemperatureAll(userId):
	global mongoNEST
	clientInfo = mongoNEST.find_one({'nest_amazonEchoID':userId})

	access_token = clientInfo['nest_usertoken']
	commandSucessfull = True
	
	getThermostats(userId)
	thermostats = dataToObject(clientInfo['thermostats']).getThermostats()

	temps = []

	for device in thermostats:
		print "Setting Temp for: " + device
		currentTemp = thermostats[device]['status']['target_temperature_f']
		deviceId = thermostats[device]['id']
		temps.append(int(currentTemp)+2)
		command = {"target_temperature_f":int(currentTemp)+2}
		command_uri = 'https://developer-api.nest.com/devices/thermostats/' + deviceId + "?auth=" + access_token
		response = requests.put(url=command_uri, data=command, json=command)
		if response.status_code != 200:
			commandSucessfull = False
			return False

	return sum(temps)/len(temps)

###############################################################################
# THIS IS WHERE I LEFT OFF
###############################################################################

def setModeAll(userId,mode):
	global mongoNEST
	clientInfo = mongoNEST.find_one({'nest_amazonEchoID':userId})
	access_token = clientInfo['nest_usertoken']
	structures = dataToObject(clientInfo['structures']).getStructures()
	command = {"away":mode}

	commandSucessfull = True


	for structure in structures:
		command_uri = 'https://developer-api.nest.com/structures/' + structure + "?auth=" + access_token
		response = requests.put(url=command_uri, data=command, json=command)
		if response.status_code != 200:
			commandSucessfull = False

	return commandSucessfull
	
'''
def getAvgTemp(userId):
	global nestData
	currentUser = nestData.getUser(userId)
	getThermostats(userId)
	thermostats = currentUser.getThermostats()
	
	temps = [a['status']['ambient_temperature_f'] for a in thermostats.values()]
	avgTemp = sum(temps)/len(temps)

	return avgTemp

def getAvgTargetTemp(userId):
	global nestData
	currentUser = nestData.getUser(userId)
	getThermostats(userId)
	thermostats = currentUser.getThermostats()
	
	temps = [a['status']['target_temperature_f'] for a in thermostats.values()]
	avgTemp = sum(temps)/len(temps)

	return avgTemp
'''
###############################################################################
# CHECK IF USER IS VALID USER
###############################################################################

def isValidNestUser(userId):
	global mongoNEST
	if(mongoNEST.find_one({'nest_amazonEchoID':userId})):
		if(mongoNEST.find_one({'nest_amazonEchoID':userId})['authenticated']):
			return True
		else:
			return False
	else:
		return False

###############################################################################
# CLASS STRUCTURES FOR DATA STORAGE
###############################################################################


def objectToData(pObject):
	return Binary(pickle.dumps(pObject))

def dataToObject(pData):
	return pickle.loads(pData)

class NestStructure:
	def __init__(self,rawData):
		self._structures = {}

		for key in rawData.keys():
			self._structures[rawData[key]['name']] = {"id":key,"thermostats":rawData[key]['thermostats']}

	def getStructureIds(self):
		ids = [a['id'] for a in self._structures.values()]
		return ids

	def getStructures(self):
		return self._structures

class NestThermostats:
	def __init__(self,rawData):
		self._thermostats = {}

		for key in rawData.keys():
			self._thermostats[rawData[key]['name']] = {"id":key,"status":rawData[key]}

	def getThermostatIds(self):
		ids = [a['id'] for a in self._thermostats.values()]
		return ids

	def getThermostats(self):
		return self._thermostats


###############################################################################
# TO BE DELETED
###############################################################################



class NestUser: 
	def __init__(self,userId):
		self.userId = userId
		self.token = None
		self.devices = {}
		self.structures = {}
		self.thermostats = {}
		self.authed = False

	def setToken(self,token):
		self.token = token
		self.authed = True

	def getToken(self):
		return self.token

	def getThermostats(self):
		return self.thermostats

	def getThermostatIds(self):
		ids = [a['id'] for a in self.thermostats.values()]
		return ids

	def getStructureIds(self):
		ids = [a['id'] for a in self.structures.values()]
		return ids

class NestDataStore:
	def __init__(self):
		self.nestUsers = {}

	def addUser(self, userId, nestUser):
		if userId not in self.nestUsers:
			self.nestUsers[userId] = nestUser

	def getUser(self, userId):
		if userId not in self.nestUsers:
			self.addUser(userId,NestUser(userId))

		return self.nestUsers[userId]

	def isValidUser(self,userId):
		if userId in self.nestUsers:
			return True
		else:
			return False

		

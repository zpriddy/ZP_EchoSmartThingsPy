#######################################
# This will help generate all sample 
# utterances for an indaviduals system
#######################################

import sampleUtterances_dict as sud
valid = set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.')

def gen_modes(modeList):
	output = ""
	for mode in modeList:
		if(set(mode).issubset(valid)):
			for sample in sud.mode_samples:
				output += sample.replace('ZPMODEALEXA',mode.lower()).replace('(','').replace(')','') + "<br>"
			output += "<br>"
	return output

def gen_switches(switchList):
	output = ""
	for switch in switchList:
		if(set(switch).issubset(valid)):
			for sample in sud.switch_samples:
				output += sample.replace('ZPSWITCHALEXA',switch.lower()).replace('(','').replace(')','') + "<br>"
			output += "<br>"
	return output

def gen_phrases(phraseList):
	output = ""
	for phrase in phraseList:
		if(set(phrase.replace('!','')).issubset(valid)):
			for sample in sud.phrase_samples:
				output += sample.replace('ZPPHRASEALEXA',phrase.lower()).replace('(','').replace(')','').replace('!','') + "<br>"
			output += "<br>"
	return output

def gen_defaults():
	output = ""
	for sample in sud.default_samples:
		output += sample + "<br>"
	return output

def gen_all(modeList, switchList, phraseList):
	output = ""
	output += gen_modes(modeList)
	output += gen_switches(switchList)
	output += gen_phrases(phraseList)
	output += gen_defaults()
	return output


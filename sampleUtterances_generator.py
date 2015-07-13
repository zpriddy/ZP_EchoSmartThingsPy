#######################################
# This will help generate all sample 
# utterances for an indaviduals system
#######################################

import sampleUtterances_dict as sud

def gen_modes(modeList):
	output = ""
	for mode in modeList:
		for sample in sud.mode_samples:
			output += sample.replace('ZPMODEALEXA',mode.lower()).replace('(','').replace(')','') + "<br>"
		output += "<br>"
	return output

def gen_switches(switchList):
	output = ""
	for switch in switchList:
		for sample in sud.switch_samples:
			output += sample.replace('ZPSWITCHALEXA',switch.lower()).replace('(','').replace(')','') + "<br>"
		output += "<br>"
	return output

def gen_all(modeList, switchList):
	output = ""
	output += gen_modes(modeList)
	output += gen_switches(switchList)
	return output


#######################################
# This will help generate all sample 
# utterances for an indaviduals system
#######################################

import sampleUtterances_dict as sud

def gen_modes(modeList):
	for mode in modeList:
		for sample in sud.mode_samples:
			print sample.replace('ZPMODEALEXA',mode.lower()).replace('(','').replace(')','')
		print ""

def gen_switches(switchList):
	for switch in switchList:
		for sample in sud.switch_samples:
			print sample.replace('ZPSWITCHALEXA',switch.lower()).replace('(','').replace(')','')
		print ""


def gen_all(modeList, switchList):
	gen_modes(modeList)
	gen_switches(switchList)


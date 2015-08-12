def generateError(errorMessage, functionName):
	output_speech = "Smart Things encountered and error. " + errorMessage + ". Please try again"
	output_type = "PlainText"

	card_type = "Simple"
	card_title = "SmartThings Error - " + functionName
	card_content = "Smart Things encountered and error. " + errorMessage

	response = {"outputSpeech": {"type":output_type,"text":output_speech},"card":{"type":card_type,"title":card_title,"content":card_content},'shouldEndSession':False}

	print response
	return response
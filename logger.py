import smartthings_settings as settings
import datetime





def init_logging():
	if settings.logger_enabled:
		global filename
		filename = settings.log_file_base + '-' + datetime.datetime.now().isoformat() + '.log'
		logfile = open(filename,'wb')
		logfile.close()


def write_log(message):
	if settings.logger_enabled:
		global filename
		with open(filename, 'a') as logfile:
			now = datetime.datetime.now().isoformat()
			logfile.write(now + ' :')
			logfile.write(message)
			logfile.close()






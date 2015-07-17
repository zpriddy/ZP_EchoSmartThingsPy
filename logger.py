import smartthings_settings as settings
import datetime





def init_logging():
	if settings.logger_enabled:
		global logfile
		filename = settings.log_file_base + '-' + datetime.datetime.now().isoformat() + '.log'
		logfile = open(filename,'wb')

def write_log(message):
	if settings.logger_enabled:
		global logfile
		now = datetime.datetime.now().isoformat()
		logfile.write(now + ' :')
		logfile.write(message)






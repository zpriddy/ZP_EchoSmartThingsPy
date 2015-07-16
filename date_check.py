import datetime
from dateutil import parser


def datecheck(utcTimestamp,okaySecondsOffset):
	now = datetime.datetime.utcnow()
	print now
	ts = parser.parse(utcTimestamp.replace('Z','.00'))
	print ts
	offset = now - ts
	print offset
	if offset.seconds <= okaySecondsOffset: 
		return True
	else: 
		return False


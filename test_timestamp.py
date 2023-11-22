from datetime import datetime, timedelta
import time

#timestamp = time.mktime(datetime.today().timetuple())
now = datetime.now()
start_timestamp = time.mktime(now.timetuple())
end_timestamp = time.mktime( (now + timedelta(days=30)).timetuple())
print(f'today : {start_timestamp}')
print(f'today + 30 : {end_timestamp}')
print(f'diff : {end_timestamp - start_timestamp}')
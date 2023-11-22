from datetime import datetime, timedelta
import time

end_timestamp = 0

def get_expiration_endtime():
    global end_timestamp
    #timestamp = time.mktime(datetime.today().timetuple())
    now = datetime.now()
    start_timestamp = time.mktime(now.timetuple())
    end_timestamp = time.mktime( (now + timedelta(days=30)).timetuple())

    return end_timestamp

def get_expiration_datetime():
    global end_timestamp
    get_expiration_endtime()
    expiration_datetime = str(datetime.fromtimestamp(end_timestamp))
    print(f'expiration_datetime : {expiration_datetime}')
    return expiration_datetime

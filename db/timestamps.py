import datetime

def current_date():
    i = datetime.datetime.now()
    time = "%s-%s-%s" % (i.day, i.month, i.year)
    return time

def current_timestamp():
    return datetime.datetime.now()
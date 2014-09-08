from time import gmtime


def generate_datetimestamp():
    curtime = gmtime()
    time = "{0}-{1}-{2}.{3}:{4}.{5}".format(
           curtime.tm_year,
           curtime.tm_mon,
           curtime.tm_mday,
           curtime.tm_hour,
           curtime.tm_min,
           curtime.tm_sec)

    return time

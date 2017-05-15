import datetime
from database.reservation import Reservation


def convert_date(d):
    return datetime.datetime.strptime(d, '%H:%M')

def convert_date_2(d):
    return datetime.datetime.strptime(d, '%Y-%m-%dT%H:%M')

def get_numeric_val(d):
    h, m = d.split(':')
    ans = int(h) * 60 + int(m)
    return ans

def dump_to_xml(id):
    resv = Reservation.by_rid(id)
    ans = '<?xml version="1.0" encoding="UTF-8"?><top>'
    for r in resv:
        ans += '<reservation>'
        ans += '<start_time>' + str(r.start_time) + '</start_time>'
        ans += '<end_time>' + str(r.end_time) + '</end_time>'
        ans += '<user>' + r.belonging_user + '</user>'
        ans += '<resource_id>' + r.rid + '</resource_id>'
        ans += '</reservation>'
    ans += '</top>'
    return ans




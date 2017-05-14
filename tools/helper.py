import datetime

def convert_date(d):
    return datetime.datetime.strptime(d, '%H:%M')

def get_numeric_val(d):
    h, m = d.split(':')
    ans = int(h) * 60 + int(m)
    return ans
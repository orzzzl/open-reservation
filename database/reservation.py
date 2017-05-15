from google.appengine.ext import db
from flask import render_template
import datetime
from resource import Resource

def reservation_key(name='default'):
    return db.Key.from_path('reservation', name)

class Reservation(db.Model):
    """
    The database of the reservation information
    """
    created = db.DateTimeProperty(auto_now_add=True)
    start_time = db.DateTimeProperty(required=True)
    end_time = db.DateTimeProperty(required=True)
    belonging_user = db.StringProperty(required=True)
    rid = db.StringProperty(required=True)


    @classmethod
    def create_reservation(cls, st, et, bu, r):
        return Reservation(start_time=st, end_time=et, belonging_user=bu, rid=r)

    @classmethod
    def by_username(cls, u):
        now_time = datetime.datetime.now()
        res = db.GqlQuery("select * from Reservation where belonging_user = :u", u=u)
        ans = []
        for i in res:
            if i.end_time > now_time:
                ans.append(i)
        return ans

    @classmethod
    def by_rid(cls, r):
        now_time = datetime.datetime.now()
        res = db.GqlQuery("select * from Reservation where rid = :r", r=r)
        ans = []
        for i in res:
            if i.end_time > now_time:
                ans.append(i)
        return ans

    @classmethod
    def delete_by_id(cls, id):
        res = db.GqlQuery("select * from Reservation")
        for r in res:
            if str(r.key()) == id:
                r.delete()

    def get_name(self):
        ans = Resource.by_id(self.rid)
        return ans.name

    def get_start_time(self):
        return str(self.start_time)

    def get_end_time(self):
        return str(self.end_time)

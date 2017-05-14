from google.appengine.ext import db
from flask import render_template
from tag import Tag

def res_key(name='default'):
    return db.Key.from_path('resource', name)

class Resource(db.Model):
    """
    The database of the resource information
    """
    created = db.DateTimeProperty(auto_now_add=True)
    start_time = db.DateTimeProperty(required=True)
    end_time = db.DateTimeProperty(required=True)
    start_time_n = db.IntegerProperty(required=True)
    end_time_n = db.IntegerProperty(required=True)
    last_time = db.DateTimeProperty()
    belonging_user = db.StringProperty(required=True)
    name = db.StringProperty(required=True)

    @classmethod
    def create_res(self, res_name, start_time, end_time, start_time_n, end_time_n, bu):
        return Resource(
                            parent=res_key(), start_time=start_time, end_time=end_time,
                            start_time_n=start_time_n, end_time_n=end_time_n,
                            belonging_user=bu,
                            name=res_name, reserved=False
                        )

    @classmethod
    def get_all(cls):
        res = db.GqlQuery("select * from Resource")
        return res

    @classmethod
    def by_id(cls, k):
        res = Resource.get_all()
        for r in res:
            if str(r.key()) == k:
                return r
        return None

    def tags(self):
        tgs = Tag.by_rid(str(self.key()))
        return tgs


    def render(self):
        return render_template('res.html', r=self)





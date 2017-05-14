from google.appengine.ext import db

def tag_key(name='default'):
    return db.Key.from_path('tag', name)

class Tag(db.Model):
    name = db.StringProperty(required=True)
    rid = db.StringProperty(required=True)

    @classmethod
    def create_tag(self, t, r):
        return Tag(parent=tag_key(), name=t, rid=r)

    @classmethod
    def by_rid(cls, rid):
        res = db.GqlQuery("select * from Tag where rid = :r", r=rid)
        return res

    @classmethod
    def get_all(cls):
        ans = db.GqlQuery("select * from Tag")
        return ans

    @classmethod
    def by_key(cls, k):
        all_instance = Tag.get_all()
        for i in all_instance:
            if str(i.key()) == k:
                return i
        return None

    @classmethod
    def by_name(cls, n):
        ans = db.GqlQuery("select * from Tag where name = :n", n = n)
        return ans

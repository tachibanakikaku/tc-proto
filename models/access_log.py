from google.appengine.ext import ndb

class AccessLog(ndb.Model):
    accessed_at = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def newest(cls):
        return cls.query().order(-cls.accessed_at).fetch(1)

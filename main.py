import webapp2
from datetime import datetime
from google.appengine.ext import ndb

class AccessLog(ndb.Model):
    accessed_at = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def newest(cls):
        return cls.query().order(-cls.accessed_at).fetch(1)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello Google App Engine (webapp2 + NDB)!')

class DbPage(webapp2.RequestHandler):
    def get(self):
        cnt = AccessLog.query().count()
        if cnt == 0:
            self.response.write('no data')
        else:
            newest = AccessLog.newest()
            self.response.write("count {}".format(cnt))
            self.response.write('<br />')
            self.response.write(newest)
    def post(self):
        AccessLog().put()

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/db', DbPage),
], debug=True)

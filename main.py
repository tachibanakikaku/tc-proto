import jinja2
import os
import webapp2

from access_log import AccessLog
from google.appengine.api import users

env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(
        os.path.dirname('./{}/'.format('templates'))))

def login(req):
    user = users.get_current_user()
    if user:
        url = users.create_logout_url(req.uri)
        url_linktext = 'Logout'
    else:
        url = users.create_login_url(req.uri)
        url_linktext = 'Login'
    return user, url, url_linktext

class MainPage(webapp2.RequestHandler):
    def get(self):
        login_info = login(self.request)
        values = {
            'user': login_info[0],
            'greeting': 'Hello Google App Engine World!',
            'url': login_info[1],
            'url_linktext': login_info[2]
        }
        template = env.get_template('index.html')
        self.response.write(template.render(values))

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

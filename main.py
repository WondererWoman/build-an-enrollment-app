
import webapp2, jinja2, os
from google.appengine.ext import db
from models import User, Course

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainHandler(Handler):
    """Renders home page"""
    def render_mainpage(self):
        self.render("mainpage.html")

    def get(self):
        self.render_mainpage()

class BrowseHandler(Handler):
    """Renders list of all available courses."""
    def render_courselist(self, name="", description=""):
        courses = db.GqlQuery("SELECT * FROM Course")
        self.render("browse.html", name=name, description=description)

    def get(self):
        self.render_courselist()


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/browse', BrowseHandler)
], debug=True)
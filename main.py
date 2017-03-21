
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
    def render_courselist(self, name="", instructor=""):
        courses = db.GqlQuery("SELECT * FROM Course ")
        self.render("browse.html", name=name, instructor=instructor, courses=courses)

    def get(self):
        self.render_courselist()

class ViewCourseHandler(Handler):
    """Renders individual course info"""
    def get(self, id, name="", instructor="", description=""):
        indcourse = Course.get_by_id(int(id), parent=None)
        self.render("indclass.html", name=name, instructor=instructor, description=description, indcourse=indcourse)

class CreateCourseHandler(Handler):
    """Renders create.html template and adds course to db"""
    def render_create(self, name="", instructor="", description="", error=""):
        self.render("create.html", name=name, instructor=instructor, description=description, error=error)

    def get(self):
        self.render_create()

    def post(self):
        name = self.request.get("course_name")
        instructor = self.request.get("instructor_name")
        description = self.request.get("description")

        if name and instructor and description:
            b = Course(name=name, instructor=instructor, description=description)
            b.put()

            self.redirect('/browse')
        else:
            error = "Please enter a Course Name, Instructor, and Description!"
            self.render_create(name, instructor, description, error)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/browse', BrowseHandler),
    webapp2.Route('/<id:\d+>', ViewCourseHandler),
    ('/create', CreateCourseHandler)
], debug=True)


import webapp2, jinja2, os, re
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

class SignUpHandler(Handler):
    def valid_un(self, name):
        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        return not not USER_RE.match(name)

    def valid_match(self, password, verify):
        Password_RE = re.compile("^.{3,20}$")
        return (password == verify)

    def valid_password(self, password):
        Password_RE = re.compile("^.{3,20}$")
        return Password_RE.match(password)


    def valid_email(self, email):
        email_RE = re.compile("^[\S]+@[\S]+.[\S]+$")
        return email_RE.match(email)

    def get(self):
        self.render("signup.html")

    def post(self):
        name = self.request.get("name")
        email = self.request.get("email")
        password = self.request.get("password")
        verify = self.request.get("verify")

        username1 = self.valid_un(name)
        user_match = self.valid_match( password, verify)
        user_email = self.valid_email(email)
        user_password = self.valid_password(password)

        error_username = ""
        if username1:
            error_username += ""
        else:
            error_username += "That is not a valid username"

        error_password = ""
        if user_password:
            error_password += ""
        else:
            error_password += "That is not a valid password"

        error_verify = ""
        if user_match:
            error_verify += ""
        else:
            error_verify += "Your passwords do not match"

        error_email = ""
        if user_email:
            error_email += ""
        elif email == "":
            error_email += ""
            user_email = True
        else:
            error_email += "That is not a valid email"

        if username1 and user_match and user_password and user_email:
            new_user = User(username=name, pw_hash=password, email=email)
            new_user.put()
            self.redirect('/browse')

        else:
            self.render("signup.html", error_username=error_username, error_password=error_password,
                        error_verify=error_verify, error_email=error_email)


class CreateCourseHandler(Handler):
    """Renders course creation template and adds course to db"""
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

class StudentHandler(Handler):
    def render_student(self, name="", course="", mylist=""):
        courses = db.GqlQuery("SELECT * FROM Course ")
        self.render("student.html", name=name, courses=courses, mylist=mylist)

    def get(self):
        self.render_student()

    def post(self):
        """Puts classes that have been enrolled in into 'mylist'"""
        coursename= self.request.get("course_list")
        mycourses = MyCourse()
        mylist = []
        if coursename not in mylist:
            mylist.append(coursename)
        self.render_student(name=coursename, course="", mylist=mylist)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/browse', BrowseHandler),
    webapp2.Route('/<id:\d+>', ViewCourseHandler),
    ('/create', CreateCourseHandler),
    ('/student', StudentHandler),
    ('/signup', SignUpHandler)
], debug=True)

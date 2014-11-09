import flask
app = flask.Flask(__name__)
app.config['DEBUG'] = True

from google.appengine.ext import ndb
import ku_grabber
import model

@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'

@app.route('/update')
def update():
    # Now we are making changes on a GET request. Not smart.
    ku_grabber.update()
    return 'Done'

@app.route('/show')
def show():
    # course_dbs, course_cursor = model.Course.query(ancestor=ndb.Key('Book','all'))
    # print model.Course.query().fetch()
    # course_dbs, course_cursor = model.Course.query().fetch()
    course_dbs = model.Course.query().fetch()
    # course_dbs = []
    return flask.render_template(
        'courses.html',
        course_dbs=course_dbs)

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404

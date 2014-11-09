from flask import Flask
app = Flask(__name__)
app.config['DEBUG'] = True

import ku_grabber

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
    course_dbs, course_cursor = model.Course.get_dbs()
    return flask.render_template(
        'templates/courses.html',
        course_dbs=course_dbs)

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404

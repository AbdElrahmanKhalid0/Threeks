from Threeks.errors import errors
from flask import render_template

@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/error.html', error=error, error_title='Page Not Found'), 404

@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/error.html', error=error, error_title='Permission Error'), 403

@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/error.html', error=error, error_title='Some Trouble'), 500
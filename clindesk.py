import logging
import os
import re
import urlparse
from flask import Flask, make_response, redirect, render_template, request, url_for
app = Flask(import_name=__name__, static_folder='s')


def register_email_logger(subject_tag, log_level):
    """
    This sends e-mails to ec2-crashes when something fails in Prod or Staging. 

    It took me a while to figure this out:
     ** The log hangler is basically *ignored* if debug=True **
    """
    ADMINS = ['ec2-prodlogs@clindesk.org']
    from logging import Formatter
    from logging.handlers import SMTPHandler
    mail_handler = SMTPHandler('email-smtp.us-east-1.amazonaws.com',
                               'ec2-crashes@clindesk.org',
                               ADMINS,
                               'ClinDesk %s Crash' % subject_tag,
                               # Only sorta-secret. We haven't requested SES prod bits, so we can only
                               # send to domains we own & addresses we verify. Little abuse potential. --semenko
                               ('AKIAIEBTTF4MLQZ3CPAQ', 'AsD8aexgu9TUcIRB1bHmfG/zF2YMyv3Bze5LTpQzw6p1'),
                               secure=())
    mail_handler.setFormatter(Formatter('''
Message type:       %(levelname)s
Location:           %(pathname)s:%(lineno)d
Module:             %(module)s
Function:           %(funcName)s
Time:               %(asctime)s

Message:

%(message)s
'''))
    mail_handler.setLevel(log_level)
    app.logger.addHandler(mail_handler)

    
# Settings based on prod/staging/dev
supervisor_name = os.environ.get('SUPERVISOR_PROCESS_NAME', False)
if supervisor_name == 'clindesk-prod':
    register_email_logger('Prod', logging.WARNING)
    app.config['STATIC_ROOT'] = 'http://static.clindesk.org/s/'
elif supervisor_name == 'clindesk-staging':
    register_email_logger('Staging', logging.WARNING)
    app.config['STAGING'] = True
else:
    # We're probably in a local dev instance.
    pass


# Create a static() handler and send content to static.clindesk.org
def static(path):
    root = app.config.get('STATIC_ROOT', None)
    if root is None: # Just use /s/ instead of CDN
        return url_for('static', filename=path)
    return urlparse.urljoin(root, path)

@app.context_processor
def inject_static():
    return dict(static=static)



#################################
# Blocks for URL Control
#################################

######
# *** Static-ish Pages
######

@app.route("/")
@app.route("/index.html") # TODO: Standardize toplevel url.
def page_index():
    return render_template('index.html')

# Support & Donate
@app.route("/support.html")
def page_support():
    return render_template('support.html')

# Help & FAQ
@app.route("/help.html")
def page_help():
    return render_template('help.html')

# About Us
@app.route("/about.html")
def page_about():
    return render_template('about.html')


######
# *** Disease / Drug Pages
######

@app.route("/diseases/")
def page_diseases_index():
    return render_template('diseases.html')

@app.route("/diseases/<level1>/")
def page_diseases_toplevel(level1):
    # TODO: Does Flask provide a similar function?
    # I see safe_join ...
    cleaned = alnum_only(level1)
    return "%s" % (cleaned)

@app.route("/diseases/<level1>/<level2>/")
def page_diseases_level2(level1, level2):
    return "%s %s" % (level1, level2)



######
# *** Odd URLs and support functions
######

@app.route("/setcookie", methods=['GET', 'POST'])
def clicked_disclaimer():
    """ Give the user a cookie if they dismiss the disclaimer. """
    resp = make_response()
    resp.set_cookie(key='disclaimer',
                    value='true',
                    max_age=60, # For testing. *60*24,
                    expires=None,
                    path='/',
                    domain=None,
                    secure=None,
                    httponly=False,
                    )
    return resp


@app.errorhandler(404)
def page_not_found(error):
    """ Return our generic error page. """
    return render_template('errors/404.html'), 404


# Strip non-alnum
pattern = re.compile('[\W+]')
def alnum_only(input):
    return pattern.sub('', input)


if __name__ == "__main__":
    # This is fine for prod purposes:
    #   The prod servers run via gunicorn & gevent, which won't invoke __main__
    app.run(host='0.0.0.0', port=5000, debug=True)


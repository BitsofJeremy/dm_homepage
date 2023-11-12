from flask import Flask, render_template
import logging
from logging.config import dictConfig
import os
import newrelic.agent

newrelic.agent.initialize('./newrelic.ini')

# define logging dict
dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '{"date": "%(asctime)s", '
                      '"log_level": "%(levelname)s", '
                      '"module": "%(module)s", '
                      '"message": "%(message)s"}'
         }
    },
    'handlers': {
        'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'default',
            'filename': 'app.log',
            'maxBytes': 1024000,
            'backupCount': 3
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': [
            'wsgi',
            'file'
        ]
    }
})


app = Flask(__name__)
logger = logging.getLogger(__name__)

# Version
APP_VERSION = '0.0.1'

# Threads
app.config['THREADS_PER_PAGE'] = 2

# Enable protection against *Cross-site Request Forgery (CSRF)*
app.config['CSRF_ENABLED'] = True

# Use a secure, unique and absolutely secret key for
# signing the data.
# Secret key for signing cookies
app.config['CSRF_SESSION_KEY'] = os.getenv('CSRF_SESSION_KEY')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    """
    Renders the index page
    """
    logger.debug(app.config)
    return render_template(
        'index.html',
        version=APP_VERSION,
    )


if __name__ == "__main__":
    app.run()

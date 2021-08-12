# Imports
import flask
import os
from werkzeug.utils import secure_filename    # Needed for image upload
import sys

# Configure app
app = flask.Flask(__name__)
app.config.from_object(__name__) # Load config from thsie file (permit_generator.py)
app.config.update(dict(
SECRET_KEY = 'key',
USERNAME = 'admin',
PASSWORD = 'default'
))




# Register view blueprints
sys.path.append(os.path.dirname(__file__))
import views
app.register_blueprint(views.views)



if __name__ == '__main__':
    app.run()

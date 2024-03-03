#!/usr/bin/python3
""" Flask Application """
from models import storage
from api.v1.views import app_views
import os
from os import environ
from flask import Flask, render_template, make_response, jsonify
from flask_cors import CORS
from flasgger import Swagger
from flasgger.utils import swag_from
from werkzeug.exceptions import HTTPException

#Application variable
app = Flask(__name__)
swagger = Swagger(app)

#global strict_slashes
app.url_map.strict_slashes = False

#flask server environment
host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', '5000')

#CORS
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

#Blueprint
#app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """
    calls close() function on the current SQLAlchemy Session
    after each request
    """
    storage.close()


@app.errorhandler(404)
def handle_404(exception):
    """
    handles 404 errors
    """
    code = exception.__str__().split()[0]
    description = exception.description
    message = {'error': description}
    return make_response(jsonify(message), code)

@app.errorhandler(400)
def handle_400(exception):
    """
    handles 400 errors
    """
    code = exception.__str__().split()[0]
    description = exception.description
    message = {'error': description}
    return make_response(jsonify(message), code)

@app.errorhandler(Exception)
def global_error_handler(error):
    """
    handles all errors
    """
    if isinstance(error, HTTPException):
        if type(error).__name__ == 'NotFound':
            error.description = "Not found"
            message = {'error': error.description}
            code = error.code
    else:
        message = {'error': error.description}
        code = 500

    return make_response(jsonify(message), code)

def setup_global_errors():
    """
    updates HTTPException class with custom error messages
    """
    for cls in HTTPException.__subclasses__():
        app.register_error_handler(cls, global_error_handler)
        


if __name__ == "__main__":
    """ 
    Main App
    """
    #initialize global error handling
    setup_global_errors()
    #run app
    app.run(host=host, port=port,)

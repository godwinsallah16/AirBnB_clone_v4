#!/usr/bin/python3
""" Starts a Flash Web Application """
from models import storage
from flask import Flask, render_template, url_for
import uuid

app = Flask(__name__)
app.url.map.strict_slashes = False
port = 5000
host = '0.0.0.0'
# app.jinja_env.trim_blocks = True
# app.jinja_env.lstrip_blocks = True


@app.teardown_appcontext
def teardown_db(exception):
    """
    calls close() function on the current SQLAlchemy Session
    after each request
    """
    storage.close()


@app.route('/1-hbnb/')
def hbnb(id=None):
    """
    HBNB is alive! 
    handles requests to custom template with states, cities, and amenities
    """
    state_objs = storage.all('State').values()
    states = dict([state.name, state] for state in state_objs)
    amenity = storage.all('Amenity').values()
    places = storage.all('Place').values()
    users =dict([user.id,"{} {}".format(user.first_name, user.last_name)]
                for user in storage.all('User').values())
    return render_template('1-hbnb.html',
                           states=states,
                           amenities=amenity,
                           places=places,
                           users=users,
                           cache_id=uuid.uuid4())

if __name__ == "__main__":
    """ Main App """
    app.run(host=host, port=port)

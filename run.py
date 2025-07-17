#run.py
import sys

from flask.cli import FlaskGroup

from app import app, db


cli: FlaskGroup = FlaskGroup(app)

if __name__ == '__main__':

    if 'run' in sys.argv:
        app.run(debug=True)
    else:
        cli()

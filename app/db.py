import sqlite3
from aifc import open

import click
from flask import current_app, g
from flask.cli import with_appcontext


def init_app(app):
     app.teardown_appcontext(close_db)
     app.cli.add_command(cli_init_db)

def get_db():
    """ Get the database """    
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'], 
        detect_types=sqlite3.PARSE_DECLTYPES
        )

        g.db.row_factory= sqlite3.Row
    return g.db


def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf-8'))  

@click.command('init-db')
@with_appcontext
def cli_init_db():
    """ clear the existing data an create the tables """
    init_db()
    click.echo("Initializing the DB")

def close_db(e=None):
    db = g.pop('db',None)
    if db is not None:
        db.close()

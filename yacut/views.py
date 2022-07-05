from flask import render_template
from strgen import StringGenerator

from . import app, db
from .models import URL_map

def get_unique_short_id():
    return StringGenerator(r'[\da-zA-Z]{6}').render()


@app.route('/')
def index_view():
    link = ''
    return render_template('index.html')

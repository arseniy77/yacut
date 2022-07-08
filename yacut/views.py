from flask import abort, flash, redirect, render_template
from strgen import StringGenerator

from . import app, db
from .CONSTANTS import RANDOM_SHORTLINK_REGEXP
from .forms import UrlForm
from .models import URL_map


def get_unique_short_id():
    for _ in range(5000):
        id = StringGenerator(RANDOM_SHORTLINK_REGEXP).render()
        if not URL_map.query.filter_by(short=id).first():
            return id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = UrlForm()
    if form.validate_on_submit():
        short = form.custom_id.data
        if URL_map.query.filter_by(short=short).first():
            flash(f'Имя {short} уже занято!')
            return render_template('mapper.html', form=form)
        if short == '':
            short = get_unique_short_id()
        map = URL_map(
            original=form.original_link.data,
            short=short,
        )
        db.session.add(map)
        db.session.commit()
        return render_template('mapper.html', map=map, form=form)
    return render_template('mapper.html', form=form)


@app.route('/<short>')
def shortlink_map_view(short):
    mapped_link = URL_map.query.filter_by(short=short).first()
    if mapped_link:
        return redirect(mapped_link.original)
    abort(404)

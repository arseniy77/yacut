import re

from flask import jsonify, request

from . import app, db
from .CONSTANTS import SHORTLINK_REGEXP
from .error_handlers import InvalidAPIUsageError
from .models import URL_map
from .views import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def create_id():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsageError('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsageError('\"url\" является обязательным полем!')
    if 'custom_id' in data and data['custom_id'] is not None:
        custom_id = data['custom_id']
        if URL_map.query.filter_by(short=custom_id).first() is not None:
            raise InvalidAPIUsageError(f'Имя \"{custom_id}\" уже занято.')
        if not re.match(f'{SHORTLINK_REGEXP}|^$', custom_id):
            raise InvalidAPIUsageError(
                'Указано недопустимое имя для короткой ссылки', 400)
    if data.get('custom_id') is None or data.get('custom_id') == '':
        data['custom_id'] = get_unique_short_id()
    map = URL_map()
    map.from_dict(data)
    db.session.add(map)
    db.session.commit()
    print(map.to_dict())
    return jsonify(map.to_dict()), 201


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_url(short_id):
    map = URL_map.query.filter_by(short=short_id).first()
    if map is None:
        raise InvalidAPIUsageError('Указанный id не найден', 404)
    return jsonify({'url': map.original})

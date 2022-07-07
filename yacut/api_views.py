import re

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URL_map
from .views import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def create_id():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')
    if 'custom_id' in data:
        if URL_map.query.filter_by(short=data['custom_id']).first() is not None or not re.match(r'^[\da-zA-Z]{1,16}$|^$', data['custom_id']):
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    if 'custom_id' not in data or data.get('custom_id') == '':
        data['custom_id'] = get_unique_short_id()
    map = URL_map()
    map.from_dict(data)
    db.session.add(map)
    db.session.commit()
    print(map.to_dict())
    return jsonify(map.to_dict()), 201

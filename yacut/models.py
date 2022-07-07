from datetime import datetime

from flask import url_for

from yacut import db


class URL_map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(4096), nullable=False)
    short = db.Column(db.String(16), unique=True, nullable=False, index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    # Вот он — новый метод:
    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for('shortlink_map_view', short=self.short, _external=True)
        )

    def from_dict(self, data):
        # Для каждого поля модели, которое можно заполнить...
        # for field in ['url', 'custom_id']:
        #     # ...выполняется проверка: есть ли ключ с таким же именем в словаре
        #     if field in data:
        #         # Если есть — добавляем значение из словаря
        #         # в соответствующее поле объекта модели:
        #         setattr(self, field, data[field])
        if 'url' in data:
            setattr(self, 'original', data['url'])
        if 'custom_id' in data:
            setattr(self, 'short', data['custom_id'])

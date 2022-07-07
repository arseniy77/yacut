from datetime import datetime

from flask import url_for
from strgen import StringGenerator

from yacut import db


class URL_map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(4096), nullable=False)
    short = db.Column(
        db.String(16),
        unique=True,
        nullable=False,
        index=True,
        default=StringGenerator(r'[\da-zA-Z]{6}').render()
    )
    timestamp = db.Column(
        db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for(
                'shortlink_map_view',
                short=self.short,
                _external=True
            )
        )

    def from_dict(self, data):
        if 'url' in data:
            setattr(self, 'original', data['url'])
        if 'custom_id' in data:
            setattr(self, 'short', data['custom_id'])

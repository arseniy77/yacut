from datetime import datetime

from yacut import db


class URL_map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(4096), nullable=False)
    short = db.Column(db.String(16), unique=True, nullable=False, index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    # Вот он — новый метод:
    def to_dict(self):
        return dict(
            id=self.id,
            original=self.original,
            short=self.short,
            timestamp=self.timestamp
        )

    def from_dict(self, data):
        # Для каждого поля модели, которое можно заполнить...
        for field in ['original', 'short', 'timestamp']:
            # ...выполняется проверка: есть ли ключ с таким же именем в словаре
            if field in data:
                # Если есть — добавляем значение из словаря
                # в соответствующее поле объекта модели:
                setattr(self, field, data[field])

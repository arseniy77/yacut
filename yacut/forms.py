from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp


class UrlForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, 4096)]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Length(1, 16, message='Длина не более 16 символов'),
                    Optional(),
                    Regexp(r'^[\da-zA-Z]{1,16}$', message='Только цифры и буквы латинского алфавита!')]
    )
    submit = SubmitField('Создать')

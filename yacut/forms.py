from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from .CONSTANTS import SHORTLINK_REGEXP, USER_SHORTLINK_MAX_LENGTH


class UrlForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, 4096)]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(
                1,
                USER_SHORTLINK_MAX_LENGTH,
                message=f'Длина не более '
                        f'{USER_SHORTLINK_MAX_LENGTH} символов'),
            Optional(),
            Regexp(
                SHORTLINK_REGEXP,
                message='Только цифры и буквы '
                        'латинского алфавита!')
        ]
    )
    submit = SubmitField('Создать')

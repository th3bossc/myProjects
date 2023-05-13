from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, URLField
from wtforms.validators import DataRequired, Length


class newPostForm(FlaskForm):
    title = StringField(
        label = "Title",
        validators = [DataRequired(), Length(max = 25)]
    )
    content = TextAreaField(
        label = "Content",
        validators = [DataRequired()]
    )

    link = URLField(
        label = 'Link' 
    )

    source = URLField(
        label = "Source code"
    )

    submit = SubmitField(label = 'Submit')




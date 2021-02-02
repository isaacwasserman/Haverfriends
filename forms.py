from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, NumberRange


class CreateProfileForm(FlaskForm):
    profilePic = FileField('Profile Pic', validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    pronouns = StringField('Pronouns', validators=[DataRequired()])
    classYear = IntegerField('Year of Expected Graduation', validators=[DataRequired(), NumberRange(min=2021)])
    funFact = StringField('A Fun Fact About Yourself')
    guideQuestionOne = StringField('What do you want people ask you about?')
    guideQuestionTwo = StringField('What do you want people ask you about?')
    guideQuestionThree = StringField('What do you want people ask you about?')
    bio = StringField('Tell us more about yourself.')
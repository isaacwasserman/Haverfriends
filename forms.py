from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, HiddenField
from wtforms.widgets import Input
from wtforms.fields.html5 import IntegerRangeField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, NumberRange
import firebase.firebaseFunctions as firebase_functions

class CreateProfileForm(FlaskForm):
    profilePic = FileField('Profile Pic', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    profilePicBase64 = HiddenField("profilePicBase64")
    pronouns = StringField('Pronouns', validators=[DataRequired()])
    classYear = IntegerField('Year of Expected Graduation', validators=[DataRequired(), NumberRange(min=2021)])
    funFact = StringField('A Fun Fact About Yourself')
    guideQuestionOne = StringField('Give us three questions that you want people to ask you about')
    guideQuestionTwo = StringField('')
    guideQuestionThree = StringField('')
    bio = StringField('Tell us more about yourself.')
    sportsQuestion = IntegerRangeField('How often do you run/walk around the nature trail? (1 to 5)', render_kw={"min": "1", "max": "5"})
    readingQuestion = IntegerRangeField('How likely are you to say yes if someone challenges you to swim in the duck pond? (1 to 5)', render_kw={"min": "1", "max": "5"})
    cookingQuestion = IntegerRangeField('How much do you enjoy using the stir fry booth in the DC? (1 to 5)', render_kw={"min": "1", "max": "5"})
    DCFoodQuestion = IntegerRangeField('How often do you visit Drinker House on Saturday nights? (1 to 5)', render_kw={"min": "1", "max": "5"})
    MoviesVBoardGamesQuestion = IntegerRangeField('How would you compare your interest in movies to your interest in board games? (1=Movies are way better, 2=Movies are slightly better, 3=They\'re equally interesting, 4=Board games are slightly better, 5=Board games are way better)', render_kw={"min": "1", "max": "5"})
    phoneNotification = StringField('Enter your phone number if you want to receive message notifictaions')
    submit = SubmitField()

class EditProfileForm(FlaskForm):
    profilePic = FileField('Change Profile Pic', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    profilePicBase64 = HiddenField("profilePicBase64")
    pronouns = StringField('Pronouns', validators=[DataRequired()], render_kw={})
    classYear = IntegerField('Year of Expected Graduation', validators=[DataRequired(), NumberRange(min=2021)])
    funFact = StringField('A Fun Fact About Yourself')
    wantMatch = BooleanField('Do you want to be available for matching?')
    guideQuestionOne = StringField('Give us three questions that you want people to ask you about')
    guideQuestionTwo = StringField('')
    guideQuestionThree = StringField('')
    bio = StringField('Tell us more about yourself.')
    sportsQuestion = IntegerRangeField('How often do you run/walk around the nature trail? (1 to 5)', render_kw={"min": "1", "max": "5"})
    readingQuestion = IntegerRangeField('How likely are you to say yes if someone challenges you to swim in the duck pond? (1 to 5)', render_kw={"min": "1", "max": "5"})
    cookingQuestion = IntegerRangeField('How much do you enjoy using the stir fry booth in the DC? (1 to 5)', render_kw={"min": "1", "max": "5"})
    DCFoodQuestion = IntegerRangeField('How often do you visit Drinker House on Saturday nights? (1 to 5)', render_kw={"min": "1", "max": "5"})
    MoviesVBoardGamesQuestion = IntegerRangeField('How would you compare your interest in movies to your interest in board games? (1=Movies are way better, 2=Movies are slightly better, 3=They\'re equally interesting, 4=Board games are slightly better, 5=Board games are way better)', render_kw={"min": "1", "max": "5"})
    phoneNotification = StringField('Enter your phone number (+1XXXXXXXXXX) if you want to receive message notifictaions')
    submit = SubmitField()

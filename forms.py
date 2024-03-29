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
    major = StringField("Major(s) and minor(s)")
    bio = StringField("What's your bio?")
    funFact = StringField('A Fun Fact About Yourself')
    guideQuestionOne = StringField('Give us three questions that you want people to ask you about')
    guideQuestionTwo = StringField('')
    guideQuestionThree = StringField('')
    classQuestionOne = StringField("What are some classes you're taking this semester?")
    classQuestionTwo = StringField('')
    classQuestionThree = StringField('')
    classQuestionFour = StringField('')
    classQuestionFive = StringField('')
    favoriteClass = StringField('Do you have a favorite subject or class?')
    extracurricularQuestion = StringField("Any sports, clubs, organizations you're involved in?")
    # Random questions time
    sportsQuestion = IntegerRangeField('How often do you go on the nature trail? (1 to 5)', render_kw={"min": "1", "max": "5"})
    readingQuestion = IntegerRangeField('How likely are you to say yes if someone challenges you to swim in the duck pond? (1 to 5)', render_kw={"min": "1", "max": "5"})
    lutnickQuestion = IntegerRangeField('Rate Lutnick Library on a scale of 1 to 10:', render_kw={"min": "1", "max": "10"})
    sciLiQuestion = IntegerRangeField('How about the Science Library on a scale of 1 to 10?', render_kw={"min": "1", "max": "10"})
    smallTalk = IntegerRangeField('How much do you like small talk? (1 hate it, 10 love it)', render_kw={"min": "1", "max": "10"})
    freeTime = IntegerRangeField('On a scale of 1-5 (1 being strongly disagree, 5 being strongle agree), I spend a lot of free time exploring random topics that pique my interest.', render_kw={"min": "1", "max": "10"})
    goodImpression = IntegerRangeField('I worry about whether I make a good impression on people I meet.', render_kw={"min": "1", "max": "5"})
    scheduleQuestion = IntegerRangeField('I prefer to follow a schedule', render_kw={"min": "1", "max": "5"})
    peopleQuestion = IntegerRangeField('How many people would you hypothetically like to hang out with at once?', render_kw={"min": "1", "max": "5"})
    moviesQuestion = IntegerRangeField('How much do you like watching movies?', render_kw={"min": "1", "max": "5"})
    introExtro = IntegerRangeField('Introvert or extrovert?', render_kw={"min": "1", "max": "10"})
    boardGamesQuestion = IntegerRangeField('How about board games?', render_kw={"min": "1", "max": "5"})
    weekendQuestion = IntegerRangeField('What kind of weekend energy level do you like (1 being low, 10 being high)', render_kw={"min": "1", "max": "10"})
    brynMawrQuestion = IntegerRangeField('How often do you take the Blue Bus to Bryn Mawr?', render_kw={"min": "1", "max": "5"})
    brunchQuestion = IntegerRangeField('How much do you like DC brunch?', render_kw={"min": "1", "max": "10"})
    headHeart = IntegerRangeField('I follow my head rather than my heart.', render_kw={"min": "1", "max": "5"})
    catDog = IntegerRangeField('Cats versus dogs? (1 for cats and 5 for dogs)', render_kw={"min": "1", "max": "5"})
    phoneNotification = StringField('Enter your phone number if you want to receive message notifictaions')
    submit = SubmitField()

class EditProfileForm(FlaskForm):
    profilePic = FileField('Profile Pic', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    profilePicBase64 = HiddenField("profilePicBase64")
    pronouns = StringField('Pronouns', validators=[DataRequired()])
    wantMatch = BooleanField('Do you want to be available for matching?')
    classYear = IntegerField('Year of Expected Graduation', validators=[DataRequired(), NumberRange(min=2021)])
    major = StringField("Major(s) and minor(s)")
    bio = StringField("What's your bio?")
    funFact = StringField('A Fun Fact About Yourself')
    guideQuestionOne = StringField('Give us three questions that you want people to ask you about')
    guideQuestionTwo = StringField('')
    guideQuestionThree = StringField('')
    classQuestionOne = StringField("What are some classes you're taking this semester?")
    classQuestionTwo = StringField('')
    classQuestionThree = StringField('')
    classQuestionFour = StringField('')
    classQuestionFive = StringField('')
    favoriteClass = StringField('Do you have a favorite subject or class?')
    extracurricularQuestion = StringField("Any sports, clubs, organizations you're involved in?")
    # Random questions time
    sportsQuestion = IntegerRangeField('How often do you go on the nature trail? (1 to 5)', render_kw={"min": "1", "max": "5"})
    readingQuestion = IntegerRangeField('How likely are you to say yes if someone challenges you to swim in the duck pond? (1 to 5)', render_kw={"min": "1", "max": "5"})
    lutnickQuestion = IntegerRangeField('Rate Lutnick Library on a scale of 1 to 10:', render_kw={"min": "1", "max": "10"})
    sciLiQuestion = IntegerRangeField('How about the Science Library on a scale of 1 to 10?', render_kw={"min": "1", "max": "10"})
    smallTalk = IntegerRangeField('How much do you like small talk? (1 hate it, 10 love it)', render_kw={"min": "1", "max": "10"})
    freeTime = IntegerRangeField('On a scale of 1-5 (1 being strongly disagree, 5 being strongle agree), I spend a lot of free time exploring random topics that pique my interest.', render_kw={"min": "1", "max": "10"})
    goodImpression = IntegerRangeField('I worry about whether I make a good impression on people I meet.', render_kw={"min": "1", "max": "5"})
    scheduleQuestion = IntegerRangeField('I prefer to follow a schedule', render_kw={"min": "1", "max": "5"})
    peopleQuestion = IntegerRangeField('How many people would you hypothetically like to hang out with at once?', render_kw={"min": "1", "max": "5"})
    moviesQuestion = IntegerRangeField('How much do you like watching movies?', render_kw={"min": "1", "max": "5"})
    introExtro = IntegerRangeField('Introvert or extrovert?', render_kw={"min": "1", "max": "10"})
    boardGamesQuestion = IntegerRangeField('How about board games?', render_kw={"min": "1", "max": "5"})
    weekendQuestion = IntegerRangeField('What kind of weekend energy level do you like (1 being low, 10 being high)', render_kw={"min": "1", "max": "10"})
    brynMawrQuestion = IntegerRangeField('How often do you take the Blue Bus to Bryn Mawr?', render_kw={"min": "1", "max": "5"})
    brunchQuestion = IntegerRangeField('How much do you like DC brunch?', render_kw={"min": "1", "max": "10"})
    headHeart = IntegerRangeField('I follow my head rather than my heart.', render_kw={"min": "1", "max": "5"})
    catDog = IntegerRangeField('Cats versus dogs? (1 for cats and 5 for dogs)', render_kw={"min": "1", "max": "5"})
    phoneNotification = StringField('Enter your phone number if you want to receive message notifictaions')
    submit = SubmitField()
    
# class CreateProfileForm(FlaskForm):
#     profilePic = FileField('Profile Pic', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
#     profilePicBase64 = HiddenField("profilePicBase64")
#     pronouns = StringField('Pronouns', validators=[DataRequired()])
#     classYear = IntegerField('Year of Expected Graduation', validators=[DataRequired(), NumberRange(min=2021)])
#     funFact = StringField('A Fun Fact About Yourself')
#     guideQuestionOne = StringField('Give us three questions that you want people to ask you about')
#     guideQuestionTwo = StringField('')
#     guideQuestionThree = StringField('')
#     bio = StringField('Tell us more about yourself.')
#     sportsQuestion = IntegerRangeField('How often do you run/walk around the nature trail? (1 to 5)', render_kw={"min": "1", "max": "5"})
#     readingQuestion = IntegerRangeField('How likely are you to say yes if someone challenges you to swim in the duck pond? (1 to 5)', render_kw={"min": "1", "max": "5"})
#     cookingQuestion = IntegerRangeField('How much do you enjoy using the stir fry booth in the DC? (1 to 5)', render_kw={"min": "1", "max": "5"})
#     DCFoodQuestion = IntegerRangeField('How often do you visit Drinker House on Saturday nights? (1 to 5)', render_kw={"min": "1", "max": "5"})
#     MoviesVBoardGamesQuestion = IntegerRangeField('How would you compare your interest in movies to your interest in board games? (1=Movies are way better, 2=Movies are slightly better, 3=They\'re equally interesting, 4=Board games are slightly better, 5=Board games are way better)', render_kw={"min": "1", "max": "5"})
#     phoneNotification = StringField('Enter your phone number if you want to receive message notifictaions')
#     submit = SubmitField()

# class EditProfileForm(FlaskForm):
#     profilePic = FileField('Change Profile Pic', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
#     profilePicBase64 = HiddenField("profilePicBase64")
#     pronouns = StringField('Pronouns', validators=[DataRequired()], render_kw={})
#     classYear = IntegerField('Year of Expected Graduation', validators=[DataRequired(), NumberRange(min=2021)])
#     funFact = StringField('A Fun Fact About Yourself')
#     wantMatch = BooleanField('Do you want to be available for matching?')
#     guideQuestionOne = StringField('Give us three questions that you want people to ask you about')
#     guideQuestionTwo = StringField('')
#     guideQuestionThree = StringField('')
#     bio = StringField('Tell us more about yourself.')
#     sportsQuestion = IntegerRangeField('How often do you run/walk around the nature trail? (1 to 5)', render_kw={"min": "1", "max": "5"})
#     readingQuestion = IntegerRangeField('How likely are you to say yes if someone challenges you to swim in the duck pond? (1 to 5)', render_kw={"min": "1", "max": "5"})
#     cookingQuestion = IntegerRangeField('How much do you enjoy using the stir fry booth in the DC? (1 to 5)', render_kw={"min": "1", "max": "5"})
#     DCFoodQuestion = IntegerRangeField('How often do you visit Drinker House on Saturday nights? (1 to 5)', render_kw={"min": "1", "max": "5"})
#     MoviesVBoardGamesQuestion = IntegerRangeField('How would you compare your interest in movies to your interest in board games? (1=Movies are way better, 2=Movies are slightly better, 3=They\'re equally interesting, 4=Board games are slightly better, 5=Board games are way better)', render_kw={"min": "1", "max": "5"})
#     phoneNotification = StringField('Enter your phone number (+1XXXXXXXXXX) if you want to receive message notifictaions')
#     submit = SubmitField()
import os
from flask import *
from firebase.firebaseInit import auth, exceptions, storage
from firebase.authenticate import authenticate
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app
import firebase.firebaseFunctions as firebase_functions
from datetime import datetime
import forms
from flask_bootstrap import Bootstrap

import datetime
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)

Bootstrap(app)

@app.route("/")  
def home():
    user = authenticate(request.cookies.get('sessionToken'))
    if "redirect" in user:
        return redirect(user["redirect"])

    return render_template('home.html')

@app.route("/chat/<chatID>", methods = ["GET","POST"]) 
def chat(chatID):
    #TESTING: Isaac's account and my account can chat at http://127.0.0.1:5000/chat/di1Lsn3iCla2Qhzk2nByBKmfUeD3_3IjzLCVthGTrlbwkk4woYHfpZB43
    #need a way to kick the user out if their userID is not in the chatID?
    #remember to always iniatialize one message in chatID['messages'] array for the chat to work 
    user = authenticate(request.cookies.get('sessionToken'))
    if request.method == "POST":
        msg=request.json['msg']
        firebase_functions.sendChat(chatID, user['user_id'], msg)
    if "redirect" in user:
        return redirect(user["redirect"])
    chatID=str(chatID)
    other_ID=chatID.replace("_","").replace(user['user_id'],"")
    other_doc=firebase_functions.getUser(other_ID) 
    other_info= [] 
    other_info.append("You are chatting with " + other_doc['name'])
    other_info.append("Their motto is " + "\"" + other_doc['bio'] + "\"")
    other_info.append("Their gender pronoun is " + other_doc['gender_pronouns']) 
    other_info.append("Their grad year is " + str(other_doc['grad_year']))
    other_info.append("One fun fact about them is " + "\"" + other_doc['fun_fact'] + "\"" )
    other_info.append("Questions they want you to ask: ") 
    for question in other_doc['guide_qns']: 
        other_info.append("\"" + question + "\"") 
    messages= firebase_functions.getChatConversation(chatID)['messages']
    messages_array=[] 
    for message in messages: 
        time = message['time_in_string']
        username=message['sender_name']
        complete_msg= time + " " + username + ": " + message['text']
        messages_array.append(complete_msg) 
    return render_template('chat.html', messages_array=messages_array, chatID=chatID, other_info=other_info)

@app.route("/chat", methods = ["GET","POST"]) 
def chat_general():
    user = authenticate(request.cookies.get('sessionToken'))
    if "redirect" in user:
        return redirect(user["redirect"])
    return render_template("chat_general.html")

@app.route("/register", methods = ["GET","POST"]) 
def register(): 
    if request.method == "POST": 
        pass
    pass 

@app.route("/login", methods = ["GET","POST"]) 
def login():
    if request.method == 'POST':
        dataString = request.get_data().decode("utf-8")
        valuePairs = dataString.split("&")
        data = {}
        for pair in valuePairs:
            splitPair = pair.split("=")
            data[splitPair[0]] = splitPair[1]
        id_token = data["idToken"]
        expires_in = datetime.timedelta(days=5)
        try:
            # Create the session cookie. This will also verify the ID token in the process.
            # The session cookie will have the same claims as the ID token.
            session_cookie = auth.create_session_cookie(id_token, expires_in=expires_in)
            # Set cookie policy for session cookie.
            expires = datetime.datetime.now() + expires_in
            response = make_response({"success": True})
            response.set_cookie('sessionToken', session_cookie, expires=expires, httponly=False, secure=False)
        except exceptions.FirebaseError:
            return flask.abort(401, 'Failed to create a session cookie')
    else:
        response = make_response(render_template('login.html'))
    return response

@app.route("/profile/<user_ID>", methods = ["GET","POST"]) 
def profile(user_ID):
    user = authenticate(request.cookies.get('sessionToken'))
    if "redirect" in user:
        return redirect(user["redirect"])
    return render_template("profile.html")

@app.route("/create-profile", methods = ["GET","POST"])
def create_profile():
    user = authenticate(request.cookies.get('sessionToken'))
    if "redirect" in user and user["redirect"] != "/create-profile":
        return redirect(user["redirect"])
    form = forms.CreateProfileForm()
    if form.validate_on_submit():
        uid = user["uid"]
        # Upload Profile Pic
        if form.profilePic.data is not None:
            form.profilePic.data.save("tempStorage/" + form.profilePic.data.filename)
            print(firebase_functions.uploadProfilePic(uid, "tempStorage/" + form.profilePic.data.filename))
        # Edit User Profile
        print(form.data)
        guide_qns = []
        for qn in [form.guideQuestionOne.data,form.guideQuestionTwo.data,form.guideQuestionThree.data]:
            if qn != "":
                guide_qns.append(qn)
        questionnaire_scores = [form.sportsQuestion.data, form.readingQuestion.data, form.cookingQuestion.data, form.DCFoodQuestion.data, form.MoviesVBoardGamesQuestion.data]
        firebase_functions.editUser(uid,{
            "gender_pronouns": form.pronouns.data,
            "grad_year": form.classYear.data,
            "fun_fact": form.funFact.data,
            "guide_qns": guide_qns,
            "bio": form.bio.data,
            "questionnaire_scores": questionnaire_scores
        })
        return "success"
    return render_template("create_profile.html", form=form)

@app.route("/edit-profile/<user_ID>", methods = ["GET","POST"])
def edit_profile(user_ID):
    user = authenticate(request.cookies.get('sessionToken'))
    if "redirect" in user:
        return redirect(user["redirect"])
    return render_template("edit_profile.html") 

if __name__ == '__main__': 
    app.run(debug=True) 



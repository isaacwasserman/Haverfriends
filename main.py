from flask import *
from firebase.firebaseInit import auth
from firebase.firebaseInit import exceptions
from firebase.authenticate import authenticate
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app
import firebase.firebaseFunctions as firebase_functions


import datetime
app = Flask(__name__)

@app.route("/")  
def home():
    user = authenticate(request.cookies.get('session'))
    if "redirect" in user:
        return redirect(user["redirect"])

    return render_template('home.html')

@app.route("/chat/<chatID>", methods = ["GET","POST"]) 
def chat(chatID):
    user = authenticate(request.cookies.get('session'))
    if "redirect" in user:
        return redirect(user["redirect"])
    chatID=str(chatID)
    messages= firebase_functions.getChatConversation(chatID).to_dict()['messages']
    messages_array=[] 
    for message in messages: 
        #two tasks remaining: need to convert Firestore time object to Python string and 
        # get sender's name from sender ID. For now, use senderID in place of sender name 
        sender=message['senderID'] 
        complete_msg= sender + ": " + message['text']
        messages_array.append(complete_msg)
    print(messages_array)
    return render_template('chat.html', messages_array=messages_array, chatID=chatID)

@app.route("/chat", methods = ["GET","POST"]) 
def chat_general():
    user = authenticate(request.cookies.get('session'))
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
            response.set_cookie('session', session_cookie, expires=expires, httponly=True, secure=False)
        except exceptions.FirebaseError:
            return flask.abort(401, 'Failed to create a session cookie')
    else:
        response = make_response(render_template('login.html'))
    return response

@app.route("/profile/<user_ID>", methods = ["GET","POST"]) 
def profile(user_ID):
    user = authenticate(request.cookies.get('session'))
    if "redirect" in user:
        return redirect(user["redirect"])
    return render_template("profile.html")

@app.route("/create-profile", methods = ["GET","POST"])
def create_profile():
    user = authenticate(request.cookies.get('session'))
    if "redirect" in user and user["redirect"] != "/create-profile":
        return redirect(user["redirect"])
    return render_template("create_profile.html")

@app.route("/edit-profile/<user_ID>", methods = ["GET","POST"])
def edit_profile(user_ID):
    user = authenticate(request.cookies.get('session'))
    if "redirect" in user:
        return redirect(user["redirect"])
    return render_template("edit_profile.html") 

if __name__ == '__main__': 
    app.run(debug=True) 



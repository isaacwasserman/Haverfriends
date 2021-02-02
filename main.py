from flask import *
import firebase_admin 
from firebase_admin import credentials, firestore, initialize_app
import firebase.firebaseFunctions as firebase_functions

app = Flask(__name__)       

@app.route("/")  
def home():
    return render_template('home.html')

@app.route("/chat/<chatID>", methods = ["GET","POST"]) 
def chat(chatID):
    if request.method == "POST": 
        print('request is working')
        msg=request.json['msg']
        firebase_functions.sendChat(chatID, "testID", msg)
    chatID=str(chatID)
    messages= firebase_functions.getChatConversation(chatID).to_dict()['messages'] 
    messages_array=[] 
    for message in messages: 
        #two tasks remaining: need to convert Firestore time object to Python string and 
        # get sender's name from sender ID. For now, use senderID in place of sender name 
        sender=message['senderID'] 
        complete_msg= sender + ": " + message['text']
        messages_array.append(complete_msg) 
    return render_template('chat.html', messages_array=messages_array, chatID=chatID)  

@app.route("/chat", methods = ["GET","POST"]) 
def chat_general(): 
    return render_template("chat_general.html")

@app.route("/register", methods = ["GET","POST"]) 
def register(): 
    if request.method == "POST": 
        pass
    pass 

@app.route("/login", methods = ["GET","POST"]) 
def login(): 
    return render_template("login.html")

@app.route("/profile/<user_ID>", methods = ["GET","POST"]) 
def profile(user_ID): 
    return render_template("profile.html")

@app.route("/create-profile/<user_ID>", methods = ["GET","POST"]) 
def create_profile(user_ID): 
    return render_template("create_profile.html")

@app.route("/edit-profile/<user_ID>", methods = ["GET","POST"])
def edit_profile(user_ID): 
    return render_template("edit_profile.html") 

if __name__ == '__main__': 
    app.run(debug=True) 



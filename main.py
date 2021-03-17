import os
from flask import *
from firebase.firebaseInit import auth, exceptions, storage
from firebase.authenticate import authenticate
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app
import firebase.firebaseFunctions as firebase_functions
from matching_algorithm import matching_algo, find_match_for_new_user
from datetime import datetime
import forms
from flask_bootstrap import Bootstrap
from flask_api import status
from flask_mail import Mail, Message
import datetime
import random
from twilio.rest import Client

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)

app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = '',
    MAIL_PASSWORD = '',
))

mail = Mail(app)
Bootstrap(app)

@app.route("/")
def home():
    print(os.listdir())
    user = authenticate(request.cookies.get('sessionToken'))
    if "redirect" in user:
        return redirect(user["redirect"])
    user_id = user["uid"]
    user_object = firebase_functions.getUser(user_id)
    matched_object_list = []
    if user_object.get('matched_count') is not None:
        matched_object_list = [firebase_functions.getUser(list(x.keys())[0]) for x in user_object['matched_count']]
    # Get conversations
    involvedConversations = firebase_functions.getInvolvedConversations(user_id)
    for conversation in involvedConversations:
        otherUserID = conversation["chat_id"].replace(user_id, "").replace("_","")
        otherUser = firebase_functions.getUser(otherUserID)
        conversation["otherUser"] = otherUser

    return render_template('home.html', user=user_object, matched_object_list=matched_object_list, involvedConversations=involvedConversations, showAccountStatus=True)

@app.route("/newchat/<uidOne>/<uidTwo>")
def newchat(uidOne, uidTwo):
    sortedUIDS = sorted([uidOne, uidTwo])
    if firebase_functions.getChatConversation(sortedUIDS[0] + "_" + sortedUIDS[1]) is None:
        conversation = firebase_functions.addChatConversation(uidOne, uidTwo)
        chatID = conversation["chat_id"]
    else:
        chatID = firebase_functions.getChatConversation(sortedUIDS[0] + "_" + sortedUIDS[1])["chat_id"]
    return redirect("/chat/" + chatID)


@app.route("/chat/<chatID>", methods = ["GET","POST"])
def chat(chatID):
    #TESTING: Isaac's account and my account can chat at http://127.0.0.1:5000/chat/di1Lsn3iCla2Qhzk2nByBKmfUeD3_3IjzLCVthGTrlbwkk4woYHfpZB43
    #need a way to kick the user out if their userID is not in the chatID?
    #remember to always iniatialize one message in chatID['messages'] array for the chat to work
    user = authenticate(request.cookies.get('sessionToken'))
    if "redirect" in user:
        return redirect(user["redirect"])
    uid = user['uid']
    print('uid', uid)
    print('_' in chatID and uid in chatID.split('_'), request.method)
    if '_' in chatID and uid in chatID.split('_'):
        if request.method == "POST":
            other_user_id = chatID.split('_')[0] if chatID.split('_')[1] == uid else chatID.split('_')[1]
            other_user = firebase_functions.getUser(other_user_id)
            if other_user['notification_settings'].get('phone') is not None:
                send_message(other_user['notification_settings']['phone'])

            # msg = Message("Hello",
            #       sender="stan1@haverford.edu",
            #       recipients=["samueltan97@hotmail.com"])

            # mail.send(msg)

            # firebase_functions.sendChat(chatID, user['user_id'], msg)

        chatID=str(chatID)
        other_ID=chatID.replace("_","").replace(user['user_id'],"")
        userInfo = firebase_functions.getUser(user['user_id'])
        other_doc=firebase_functions.getUser(other_ID)
        # question= "They do not have any question yet."
        #if other_doc['guide_qns] == []: then do the following things:
        question= "Here is something you can ask to kickstart the conversation: "
        question+= "\"" + random.choice(other_doc['guide_qns']) + "\""
        messages= firebase_functions.getChatConversation(chatID)['messages']
        messages_array=[]
        for message in messages:
            time = message['time_in_string']
            username=message['sender_name']
            complete_msg= time + " " + username + ": " + message['text']
            messages_array.append(complete_msg)
        return render_template('chat.html', messages_array=messages_array, chatID=chatID, uid=user["uid"], user=userInfo, otherUser=other_doc, userName=user["name"], question=question, showAccountStatus=True)
    else:
        content = 'Unauthorized to access this chat conversation'
        #TODO add option to show error-message in template
        return render_template("chat_general.html", error_message=content, showAccountStatus=True)

@app.route("/chat", methods = ["GET","POST"])
def chat_general():
    user = authenticate(request.cookies.get('sessionToken'))
    if "redirect" in user:
        return redirect(user["redirect"])
    return render_template("chat_general.html", showAccountStatus=True)

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
        if request.cookies.get('sessionToken') is None:
            response = make_response(render_template('login.html'))
        else:
            response = make_response(redirect("/"))
    return response

@app.route("/logout", methods = ["GET","POST"])
def logout():
    response = make_response(redirect("/login"))
    response.set_cookie('sessionToken', "", expires=0, httponly=False, secure=False)
    return response

@app.route("/about", methods = ["GET","POST"])
def about():
    user = authenticate(request.cookies.get('sessionToken'))
    if "redirect" in user:
        return redirect(user["redirect"])
    uid = user["uid"]
    user_object= firebase_functions.getUser(uid)
    return render_template("about.html", showAccountStatus=True, user=user_object)

@app.route("/create-profile", methods = ["GET","POST"])
def create_profile():
    user = authenticate(request.cookies.get('sessionToken'))
    existingUserInfo = firebase_functions.getUser(user['uid'])
    if existingUserInfo is not None and existingUserInfo.get('grad_year') is not '': # if user already has a profile, redirect to edit profile. This is important since we are doing free first 3 matches only for new user
        return redirect('/edit-profile')
    if "redirect" in user and user["redirect"] != "/create-profile":
        print(user['redirect'])
        return redirect(user["redirect"])
    form = forms.CreateProfileForm()
    if form.validate_on_submit():
        uid = user["uid"]
        # Upload Profile Pic
        if form.profilePic.data is not None:
            form.profilePic.data.save(os.path.join("tempStorage",form.profilePic.data.filename))
            print(firebase_functions.uploadProfilePic(uid, os.path.join("tempStorage",form.profilePic.data.filename)))
        # Edit User Profile
        print(form.data)
        guide_qns = []
        for qn in [form.guideQuestionOne.data,form.guideQuestionTwo.data,form.guideQuestionThree.data]:
            if qn != "":
                guide_qns.append(qn)
        questionnaire_scores = [form.sportsQuestion.data, form.readingQuestion.data, form.cookingQuestion.data, form.DCFoodQuestion.data, form.MoviesVBoardGamesQuestion.data]
        newInfo = {}
        # Add nonempty values to update
        if form.pronouns.data != "":
            newInfo["gender_pronouns"] = form.pronouns.data
        if form.classYear.data != "":
            newInfo["grad_year"] = form.classYear.data
        if form.funFact.data != "":
            newInfo["fun_fact"] = form.funFact.data
        if form.funFact.data != "":
            newInfo["fun_fact"] = form.funFact.data
        if guide_qns != []:
            newInfo["guide_qns"] = guide_qns
        if form.bio.data != "":
            newInfo["bio"] = form.bio.data
        if form.phoneNotification.data != "":
            newInfo["notification_settings"] = {'phone': form.phoneNotification.data}
        newInfo["questionnaire_scores"] = questionnaire_scores
        firebase_functions.editUser(uid, newInfo)
        all_users = firebase_functions.getAllUsers()
        matched_dict, unmatched_group = find_match_for_new_user(uid, all_users)
        matches_and_unmatched_handler(matched_dict, unmatched_group)
        return redirect("/")
    return render_template("create_profile.html", form=form)

@app.route("/edit-profile", methods = ["GET","POST"])
def edit_profile():
    user = authenticate(request.cookies.get('sessionToken'))
    if "redirect" in user:
        return redirect(user["redirect"])
    uid = user["uid"]
    user_object= firebase_functions.getUser(uid)
    existingUserInfo = firebase_functions.getUser(uid)
    class ExistingUserInfo(object):
        existingUserInfo = firebase_functions.getUser(uid)
        profilePic = ""
        pronouns = existingUserInfo["gender_pronouns"]
        classYear = existingUserInfo["grad_year"]
        funFact = existingUserInfo["fun_fact"]
        wantMatch = existingUserInfo["want_match"]
        guideQuestionOne = existingUserInfo["guide_qns"][0] if len(existingUserInfo["guide_qns"]) > 0 else ""
        guideQuestionTwo = existingUserInfo["guide_qns"][1] if len(existingUserInfo["guide_qns"]) > 1 else ""
        guideQuestionThree = existingUserInfo["guide_qns"][2] if len(existingUserInfo["guide_qns"]) > 2 else ""
        bio = existingUserInfo["bio"]
        sportsQuestion = existingUserInfo["questionnaire_scores"][0]
        readingQuestion = existingUserInfo["questionnaire_scores"][1]
        cookingQuestion = existingUserInfo["questionnaire_scores"][2]
        DCFoodQuestion = existingUserInfo["questionnaire_scores"][3]
        MoviesVBoardGamesQuestion = existingUserInfo["questionnaire_scores"][4]
        phoneNotification = existingUserInfo['notification_settings']['phone'] if existingUserInfo['notification_settings'].get('phone') is not None else ''
    form = forms.EditProfileForm(obj=ExistingUserInfo)
    if form.validate_on_submit():
        if form.profilePic.data is not None and form.profilePic.data != "":
            form.profilePic.data.save(os.path.join("tempStorage",form.profilePic.data.filename))
            print(firebase_functions.uploadProfilePic(uid, os.path.join("tempStorage",form.profilePic.data.filename)))
        # Edit User Profile
        guide_qns = []
        for qn in [form.guideQuestionOne.data,form.guideQuestionTwo.data,form.guideQuestionThree.data]:
            if qn != "":
                guide_qns.append(qn)
        questionnaire_scores = [form.sportsQuestion.data, form.readingQuestion.data, form.cookingQuestion.data, form.DCFoodQuestion.data, form.MoviesVBoardGamesQuestion.data]
        newInfo = {}
        # Add values to update
        newInfo["gender_pronouns"] = form.pronouns.data
        newInfo["grad_year"] = form.classYear.data
        newInfo["want_match"] = form.wantMatch.data
        newInfo["fun_fact"] = form.funFact.data
        newInfo["fun_fact"] = form.funFact.data
        newInfo["guide_qns"] = guide_qns
        newInfo["bio"] = form.bio.data
        newInfo["questionnaire_scores"] = questionnaire_scores
        if form.phoneNotification.data != "":
            newInfo["notification_settings"] = {'phone': form.phoneNotification.data}
        else:
            newInfo["notification_settings"] = {}
        firebase_functions.editUser(uid, newInfo)
        return redirect("/")
    return render_template("edit_profile.html", form=form, userInfo=existingUserInfo, showAccountStatus=True, user=user_object)

@app.route("/match", methods=["GET"])
def match_users():
    user_id = authenticate(request.cookies.get('sessionToken'))['user_id']
    if user_id == "di1Lsn3iCla2Qhzk2nByBKmfUeD3":

        all_users = firebase_functions.getAllUsers()

        # Remove chats that were never used in the previous match and clear matches that were made in the
        # previous match cycle from matched_count

        for user_id, user_details in all_users.items():
            if user_details.get('matched_count') is None or user_details['matched_count'] == []:
                continue
            else:
                matches = user_details['matched_count']
                for match in matches:
                    partner_id = list(match.keys())[0]
                    chat_id = list(match.values())[0]
                    chat = firebase_functions.getChatConversation(chat_id)
                    if chat is not None:
                        if len(chat['messages']) > 1:
                            if user_details.get('active_chat_partners') is None:
                                firebase_functions.editUser(user_id,{
                                    "active_chat_partners": [partner_id]
                                })
                            else:
                                new_chat_partners = user_details['active_chat_partners'].copy()
                                new_chat_partners.append(partner_id)
                                firebase_functions.editUser(user_id,{
                                    "active_chat_partners": new_chat_partners
                                })
                        else:
                            firebase_functions.deleteChatConversation(chat_id)
                firebase_functions.editUser(user_id,{
                    "matched_count": []
                })

        # Matching algorithm

        matched_dict, unmatched_group = matching_algo(all_users)
        # Add new match to the different users
        matches_and_unmatched_handler(matched_dict, unmatched_group)

        content = {'matching done': 'chats that were never initiated are removed'}
        return content, status.HTTP_200_OK
    else:
        content = {'please move along': 'nothing to see here'}
        return content, status.HTTP_404_NOT_FOUND

def matches_and_unmatched_handler(matched_dict, unmatched_group):
    for key, value in matched_dict.items():
            if key != "unmatched":
                key_user = firebase_functions.getUser(key)
                if key_user.get('matched_count') is None:
                    matched_count_info = []
                    for single_match in value:
                        matched_count_info.append({single_match[0]: single_match[1]}) # key: matched user_id and value: chat_id
                    firebase_functions.editUser(key_user['uid'],{
                        "matched_count": matched_count_info
                    })
                else:
                    new_matched_count = key_user['matched_count'].copy()
                    for single_match in value:
                        new_matched_count.append({single_match[0]: single_match[1]}) # key: matched user_id and value: chat_id
                    firebase_functions.editUser(key_user['uid'],{
                        "matched_count": new_matched_count
                    })
                for indiv in value:
                    value_user = firebase_functions.getUser(indiv[0])
                    if value_user.get('matched_count') is None:
                        firebase_functions.editUser(value_user['uid'],{
                            "matched_count": [{key: indiv[1]}]
                        })
                    else:
                        new_matched_count = value_user['matched_count'].copy()
                        new_matched_count.append({key: indiv[1]})
                        firebase_functions.editUser(value_user['uid'],{
                            "matched_count": new_matched_count
                        })

    # Add empty list to the users with no matches
    for unmatched_user in unmatched_group:
        firebase_functions.editUser(unmatched_user[0],{
                "matched_count": []
        })

def send_message(to_number, from_number='+17865634468', message='You have a new message on HaverFriends'):

    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    message = client.messages.create(
                                body=message,
                                from_=from_number,
                                to=to_number
                            )
    print(message.sid)

@app.route("/user_session", methods=["GET"])
def user_session(): 
    if authenticate(request.cookies.get('sessionToken')):
        if 'redirect' in authenticate(request.cookies.get('sessionToken')):  
            return "create-profile" 
        else: 
            return "homepage"
    else: 
        return "no" 

if __name__ == '__main__':
    if 'PORT' in os.environ:
        # get the heroku port
        port = int(os.environ.get('PORT', 5000))
    else:
        port = 5000
    app.run(host='0.0.0.0', port=port, debug=True)

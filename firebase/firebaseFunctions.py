from .firebaseInit import firebase
from firebase_admin import firestore
import time 
from datetime import datetime
db = firestore.client()


def addUser(user):
    users = db.collection('users')
    users.document(user["uid"]).set({
        'uid': user["uid"],
        'name': user["name"],
        'email': user["email"],
        'photo': "https://upload.wikimedia.org/wikipedia/commons/7/7c/Profile_avatar_placeholder_large.png",
        'gender_pronouns': "",
        'grad_year': "",
        'fun_fact': "",
        'guide_qns': [],
        'bio': "",
        'want_platonic': True,
        'questionnaire_scores': [],
        'notification_settings': {},
        'active_chat_partners': [],
        'match_count': 0
    })
    return users.document(user["uid"]).get().to_dict()

def editUser(uid, newInfo):
    user = db.collection('users').document(uid)
    user.update(newInfo)
    return user.get().to_dict()

def getUser(uid):
    user = db.collection('users').document(uid)
    return user.get().to_dict()

def addChatConversation(userOneID, userTwoID):
    chats = db.collection('chats')
    sortedUIDS = sorted([userOneID, userTwoID])
    chat_id = sortedUIDS[0] + "_" + sortedUIDS[1]
    chats.document(chat_id).set({
        "chat_id": chat_id,
        "messages": [],
        "matched_time": time.time()
    })

    editUser(userOneID, {'active_chat_partners': firestore.ArrayUnion([userTwoID])})
    editUser(userTwoID, {'active_chat_partners': firestore.ArrayUnion([userOneID])})
    return chats.document(chat_id).get().to_dict()

def getChatConversation(chat_id):
    conversation = db.collection('chats').document(chat_id)
    return conversation.get().to_dict()

def sendChat(chat_id, senderID, message):
    conversation = db.collection('chats').document(chat_id)
    conversation.update({
        'messages': firestore.ArrayUnion([{
            'senderID':senderID,
            'sender_name': getUser(senderID)['name'],
            'time': time.time(),
            'text': message, 
            'time_in_string': datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %I:%M")
        }])
    })
    return {'senderID':senderID, 'time': time.time(), 'text': message}
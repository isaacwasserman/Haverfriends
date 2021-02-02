import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import time

cred = credentials.Certificate("private-key.json")
firebase = firebase_admin.initialize_app(cred)

db = firestore.client()



def addUser(user):
    users = db.collection('users')
    users.document(uid).set({
        'uid': user.uid,
        'name': user.displayName,
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
    return user.get()

def editUser(uid, newInfo):
    user = db.collection('users').document(uid)
    user.update(newInfo)
    return user.get()

def getUser(uid):
    user = db.collection('users').document(uid)
    return user.get()

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
    return chats.document(chat_id).get()

def getChatConversation(chat_id):
    conversation = db.collection('chats').document(chat_id)
    return conversation.get()

def sendChat(chat_id, senderID, message):
    conversation = db.collection('chats').document(chat_id)
    conversation.update({
        'messages': firestore.ArrayUnion([{
            'senderID':senderID,
            'time': time.time(),
            'text': message
        }])
    })
    return {'senderID':senderID, 'time': time.time(), 'text': message}
from .firebaseInit import firebase, firestore, storage
import time
import os
import datetime
db = firestore.client()
bucket = storage.bucket()


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
        'want_match': True,
        'want_platonic': True,
        'questionnaire_scores': [],
        'notification_settings': {},
        'active_chat_partners': [],
        'matched_count': []
    })
    return users.document(user["uid"]).get().to_dict()

def editUser(uid, newInfo):
    user = db.collection('users').document(uid)
    user.update(newInfo)
    return user.get().to_dict()

def getUser(uid):
    print(uid)
    user = db.collection('users').document(uid)
    return user.get().to_dict()

def getAllUsers():
    users = db.collection('users').stream()
    users_dict = dict()
    for user in users:
        users_dict[user.id] = user.to_dict()
    return users_dict

def uploadProfilePic(uid, tempPath):
    extension = tempPath.split(".")[-1]
    blob = bucket.blob('profilePics/' + uid + '.' + extension)
    blob.upload_from_filename(tempPath)
    if os.path.exists(tempPath):
        os.remove(tempPath)
    editUser(uid, {"photo": blob.public_url})
    return blob.public_url

def addChatConversation(userOneID, userTwoID):
    chats = db.collection('chats')
    sortedUIDS = sorted([userOneID, userTwoID])
    chat_id = sortedUIDS[0] + "_" + sortedUIDS[1]
    chats.document(chat_id).set({
        "chat_id": chat_id,
        "messages": [{"senderID": "None", "sender_name": "Bot", "text": "You've been matched", "time": 0, "time_in_string": "Just Now"}],
        "matched_time": time.time()
    })

    editUser(userOneID, {'active_chat_partners': firestore.ArrayUnion([userTwoID])})
    editUser(userTwoID, {'active_chat_partners': firestore.ArrayUnion([userOneID])})
    return chats.document(chat_id).get().to_dict()

def getChatConversation(chat_id):
    conversation = db.collection('chats').document(chat_id)
    return conversation.get().to_dict()

def deleteChatConversation(chat_id):
    db.collection('chats').document(chat_id).delete()

def getInvolvedConversations(uid):
    conversations = db.collection('chats').get()
    involved = []
    for conversation in conversations:
        conversationDict = conversation.to_dict()
        if "chat_id" in conversationDict:
            if uid in conversationDict["chat_id"]:
                involved.append(conversationDict)
    return involved

def sendChat(chat_id, senderID, message):
    conversation = db.collection('chats').document(chat_id)
    conversation.update({
        'messages': firestore.ArrayUnion([{
            'senderID':senderID,
            'sender_name': getUser(senderID)['name'],
            'time': time.time(),
            'text': message,
            'time_in_string': datetime.datetime.fromtimestamp(time.time()).strftime("%Y/%m/%d %H:%M")
        }])
    })
    return {'senderID':senderID, 'time': time.time(), 'text': message}
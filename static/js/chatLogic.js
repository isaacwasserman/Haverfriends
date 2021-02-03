var firebaseConfig = {
    apiKey: "AIzaSyCe_db6Qj1jHISdWZigvlBAXzLZNzfzFKs",
    authDomain: "haverfriends-9b932.firebaseapp.com",
    projectId: "haverfriends-9b932",
    storageBucket: "haverfriends-9b932.appspot.com",
    messagingSenderId: "68391205434",
    appId: "1:68391205434:web:48456413b5f62da16b9303",
    measurementId: "G-Z8WYEKVQRH"
  };
// Initialize Firebase
firebase.initializeApp(firebaseConfig)
let db = firebase.firestore();

$(document).ready(function() {
    var frontendSend = function(chatID, text){
        let date = new Date()
        let time = (new Date()).getTime() / 1000
        let time_in_string = date.getFullYear() + "/" + ("0" + (date.getMonth()+1)).slice(-2) + "/" + ("0" + date.getDate()).slice(-2) + " " + ("0" + date.getHours()).slice(-2) + ":" + ("0" + date.getMinutes()).slice(-2);
        let message = {
            senderID: "{{ uid }}",
            sender_name: "{{ userName }}",
            text: text,
            time: time,
            time_in_string: time_in_string
        }
        console.log(message)
        let conversation = db.collection("chats").doc(chatID)
        conversation.update({
           messages: firebase.firestore.FieldValue.arrayUnion(message)
        }).then(function(){
          console.log("success")
        })
    }
    const chatID = "{{ chatID }}"
    console.log(chatID)
    $(document).on('click', '#btn-chat', function(e){
      let text = document.querySelector("#btn-input").value
      document.querySelector("#btn-input").value = ""
      let chatID = document.querySelector("#chatID").innerHTML
      frontendSend(chatID, text)
    })
    $('#send').on('click', function() {
        var message = $('#message-input').val()
        $('#message-input').val('');
        frontendSend(chatID, message)
        // $.ajax({
        //         type : "POST",
        //         url : window.location.origin + "/chat/" + chatID,
        //         data: JSON.stringify({"msg": message}),
        //         dataType:"json",
        //         contentType: 'application/json;charset=UTF-8',
        //         success: function() {
        //             console.log("Success")
        //         }
        //     });
});
var initState = true;

db.collection("chats").doc(chatID).onSnapshot(function(doc) {
    if (initState) {
        initState=false
    }
    else {
    msg_doc= doc.data()['messages'][doc.data()['messages'].length-1];
    complete_message=msg_doc['time_in_string'] + " " + msg_doc['sender_name'] + ": " + msg_doc['text']
    $("#message-display").append(complete_message)
    $("#message-display").append('<br>')
    }
});
});

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
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
firebase.initializeApp(firebaseConfig);

initApp = function() {
    firebase.auth().onAuthStateChanged(function(user) {
      if (user) {
        // User is signed in.
        var displayName = user.displayName;
        var email = user.email;
        var emailVerified = user.emailVerified;
        var photoURL = user.photoURL;
        var uid = user.uid;
        var phoneNumber = user.phoneNumber;
        var providerData = user.providerData;
        user.getIdToken().then(function(accessToken) {
//          document.getElementById('sign-in-status').textContent = 'Signed in';
//          document.getElementById('sign-in').textContent = 'Sign out';
//          document.getElementById('account-details').textContent = JSON.stringify({
            displayName: displayName,
            email: email,
            emailVerified: emailVerified,
            phoneNumber: phoneNumber,
            photoURL: photoURL,
            uid: uid,
            accessToken: accessToken,
            providerData: providerData
          }, null, '  ');
        });
      } else {
        // User is signed out.
//        document.getElementById('sign-in-status').textContent = 'Signed out';
//        document.getElementById('sign-in').textContent = 'Sign in';
//        document.getElementById('account-details').textContent = 'null';
      }
    }, function(error) {
      console.log(error);
    });
  };

  window.addEventListener('load', function() {
    initApp()
  });
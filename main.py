from flask import *   
app = Flask(__name__)       

@app.route("/")  
def home():
    return render_template('home.html')

@app.route("/chat/<chatID>", methods = ["GET","POST"]) #later need to add specific chatID to endpoint
def chat(): 
    return render_template('chat.html')  

@app.route("/chat", methods = ["GET","POST"]) 
def chat_general(): 
    return render_template("chat_general.html")

@app.route("/register", methods = ["GET","POST"]) 
def register(): 
    return render_template("register.html")

@app.route("/login", methods = ["GET","POST"]) 
def login(): 
    return render_template("login.html")

@app.route("/profile/<user_ID>", methods = ["GET","POST"]) 
def profile(): 
    return render_template("profile.html")

@app.route("/create-profile/<user_ID>", methods = ["GET","POST"]) 
def create_profile(): 
    return render_template("create_profile.html")

@app.route("/edit-profile/<user_ID>", methods = ["GET","POST"])
def edit_profile(): 
    return render_template("edit_profile.html") 

if __name__ == '__main__': 
    app.run(debug=True) 



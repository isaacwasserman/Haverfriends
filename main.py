from flask import *   
app = Flask(__name__)       

@app.route("/")  
def home():
    return render_template('home.html')

@app.route("/chat") #later need to add specific chatID to endpoint
def chat(): 
    return render_template('chat.html')  

@app.route("/chat_general") 
def chat_general(): 
    return render_template("chat_general.html")

@app.route("/register") 
def register(): 
    return render_template("register.html")

@app.route("/login") 
def login(): 
    return render_template("login.html")

@app.route("/profile") 
def profile(): 
    return render_template("profile.html")

@app.route("/create-profile") 
def create_profile(): 
    return render_template("create_profile.html")

@app.route("/edit-profile")
def edit_profile(): 
    return render_template("edit_profile.html") 

if __name__ == '__main__': 
    app.run(debug=True) 



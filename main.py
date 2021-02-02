from flask import *   
app = Flask(__name__)       

@app.route("/")  
def home():
    return render_template('home.html')

@app.route("/chat") #later need to add specific chatID to endpoint
def chat(): 
    return render_template('chat.html')  

if __name__ == '__main__': 
    app.run(debug=True)
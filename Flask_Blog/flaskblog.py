from flask import Flask, render_template, url_for     #import Flask class and render_template function from Flask
from posts import Posts
app = Flask(__name__)       #create variable app and setting an instance to it

Posts = Posts()
"""
posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]
"""

@app.route("/")             #route decorators (learn at some point) "/" is root/homepage
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():                #change function name
    return render_template('about.html', title='About')

@app.route("/about")
def about():                #change function name
    return render_template('posts.html', title='Posts')


if __name__ == '__main__':  #will only be true if we run the script directly in Python
    app.run(debug=True)
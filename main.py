from flask import Flask, render_template
import requests

r = requests.get("https://api.npoint.io/f740b1f28c9d9fe719fe")
posts = r.json()

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", posts=posts)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/post/<int:index>")
def get_blog(index):
    blog_post = None
    for post in posts:
        if post["id"] == index:
            blog_post = post
    return render_template("post.html", post=blog_post)

if __name__ == "__main__":
    app.run(debug=True)

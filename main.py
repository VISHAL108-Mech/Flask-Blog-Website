from flask import Flask, render_template, request
import requests
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

MY_GMAIL = os.getenv("SMTP_GMAIL_ID")
MY_PASSWORD = os.getenv("SMTP_GMAIL_PASSWORD")

r = requests.get("https://api.npoint.io/f740b1f28c9d9fe719fe")
posts = r.json()

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html", posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        data = request.form
        my_msg = (f"Subject:New Message\n\n"
                  f"Name: {data['name']}\n"
                  f"Email: {data['email']}\n"
                  f"Phone: {data['phone']}\n"
                  f"Message: {data['message']}")

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_GMAIL, password=MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_GMAIL,
                to_addrs=MY_GMAIL,
                msg=my_msg.encode("utf-8"),
            )

        return render_template("contact.html", post=True)
    return render_template("contact.html", post=False)


@app.route("/post/<int:index>")
def get_blog(index):
    blog_post = None
    for post in posts:
        if post["id"] == index:
            blog_post = post
    return render_template("post.html", post=blog_post)


if __name__ == "__main__":
    app.run(debug=True)

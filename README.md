# Flask Blog

A simple blog website built with Flask. The blog posts are loaded from an online JSON API, listed on the home page, and each post opens on its own page. The site also has an About page and a working Contact page: when someone fills in the form, the message is emailed to me.

I built it to practice Flask routing, Jinja templates, handling form submissions and working with data from an API. The design is the free Clean Blog theme from Start Bootstrap, which I turned into reusable Flask templates.

<img width="600" height="300" alt="Screenshot 2026-10-27 195124" src="https://github.com/user-attachments/assets/efd1add5-3a88-48d6-88ed-442655e3bce6" />
<img width="300" height="200" alt="Screenshot 2026-10-30 214931" src="https://github.com/user-attachments/assets/720c4a51-f044-44f0-b487-5fd7242ba56e" />


## Pages

| Route | Page |
|---|---|
| `/` | Home page with a list of all blog posts |
| `/post/<id>` | A single blog post |
| `/about` | About page |
| `/contact` | Contact page. A GET request shows the form, and a POST request sends the message by email |

## Built with

- Python 3
- Flask and Jinja2 templates
- `requests` for fetching the posts
- `smtplib` for sending the contact form messages by email
- `python-dotenv` for keeping the email login out of the code
- HTML, CSS and Bootstrap (Start Bootstrap's Clean Blog theme)

## Project structure

```
Flask Blog/
├── main.py              # Flask app and routes
├── .env                 # Gmail login details (not committed)
├── templates/
│   ├── header.html      # navbar and <head>, shared by every page
│   ├── footer.html      # footer and scripts, shared by every page
│   ├── index.html       # home page with the post list
│   ├── post.html        # single post page
│   ├── about.html
│   └── contact.html
├── static/
│   ├── css/
│   ├── js/
│   └── assets/          # images and favicon
└── README.md
```

## Setup

Install the packages:

```bash
pip install flask requests python-dotenv
```

Create a `.env` file in the project folder with the Gmail account that should receive the contact messages:

```
SMTP_GMAIL_ID=your_email@gmail.com
SMTP_GMAIL_PASSWORD=your_app_password
```

Use a Gmail app password, not your normal password, and add `.env` to your `.gitignore` so it never gets pushed.

Run the app:

```bash
python main.py
```

Then open `http://127.0.0.1:5000` in your browser. You need an internet connection, because the posts are downloaded when the app starts and the contact form sends email through Gmail.

## How it works

**Getting the posts.** When the app starts, it downloads the list of posts from a JSON API and keeps it in a variable.

```python
r = requests.get("https://api.npoint.io/f740b1f28c9d9fe719fe")
posts = r.json()
```

**Routes.** The home and about pages each render a template. The home page also passes in the list of posts.

```python
@app.route("/")
def home():
    return render_template("index.html", posts=posts)

@app.route("/about")
def about():
    return render_template("about.html")
```

**Single post page.** The post route takes the post's id from the URL, finds the matching post in the list and passes it to the template.

```python
@app.route("/post/<int:index>")
def get_blog(index):
    blog_post = None
    for post in posts:
        if post["id"] == index:
            blog_post = post
    return render_template("post.html", post=blog_post)
```

**Contact form.** The contact route accepts both GET and POST. A GET request just shows the form. When the form is submitted, the route reads the fields, builds an email and sends it to me through Gmail, then shows the page again with a success heading. The login details come from the `.env` file.

```python
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
```

On the template side, the form posts back to the same route, and each input has a `name` that matches what the route reads. The heading changes after a successful send:

```html
<form action="{{ url_for('contact') }}" method="post" id="contactForm" name="sentMessage">
    <input class="form-control" id="name" name="name" type="text" required />
    ...
</form>

{% if post: %}
<h1>Successfully sent your message</h1>
{% else: %}
<h1>Contact Me</h1>
{% endif %}
```

**Templates.** The navbar and footer live in `header.html` and `footer.html`, and every page includes them, so I only write them once.

```html
{% include "header.html" %}
...
{% include "footer.html" %}
```

The home page loops over the posts with Jinja and builds a link to each one with `url_for`:

```html
{% for post in posts %}
<div class="post-preview">
    <a href="{{ url_for('get_blog', index=post.id) }}">
        <h2 class="post-title">{{post.title}}</h2>
        <h3 class="post-subtitle">{{post.subtitle}}</h3>
    </a>
    <p class="post-meta">
        Posted by <a href="#!">{{post.author}}</a> on {{post.date}}
    </p>
</div>
{% endfor %}
```

## What I learned

- Creating routes in Flask, including routes that take a value from the URL
- Splitting a site into reusable templates with `include`
- Looping over data in Jinja and linking pages with `url_for`
- Fetching JSON from an API and using it to build pages
- Handling a form submission with a POST route and sending the data by email
- Keeping login details in a `.env` file

## Things to improve

This is a learning project, so there are rough edges.

- The About page still has placeholder text, and the footer still has the template's default links and copyright
- The navbar brand link points to `index.html`, which doesn't exist as a route, so it should use `url_for('home')`
- The contact route has no error handling, so if the email fails to send, the visitor sees an error page instead of a message
- Messages are only validated by the browser's `required` attributes, so the server should check the fields too
- If a post id doesn't exist, the post page renders empty. It should return a 404 instead
- The posts are only fetched once when the app starts, so the app needs a restart to see new posts, and it won't start if the API is down
- Add a way to write new posts instead of relying on an external API

## Credits

Theme: [Clean Blog](https://startbootstrap.com/theme/clean-blog) by Start Bootstrap.

## Author

**VISHAL YADAV**
- GitHub: [@VISHAL108-Mech](https://github.com/VISHAL108-Mech)
- LinkedIn: [vishal-yadav-2a91a7428](https://www.linkedin.com/in/vishal-yadav-2a91a7428)
- Email: [vy4122000@gmail.com](mailto:vy4122000@gmail.com)

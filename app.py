from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello():
    name = "김철수"
    posts = ["첫번째 글", "두번째 글", "세번째 글"]
    return render_template("index.html", name=name, posts=posts)

@app.route("/about")
def about():
    return "소개 페이지"

@app.route("/user/<username>")
def user(username):
    return render_template("index.html", name=username, posts=[])

app.run()
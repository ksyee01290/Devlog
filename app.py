from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "123123"

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

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        flash(f"{username}님 로그인 성공")
        return redirect(url_for("hello"))
    return render_template("login.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

app.run(debug=True)
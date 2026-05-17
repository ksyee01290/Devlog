from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///devlog.db"
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(50))
    
app.secret_key = "123123"

@app.route("/")
def hello():
    posts = Post.query.all()
    return render_template("index.html", posts=posts)

@app.route("/test")
def test():
    new_post = Post(title='첫번째 글', content='내용입니다', date='2026-05-18')
    db.session.add(new_post)
    db.session.commit()
    return "데이터 추가 완료!"
# 글쓰기
@app.route("/write", methods=["GET", "POST"])
def write():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        date = datetime.now().strftime("%Y-%m-%d | %H:%M:%S")
        new_post = Post(title=title, content=content, date=date)
        db.session.add(new_post)
        db.session.commit()
        flash("글이 작성되었습니다.")
        return redirect(url_for("posts"))
    return render_template("write.html")

# 조회
@app.route("/posts")
def posts():
    posts = Post.query.all()
    return render_template("index.html", posts=posts)

# 수정
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    post = Post.query.get(id)
    if request.method == "POST":
        post.title = request.form["title"]
        post.content = request.form["content"]
        db.session.commit()
        flash("글이 수정되었습니다!")
        return redirect(url_for("hello"))
    return render_template("edit.html", post=post)

# 삭제
@app.route("/delete/<int:id>")
def delete(id):
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    flash("글이 삭제되었습니다!")
    return redirect(url_for("hello"))

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
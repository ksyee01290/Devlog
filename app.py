from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
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
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    
app.secret_key = "123123"

@app.route("/")
def hello():
    posts = Post.query.all()
    return render_template("index.html", posts=posts)

# 글쓰기
@app.route("/write", methods=["GET", "POST"])
def write():
    if "username" not in session:
        flash("로그인이 필요합니다!")
        return redirect(url_for("login"))
    
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
    if "username" not in session:
        flash("로그인이 필요합니다.")
        return redirect(url_for("login"))
    
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
    if "username" not in session:
        flash("로그인이 필요합니다.")
        return redirect(url_for("login"))
    
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    flash("글이 삭제되었습니다!")
    return redirect(url_for("hello"))

# user정보
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password2 = request.form["password2"]
        
        if password != password2:
            flash("비밀번호가 일치하지 않습니다!")
            return redirect(url_for("register"))
        
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("회원가입 완료!")
        return redirect(url_for("login"))
    return render_template("register.html")

# 로그인
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session["username"] = username
            flash(f"{username}님 로그인 성공!")
            return redirect(url_for("hello"))
        else:
            flash("아이디 또는 비밀번호가 틀렸습니다!")
            return redirect(url_for("login"))
    return render_template("login.html")

# 로그아웃
@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("로그아웃 되었습니다!")
    return redirect(url_for("hello"))

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True)
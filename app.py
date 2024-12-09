from time import sleep
from flask import Flask, request, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from os import mkdir
from os.path import exists
from sqlite3 import connect

if not exists("instance"):
    mkdir("instance")

with connect("instance/comment.db") as db:
    cour = db.cursor()
    cour.execute("""CREATE TABLE IF NOT EXISTS article(
                    id INTEGER NOT NULL,
                    title VARCHAR(100),
                    text TEXT,
                    PRIMARY KEY (id))""")
    db.commit()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comment.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
    #Создание колонок
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=True)
    text = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route("/")
def start_screen():
    return render_template("start.html")


@app.route('/state')
def index():
    articles = Article.query.all()
    print(articles)
    return render_template("home.html", articles=articles)


@app.route("/create_comment", methods=["POST", "GET"])
def create_comment():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']

        article = Article(title=title, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/state')
        except:
            return "При додаванні коментаря виникла проблема"
    else:
        return render_template("create_comment.html")


@app.route("/state/<int:id>/update", methods=['POST', 'GET'])
def update_comment(id):
    article = Article.query.get(id)
    if request.method == "POST":
        article.title = request.form['title']
        article.text = request.form['text']

        try:
            db.session.commit()
            return redirect("/state")
        except:
            return "При оновлені коментаря виникла проблема"
    else:
        return render_template("update_comment.html", article=article)


@app.route("/state/<int:id>/delete", methods=['POST', 'GET'])
def delete_comment(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect("/state")
    except:
        return "При видалені коментаря виникла проблема"


if __name__=="__main__":
    print("Зараз запуститься локальний сервер, щоб все правильно відображалось\n"
          "Зайдіть на локальний адрес. Він відображаєть біля поля 'Running on http...'")
    sleep(2)
    app.run(debug=True)
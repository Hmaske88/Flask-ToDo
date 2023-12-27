from flask import Flask,render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

with open('templates/config.json', 'r') as c:
    params = json.load(c)["params"]

local_server=True
app = Flask(__name__)

if(local_server):
    app.config["SQLALCHEMY_DATABASE_URI"] = params["local_uri"]
db=SQLAlchemy(app)



class Tasks(db.Model):
    # sno	title	detail	date
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(25), nullable=False)
    detail = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(12))

@app.route('/',methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        title = request.form['title']
        detail = request.form['desc']
        entry = Tasks(title=title, detail=detail, date=datetime.now())
        db.session.add(entry)
        db.session.commit()
    tasks=Tasks.query.filter_by().all()
    return render_template("index.html", tasks=tasks)


@app.route('/login',methods = ['POST', 'GET'])
def login():
    if(request.method=='POST'):
        email=request.form['email']
        password=request.form['pass']
    return render_template("login.html")


@app.route('/edit/<string:sno>',methods = ['POST', 'GET'])
def edit(sno):
    if request.method == 'POST':
        title = request.form['title']
        detail = request.form['desc']

        task=Tasks.query.filter_by(sno=sno).first()
        task.title=title
        task.detail=detail
        task.date=datetime.now()
        db.session.commit()
        return redirect("/edit/"+sno)
    task = Tasks.query.filter_by(sno=sno).first()
    return render_template("edit.html", task=task)


@app.route('/delete/<string:sno>',methods = ['POST', 'GET'])
def delete(sno):
    task=Tasks.query.filter_by(sno=sno).first()
    db.session.delete(task)
    db.session.commit()
    return redirect("/")


app.run(debug=True)
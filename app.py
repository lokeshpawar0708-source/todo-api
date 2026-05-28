from flask import Flask,render_template,request,redirect,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app=Flask(__name__)
app.secret_key="6080"
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class Todo(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(200), nullable=False)
    desc=db.Column(db.String(500), nullable=False)
    completed=db.Column(db.Boolean, default=False)
    date_created=db.Column(db.DateTime, default=datetime.utcnow)
   
    
    def __repr__(self) ->str:
        return f"{self.sno} - {self.title}" 
    
    
@app.route('/', methods=["GET","POST"])
def add():
    if request.method=="POST":
        title=request.form['title']
        desc=request.form['desc']

        if not title or not desc:
           flash("Title and Description both are required")
           return  redirect('/')
    
        todo=Todo(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit() 
        return redirect('/')
    allTodo=Todo.query.all()
    return render_template("index.html",allTodo=allTodo)


@app.route('/show')
def products():
    allTodo=Todo.query.all()
    print(allTodo)
    return 'this is product page'

# @app.route('/about',methods=["GET","POST"])
# def about():
#     if request.method=="POST":
#       allTodo=Todo.query.all()
#       print(allTodo)
#     return render_template("base.html")

@app.route('/update/<int:sno>',methods=["GET","POST"])
def update(sno):
    if request.method=="POST":
        title=request.form['title']
        desc=request.form['desc']
        todo=Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")

    todo=Todo.query.filter_by(sno=sno).first()
    return render_template("update.html",todo=todo)

@app.route('/done/<int:sno>')
def mark_done(sno):
    task= db.session.get(Todo,sno)
    task.completed=True
    db.session.commit()
    return redirect("/")
      
@app.route('/delete/<int:sno>')
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route('/search' ,methods=["GET"])
def search():
    query=request.args.get('query')
    if query:
        results=Todo.query.filter(Todo.title.contains(query) | Todo.desc.contains(query)).all()
    else:
        results=Todo.query.all()
    return render_template("index.html",allTodo=results)

if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True,port=8000)
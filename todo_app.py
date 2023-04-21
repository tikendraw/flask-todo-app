from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo_db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_title = db.Column(db.String, nullable=False)
    status = db.Column(db.Boolean)

    def __init__(self, task_title, status=False):
        self.task_title = task_title
        self.status = status

    def __repr__(self):
        return f"{self.task_title} : {self.status}"

@app.route('/')
@app.route('/home')
def home():
    all_tasks = Task.query.all()
    return render_template('base.html', all_tasks = all_tasks)

@app.route('/add', methods = ['POST'])
def add():
    task_title = request.form['tasktitle']
    print(task_title)
    new_task = Task(task_title=task_title, status = False)
    
    with app.app_context():
        db.session.add(new_task)
        db.session.commit()
    
    return redirect(url_for('home'))


@app.route('/update/<int:todo_id>')
def update(todo_id):
    
    task = Task.query.filter_by(id = todo_id).first()
    task.status = not task.status
    # with app.app_context():
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    
    task = Task.query.filter_by(id = todo_id).first()
    db.session.delete(task)
    db.session.commit()  

    return redirect(url_for('home'))

if __name__=='__main__':
    # with app.app_context():
    #     db.create_all()
    
    # t1 = Task('Eat', status = False)
    # print(t1)

    # with app.app_context():
    #     db.session.add(t1)
    #     db.session.commit()

    app.run(debug=True)     
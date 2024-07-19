from datetime import datetime
from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pytz

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(200), default=datetime.utcnow, nullable=False)
    isDone = db.Column(db.Boolean, default=False)
    notes = db.relationship('Notes', back_populates='task', cascade='all')

    def __init__(self, title, isDone, notes=None):
        self.title = title
        self.isDone = isDone
        istanbul_tz = pytz.timezone('Europe/Istanbul')
        self.date = datetime.now(istanbul_tz).strftime('%d-%m-%Y %H:%M')
        if notes is not None:
            self.notes = notes

    def __repr__(self):
        return f'Task {self.title}'


class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    task = db.relationship('Task', back_populates='notes')

    def __repr__(self):
        return f'Detail {self.description}'

    def __init__(self, description):
        self.description = description

'''
@app.route('/')
def hello_world():
    todos_length = len(Task.query.all())
    # todos = Task.query.order_by(Task.id).all()
    todos = Task.query.order_by(Task.id).all()
    # todos = Task.query.paginate(per_page=5, page_num=page_num, error_out=True)
    return render_template('index.html', todos=todos, todos_length=todos_length)
'''
@app.route('/')

@app.route('/page/<int:page>')
def hello_world(page=1):
    per_page = 3
    pagination = Task.query.order_by(Task.id).paginate(page=page, per_page=per_page, error_out=False)
    todos_length = pagination.total
    todos = pagination
    return render_template('index.html', todos=todos, todos_length=todos_length)
@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        isDone = 'isDone' in request.form
        details = request.form.getlist('details[]')
        # notes = [Notes(description=detail) for detail in details if detail.strip()]
        new_task = Task(title=title, isDone=isDone)
        for detail in details:
            if detail.strip():
                new_note = Notes(description=detail)
                new_task.notes.append(new_note)
        db.session.add(new_task)
        db.session.commit()

        return redirect(url_for('hello_world'))
    return render_template('add.html')


@app.route('/delete/<int:id>')
def delete_task(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('hello_world'))


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    task = Task.query.get_or_404(id)
    if request.method == 'POST':
        task.title = request.form['title']
        task.isDone = 'isDone' in request.form

        submitted_details = request.form.getlist('details[]')
        submitted_notes_ids = [int(key.split('[')[-1].split(']')[0]) for key in request.form.keys() if
                               key.startswith('notes[')]

        existing_notes = {note.id: note for note in task.notes}


        updated_notes_ids = []
        for note_id in submitted_notes_ids:
            if note_id in existing_notes:
                existing_notes[note_id].description = request.form[f'notes[{note_id}]']
                updated_notes_ids.append(note_id)


        for detail in submitted_details:
            if detail.strip():
                new_note = Notes(description=detail)
                task.notes.append(new_note)


        for note_id in set(existing_notes.keys()) - set(updated_notes_ids):
            db.session.delete(existing_notes[note_id])

        db.session.commit()
        return redirect(url_for('hello_world'))
    return render_template('edit.html', task=task)


@app.route('/delete_note/<int:id>', methods=['POST'])
def delete_note(id):
    note = Notes.query.get_or_404(id)
    if note is not None:
        task_id = note.task_id
        db.session.delete(note)
        db.session.commit()
        return redirect(url_for('edit_task', id=task_id))
    return redirect(url_for('hello_world'))


@app.route('/detail/<int:id>', methods=['GET', 'POST'])
def detail_task(id):
    task = Task.query.get(id)
    return render_template('details.html', task=task)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)

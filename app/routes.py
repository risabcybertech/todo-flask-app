from flask import Blueprint, render_template, redirect, url_for, flash, request
from .models import Task
from .forms import TaskForm
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    tasks = Task.query.order_by(Task.due_date).all()
    return render_template('index.html', tasks=tasks)

@main.route('/add', methods=['GET', 'POST'])
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            description=form.description.data,
            due_date=form.due_date.data,
            priority=form.priority.data,
            category=form.category.data
        )
        db.session.add(task)
        db.session.commit()
        flash('Task added successfully!', 'success')
        return redirect(url_for('main.index'))
    return render_template('add_task.html', form=form)

@main.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    form = TaskForm(obj=task)
    if form.validate_on_submit():
        form.populate_obj(task)
        db.session.commit()
        flash('Task updated!', 'info')
        return redirect(url_for('main.index'))
    return render_template('edit_task.html', form=form, task=task)

@main.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted!', 'danger')
    return redirect(url_for('main.index'))

@main.route('/complete/<int:task_id>')
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.completed = not task.completed
    db.session.commit()
    flash('Task status changed!', 'success')
    return redirect(url_for('main.index'))

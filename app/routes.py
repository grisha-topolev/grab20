from flask import render_template, request, redirect, url_for
from app import app, db
from app.models import Submission
import json

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        names = request.form.getlist('name[]')
        submission = Submission(data=names)
        db.session.add(submission)
        db.session.commit()
        return redirect(url_for('view_data'))
    return render_template('form.html')

@app.route('/view')
def view_data():
    subs = Submission.query.order_by(Submission.created_at.desc()).all()
    return render_template('view.html', submissions=subs)

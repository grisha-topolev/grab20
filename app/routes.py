#app/routes.py
import json

from flask import redirect, render_template, request, url_for

from app import app, db
from app.models import Submission


@app.route('/', methods=['GET', 'POST'])
def index() -> str:
    if request.method == 'POST':
        names: list[str] = request.form.getlist('name[]')
        submission: Submission = Submission(data=names)
        db.session.add(submission)
        db.session.commit()
        return redirect(url_for('view_data'))
    return render_template('form.html')


@app.route('/view')
def view_data() -> str:
    subs: list[Submission] = Submission.query.order_by(
        Submission.created_at.desc()
    ).all()
    return render_template('view.html', submissions=subs)
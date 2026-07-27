from flask import Blueprint, render_template
from flask_login import login_required

history = Blueprint('history', __name__)

@history.route('/history')
@login_required
def view_history():
    return render_template('history.html')
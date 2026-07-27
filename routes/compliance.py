from flask import Blueprint, render_template
from flask_login import login_required

compliance = Blueprint('compliance', __name__)

@compliance.route('/upload')
@login_required
def upload():
    return render_template('upload.html')

@compliance.route('/report/<int:report_id>')
@login_required
def view_report(report_id):
    return "Report coming soon", 200
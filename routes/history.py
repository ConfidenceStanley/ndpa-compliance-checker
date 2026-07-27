from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.compliance import ComplianceReport

history = Blueprint('history', __name__)


@history.route('/history')
@login_required
def view_history():
    reports = ComplianceReport.query.filter_by(
        user_id=current_user.id
    ).order_by(ComplianceReport.date_checked.desc()).all()

    return render_template('history.html', reports=reports)
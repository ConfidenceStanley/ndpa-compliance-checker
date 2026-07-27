from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.compliance import ComplianceReport

dashboard = Blueprint('dashboard', __name__)


@dashboard.route('/dashboard')
@login_required
def home():
    total_checks = ComplianceReport.query.filter_by(
        user_id=current_user.id
    ).count()

    reports = ComplianceReport.query.filter_by(
        user_id=current_user.id
    ).all()

    average_score = 0
    if reports:
        average_score = round(
            sum(r.compliance_score for r in reports) / len(reports), 1
        )

    recent_reports = ComplianceReport.query.filter_by(
        user_id=current_user.id
    ).order_by(ComplianceReport.date_checked.desc()).limit(5).all()

    return render_template(
        'dashboard.html',
        total_checks=total_checks,
        average_score=average_score,
        recent_reports=recent_reports
    )
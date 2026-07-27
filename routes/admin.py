from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db
from models.user import User
from models.compliance import ComplianceReport

admin = Blueprint('admin', __name__)


def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Admin access required.', 'danger')
            return redirect(url_for('dashboard.home'))
        return f(*args, **kwargs)
    return decorated


@admin.route('/admin')
@login_required
@admin_required
def admin_home():
    users = User.query.order_by(User.date_created.desc()).all()
    reports = ComplianceReport.query.order_by(
        ComplianceReport.date_checked.desc()
    ).all()

    total_users = len(users)
    total_reports = len(reports)
    avg_score = 0
    if reports:
        avg_score = round(
            sum(r.compliance_score for r in reports) / len(reports), 1
        )

    return render_template(
        'admin.html',
        users=users,
        reports=reports,
        total_users=total_users,
        total_reports=total_reports,
        avg_score=avg_score
    )


@admin.route('/admin/delete/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    if user_id == current_user.id:
        flash('You cannot delete your own account.', 'danger')
        return redirect(url_for('admin.admin_home'))

    user = User.query.get_or_404(user_id)
    ComplianceReport.query.filter_by(user_id=user_id).delete()
    db.session.delete(user)
    db.session.commit()
    flash(f'User {user.username} deleted successfully.', 'success')
    return redirect(url_for('admin.admin_home'))
from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash, send_file, current_app
)
from flask_login import login_required, current_user
from models import db
from models.compliance import ComplianceReport
from services.pdf_extractor import extract_text_from_file, split_into_sentences
from services.rule_matcher import run_compliance_check
from services.report_generator import generate_pdf_report
import os
import json
import uuid
from datetime import datetime

compliance = Blueprint('compliance', __name__)


def allowed_file(filename):
    allowed = current_app.config.get('ALLOWED_EXTENSIONS', {'pdf', 'txt'})
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed


@compliance.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        if 'document' not in request.files:
            flash('No file selected.', 'danger')
            return redirect(url_for('compliance.upload'))

        file = request.files['document']

        if file.filename == '':
            flash('No file selected.', 'danger')
            return redirect(url_for('compliance.upload'))

        if not allowed_file(file.filename):
            flash('Only PDF and TXT files are allowed.', 'danger')
            return redirect(url_for('compliance.upload'))

        original_filename = file.filename
        safe_filename = f"{uuid.uuid4().hex}_{original_filename}"
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, safe_filename)
        file.save(file_path)

        try:
            srs_text = extract_text_from_file(file_path, original_filename)

            if not srs_text or len(srs_text) < 50:
                flash('Could not extract text from the document. Please check the file.', 'danger')
                os.remove(file_path)
                return redirect(url_for('compliance.upload'))

            srs_sentences = split_into_sentences(srs_text)

            if len(srs_sentences) < 2:
                flash('Document has too little content to analyse.', 'danger')
                os.remove(file_path)
                return redirect(url_for('compliance.upload'))

            summary = run_compliance_check(srs_text, srs_sentences)

            if not summary:
                flash('Compliance check failed. Please try again.', 'danger')
                os.remove(file_path)
                return redirect(url_for('compliance.upload'))

            report = ComplianceReport(
                user_id=current_user.id,
                file_name=original_filename,
                compliance_score=summary['compliance_score'],
                total_rules=summary['total_rules'],
                compliant_count=summary['compliant_count'],
                non_compliant_count=summary['non_compliant_count'],
                not_addressed_count=summary['not_addressed_count'],
                report_data=json.dumps(summary),
                date_checked=datetime.utcnow()
            )
            db.session.add(report)
            db.session.commit()

            os.remove(file_path)

            flash('Compliance check completed successfully.', 'success')
            return redirect(url_for('compliance.view_report', report_id=report.id))

        except Exception as e:
            print(f"Compliance check error: {e}")
            if os.path.exists(file_path):
                os.remove(file_path)
            flash('An error occurred during analysis. Please try again.', 'danger')
            return redirect(url_for('compliance.upload'))

    return render_template('upload.html')


@compliance.route('/report/<int:report_id>')
@login_required
def view_report(report_id):
    report = ComplianceReport.query.filter_by(
        id=report_id,
        user_id=current_user.id
    ).first_or_404()

    report_data = json.loads(report.report_data)
    results = report_data.get('results', [])

    return render_template('report.html', report=report, results=results)


@compliance.route('/report/<int:report_id>/download')
@login_required
def download_report(report_id):
    report = ComplianceReport.query.filter_by(
        id=report_id,
        user_id=current_user.id
    ).first_or_404()

    reports_folder = os.path.join(current_app.root_path, 'generated_reports')
    os.makedirs(reports_folder, exist_ok=True)
    output_path = os.path.join(reports_folder, f"report_{report_id}.pdf")

    generate_pdf_report(report, output_path)

    return send_file(
        output_path,
        as_attachment=True,
        download_name=f"NDPA_Compliance_Report_{report_id}.pdf"
    )
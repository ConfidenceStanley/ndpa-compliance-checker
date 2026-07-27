from . import db
from datetime import datetime

class NdpaRule(db.Model):
    __tablename__ = 'ndpa_rules'

    id = db.Column(db.Integer, primary_key=True)
    section = db.Column(db.String(50))
    rule_text = db.Column(db.Text, nullable=False)
    rule_type = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<NdpaRule {self.section}>'


class ComplianceReport(db.Model):
    __tablename__ = 'compliance_reports'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    file_name = db.Column(db.String(255))
    compliance_score = db.Column(db.Float, default=0.0)
    total_rules = db.Column(db.Integer, default=0)
    compliant_count = db.Column(db.Integer, default=0)
    non_compliant_count = db.Column(db.Integer, default=0)
    not_addressed_count = db.Column(db.Integer, default=0)
    report_data = db.Column(db.Text)
    date_checked = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ComplianceReport {self.id}>'
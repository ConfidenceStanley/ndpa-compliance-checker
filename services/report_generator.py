from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import json
import os


def generate_pdf_report(report, output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=18,
        textColor=colors.HexColor('#15803d'),
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#64748b'),
        spaceAfter=4,
        alignment=TA_CENTER
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=16,
        spaceAfter=8,
        fontName='Helvetica-Bold'
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=4,
        leading=14
    )

    small_style = ParagraphStyle(
        'SmallBody',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#475569'),
        leading=12
    )

    story = []

    story.append(Paragraph("NDPA 2023 Compliance Report", title_style))
    story.append(Paragraph("Nigeria Data Protection Act 2023 - Automated Compliance Analysis", subtitle_style))
    story.append(Paragraph(f"Generated: {datetime.utcnow().strftime('%d %B %Y at %H:%M UTC')}", subtitle_style))
    story.append(Spacer(1, 0.3 * cm))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#e2e8f0')))
    story.append(Spacer(1, 0.4 * cm))

    story.append(Paragraph("Summary", heading_style))

    if report.compliance_score >= 70:
        score_color = colors.HexColor('#16a34a')
        verdict = "COMPLIANT"
    elif report.compliance_score >= 40:
        score_color = colors.HexColor('#d97706')
        verdict = "PARTIALLY COMPLIANT"
    else:
        score_color = colors.HexColor('#dc2626')
        verdict = "NON-COMPLIANT"

    summary_data = [
        ["Document", report.file_name],
        ["Overall Score", f"{report.compliance_score}%"],
        ["Verdict", verdict],
        ["Total Rules Checked", str(report.total_rules)],
        ["Compliant", str(report.compliant_count)],
        ["Non-Compliant", str(report.non_compliant_count)],
        ["Not Addressed", str(report.not_addressed_count)],
        ["Date Checked", report.date_checked.strftime('%d %B %Y')]
    ]

    summary_table = Table(summary_data, colWidths=[5 * cm, 12 * cm])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0fdf4')),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#15803d')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 0.5 * cm))

    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#e2e8f0')))
    story.append(Paragraph("Detailed Findings", heading_style))

    report_data = json.loads(report.report_data)
    results = report_data.get('results', [])

    for idx, result in enumerate(results, 1):
        status = result.get('status', '')

        if status == "COMPLIANT":
            status_color = colors.HexColor('#16a34a')
            bg_color = colors.HexColor('#f0fdf4')
        elif status == "NON-COMPLIANT":
            status_color = colors.HexColor('#dc2626')
            bg_color = colors.HexColor('#fef2f2')
        else:
            status_color = colors.HexColor('#d97706')
            bg_color = colors.HexColor('#fffbeb')

        finding_data = [
            [f"#{idx}", result.get('section', ''), result.get('rule_type', ''), status],
            ["Rule:", Paragraph(result.get('rule_text', ''), small_style), "", ""],
            ["Match:", Paragraph(result.get('matched_sentence', ''), small_style), "", ""],
            ["Action:", Paragraph(result.get('recommendation', ''), small_style), "", ""]
        ]

        finding_table = Table(
            finding_data,
            colWidths=[1.5 * cm, 10 * cm, 2.5 * cm, 3 * cm]
        )
        finding_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), bg_color),
            ('TEXTCOLOR', (3, 0), (3, 0), status_color),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.3, colors.HexColor('#e2e8f0')),
            ('SPAN', (1, 1), (3, 1)),
            ('SPAN', (1, 2), (3, 2)),
            ('SPAN', (1, 3), (3, 3)),
            ('PADDING', (0, 0), (-1, -1), 6),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        story.append(finding_table)
        story.append(Spacer(1, 0.2 * cm))

    story.append(Spacer(1, 0.3 * cm))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#e2e8f0')))
    story.append(Spacer(1, 0.2 * cm))
    story.append(Paragraph(
        "This report was generated automatically by the NDPA Compliance Checker system. "
        "It is intended for informational purposes and does not constitute legal advice. "
        "Always consult a qualified legal professional for formal compliance assessment.",
        subtitle_style
    ))

    doc.build(story)
    return output_path
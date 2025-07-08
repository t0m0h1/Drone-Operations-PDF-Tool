from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from datetime import datetime
import os

def generate_pdf(checklists, logo_filename):
    output_path = 'checklist_output.pdf'
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    margin = 20 * mm
    y = height - margin

    # Draw logo if provided
    if logo_filename:
        logo_path = os.path.join("static", "uploads", logo_filename)
        if os.path.exists(logo_path):
            logo_width = 60 * mm
            logo_height = 30 * mm
            c.drawImage(logo_path, (width - logo_width) / 2, y - logo_height, width=logo_width, height=logo_height, mask='auto')
            y -= (logo_height + 10)

    # Title
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, y, "Drone Pre-Flight Checklist")
    y -= 25

    # Date/time
    c.setFont("Helvetica", 10)
    c.drawCentredString(width / 2, y, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    y -= 25

    c.setFont("Helvetica", 12)
    line_height = 14

    for section, subsections in checklists.items():
        # Main section title
        c.setFont("Helvetica-Bold", 16)
        y -= 10
        if y < margin:
            c.showPage()
            y = height - margin
        c.drawString(margin, y, section)
        y -= line_height

        for subsection, items in subsections.items():
            # Subsection title
            c.setFont("Helvetica-BoldOblique", 14)
            if y < margin:
                c.showPage()
                y = height - margin
            c.drawString(margin + 10, y, subsection)
            y -= line_height

            # Items as bullet points
            c.setFont("Helvetica", 12)
            bullet_indent = margin + 20
            for item in items:
                if y < margin + line_height:
                    c.showPage()
                    y = height - margin
                c.drawString(bullet_indent, y, u"• " + item)
                y -= line_height

            y -= 5  # small space after subsection

        y -= 10  # extra space after main section

    c.save()
    return output_path

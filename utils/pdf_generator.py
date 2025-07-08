from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os

def generate_pdf(checklists, logo_filename):
    output_path = 'checklist_output.pdf'
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    y = height - 50

    # Draw logo
    if logo_filename:
        logo_path = os.path.join("static", "uploads", logo_filename)
        if os.path.exists(logo_path):
            c.drawImage(logo_path, 200, y - 100, width=200, preserveAspectRatio=True, mask='auto')
            y -= 120

    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width / 2, y, "Drone Pre-Flight Checklist")
    y -= 40

    c.setFont("Helvetica", 12)
    c.drawString(40, y, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    y -= 30

    for section, items in checklists.items():
        c.setFont("Helvetica-Bold", 14)
        c.drawString(40, y, section)
        y -= 20
        c.setFont("Helvetica", 12)
        for item in items:
            c.drawString(60, y, f"• {item}")
            y -= 15
            if y < 50:
                c.showPage()
                y = height - 50
        y -= 10

    c.save()
    return output_path

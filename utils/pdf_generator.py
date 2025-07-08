from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import os
import datetime

def generate_pdf(checklists, logo_filename=None):
    pdf_path = "static/checklist_output.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # Add logo if present
    if logo_filename:
        logo_path = os.path.join("static", "uploads", logo_filename)
        if os.path.isfile(logo_path):
            try:
                img = Image(logo_path, width=2.5*inch, height=1*inch)
                story.append(img)
                story.append(Spacer(1, 12))
            except Exception as e:
                print(f"Error loading logo image: {e}")
        else:
            print(f"Logo file not found: {logo_path}")

    # Title and date
    story.append(Paragraph("<strong>Drone Pre-Flight Checklist</strong>", styles['Title']))
    story.append(Paragraph(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
    story.append(Spacer(1, 12))

    # Loop through all sections and subsections
    for section, subsections in checklists.items():
        story.append(Paragraph(f"<strong>{section}</strong>", styles['Heading2']))
        for subsection, items in subsections.items():
            story.append(Paragraph(f"<u>{subsection}</u>", styles['Heading4']))
            if items:
                for item in items:
                    story.append(Paragraph(f"• {item}", styles['Normal']))
            else:
                story.append(Paragraph("<i>No items selected</i>", styles['Normal']))
            story.append(Spacer(1, 6))
        story.append(Spacer(1, 12))

    doc.build(story)
    return pdf_path

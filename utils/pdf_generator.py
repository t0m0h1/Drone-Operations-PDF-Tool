from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import os
import datetime

def generate_pdf(checklists, logo_path=None):
    print(f"[DEBUG] generate_pdf received logo_path: {logo_path}")
    pdf_path = "static/checklist_output.pdf"
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

    doc = SimpleDocTemplate(pdf_path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # Add logo if valid
    if logo_path:
        abs_path = os.path.abspath(logo_path)
        print(f"[DEBUG] Attempting to load logo from: {abs_path}")
        if os.path.isfile(logo_path):
            try:
                img = Image(logo_path, width=2.5 * inch, height=1 * inch)
                story.append(img)
                story.append(Spacer(1, 12))
                print("[DEBUG] Logo image added to PDF.")
            except Exception as e:
                print(f"[ERROR] Failed to load image into PDF: {e}")
        else:
            print(f"[ERROR] Logo file does not exist at: {logo_path}")
    else:
        print("[DEBUG] No logo_path provided.")

    # Title and timestamp
    story.append(Paragraph("<strong>Drone Pre-Flight Checklist</strong>", styles['Title']))
    story.append(Paragraph(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
    story.append(Spacer(1, 12))

    # Checklist content
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

    try:
        doc.build(story)
        print("[DEBUG] PDF build successful.")
    except Exception as e:
        print(f"[ERROR] Failed to build PDF: {e}")

    return pdf_path

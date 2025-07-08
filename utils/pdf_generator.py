from xhtml2pdf import pisa
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

def generate_pdf(checklists, logo_filename):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('pdf_template.html')

    html_out = template.render(
        checklists=checklists,
        logo=f'static/uploads/{logo_filename}' if logo_filename else None,
        now=datetime.now().strftime('%Y-%m-%d %H:%M')
    )

    output_path = 'checklist_output.pdf'
    with open(output_path, "w+b") as pdf_file:
        pisa.CreatePDF(html_out, dest=pdf_file)
    return output_path

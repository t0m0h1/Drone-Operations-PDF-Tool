import os
from flask import Flask, render_template, request, redirect, send_file
from werkzeug.utils import secure_filename
from utils.pdf_generator import generate_pdf
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB

checklists = {
    'Loading List': [],
    'Flight Reference Cards': [],
    'Procedures': []
}
logo_filename = None

@app.route('/', methods=['GET', 'POST'])
def index():
    global logo_filename
    if request.method == 'POST':
        section = request.form.get('section')
        item = request.form.get('item')
        if section in checklists and item:
            checklists[section].append(item)
        if 'logo' in request.files:
            logo = request.files['logo']
            if logo.filename != '':
                logo_filename = secure_filename(logo.filename)
                logo.save(os.path.join(app.config['UPLOAD_FOLDER'], logo_filename))
    return render_template('index.html', checklists=checklists, logo=logo_filename)

@app.route('/delete_item/<section>/<int:index>')
def delete_item(section, index):
    if section in checklists and 0 <= index < len(checklists[section]):
        del checklists[section][index]
    return redirect('/')

@app.route('/download_pdf')
def download_pdf():
    pdf_path = generate_pdf(checklists, logo_filename)
    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)

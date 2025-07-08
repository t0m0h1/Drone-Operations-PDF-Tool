import os
from flask import Flask, render_template, request, redirect, send_file
from werkzeug.utils import secure_filename
from utils.pdf_generator import generate_pdf

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB

# Checklist structure: Section → Subsection → [items]
PREDEFINED_ITEMS = {
    'Loading List': {
        'Pre-flight': [
            'Check power station packed',
            'Pack anemometer',
            'Prepare spare batteries',
            'Load SD cards'
        ],
        'In-flight': [],
        'Post-flight': [
            'Collect all equipment',
            'Check for damage after flight'
        ]
    },
    'Flight Reference Cards': {
        'Pre-flight': [
            'Verify GPS lock',
            'Check compass calibration',
            'Confirm firmware updates'
        ],
        'In-flight': [
            'Monitor signal strength',
            'Check obstacle sensors',
            'Maintain altitude awareness'
        ],
        'Post-flight': [
            'Download flight logs',
            'Review flight data for anomalies'
        ]
    },
    'Procedures': {
        'Pre-flight': [
            'Confirm emergency landing sites',
            'Review weather and NOTAMs'
        ],
        'In-flight': [
            'Loss of signal procedure',
            'Emergency landing protocol'
        ],
        'Post-flight': [
            'Battery swap procedure',
            'Post-flight inspection'
        ]
    }
}

# Persistent checklist (including custom items)
checklists = {
    section: {sub: [] for sub in subs}
    for section, subs in PREDEFINED_ITEMS.items()
}

logo_filename = None

def encode_key(s):
    return s.replace(' ', '_')

@app.route('/', methods=['GET', 'POST'])
def index():
    global logo_filename
    if request.method == 'POST':
        # Handle logo upload
        if 'logo' in request.files:
            logo = request.files['logo']
            if logo and logo.filename != '':
                logo_filename = secure_filename(logo.filename)
                logo.save(os.path.join(app.config['UPLOAD_FOLDER'], logo_filename))

        # Handle checklist selection update (only when checkbox form submitted)
        for section, subsections in PREDEFINED_ITEMS.items():
            for subsection in subsections:
                field_name = f'predefined-{encode_key(section)}-{encode_key(subsection)}'
                selected_items = request.form.getlist(field_name)

                predefined = PREDEFINED_ITEMS[section][subsection]
                existing_custom_items = [
                    item for item in checklists[section][subsection]
                    if item not in predefined
                ]

                if selected_items:  # Only update if this form includes checkbox data
                    checklists[section][subsection] = selected_items + existing_custom_items

        # Handle custom item addition
        custom_section = request.form.get('custom-section')
        custom_subsection = request.form.get('custom-subsection')
        custom_item = request.form.get('custom-item')
        if (
            custom_section in checklists and
            custom_subsection in checklists[custom_section] and
            custom_item and custom_item.strip()
        ):
            checklists[custom_section][custom_subsection].append(custom_item.strip())

    return render_template(
        'index.html',
        predefined=PREDEFINED_ITEMS,
        checklists=checklists,
        logo=logo_filename
    )

@app.route('/delete_item/<section>/<subsection>/<int:index>')
def delete_item(section, subsection, index):
    if (
        section in checklists and
        subsection in checklists[section] and
        0 <= index < len(checklists[section][subsection])
    ):
        del checklists[section][subsection][index]
    return redirect('/')

@app.route('/download_pdf')
def download_pdf():
    pdf_path = generate_pdf(checklists, logo_filename)
    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)

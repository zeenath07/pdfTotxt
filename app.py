from flask import Flask, request, render_template, send_file, redirect, url_for, flash
import io
from werkzeug.utils import secure_filename
from utils.pdf_to_text import pdf_to_text

app = Flask(__name__)
app.secret_key = "change-me-to-secure-key"
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 MB limit

ALLOWED = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'pdf_file' not in request.files:
        flash("No file part")
        return redirect(url_for('index'))
    f = request.files['pdf_file']
    if f.filename == '':
        flash("No selected file")
        return redirect(url_for('index'))
    if not allowed_file(f.filename):
        flash("Only PDF files allowed")
        return redirect(url_for('index'))

    filename = secure_filename(f.filename)
    # read file bytes
    file_bytes = f.read()
    # convert pdf bytes to text
    text = pdf_to_text(io.BytesIO(file_bytes))

    # create text file in memory
    txt_io = io.BytesIO()
    txt_io.write(text.encode('utf-8'))
    txt_io.seek(0)

    out_name = filename.rsplit('.',1)[0] + '.txt'
    return send_file(txt_io,
                     as_attachment=True,
                     download_name=out_name,
                     mimetype='text/plain')

if __name__ == '__main__':
    # For local testing
    app.run(host='0.0.0.0', port=8000, debug=True)

import os
import io
import tempfile
import zipfile
from flask import Flask, render_template, request, send_file, redirect
from pypdf import PdfReader, PdfWriter

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        files = request.files.getlist('files')
        if not files:
            return redirect('/')
        writer = PdfWriter()
        for f in files:
            if f.filename and f.filename.lower().endswith('.pdf'):
                reader = PdfReader(f)
                for page in reader.pages:
                    writer.add_page(page)
        if not writer.pages:
            return redirect('/')
        fd, path = tempfile.mkstemp(suffix='.pdf')
        os.close(fd)
        with open(path, 'wb') as out:
            writer.write(out)
        return send_file(path, as_attachment=True, download_name='merged.pdf')
    return render_template('index.html')


@app.route('/split', methods=['GET', 'POST'])
def split_pdf():
    if request.method == 'POST':
        f = request.files.get('file')
        if not f or not f.filename.lower().endswith('.pdf'):
            return redirect('/split')
        reader = PdfReader(f)
        mem_zip = io.BytesIO()
        with zipfile.ZipFile(mem_zip, 'w') as zf:
            for i, page in enumerate(reader.pages):
                writer = PdfWriter()
                writer.add_page(page)
                page_bytes = io.BytesIO()
                writer.write(page_bytes)
                zf.writestr(f'page_{i+1}.pdf', page_bytes.getvalue())
        mem_zip.seek(0)
        return send_file(mem_zip, as_attachment=True,
                         download_name='split_pages.zip',
                         mimetype='application/zip')
    return render_template('split.html')

if __name__ == '__main__':
    app.run(debug=True)

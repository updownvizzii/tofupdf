# PDF Fusion Wizard

A simple web application to merge or split PDF files using a Python back end.

## Running the Server

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the web server:
   ```bash
   python webapp/app.py
   ```
3. Open `http://localhost:5000` in your browser.

Upload PDF files through the landing page and the merged file will download automatically.

To split a PDF into individual pages, visit `http://localhost:5000/split` and upload a single PDF. The pages will be returned in a ZIP file.

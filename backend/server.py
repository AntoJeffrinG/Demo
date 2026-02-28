import os
from flask import Flask, send_from_directory, abort
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

FRONTEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'frontend')
 
@app.route('/')
def index():
    return send_from_directory(FRONTEND_DIR, 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    file_path = os.path.join(FRONTEND_DIR, filename)
    if os.path.exists(file_path):
        return send_from_directory(FRONTEND_DIR, filename)
     
    html_file_path = os.path.join(FRONTEND_DIR, filename + '.html')
    if os.path.exists(html_file_path):
        return send_from_directory(FRONTEND_DIR, filename + '.html')
    
    abort(404)

if __name__ == '__main__':
    app.run(debug=False, port=5000)

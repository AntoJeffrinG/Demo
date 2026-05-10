import os
from datetime import datetime
from flask import Flask, render_template, abort
try:
    from flask_cors import CORS
except ImportError:
    CORS = None

template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend'))
app = Flask(__name__, template_folder=template_dir)
if CORS:
    CORS(app)

# Disable template caching so edits to HTML files are always reflected immediately
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.auto_reload = True

# ── Jinja2 compatibility shims ──────────────────────────────────────────────
# LLMs sometimes generate filters/globals that don't exist in Flask's default
# Jinja2 environment. Register them here so the preview never 500s.

def _date_filter(value, fmt="%Y"):
    """Handles {{ 'now'|date('Y') }} and {{ datetime_obj|date('%Y-%m-%d') }}"""
    if value == 'now' or value is None:
        value = datetime.now()
    if isinstance(value, datetime):
        # Convert PHP-style 'Y' to Python '%Y'
        fmt = fmt.replace('Y', '%Y').replace('m', '%m').replace('d', '%d')
        if not fmt.startswith('%'):
            fmt = '%' + fmt
        return value.strftime(fmt)
    return str(value)

app.jinja_env.filters['date'] = _date_filter
app.jinja_env.filters['strftime'] = lambda v, f='%Y-%m-%d': (
    v.strftime(f) if isinstance(v, datetime) else str(v)
)
app.jinja_env.globals['now'] = datetime.now
app.jinja_env.globals['current_year'] = datetime.now().year
# ────────────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    for name in ('index.html', 'home.html'):
        if os.path.exists(os.path.join(app.template_folder, name)):
            return render_template(name)
    abort(404)

@app.route('/<path:filename>')
def serve_any(filename):
    if os.path.exists(os.path.join(app.template_folder, filename)):
        return render_template(filename)
    html_version = f"{filename}.html"
    if os.path.exists(os.path.join(app.template_folder, html_version)):
        return render_template(html_version)
    abort(404)

if __name__ == '__main__':
    print("SynthSite Preview Server starting on http://127.0.0.1:5000")
    app.run(debug=False, port=5000)

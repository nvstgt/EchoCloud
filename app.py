from flask import Flask, render_template, request, redirect, url_for, jsonify, render_template_string, session, flash
from markupsafe import escape
from jinja2 import Environment, BaseLoader
import os, time, threading, requests
import sqlite3
import requests
from init_db import get_db, init_db

app = Flask(__name__)
app.secret_key = 'd4b8f10e96d8ff7e5a3cf22b7dbb3e26a9e19f6adf6e8a3e5c0c9174c4e1f67d'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/music/SSTI.mp3')
def ssti_track():
    if 'username' in session and session['username'] == 'TheProfezzorJ':
        return render_template_string("""
        <html>
        <body>
            <h1>Track Not Found</h1>
            <p>Sorry, that track couldn't be found. Please re-upload the track below.</p>
            <form action="{{ url_for('upload') }}" method="POST">
                <label for="track_name">Track Name:</label>
                <input type="text" name="track_name" required><br><br>
                
                <label for="artist_name">Artist Name:</label>
                <input type="text" name="artist_name" required><br><br>
                
                <label for="description">Description:</label>
                <textarea name="description" required></textarea><br><br>
                
                <label for="custom_html">Custom Artwork (HTML allowed):</label>
                <textarea name="custom_html"></textarea><br><br>
                
                <button type="submit">Upload Track</button>
            </form>
        </body>
        </html>
        """)
    
    flash("You need to be logged in as TheProfezzorJ to upload tracks.")
    return redirect(url_for('login', next=request.path))

@app.route('/profile')
def profile():
    if 'username' not in session:
        flash("You need to login to access the profile page.")
        return redirect(url_for('login'))
    
    username = session['username']
    db = get_db()
    
    user = db.execute("SELECT email, favorite_genre, member_since FROM users WHERE username = ?", (username,)).fetchone()
    
    uploads = db.execute("SELECT date, title, artist FROM uploads WHERE username = ? ORDER BY date DESC LIMIT 10", (username,)).fetchall()
    
    return render_template('profile.html',
                           username=username,
                           email=user['email'] if user else "N/A",
                           favorite_genre=user['favorite_genre'] if user else "Unknown",
                           member_since=user['member_since'] if user else "N/A",
                           uploads=uploads)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password)).fetchone()
        
        if user:
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Invalid credentials', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("Successfully logged out.")
    return redirect(url_for('index'))

@app.route('/explore')
def explore():
    return render_template('explore.html')

UPLOAD_FOLDER = os.path.join(os.getcwd(), "static", "images", "uploads")
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def schedule_file_deletion(filepath, delay=1800):
    """Schedule deletion of the file after 'delay' seconds (default 30 minutes)."""
    def delete_file():
        time.sleep(delay)
        try:
            os.remove(filepath)
            print(f"Deleted file: {filepath}")
        except Exception as e:
            print(f"Error deleting file: {e}")
    threading.Thread(target=delete_file, daemon=True).start()

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'username' not in session:
        flash('Unauthorized access. Please log in.', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == "upload":
            track_name = request.form.get('track_name', '')
            artist_name = request.form.get('artist_name', '')
            description = request.form.get('description', '')
            custom_template = request.form.get('custom_template', '')
            xml_data = request.form.get('xml_data', '')
            artwork_file = request.files.get('artwork_file')
    
            file_info = "No file uploaded"
            if artwork_file:
                filename = artwork_file.filename
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                artwork_file.save(file_path)
                schedule_file_deletion(file_path)
                file_info = url_for('static', filename=f"images/uploads/{filename}")
    
            xml_parsed = ""
            if xml_data:
                import xml.etree.ElementTree as ET
                try:
                    tree = ET.fromstring(xml_data)
                    xml_parsed = ET.tostring(tree, encoding='unicode')
                except Exception as e:
                    xml_parsed = f"XML Parsing Error: {e}"
    
            try:
                ssti_output = render_template_string(custom_template)
            except Exception as e:
                ssti_output = f"error: {e}"
    
            upload_result_template = """
            {% extends "base.html" %}
            {% block content %}
            <section class="upload-result">
                <h1>Upload Complete!</h1>
                <p>Track Name: {{ track_name|safe }}</p>
                <p>Artist: {{ artist_name|safe }}</p>
                <p>Description: {{ description|safe }}</p>
                <p>Album Art Path: {{ file_info|safe }}</p>
                {% if xml_data %}
                <h2>Parsed XML Metadata:</h2>
                <pre>{{ xml_parsed|safe }}</pre>
                {% endif %}
                {% if custom_template %}
                <h2>Custom Template Output (SSTI):</h2>
                <div>{{ ssti_output|safe }}</div>
                {% endif %}
                <p><small>Note: Uploaded files will be automatically deleted after 30 minutes.</small></p>
                <a href="{{ url_for('index') }}">Return to Homepage</a>
            </section>
            {% endblock %}
            """
            return render_template_string(
                upload_result_template,
                track_name=track_name,
                artist_name=artist_name,
                description=description,
                file_info=file_info,
                xml_data=xml_data,
                xml_parsed=xml_parsed,
                custom_template=custom_template,
                ssti_output=ssti_output
            )
    
        elif action == "fetch_metadata":
            target = request.args.get('target', 'http://nonexistent.example.com/metadata.xml')
            try:
                r = requests.get(target)
                xml_data = r.text
            except Exception as e:
                xml_data = f"Error fetching metadata: {e}"
    
            import xml.etree.ElementTree as ET
            try:
                tree = ET.fromstring(xml_data)
                xml_parsed = ET.tostring(tree, encoding='unicode')
            except Exception as e:
                xml_parsed = f"XML Parsing Error: {e}"
    
            fetch_result_template = """
            {% extends "base.html" %}
            {% block content %}
            <section class="metadata-result">
                <h1>Metadata Fetch Result</h1>
                <p>Target: {{ target }}</p>
                <pre>{{ xml_parsed|safe }}</pre>
                <a href="{{ url_for('upload') }}">Return to Upload Page</a>
            </section>
            {% endblock %}
            """
            return render_template_string(fetch_result_template, target=target, xml_parsed=xml_parsed)
    
    else:
        return render_template_string("""
        {% extends "base.html" %}
        {% block content %}
        <section class="upload-section">
            <h1>Upload Track</h1>
            <form method="POST" action="{{ url_for('upload') }}" enctype="multipart/form-data">
                <label for="track_name">Track Name:</label>
                <input type="text" name="track_name" required><br><br>
                
                <label for="artist_name">Artist Name:</label>
                <input type="text" name="artist_name" required><br><br>
                
                <label for="description">Description:</label>
                <textarea name="description" required></textarea><br><br>
                
                <label for="artwork_file">Upload Artwork:</label>
                <input type="file" name="artwork_file" required><br><br>
                
                <!-- New field vulnerable to SSTI -->
                <label for="custom_template">Custom Template:</label>
                <textarea name="custom_template" placeholder="Enter custom template code"></textarea><br><br>
                
                <!-- Hidden XML metadata field (could be replaced by fetch) -->
                <input type="hidden" name="xml_data" value="<foo>Default XML</foo>">
                
                <!-- Two buttons: one for normal upload, one for fetching metadata -->
                <button type="submit" name="action" value="upload">Upload Track</button>
                <button type="submit" name="action" value="fetch_metadata">Fetch Metadata</button>
            </form>
        </section>
        {% endblock %}
        """)

@app.route('/fetch_metadata', methods=['GET'])
def fetch_metadata():
    target = request.args.get('target', 'http://nonexistent.example.com/metadata.xml')
    try:
        r = requests.get(target)
        xml_data = r.text
    except Exception as e:
        xml_data = f"Error fetching metadata: {e}"
    return render_template_string("""
    {% extends "base.html" %}
    {% block content %}
    <section class="metadata-result">
      <h1>Metadata Fetch Result</h1>
      <p>Target: {{ target }}</p>
      <pre>{{ xml_data }}</pre>
      <a href="{{ url_for('upload') }}">Return to Upload</a>
    </section>
    {% endblock %}
    """, target=target, xml_data=xml_data)

@app.route('/test')
def test():
    return render_template_string("{{ 7 * 7 }}")

@app.route('/<path:filename>')
def static_files(filename):
    return app.send_static_file(filename)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.after_request
def add_security_headers(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; img-src 'self' data:;"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

@app.route('/search_artists')
def search_artists():
    q = request.args.get('q', '')
    db = get_db()
    
    sql = "SELECT name, bio FROM artists WHERE name LIKE '%" + q + "%'"
    
    try:
        results = db.execute(sql).fetchall()
    except Exception as e:
        return f"SQL Error: {e}"
    
    return render_template("search.html", results=results)

@app.route('/fetch', methods=['GET'])
def fetch():
    url = request.args.get('url', '')
    fetched_content = None
    if url:
        try:
            r = requests.get(url)
            fetched_content = r.text
        except Exception as e:
            fetched_content = f"Error fetching URL: {e}"
    return render_template("fetch.html", fetched_content=fetched_content, url=url)

@app.route('/parse_xml', methods=['POST'])
def parse_xml():
    import xml.etree.ElementTree as ET
    xml_data = request.data.decode()
    try:
        tree = ET.fromstring(xml_data)
        return "XML Parsed Successfully!"
    except Exception as e:
        return f"XML Parsing Error: {e}"

@app.route('/deserialize', methods=['POST'])
def deserialize():
    data = request.form.get('data', '')
    try:
        obj = eval(data)
        return f"Deserialized object: {obj}"
    except Exception as e:
        return f"Deserialization Error: {e}"

DATABASE_PATH = os.path.join(os.getcwd(), "vulnerable.db")
if not os.path.exists(DATABASE_PATH):
    init_db()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10405)

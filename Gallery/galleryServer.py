import os
from flask import Flask, render_template_string, send_from_directory
import sqlite3

app = Flask(__name__)
DB_PATH = "gallery.db"

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>VRChat Gallery</title>
    <style>
        body { font-family: sans-serif; background: #111; color: #eee; padding: 2em; }
        .gallery { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5em; }
        .item { background: #222; padding: 1em; border-radius: 10px; }
        img { max-width: 100%; border-radius: 10px; }
        .meta { margin-top: 0.5em; font-size: 0.9em; color: #ccc; }
    </style>
</head>
<body>
    <h1>VRChat Gallery</h1>
    <div class="gallery">
        {% for entry in entries %}
        <div class="item">
            <img src="{{ entry.image_path }}" alt="{{ entry.title }}">
            <h2>{{ entry.title }}</h2>
            <div class="meta">By {{ entry.user }} at {{ entry.timestamp }}</div>
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../DiscordBot/gallery_images"))

@app.route('/gallery_images/<filename>')
def uploaded_image(filename):
    return send_from_directory(BASE_DIR, filename)

@app.route("/")
def gallery():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT user, title, image_path, timestamp FROM submissions ORDER BY id DESC")
        entries = [dict(zip(["user", "title", "image_path", "timestamp"], row)) for row in c.fetchall()]
    return render_template_string(HTML, entries=entries)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
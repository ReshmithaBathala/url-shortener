from flask import Flask, jsonify, request, redirect, abort
from app.utils import generate_short_code, is_valid_url
from datetime import datetime, timezone


app = Flask(__name__)

# In-memory storage
url_db = {}  # short_code → {original_url, clicks, created_at}

@app.route('/')
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "URL Shortener API"
    })

@app.route('/api/health')
def api_health():
    return jsonify({
        "status": "ok",
        "message": "URL Shortener API is running"
    })

# Shorten URL
@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    original_url = data.get("url")

    if not original_url or not is_valid_url(original_url):
        return jsonify({"error": "Invalid or missing URL"}), 400

    short_code = generate_short_code()
    while short_code in url_db:
        short_code = generate_short_code()  # ensure uniqueness

    url_db[short_code] = {
        "url": original_url,
        "clicks": 0,
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    return jsonify({
        "short_code": short_code,
        "short_url": f"http://localhost:5000/{short_code}"
    }), 201

# Redirect handler
@app.route('/<short_code>')
def redirect_to_url(short_code):
    entry = url_db.get(short_code)
    if not entry:
        abort(404)

    entry["clicks"] += 1
    return redirect(entry["url"])

# Stats endpoint
@app.route('/api/stats/<short_code>')
def get_stats(short_code):
    entry = url_db.get(short_code)
    if not entry:
        return jsonify({"error": "Short code not found"}), 404

    return jsonify({
        "url": entry["url"],
        "clicks": entry["clicks"],
        "created_at": entry["created_at"]
    })

@app.route('/debug')
def debug():
    return jsonify(url_db)

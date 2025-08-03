# TODO: Implement your data models here
# Consider what data structures you'll need for:
# - Storing URL mappings
# - Tracking click counts
# - Managing URL metadata

# app/models.py
from datetime import datetime
from threading import Lock

# In-memory database: short_code → data
url_store = {}
store_lock = Lock()

def save_url_mapping(short_code, original_url):
    with store_lock:
        url_store[short_code] = {
            "url": original_url,
            "created_at": datetime.utcnow(),
            "clicks": 0
        }

def get_url_mapping(short_code):
    with store_lock:
        return url_store.get(short_code)

def increment_click(short_code):
    with store_lock:
        if short_code in url_store:
            url_store[short_code]["clicks"] += 1

def get_stats(short_code):
    with store_lock:
        data = url_store.get(short_code)
        if data:
            return {
                "url": data["url"],
                "clicks": data["clicks"],
                "created_at": data["created_at"].isoformat()
            }
        return None

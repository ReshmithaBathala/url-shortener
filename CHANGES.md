# CHANGES.md

##  Features Implemented

1. **POST /api/shorten**
   - Accepts a long URL in JSON.
   - Validates input format.
   - Generates a 6-character alphanumeric short code.
   - Returns a short URL and code.

2. **GET /<short_code>**
   - Redirects to the original URL.
   - Increments click count.
   - Returns 404 if code doesn't exist.

3. **GET /api/stats/<short_code>**
   - Returns original URL, click count, creation timestamp.
   - Returns 404 if code not found.

---

##  Architectural Decisions

- Used **in-memory storage** (`dict`) for simplicity.
- Separated concerns:
  - `main.py` for routes.
  - `utils.py` for helpers (validation + code gen).
  - `models.py` reserved for future DB.
- Testing done with **pytest** in `tests/`.

---

##  Error Handling

- Invalid URL → 400 Bad Request
- Missing field → 400 Bad Request
- Unknown short code → 404 Not Found
- Repeated short code → auto-resolved

---

##  Tests Written (5)

1. Health check
2. Valid URL shortening
3. Invalid URL handling
4. Redirection
5. Stats fetching


##  AI Usage Disclosure
 # Used ChatGPT-4 to:

1. Draft code structure
2. Validate Flask idioms
3. Review test coverage
4. modified or rejected some of the code snippents provided for the     chatgpt as they are depreciated (like: replaced datetime.utcnow() is deprecated... with from datetime import datetime, timezone
datetime.now(timezone.utc).isoformat())

``` python -m flask --app app.main run```

All pass ✅ with:
```bash
pytest




## Steps by step implementation


---

### 1.  Initial Setup

1. Set up project with Python 3.8+ and Flask.
2. Verified `/` and `/api/health` endpoints work.
3. Ran pre-existing test via `pytest` – passed.

---

### 2.  Shorten URL Endpoint

4. Created `POST /api/shorten` to accept and shorten long URLs.
5. Validated URL using `is_valid_url()` in `utils.py`.
6. Generated 6-char alphanumeric code via `generate_short_code()`.
7. Ensured code uniqueness by checking `url_db` collisions.
8. Stored mapping in in-memory `url_db` with timestamp and click count.

---

### 3.  Redirect Endpoint

9. Created `GET /<short_code>` to redirect to original URL.
10. Incremented click count on each redirect.
11. Handled missing short codes with `abort(404)`.

---

### 4.  Stats Endpoint

12. Built `GET /api/stats/<short_code>` to return URL, clicks, and created timestamp.
13. Returned 404 if short code was not found.

---

### 5.  Error Handling

14. Returned 400 for missing or invalid URLs.
15. Returned 404 for nonexistent short codes in both redirect and stats.
16. Used `jsonify()` for consistent error responses.

---

### 6.  Testing

17. Added 4 new test cases for shorten, redirect, stats, and error flows.
18. All 5 tests passed via `pytest`.
19. Used Flask test client fixture to isolate test environment.

---

### 7.  Architecture & Utilities

20. Used in-memory `url_db` dictionary for fast access.
21. Utility file `utils.py` houses reusable functions.
22. Time stored using `datetime.utcnow().isoformat()`.

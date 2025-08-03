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

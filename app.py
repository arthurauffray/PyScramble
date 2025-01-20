# app.py

import re
import logging
import functools
import flask
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from pyscramble.unscrambler import PyScramble

# ------------------------------------------------------------------------------
# Logging Configuration
# ------------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    filename='pyscramble/data/logs/app.log',
)
logger = logging.getLogger(__name__)

# ------------------------------------------------------------------------------
# Flask & PyScramble Setup
# ------------------------------------------------------------------------------
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JSON_SORT_KEYS'] = False

pyscramble = PyScramble()

# ------------------------------------------------------------------------------
# Rate Limiting
# #TODO upgrade to proper storage for prod
# ------------------------------------------------------------------------------
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per hour"]  # global default; adjust as needed
)

# ------------------------------------------------------------------------------
# Content length check
# ------------------------------------------------------------------------------
def check_content_length(max_content_length):
    def wrapper(fn):
        @functools.wraps(fn)
        def decorated_view(*args, **kwargs):
            if int(flask.request.headers.get('Content-Length') or 0) > max_content_length:
                return flask.abort(400, description='Content-Length is too large.')
            else:
                return fn(*args, **kwargs)
        return decorated_view
    return wrapper

# ------------------------------------------------------------------------------
# Helper Function: Validate letters
# ------------------------------------------------------------------------------
def validate_letters(letters: str) -> tuple[bool, str]:
    """
    Validates the letters parameter:
      - Must only contain alphabetic characters
      - Must be no longer than 50 characters
    Returns a tuple (is_valid, error_message).
    """
    if not re.match(r"^[A-Za-z]+$", letters):
        return False, "Invalid input. Only alphabetic letters are allowed."
    if len(letters) > 50:
        return False, "Input too large. Maximum length is 50 letters."
    return True, ""

# ------------------------------------------------------------------------------
# /unscramble Route
# ------------------------------------------------------------------------------
@app.route("/unscramble", methods=["GET", "POST"])
@limiter.limit("10/minute")  # endpoint-specific rate limit
@check_content_length(75) # limit content length to 75 bytes
def unscramble_endpoint():
    """
    GET /unscramble?letters=abcxyz
    or
    POST /unscramble
    {
      "letters": "abcxyz"
    }

    Returns JSON { "results": [...] } or { "error": ... }
    """
    try:
        if request.method == "POST":
            # Attempt to parse JSON body
            data = request.get_json(force=True, silent=True)
            if not data or "letters" not in data:
                return jsonify({"status": "error", "message": "Missing or invalid 'letters' parameter."}), 400
            letters = data["letters"]
        else:
            # GET request: read letters from the query string
            letters = request.args.get("letters", "").strip()
            if not letters:
                return jsonify({"status": "error", "message": "Missing 'letters' query parameter."}), 400

        # Validate input
        valid, error_msg = validate_letters(letters)
        if not valid:
            return jsonify({"status": "error", "message": error_msg}), 400

        # Call the unscramble function
        results = pyscramble.unscramble(scrambled_string=letters)

        return jsonify({"status": "ok", "message": results}), 200

    except Exception as err:
        # Log the error; do not expose internal info in production
        logger.error("Exception in unscramble_endpoint: %s", str(err), exc_info=True)
        return jsonify({"status": "error", "message": "An internal error occurred. Please try again later."}), 500

# ------------------------------------------------------------------------------
# Home & Ping Route
# ------------------------------------------------------------------------------
@app.route("/ping", methods=["GET", "HEAD"])
@limiter.limit("10/minute")  # endpoint-specific rate limit
@check_content_length(5) # limit content length to 5 bytes (post?)
def ping():
    """
    GET /ping

    Returns a simple 200 response for health checks.
    """
    return jsonify({"status": "ok", "message":"Pong!"}), 200

@app.route("/", methods=["GET"])
@limiter.limit("10/minute")  # endpoint-specific rate limit
@check_content_length(19) # limit content length to 5 bytes (post?)
def home():
    """
    GET /

    Returns a simple 200 response.
    """
    return jsonify({"status": "ok"}), 200

# ------------------------------------------------------------------------------
# Production Run (Gunicorn / uWSGI)
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # In prod, run via gunicorn/uwsgi, e.g.:
    #   gunicorn --bind 0.0.0.0:5000 app:app
    app.run(debug=True, host="0.0.0.0", port=8080)

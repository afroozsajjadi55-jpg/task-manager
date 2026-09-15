import os

from flask import Flask, send_from_directory


# =========================================
# APP
# =========================================

app = Flask(__name__)


# =========================================
# PATH
# =========================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


# =========================================
# WEBSITE
# =========================================

@app.route("/")
def home():

    return send_from_directory(
        BASE_DIR,
        "index.html"
    )


@app.route("/<path:filename>")
def website_files(filename):

    return send_from_directory(
        BASE_DIR,
        filename
    )


# =========================================
# HEALTH CHECK
# =========================================

@app.route("/health")
def health():

    return {
        "status": "ok"
    }


# =========================================
# RUN
# =========================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
    

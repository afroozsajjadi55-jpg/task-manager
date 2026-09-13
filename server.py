import os

from flask import (
    Flask,
    request,
    jsonify,
    session,
    send_from_directory
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from supabase import create_client
from dotenv import load_dotenv


# =========================================
# ENV
# =========================================

load_dotenv()


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")


if not SUPABASE_URL:
    raise RuntimeError(
        "SUPABASE_URL is missing from .env"
    )


if not SUPABASE_KEY:
    raise RuntimeError(
        "SUPABASE_KEY is missing from .env"
    )


if not SECRET_KEY:
    raise RuntimeError(
        "SECRET_KEY is missing from .env"
    )


# =========================================
# APP
# =========================================

app = Flask(__name__)

app.secret_key = SECRET_KEY

app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

# روی localhost لازم نیست Secure باشد.
# وقتی سایت را HTTPS آنلاین کردیم، True می‌کنیم.
app.config["SESSION_COOKIE_SECURE"] = (
    os.getenv("HTTPS_ENABLED", "0") == "1"
)


# =========================================
# PATH
# =========================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


# =========================================
# SUPABASE
# =========================================

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
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
# SIGN UP
# =========================================

@app.route(
    "/api/signup",
    methods=["POST"]
)
def signup():

    data = request.get_json(
        silent=True
    ) or {}


    email = (
        data.get("email", "")
        .strip()
        .lower()
    )


    password = data.get(
        "password",
        ""
    )


    if not email or not password:

        return jsonify({
            "success": False,
            "message":
                "Email and password are required."
        }), 400


    if len(password) < 6:

        return jsonify({
            "success": False,
            "message":
                "Password must be at least 6 characters."
        }), 400


    # Check duplicate email

    result = (
        supabase
        .table("users")
        .select("id")
        .eq("email", email)
        .limit(1)
        .execute()
    )


    if result.data:

        return jsonify({
            "success": False,
            "message":
                "An account with this email already exists."
        }), 409


    # Hash password

    password_hash = generate_password_hash(
        password
    )


    # Create user

    result = (
        supabase
        .table("users")
        .insert({
            "email": email,
            "password_hash": password_hash,
            "premium": False,
            "plan": None
        })
        .execute()
    )


    if not result.data:

        return jsonify({
            "success": False,
            "message":
                "Could not create account."
        }), 500


    user = result.data[0]


    # Create login session

    session["user_id"] = user["id"]


    return jsonify({
        "success": True,
        "message":
            "Account created successfully."
    })


# =========================================
# LOGIN
# =========================================

@app.route(
    "/api/login",
    methods=["POST"]
)
def login():

    data = request.get_json(
        silent=True
    ) or {}


    email = (
        data.get("email", "")
        .strip()
        .lower()
    )


    password = data.get(
        "password",
        ""
    )


    if not email or not password:

        return jsonify({
            "success": False,
            "message":
                "Email and password are required."
        }), 400


    result = (
        supabase
        .table("users")
        .select("*")
        .eq("email", email)
        .limit(1)
        .execute()
    )


    if not result.data:

        return jsonify({
            "success": False,
            "message":
                "Incorrect email or password."
        }), 401


    user = result.data[0]


    if not check_password_hash(
        user["password_hash"],
        password
    ):

        return jsonify({
            "success": False,
            "message":
                "Incorrect email or password."
        }), 401


    session.clear()

    session["user_id"] = user["id"]


    return jsonify({
        "success": True,
        "message":
            "Login successful."
    })


# =========================================
# CURRENT USER
# =========================================

@app.route("/api/me")
def current_user():

    user_id = session.get(
        "user_id"
    )


    if not user_id:

        return jsonify({
            "logged_in": False
        })


    result = (
        supabase
        .table("users")
        .select(
            "id,email,premium,plan"
        )
        .eq("id", user_id)
        .limit(1)
        .execute()
    )


    if not result.data:

        session.clear()

        return jsonify({
            "logged_in": False
        })


    user = result.data[0]


    return jsonify({

        "logged_in": True,

        "user": {
            "id": user["id"],
            "email": user["email"],
            "premium": bool(
                user["premium"]
            ),
            "plan": user["plan"]
        }

    })


# =========================================
# LOGOUT
# =========================================

@app.route(
    "/api/logout",
    methods=["POST"]
)
def logout():

    session.clear()


    return jsonify({
        "success": True,
        "message": "Logged out."
    })


# =========================================
# PREMIUM
# =========================================

@app.route(
    "/api/upgrade",
    methods=["POST"]
)
def upgrade():

    user_id = session.get(
        "user_id"
    )


    if not user_id:

        return jsonify({
            "success": False,
            "message":
                "Please sign in first."
        }), 401


    data = request.get_json(
        silent=True
    ) or {}


    plan = (
        data.get(
            "plan",
            "monthly"
        )
        .strip()
        .lower()
    )


    if plan not in (
        "monthly",
        "yearly"
    ):

        return jsonify({
            "success": False,
            "message":
                "Invalid plan."
        }), 400


    # -------------------------------------
    # DEMO PREMIUM
    # -------------------------------------
    #
    # هنوز پرداخت واقعی وصل نشده.
    # فعلاً Premium را برای تست فعال می‌کنیم.
    #

    result = (
        supabase
        .table("users")
        .update({
            "premium": True,
            "plan": plan
        })
        .eq("id", user_id)
        .execute()
    )


    if not result.data:

        return jsonify({
            "success": False,
            "message":
                "Could not activate Premium."
        }), 500


    # Save purchase record

    purchase_result = (
        supabase
        .table("purchases")
        .insert({
            "user_id": user_id,
            "plan": plan,
            "status": "demo_active"
        })
        .execute()
    )


    if not purchase_result.data:

        return jsonify({
            "success": False,
            "message":
                "Premium was activated, but purchase record failed."
        }), 500


    return jsonify({
        "success": True,
        "message":
            "Premium activated successfully.",
        "plan": plan
    })


# =========================================
# HEALTH CHECK
# =========================================

@app.route("/health")
def health():

    return jsonify({
        "status": "ok"
    })


# =========================================
# RUN
# =========================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
    
import os
import re
import sqlite3
import hashlib
import hmac
import secrets
from pathlib import Path

def get_data_dir():
    base = Path(os.environ.get("APPDATA", Path.home() / ".local" / "share"))
    folder = base / "STARCORE"
    folder.mkdir(parents=True, exist_ok=True)
    if os.name != "nt":
        folder.chmod(0o700)
    return folder

DB_PATH = get_data_dir() / "accounts.db"
ITERATIONS = 600_000

def connect():
    db = sqlite3.connect(DB_PATH)
    db.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            username_key TEXT PRIMARY KEY,
            username TEXT NOT NULL,
            salt BLOB NOT NULL,
            password_hash BLOB NOT NULL
        )
    """)
    return db

def create_account(username, password):
    username = username.strip()

    if not 3 <= len(username) <= 24:
        raise ValueError("Username must be 3 to 24 characters.")

    if not re.fullmatch(r"[\w.-]+", username, re.UNICODE):
        raise ValueError("Username contains invalid characters.")

    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters.")

    salt = secrets.token_bytes(16)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, ITERATIONS
    )

    try:
        with connect() as db:
            db.execute(
                "INSERT INTO accounts VALUES (?, ?, ?, ?)",
                (username.casefold(), username, salt, password_hash)
            )
    except sqlite3.IntegrityError:
        raise ValueError("Username already exists.")

    if os.name != "nt":
        DB_PATH.chmod(0o600)

    return True

def verify_login(username, password):
    with connect() as db:
        row = db.execute(
            "SELECT salt, password_hash FROM accounts WHERE username_key = ?",
            (username.strip().casefold(),)
        ).fetchone()

    if row is None:
        return False

    salt, saved_hash = row
    entered_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, ITERATIONS
    )

    return hmac.compare_digest(saved_hash, entered_hash)

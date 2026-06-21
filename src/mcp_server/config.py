import os
import json
from dotenv import load_dotenv

load_dotenv()

# ------------------------------------------------------------
# Calibre container configuration
# ------------------------------------------------------------

CALIBRE_CONTAINER = os.getenv("CALIBRE_CONTAINER_NAME", "calibre")
LIBRARY_BASE_PATH = os.getenv("CALIBRE_LIBRARY_BASE_PATH", "/")

# ------------------------------------------------------------
# Load dynamic user registry
# ------------------------------------------------------------

USERS_FILE = os.path.join(os.path.dirname(__file__), "users.json")

with open(USERS_FILE, "r") as f:
    USER_REGISTRY = json.load(f)


def resolve_user_config():
    """
    Resolves environment variables for API keys and Kindle emails.
    Returns a dict:
    {
        "sam": {
            "api_key": "...",
            "library_path": "...",
            "kindle_email": "..."
        },
        ...
    }
    """
    resolved = {}

    for username, entry in USER_REGISTRY.items():
        api_key = os.getenv(entry["api_key_env"])
        kindle_email = os.getenv(entry.get("kindle_email_env", ""))

        resolved[username] = {
            "api_key": api_key,
            "library_path": entry["library_path"],
            "kindle_email": kindle_email,
        }

    return resolved


USERS = resolve_user_config()

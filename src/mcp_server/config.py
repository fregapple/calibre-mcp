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
    resolved = {}

    for username, entry in USER_REGISTRY.items():
        resolved[username] = {
            "api_key": os.getenv(entry["api_key_env"]),
            "library_path": os.getenv(entry["library_path_env"]),
            "ereader_type": entry.get("ereader_type", "unknown"),

            "enable_send_to_kindle": entry.get("enable_send_to_kindle", False),
            "enable_koreader_push": entry.get("enable_koreader_push", False),

            "kindle_email": os.getenv(entry.get("kindle_email_env", "")),

            "koreader_host": entry.get("koreader_host"),
            "koreader_port": entry.get("koreader_port")
        }

    return resolved

from typing import Dict, Optional
from .config import USERS


class UnknownAPIKeyError(Exception):
    pass


def get_user_from_key(api_key: str) -> Dict[str, str]:
    """
    Returns full user info based on API key.
    Includes library path, device type, and delivery capabilities.
    """
    for username, data in USERS.items():
        if data["api_key"] == api_key:
            return {
                "user": username,
                "library_path": data["library_path"],
                "ereader_type": data.get("ereader_type"),

                # Delivery capabilities
                "enable_send_to_kindle": data.get("enable_send_to_kindle", False),
                "enable_koreader_push": data.get("enable_koreader_push", False),

                # Device-specific config
                "kindle_email": data.get("kindle_email"),
                "koreader_host": data.get("koreader_host"),
                "koreader_port": data.get("koreader_port"),
            }

    raise UnknownAPIKeyError(f"Invalid API key: {api_key}")


def get_library_from_key(api_key: str) -> str:
    return get_user_from_key(api_key)["library_path"]


def get_kindle_email_from_key(api_key: str) -> Optional[str]:
    return get_user_from_key(api_key).get("kindle_email")

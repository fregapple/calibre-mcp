from typing import Dict, Optional
from .config import USERS


class UnknownAPIKeyError(Exception):
    pass


def get_user_from_key(api_key: str) -> Dict[str, str]:
    """
    Returns user info based on API key.
    """
    for username, data in USERS.items():
        if data["api_key"] == api_key:
            return {
                "user": username,
                "library_path": data["library_path"],
                "kindle_email": data.get("kindle_email"),
            }

    raise UnknownAPIKeyError(f"Invalid API key: {api_key}")


def get_library_from_key(api_key: str) -> str:
    return get_user_from_key(api_key)["library_path"]


def get_kindle_email_from_key(api_key: str) -> Optional[str]:
    return get_user_from_key(api_key).get("kindle_email")

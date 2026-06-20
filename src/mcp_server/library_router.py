from typing import Optional, Dict

from .config import (
    SAM_API_KEY,
    JENNA_API_KEY,
    SAM_LIBRARY,
    JENNA_LIBRARY,
    SAM_KINDLE_EMAIL,
    JENNA_KINDLE_EMAIL,
)


class UnknownAPIKeyError(Exception):
    """Raised when an API key does not match any known user."""
    pass


def get_user_from_key(api_key: str) -> Dict[str, str]:
    """
    Returns a dictionary describing the user associated with the API key.
    Includes library path and optional Kindle email.
    Raises UnknownAPIKeyError if the key is invalid.
    """

    if api_key == SAM_API_KEY:
        return {
            "user": "sam",
            "library_path": SAM_LIBRARY,
            "kindle_email": SAM_KINDLE_EMAIL,
        }

    if api_key == JENNA_API_KEY:
        return {
            "user": "jenna",
            "library_path": JENNA_LIBRARY,
            "kindle_email": JENNA_KINDLE_EMAIL,
        }

    raise UnknownAPIKeyError(f"Invalid API key: {api_key}")


def get_library_from_key(api_key: str) -> str:
    """
    Convenience wrapper: returns only the library path.
    """
    return get_user_from_key(api_key)["library_path"]


def get_kindle_email_from_key(api_key: str) -> Optional[str]:
    """
    Convenience wrapper: returns the user's Kindle email (if configured).
    """
    return get_user_from_key(api_key).get("kindle_email")

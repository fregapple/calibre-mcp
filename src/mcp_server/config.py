import os
from dotenv import load_dotenv
load_dotenv()


# ------------------------------------------------------------
# Calibre container configuration
# ------------------------------------------------------------

# Name of the Docker container running Calibre
CALIBRE_CONTAINER = os.getenv("CALIBRE_CONTAINER_NAME", "calibre")

# Base directory where all Calibre libraries live
# Example: /data/calibre
LIBRARY_BASE_PATH = os.getenv("CALIBRE_LIBRARY_BASE_PATH", "/data/calibre")


# ------------------------------------------------------------
# API keys for user identity → library mapping
# ------------------------------------------------------------

SAM_API_KEY = os.getenv("SAM_API_KEY")
JENNA_API_KEY = os.getenv("JENNA_API_KEY")

# Library paths derived from base path
SAM_LIBRARY = os.path.join(LIBRARY_BASE_PATH, "sam")
JENNA_LIBRARY = os.path.join(LIBRARY_BASE_PATH, "jenna")


# ------------------------------------------------------------
# Optional: Kindle email configuration (future use)
# ------------------------------------------------------------

SAM_KINDLE_EMAIL = os.getenv("SAM_KINDLE_EMAIL")
JENNA_KINDLE_EMAIL = os.getenv("JENNA_KINDLE_EMAIL")


# ------------------------------------------------------------
# Validation (optional but recommended)
# ------------------------------------------------------------

def validate_config():
    """
    Ensures required environment variables are present.
    Call this once at server startup.
    """
    missing = []

    if SAM_API_KEY is None:
        missing.append("SAM_API_KEY")

    if JENNA_API_KEY is None:
        missing.append("JENNA_API_KEY")

    if missing:
        raise RuntimeError(
            f"Missing required environment variables: {', '.join(missing)}"
        )

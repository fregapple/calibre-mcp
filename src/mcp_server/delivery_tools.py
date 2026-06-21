from typing import Dict, Any
import os
import smtplib
from email.message import EmailMessage

from .library_router import get_user_from_key
from .calibre_tools import (
    get_metadata,
    run_calibredb,
    convert_book,
)


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

def _export_book(library_path: str, book_id: str, output_dir: str = "/tmp/export") -> Dict[str, Any]:
    """
    Uses calibredb export to extract a book's files.
    Returns the export result including file paths.
    """
    return run_calibredb([
        "--with-library", library_path,
        "export", book_id,
        "--to-dir", output_dir
    ])


# ------------------------------------------------------------
# Delivery Methods
# ------------------------------------------------------------

def send_via_kindle_email(user, library_path, book_id):
    kindle_email = user.get("kindle_email")
    if not kindle_email:
        return {"status": "error", "message": "No Kindle email configured."}

    # 1. Export the book
    export_result = _export_book(library_path, book_id)
    exported_files = export_result["stdout"]

    # 2. Pick a supported format
    supported_exts = [".epub", ".pdf", ".docx", ".txt"]
    selected_file = None

    for ext in supported_exts:
        if ext in exported_files:
            selected_file = exported_files.split(ext)[0] + ext
            break

    if not selected_file:
        return {
            "status": "error",
            "message": "No Kindle-supported format found. Convert first."
        }

    # 3. Build email
    msg = EmailMessage()
    msg["Subject"] = ""
    msg["From"] = os.getenv("SMTP_FROM")
    msg["To"] = kindle_email

    with open(selected_file, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="octet-stream",
            filename=os.path.basename(selected_file)
        )

    # 4. Send email
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)

    return {
        "status": "success",
        "method": "send_to_kindle",
        "sent_to": kindle_email,
        "file": selected_file
    }


def send_via_koreader(user: Dict[str, Any], library_path: str, book_id: str) -> Dict[str, Any]:
    """
    Sends a book to KOReader.
    NOTE: This is a placeholder.
    """
    host = user.get("koreader_host")
    port = user.get("koreader_port")

    if not host or not port:
        return {"status": "error", "message": "KOReader host/port not configured."}

    # Export book
    export_result = _export_book(library_path, book_id)

    return {
        "status": "success",
        "method": "koreader_push",
        "koreader_host": host,
        "koreader_port": port,
        "export_result": export_result,
        "message": "Book exported. KOReader push not yet implemented."
    }


# ------------------------------------------------------------
# Unified Delivery Entry Point
# ------------------------------------------------------------

def send_to_device(api_key: str, book_id: str) -> Dict[str, Any]:
    """
    Main entry point for sending a book to the user's e-reader.
    Automatically selects the correct delivery method based on user config.
    """
    user = get_user_from_key(api_key)
    library_path = user["library_path"]

    # 1. Kindle email delivery
    if user.get("enable_send_to_kindle"):
        return send_via_kindle_email(user, library_path, book_id)

    # 2. KOReader push
    if user.get("enable_koreader_push"):
        return send_via_koreader(user, library_path, book_id)

    # 3. No delivery method enabled
    return {
        "status": "error",
        "message": "No delivery methods enabled for this user."
    }

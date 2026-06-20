from typing import List, Dict, Any

from .docker_exec import run_docker_command


# ------------------------------------------------------------
# Low-level wrappers around Calibre CLI tools
# ------------------------------------------------------------

def run_calibredb(args: List[str]) -> Dict[str, Any]:
    """
    Runs calibredb with the given arguments inside the Calibre container.
    """
    return run_docker_command(["calibredb"] + args)


def run_ebook_meta(args: List[str]) -> Dict[str, Any]:
    """
    Runs ebook-meta with the given arguments inside the Calibre container.
    """
    return run_docker_command(["ebook-meta"] + args)


def run_ebook_convert(args: List[str]) -> Dict[str, Any]:
    """
    Runs ebook-convert with the given arguments inside the Calibre container.
    """
    return run_docker_command(["ebook-convert"] + args)


# ------------------------------------------------------------
# High-level Calibre operations
# ------------------------------------------------------------

def import_book_to_library(library_path: str, file_path: str) -> Dict[str, Any]:
    """
    Imports a book into the specified Calibre library.
    """
    return run_calibredb([
        "--with-library", library_path,
        "add", file_path
    ])


def search_library(library_path: str, query: str) -> Dict[str, Any]:
    """
    Searches the library using calibredb list.
    """
    return run_calibredb([
        "--with-library", library_path,
        "list",
        "--search", query,
        "--fields", "id,title,authors,formats"
    ])


def get_metadata(library_path: str, book_id: str) -> Dict[str, Any]:
    """
    Retrieves metadata for a specific book.
    """
    return run_calibredb([
        "--with-library", library_path,
        "show_metadata", book_id
    ])


def set_metadata(library_path: str, book_id: str, opf_path: str) -> Dict[str, Any]:
    """
    Sets metadata for a book using an OPF file.
    """
    return run_calibredb([
        "--with-library", library_path,
        "set_metadata", book_id, opf_path
    ])


def convert_book(input_path: str, output_path: str) -> Dict[str, Any]:
    """
    Converts a book from one format to another.
    """
    return run_ebook_convert([input_path, output_path])

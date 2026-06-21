from mcp.server.fastmcp import FastMCP

from src.mcp_server.library_router import get_library_from_key, UnknownAPIKeyError
from src.mcp_server.calibre_tools import (
    import_book_to_library,
    search_library,
    get_metadata,
    set_metadata,
    convert_book,
)
from src.mcp_server.delivery_tools import send_to_device


# -----------------------------
# MCP SERVER
# -----------------------------
mcp = FastMCP(
    "calibre-mcp",
    stateless_http=True,
    json_response=True,
    host="0.0.0.0",
    port=8002
)

# -----------------------------
# TOOLS
# -----------------------------
@mcp.tool(description="Import a book file into the user's Calibre library.")
def import_book(api_key: str, file_path: str):
    try:
        library = get_library_from_key(api_key)
    except UnknownAPIKeyError as e:
        return {"status": "error", "message": str(e)}

    result = import_book_to_library(library, file_path)
    return {"status": "success", "result": result}


@mcp.tool(description="Search for books in the user's Calibre library.")
def search_books(api_key: str, query: str):
    try:
        library = get_library_from_key(api_key)
    except UnknownAPIKeyError as e:
        return {"status": "error", "message": str(e)}

    result = search_library(library, query)
    return {"status": "success", "result": result}


@mcp.tool(description="Retrieve metadata for a specific book.")
def get_book_metadata(api_key: str, book_id: str):
    try:
        library = get_library_from_key(api_key)
    except UnknownAPIKeyError as e:
        return {"status": "error", "message": str(e)}

    result = get_metadata(library, book_id)
    return {"status": "success", "result": result}


@mcp.tool(description="Update metadata for a book using an OPF file.")
def update_book_metadata(api_key: str, book_id: str, opf_path: str):
    try:
        library = get_library_from_key(api_key)
    except UnknownAPIKeyError as e:
        return {"status": "error", "message": str(e)}

    result = set_metadata(library, book_id, opf_path)
    return {"status": "success", "result": result}


@mcp.tool(description="Convert a book from one format to another.")
def convert_format(api_key: str, input_path: str, output_path: str):
    try:
        # Only validates identity
        get_library_from_key(api_key)
    except UnknownAPIKeyError as e:
        return {"status": "error", "message": str(e)}

    result = convert_book(input_path, output_path)
    return {"status": "success", "result": result}


@mcp.tool(description="Send a book to the user's e-reader.")
def send_book(api_key: str, book_id: str):
    try:
        return send_to_device(api_key, book_id)
    except UnknownAPIKeyError as e:
        return {"status": "error", "message": str(e)}


# -----------------------------
# ENTRY POINT
# -----------------------------
if __name__ == "__main__":
    mcp.run(transport="streamable-http")

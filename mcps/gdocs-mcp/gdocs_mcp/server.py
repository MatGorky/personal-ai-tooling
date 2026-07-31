"""
A minimal MCP server exposing read and write access to Google Docs.

It authenticates with a Google service account (the same key you already use
for Sheets) and exposes these tools:

  - read_doc(doc): return the full plain text of a document
  - get_doc_info(doc): return the document's title and id
  - append_text(doc, text): append text to the end of a document
  - insert_text(doc, text, index): insert text at a specific character index
  - replace_document(doc, text): replace the entire body with new text
  - replace_all_text(doc, find, replace): swap all occurrences of a string
  - format_text(doc, targets, ...): style occurrences of text (bold, italic,
    size, font family, color)
  - style_paragraphs(doc, targets, ...): paragraph spacing, line spacing,
    alignment, and bottom-border rules
  - bullet_paragraphs(doc, prefix): turn plain "- " list lines into real bullets
  - set_base_font(doc, font_family, font_size): font for the whole body
  - set_document_style(doc, ...): page margins

`doc` may be either a bare document id or a full Google Docs URL.

The service account can only open documents that are public or explicitly
shared with its email (the `client_email` in the key file). For writing, the
document must be shared with the service account as an Editor.
"""

import os
import re

from google.oauth2 import service_account
from googleapiclient.discovery import build
from mcp.server.fastmcp import FastMCP

# Full documents scope: covers both reading and writing.
SCOPES = ["https://www.googleapis.com/auth/documents"]

mcp = FastMCP("gdocs")

# The Docs service is built lazily and cached so we authenticate only once,
# not on every tool call.
_service = None


def _get_service():
    global _service
    if _service is None:
        key_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        if not key_path:
            raise RuntimeError(
                "GOOGLE_APPLICATION_CREDENTIALS is not set; point it at the "
                "service-account JSON key."
            )
        creds = service_account.Credentials.from_service_account_file(
            key_path, scopes=SCOPES
        )
        _service = build("docs", "v1", credentials=creds, cache_discovery=False)
    return _service


def _extract_doc_id(doc):
    """Accept a bare id or any Google Docs URL and return the document id."""
    m = re.search(r"/document/d/([a-zA-Z0-9_-]+)", doc)
    if m:
        return m.group(1)
    # Otherwise assume the caller already passed a bare id.
    return doc.strip()


def _hex_to_rgb(hex_color):
    """Convert '#RRGGBB' (or '#RGB') to a Docs API rgbColor dict."""
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return {
        "red": int(h[0:2], 16) / 255.0,
        "green": int(h[2:4], 16) / 255.0,
        "blue": int(h[4:6], 16) / 255.0,
    }


def _text_from_elements(elements):
    """Concatenate the text runs inside a paragraph's elements."""
    out = []
    for el in elements:
        text_run = el.get("textRun")
        if text_run:
            out.append(text_run.get("content", ""))
    return "".join(out)


def _text_from_content(content):
    """Recursively flatten a list of structural elements into plain text.

    Handles paragraphs and tables (tables recurse into their cells); other
    structural elements contribute no text. Bulleted paragraphs are prefixed
    with "- " (indented two spaces per nesting level) so list structure
    survives the plain-text round trip.
    """
    parts = []
    for element in content:
        if "paragraph" in element:
            paragraph = element["paragraph"]
            text = _text_from_elements(paragraph.get("elements", []))
            if "bullet" in paragraph and text.strip():
                level = paragraph["bullet"].get("nestingLevel", 0)
                text = "  " * level + "- " + text
            parts.append(text)
        elif "table" in element:
            for row in element["table"].get("tableRows", []):
                cells = [
                    _text_from_content(cell.get("content", [])).strip()
                    for cell in row.get("tableCells", [])
                ]
                parts.append("\t".join(cells) + "\n")
    return "".join(parts)


@mcp.tool()
def read_doc(doc: str) -> str:
    """Return the full plain text of a Google Doc.

    Args:
        doc: A Google Docs document id or full document URL.
    """
    doc_id = _extract_doc_id(doc)
    document = _get_service().documents().get(documentId=doc_id).execute()
    body = document.get("body", {}).get("content", [])
    return _text_from_content(body).rstrip("\n")


@mcp.tool()
def get_doc_info(doc: str) -> dict:
    """Return basic metadata (title and id) for a Google Doc.

    Args:
        doc: A Google Docs document id or full document URL.
    """
    doc_id = _extract_doc_id(doc)
    document = _get_service().documents().get(documentId=doc_id).execute()
    return {
        "documentId": document.get("documentId", doc_id),
        "title": document.get("title", ""),
    }


def _end_index(document):
    """Return the last insertable character index of a document body.

    The body always ends with a trailing newline segment; the last valid
    insertion index is one before the body's reported end.
    """
    content = document.get("body", {}).get("content", [])
    end = 1
    for element in content:
        if "endIndex" in element:
            end = element["endIndex"]
    return max(1, end - 1)


@mcp.tool()
def append_text(doc: str, text: str) -> dict:
    """Append text to the end of a Google Doc.

    The document must be shared with the service account as an Editor.

    Args:
        doc: A Google Docs document id or full document URL.
        text: The text to append at the end of the document.
    """
    doc_id = _extract_doc_id(doc)
    service = _get_service()
    document = service.documents().get(documentId=doc_id).execute()
    index = _end_index(document)
    service.documents().batchUpdate(
        documentId=doc_id,
        body={"requests": [{"insertText": {"location": {"index": index}, "text": text}}]},
    ).execute()
    return {"documentId": doc_id, "insertedAt": index, "inserted": text}


@mcp.tool()
def insert_text(doc: str, text: str, index: int) -> dict:
    """Insert text at a specific character index in a Google Doc.

    The document must be shared with the service account as an Editor.

    Args:
        doc: A Google Docs document id or full document URL.
        text: The text to insert.
        index: 1-based character index at which to insert the text.
    """
    doc_id = _extract_doc_id(doc)
    service = _get_service()
    service.documents().batchUpdate(
        documentId=doc_id,
        body={"requests": [{"insertText": {"location": {"index": index}, "text": text}}]},
    ).execute()
    return {"documentId": doc_id, "insertedAt": index, "inserted": text}


def _clear_body(service, doc_id):
    """Delete all body content except the mandatory trailing newline."""
    document = service.documents().get(documentId=doc_id).execute()
    end = 1
    for element in document.get("body", {}).get("content", []):
        if "endIndex" in element:
            end = element["endIndex"]
    if end - 1 > 1:
        service.documents().batchUpdate(
            documentId=doc_id,
            body={"requests": [{"deleteContentRange": {
                "range": {"startIndex": 1, "endIndex": end - 1}}}]},
        ).execute()


@mcp.tool()
def replace_document(doc: str, text: str) -> dict:
    """Replace the entire body of a Google Doc with new text.

    Clears all existing content, then inserts `text` from the top. Use this to
    rewrite a document wholesale. The document must be shared with the service
    account as an Editor.

    Args:
        doc: A Google Docs document id or full document URL.
        text: The new full text of the document body.
    """
    doc_id = _extract_doc_id(doc)
    service = _get_service()
    _clear_body(service, doc_id)
    service.documents().batchUpdate(
        documentId=doc_id,
        body={"requests": [{"insertText": {"location": {"index": 1}, "text": text}}]},
    ).execute()
    return {"documentId": doc_id, "length": len(text)}


@mcp.tool()
def replace_all_text(doc: str, find: str, replace: str, match_case: bool = True) -> dict:
    """Replace every occurrence of `find` with `replace` in a Google Doc.

    Args:
        doc: A Google Docs document id or full document URL.
        find: The exact text to search for.
        replace: The text to substitute in its place.
        match_case: Whether the search is case-sensitive (default True).
    """
    doc_id = _extract_doc_id(doc)
    service = _get_service()
    result = service.documents().batchUpdate(
        documentId=doc_id,
        body={"requests": [{"replaceAllText": {
            "containsText": {"text": find, "matchCase": match_case},
            "replaceText": replace,
        }}]},
    ).execute()
    changed = (result.get("replies", [{}]) or [{}])[0].get(
        "replaceAllText", {}).get("occurrencesChanged", 0)
    return {"documentId": doc_id, "occurrencesChanged": changed}


def _iter_text_runs(document):
    """Yield (absolute_start_index, run_text) for each text run in the body."""
    for element in document.get("body", {}).get("content", []):
        paragraph = element.get("paragraph")
        if not paragraph:
            continue
        for el in paragraph.get("elements", []):
            run = el.get("textRun")
            if run and "startIndex" in el:
                yield el["startIndex"], run.get("content", "")


@mcp.tool()
def format_text(doc: str, targets: list[str], bold: bool | None = True,
                font_size: float | None = None, italic: bool | None = None,
                font_family: str | None = None,
                foreground_color: str | None = None) -> dict:
    """Style every occurrence of each target string.

    For each string in `targets`, finds its occurrences in the document and
    styles those ranges. Matches must fall within a single text run, which is
    fine for section headings and label lines.

    Args:
        doc: A Google Docs document id or full document URL.
        targets: Exact strings to style (e.g. section headings).
        bold: True/False to set boldness, None to leave it unchanged
            (default True).
        font_size: Optional font size in points to apply.
        italic: True/False to set italics, None to leave unchanged.
        font_family: Optional font family name (e.g. "Lato").
        foreground_color: Optional text color as '#RRGGBB'.
    """
    doc_id = _extract_doc_id(doc)
    service = _get_service()
    document = service.documents().get(documentId=doc_id).execute()

    text_style = {}
    fields = []
    if bold is not None:
        text_style["bold"] = bool(bold)
        fields.append("bold")
    if italic is not None:
        text_style["italic"] = bool(italic)
        fields.append("italic")
    if font_size is not None:
        text_style["fontSize"] = {"magnitude": font_size, "unit": "PT"}
        fields.append("fontSize")
    if font_family is not None:
        text_style["weightedFontFamily"] = {"fontFamily": font_family}
        fields.append("weightedFontFamily")
    if foreground_color is not None:
        text_style["foregroundColor"] = {
            "color": {"rgbColor": _hex_to_rgb(foreground_color)}}
        fields.append("foregroundColor")
    if not fields:
        return {"documentId": doc_id, "rangesStyled": 0,
                "note": "no style properties given"}

    requests = []
    for target in targets:
        for start, content in _iter_text_runs(document):
            offset = content.find(target)
            while offset != -1:
                s = start + offset
                requests.append({"updateTextStyle": {
                    "range": {"startIndex": s, "endIndex": s + len(target)},
                    "textStyle": text_style,
                    "fields": ",".join(fields),
                }})
                offset = content.find(target, offset + 1)

    if requests:
        service.documents().batchUpdate(
            documentId=doc_id, body={"requests": requests}).execute()
    return {"documentId": doc_id, "rangesStyled": len(requests)}


def _iter_paragraphs(document):
    """Yield (start_index, end_index, text) for each paragraph in the body."""
    for element in document.get("body", {}).get("content", []):
        paragraph = element.get("paragraph")
        if paragraph and "startIndex" in element:
            text = _text_from_elements(paragraph.get("elements", []))
            yield element["startIndex"], element["endIndex"], text


@mcp.tool()
def style_paragraphs(doc: str, targets: list[str] | None = None,
                     space_above: float | None = None,
                     space_below: float | None = None,
                     line_spacing: float | None = None,
                     alignment: str | None = None,
                     border_bottom: bool = False,
                     border_color: str = "#666666",
                     border_width: float = 0.75) -> dict:
    """Style whole paragraphs: spacing, line spacing, alignment, bottom rule.

    Args:
        doc: A Google Docs document id or full document URL.
        targets: Paragraphs whose stripped text exactly matches one of these
            strings are styled. None (default) styles the entire document.
        space_above: Extra space before the paragraph, in points.
        space_below: Extra space after the paragraph, in points.
        line_spacing: Line spacing as a percentage (100 = single, 115 = 1.15x).
        alignment: One of START, CENTER, END, JUSTIFIED.
        border_bottom: Draw a horizontal rule under the paragraph.
        border_color: Rule color as '#RRGGBB' (default gray).
        border_width: Rule thickness in points.
    """
    doc_id = _extract_doc_id(doc)
    service = _get_service()
    document = service.documents().get(documentId=doc_id).execute()

    style = {}
    fields = []
    if space_above is not None:
        style["spaceAbove"] = {"magnitude": space_above, "unit": "PT"}
        fields.append("spaceAbove")
    if space_below is not None:
        style["spaceBelow"] = {"magnitude": space_below, "unit": "PT"}
        fields.append("spaceBelow")
    if line_spacing is not None:
        style["lineSpacing"] = line_spacing
        fields.append("lineSpacing")
    if alignment is not None:
        style["alignment"] = alignment
        fields.append("alignment")
    if border_bottom:
        style["borderBottom"] = {
            "color": {"color": {"rgbColor": _hex_to_rgb(border_color)}},
            "width": {"magnitude": border_width, "unit": "PT"},
            "padding": {"magnitude": 2, "unit": "PT"},
            "dashStyle": "SOLID",
        }
        fields.append("borderBottom")
    if not fields:
        return {"documentId": doc_id, "paragraphsStyled": 0,
                "note": "no style properties given"}

    requests = []
    if targets:
        wanted = {t.strip() for t in targets}
        for start, end, text in _iter_paragraphs(document):
            if text.strip() in wanted:
                requests.append({"updateParagraphStyle": {
                    "range": {"startIndex": start, "endIndex": end},
                    "paragraphStyle": style,
                    "fields": ",".join(fields),
                }})
    else:
        end = _end_index(document)
        if end > 1:
            requests.append({"updateParagraphStyle": {
                "range": {"startIndex": 1, "endIndex": end},
                "paragraphStyle": style,
                "fields": ",".join(fields),
            }})

    if requests:
        service.documents().batchUpdate(
            documentId=doc_id, body={"requests": requests}).execute()
    return {"documentId": doc_id, "paragraphsStyled": len(requests)}


@mcp.tool()
def bullet_paragraphs(doc: str, prefix: str = "- ",
                      preset: str = "BULLET_DISC_CIRCLE_SQUARE") -> dict:
    """Convert plain-text list lines into real Google Docs bullets.

    Finds paragraphs that begin with `prefix` (ignoring leading whitespace),
    strips the whitespace and prefix, and applies a bullet preset. All bullets
    end up at the top nesting level.

    Args:
        doc: A Google Docs document id or full document URL.
        prefix: The literal marker that starts a list line (default "- ").
        preset: A Docs API bullet preset name.
    """
    doc_id = _extract_doc_id(doc)
    service = _get_service()
    document = service.documents().get(documentId=doc_id).execute()

    found = []
    for start, end, text in _iter_paragraphs(document):
        stripped = text.lstrip()
        if stripped.startswith(prefix) and len(stripped.rstrip("\n")) > len(prefix):
            cut = (len(text) - len(stripped)) + len(prefix)
            found.append((start, end, cut))

    # Work backward through the document so the index shifts from deleting
    # prefixes never affect ranges that are still pending.
    requests = []
    for start, end, cut in reversed(found):
        requests.append({"createParagraphBullets": {
            "range": {"startIndex": start, "endIndex": max(start + 1, end - 1)},
            "bulletPreset": preset,
        }})
        requests.append({"deleteContentRange": {
            "range": {"startIndex": start, "endIndex": start + cut},
        }})

    if requests:
        service.documents().batchUpdate(
            documentId=doc_id, body={"requests": requests}).execute()
    return {"documentId": doc_id, "bulleted": len(found)}


@mcp.tool()
def set_base_font(doc: str, font_family: str,
                  font_size: float | None = None) -> dict:
    """Apply a font family (and optional size) to the entire document body.

    Args:
        doc: A Google Docs document id or full document URL.
        font_family: Font family name as shown in Docs (e.g. "Lato").
        font_size: Optional size in points for all body text.
    """
    doc_id = _extract_doc_id(doc)
    service = _get_service()
    document = service.documents().get(documentId=doc_id).execute()

    text_style = {"weightedFontFamily": {"fontFamily": font_family}}
    fields = ["weightedFontFamily"]
    if font_size is not None:
        text_style["fontSize"] = {"magnitude": font_size, "unit": "PT"}
        fields.append("fontSize")

    end = _end_index(document)
    if end > 1:
        service.documents().batchUpdate(
            documentId=doc_id,
            body={"requests": [{"updateTextStyle": {
                "range": {"startIndex": 1, "endIndex": end},
                "textStyle": text_style,
                "fields": ",".join(fields),
            }}]},
        ).execute()
    return {"documentId": doc_id, "fontFamily": font_family,
            "fontSize": font_size}


@mcp.tool()
def set_document_style(doc: str, margin_top: float | None = None,
                       margin_bottom: float | None = None,
                       margin_left: float | None = None,
                       margin_right: float | None = None) -> dict:
    """Set page margins, in points (72 pt = 1 inch).

    Args:
        doc: A Google Docs document id or full document URL.
        margin_top: Top margin in points.
        margin_bottom: Bottom margin in points.
        margin_left: Left margin in points.
        margin_right: Right margin in points.
    """
    doc_id = _extract_doc_id(doc)
    service = _get_service()

    style = {}
    fields = []
    for name, value in (("marginTop", margin_top),
                        ("marginBottom", margin_bottom),
                        ("marginLeft", margin_left),
                        ("marginRight", margin_right)):
        if value is not None:
            style[name] = {"magnitude": value, "unit": "PT"}
            fields.append(name)
    if not fields:
        return {"documentId": doc_id, "note": "no margins given"}

    service.documents().batchUpdate(
        documentId=doc_id,
        body={"requests": [{"updateDocumentStyle": {
            "documentStyle": style,
            "fields": ",".join(fields),
        }}]},
    ).execute()
    return {"documentId": doc_id, "marginsSet": fields}


def main():
    mcp.run()


if __name__ == "__main__":
    main()

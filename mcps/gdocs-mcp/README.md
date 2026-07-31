# gdocs-mcp

A minimal [Model Context Protocol](https://modelcontextprotocol.io) server exposing
read/write/format access to Google Docs, authenticated with a Google **service account**
(no interactive OAuth). Built on `FastMCP`.

## Tools

| Tool | Description |
| --- | --- |
| `read_doc(doc)` | Full plain text of a document (handles paragraphs and tables; bulleted paragraphs come back prefixed with `- ` so lists survive the round trip). |
| `get_doc_info(doc)` | Title and id. |
| `append_text(doc, text)` | Append to the end. |
| `insert_text(doc, text, index)` | Insert at a character index. |
| `replace_document(doc, text)` | Replace the entire body. |
| `replace_all_text(doc, find, replace)` | Swap all occurrences of a string. |
| `format_text(doc, targets, …)` | Style every occurrence of each target string: bold, italic, size, font family, color. |
| `style_paragraphs(doc, targets, …)` | Paragraph spacing, line spacing, alignment, bottom-border rules. Omit `targets` to style the whole document. |
| `bullet_paragraphs(doc, prefix)` | Convert plain `"- "` list lines into real bullets. |
| `set_base_font(doc, font_family, font_size)` | Font family/size for the entire body. |
| `set_document_style(doc, margins…)` | Page margins. |

`doc` may be a bare document id or a full Google Docs URL.

## Auth & scopes

Authenticates via the service-account key at `$GOOGLE_APPLICATION_CREDENTIALS`. The
service account can only open documents that are **public or explicitly shared with its
email** (Editor access is required for writes).

Current scope: `https://www.googleapis.com/auth/documents` (Docs only).

## Roadmap

- [ ] Add Google **Drive** tools: `create_doc`, `find_doc_by_name`, `duplicate_doc`
- [ ] Scope Drive access with least privilege (`drive.file` + a metadata-search scope
      rather than full `drive`)

## Run

```bash
uv sync
GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json uv run -m gdocs_mcp
```

Or wire it into an MCP client (`.mcp.json`):

```json
{
  "mcpServers": {
    "gdocs": {
      "command": "uv",
      "args": ["--directory", "/path/to/gdocs-mcp", "run", "-m", "gdocs_mcp"],
      "env": { "GOOGLE_APPLICATION_CREDENTIALS": "/path/to/key.json" }
    }
  }
}
```

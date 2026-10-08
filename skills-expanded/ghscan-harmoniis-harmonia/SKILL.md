# Search (Brave) -- Skill/MCP Definition

## Tool Name: `search_brave`

## Description

Web search via Brave Search API. Returns structured search results with titles, URLs, and descriptions. Good for general web search with privacy-focused indexing.

## Input Schema

```json
{
  "type": "object",
  "properties": {
    "query": {
      "type": "string",
      "description": "Search query text"
    },
    "count": {
      "type": "integer",
      "default": 10,
      "description": "Number of results to return"
    },
    "freshness": {
      "type": "string",
      "enum": ["pd", "pw", "pm", "py", ""],
      "default": "",
      "description": "Freshness filter: past day/week/month/year"
    }
  },
  "required": ["query"]
}
```

## Output Format

JSON object from Brave API containing `web.results` array:
```json
{
  "web": {
    "results": [
      {"title": "...", "url": "...", "description": "...", "age": "..."}
    ]
  }
}
```

## Vault Symbols Required

- `brave_api_key` -- Brave Search API subscription token

## FFI Entry Point

```c
char* harmonia_search_brave_query(const char* query);
```

## Example

```lisp
(tool op=search-brave query="rust async runtime comparison")
```

## Error Handling

Returns `NULL` on failure. Check `harmonia_search_brave_last_error()` for details. Common errors:
- `missing secret: brave_api_key` -- Vault not initialized or key missing
- `curl exec failed` -- Network/curl issue
- `brave query failed` -- API returned error

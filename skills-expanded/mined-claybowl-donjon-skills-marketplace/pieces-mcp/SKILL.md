# Pieces MCP Skill

Access your Pieces Long-Term Memory (LTM) through the Model Context Protocol (MCP) server.

## Overview

This skill connects to your local Pieces MCP server to query your coding activity, saved snippets, and work history stored in PiecesOS.

**Required:** PiecesOS must be running locally with the MCP server enabled.

## Configuration

The skill connects to: `http://localhost:39300/model_context_protocol/2025-03-26/mcp`

Add to your `.opencode/mcp-config.json`:
```json
{
  "mcpServers": {
    "pieces": {
      "url": "http://localhost:39300/model_context_protocol/2025-03-26/mcp"
    }
  }
}
```

## Available Tools

### ask_pieces_ltm
Query your Pieces Long-Term Memory for context about your work history.

**Parameters:**
- `query` (string): Natural language question about your activity
- `time_range` (string, optional): Time period to search (e.g., "yesterday", "last week", "February 7, 2026")

**Examples:**
- "What did I work on yesterday?"
- "Show me code snippets I saved last week"
- "What files did I edit on February 7, 2026?"
- "Summarize my coding activity from yesterday"

### list_recent_snippets
Get recently saved code snippets from Pieces.

**Parameters:**
- `limit` (number, optional): Number of snippets to return (default: 10)
- `date_filter` (string, optional): Filter by date (e.g., "2026-02-07")

### search_snippets
Search your saved code snippets.

**Parameters:**
- `query` (string): Search terms
- `language` (string, optional): Filter by programming language

## Usage Examples

**Check yesterday's activity:**
```
Ask Pieces: What did I do yesterday on February 7, 2026?
```

**Find specific code:**
```
Search Pieces for React hooks examples I saved last week
```

**Get recent work summary:**
```
Ask Pieces to summarize my coding activity from the past 3 days
```

## Troubleshooting

**"Failed to extract context" error:**
- Ensure PiecesOS is running
- Check that the MCP server is enabled in Pieces settings
- Verify the URL in mcp-config.json matches your Pieces version

**No results returned:**
- Pieces LTM requires data to be captured first
- Ensure Pieces Desktop App or IDE extension is actively saving context
- Some activity may take time to be indexed by LTM

## Resources

- [Pieces MCP Documentation](https://docs.pieces.app/products/mcp/get-started)
- [Pieces LTM Overview](https://docs.pieces.app/products/core-dependencies/pieces-os#ltm-27)
- Local MCP Endpoint: http://localhost:39300/model_context_protocol/2025-03-26/mcp

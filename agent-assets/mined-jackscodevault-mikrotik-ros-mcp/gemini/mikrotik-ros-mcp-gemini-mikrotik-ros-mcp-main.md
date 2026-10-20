# MikroTik ISP Management System Development

## Project Structure
- `mikrotik-docs-processor/`: Tools and raw data for processing documentation.
  - `mikrotik_markdown_docs/`: Cleaned Markdown documentation organized by Space (ROS, UM, SWOS, RKB).
- `mikrotik-mcp-server/`: MCP server providing access to the documentation.
  - `chroma_db/`: Vector database for semantic search.

## Documentation MCP Server
The MCP server provides semantic search over the entire MikroTik documentation. **Docker is the recommended way to run this server.**

### Docker Image: `mikrotik-docs-mcp-server`

### Integration Snippets:

#### Gemini CLI (`config.json`)
```json
"mikrotik-docs": {
  "command": "docker",
  "args": ["run", "-i", "--rm", "mikrotik-docs-mcp-server"]
}
```

#### Cursor / VS Code (MCP Settings)
- **Type:** `command`
- **Command:** `docker`
- **Arguments:** `run`, `-i`, `--rm`, `mikrotik-docs-mcp-server`

### Tools:
- `search_docs(query: str, n_results: int = 5)`: Perform a vector search for a given query.
- `read_doc(path: str)`: Read the full content of a specific document.
- `list_spaces()`: List available documentation spaces (ROS, UM, SWOS, etc.).

## Development Agent Instructions
- **Priority:** Always use the Docker-based MCP server if available.
- Always search the documentation before proposing a configuration or feature implementation.
- Use `read_doc` to get the full context of a relevant page identified via `search_docs`.
- Focus on RouterOS v7 features as documented in the `ROS` space.
- Hardware specifications can be found in the `UM` (User Manual) space.

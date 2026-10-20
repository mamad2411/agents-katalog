---
name: browsing-with-context7
description: Fetch up-to-date documentation and code examples from any library using Context7 MCP. Retrieve official docs, API references, tutorials, and examples. Use for library integration, API lookups, or learning new frameworks. NOT for static content (use web search/curl).
---

# Library Documentation Access

Fetch official documentation and code examples via Context7 MCP server.

## Server Lifecycle

### Start Server
```bash
# Using helper script (recommended)
bash scripts/start-server.sh

# Or manually
npx @context7/mcp@latest --port 8809 &
```

### Stop Server
```bash
# Using helper script
bash scripts/stop-server.sh

# Or manually
pkill -f "@context7/mcp"
```

### When to Stop
- **End of task**: Stop when documentation work is complete
- **Long sessions**: Keep running if doing multiple documentation lookups
- **Errors**: Stop and restart if server becomes unresponsive

**Important:** Always resolve library IDs first using `resolve-library-id` before querying documentation to ensure you use the correct Context7-compatible library ID format (e.g., `/org/project` or `/org/project/version`).

## Quick Reference

### Resolve Library ID

```bash
# Find the correct library ID for a library
python3 scripts/mcp-client.py call -u http://localhost:8809 -t resolve-library-id \
  -p '{"libraryName": "react", "query": "How to create a component"}'
```

### Query Documentation

```bash
# Fetch documentation for a specific library
python3 scripts/mcp-client.py call -u http://localhost:8809 -t query-docs \
  -p '{"libraryId": "/facebook/react", "query": "How to create a functional component"}'

# Query with version-specific documentation
python3 scripts/mcp-client.py call -u http://localhost:8809 -t query-docs \
  -p '{"libraryId": "/facebook/react/v18.2.0", "query": "useState hook examples"}'
```

### Get Code Examples

```bash
# Retrieve code examples for specific functionality
python3 scripts/mcp-client.py call -u http://localhost:8809 -t query-docs \
  -p '{"libraryId": "/vercel/next.js", "query": "getServerSideProps examples"}'

# Fetch API reference documentation
python3 scripts/mcp-client.py call -u http://localhost:8809 -t query-docs \
  -p '{"libraryId": "/expressjs/express", "query": "Express Router usage"}'
```

### Advanced Queries

```bash
# Search for best practices
python3 scripts/mcp-client.py call -u http://localhost:8809 -t query-docs \
  -p '{"libraryId": "/mongodb/docs", "query": "MongoDB connection best practices"}'

# Find migration guides
python3 scripts/mcp-client.py call -u http://localhost:8809 -t query-docs \
  -p '{"libraryId": "/prisma/prisma", "query": "Migration from v4 to v5"}'
```

For error handling scenarios, use `resolve-library-id` to gracefully handle invalid or unknown library names:

```bash
# Handle invalid library IDs gracefully
python3 scripts/mcp-client.py call -u http://localhost:8809 -t resolve-library-id \
  -p '{"libraryName": "nonexistent-library", "query": "some query"}'
```

**Tip:** Always resolve library IDs first using `resolve-library-id` before querying documentation to ensure you use the correct format.

## Workflow: Library Integration

1. Identify the library you need documentation for
2. Resolve the correct library ID using `resolve-library-id`
3. Query documentation using the resolved ID
4. Apply learned patterns to your code
5. Verify implementation against documentation

## Workflow: API Discovery

1. Determine the library/framework to research
2. Find the appropriate library ID
3. Query for specific API endpoints/methods
4. Extract usage patterns and parameters
5. Implement based on official examples

## Verification

Run: `python3 scripts/verify.py`

Expected: `✓ Context7 MCP server running`

## If Verification Fails

1. Run diagnostic: `pgrep -f "@context7/mcp"`
2. Check: Server process running on port 8809
3. Try: `bash scripts/start-server.sh`
4. **Stop and report** if still failing - do not proceed with downstream steps

## Tool Reference

See [references/context7-tools.md](references/context7-tools.md) for complete tool documentation.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Library not found | Verify library name spelling or try broader terms |
| Invalid library ID | Use resolve-library-id to get correct format |
| No results returned | Try different query phrasing or check library version |
| Server not responding | Stop and restart: `bash scripts/stop-server.sh && bash scripts/start-server.sh` |
| Outdated information | Specify version in library ID: `/org/lib/vX.X.X` |
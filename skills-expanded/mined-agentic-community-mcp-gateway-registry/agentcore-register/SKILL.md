---
name: agentcore-register
description: Given an MCP server URL, probe the server via curl to discover its metadata and tools, then generate a markdown file with copy-pasteable content for each field in the Amazon Bedrock AgentCore "Create record" form.
argument-hint: "<mcp-server-url>"
---

# AgentCore Register

Given a remote MCP server URL, probe it to discover server info and tools, then generate a markdown file containing copy-pasteable values for every field in the Amazon Bedrock AgentCore **Create record** form.

The MCP server URL is provided as `$ARGUMENTS`.

If `$ARGUMENTS` is empty, ask the user for the MCP server URL using AskUserQuestion.

## Steps

### 1. Initialize the MCP session

Send the MCP `initialize` request and capture the response headers (for the session ID) and body (for server info).

```bash
curl -s --max-time 15 -D /tmp/_agentcore_mcp_headers.txt \
  -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
      "protocolVersion": "2024-11-05",
      "capabilities": {},
      "clientInfo": {"name": "agentcore-register", "version": "1.0.0"}
    }
  }' > /tmp/_agentcore_mcp_init.json 2>&1
```

Parse the response to extract:
- `serverInfo.name` - the server name
- `serverInfo.version` - the server version
- `protocolVersion` - the MCP protocol version
- `capabilities` - what the server supports

Extract the `mcp-session-id` header value from `/tmp/_agentcore_mcp_headers.txt`.

#### Error handling

- If the curl request fails or times out, tell the user the server is unreachable and stop.
- If the response is a 502/503/504, tell the user the server backend is down and stop.
- If the response is HTML (not JSON), tell the user the URL may not be an MCP endpoint and stop.

### 2. List the tools

Using the session ID from step 1, send a `tools/list` request:

```bash
SESSION_ID=$(grep -i 'mcp-session-id' /tmp/_agentcore_mcp_headers.txt | awk '{print $2}' | tr -d '\r')

curl -s --max-time 15 \
  -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-session-id: $SESSION_ID" \
  -d '{"jsonrpc": "2.0", "id": 3, "method": "tools/list", "params": {}}' \
  > /tmp/_agentcore_mcp_tools.json 2>&1
```

The response may be plain JSON or SSE-formatted (`data: {...}`). Handle both:
- If the response starts with `{`, parse it directly as JSON.
- If the response contains `data:` lines, extract the JSON from the `data:` line.

Parse the tools array from `result.tools`. For each tool, capture:
- `name`
- `description`
- `inputSchema` (the full JSON schema object)

### 3. Generate the markdown file

Create a markdown file at `.scratchpad/agentcore-register-<server-name>.md` with all the values the user needs to copy-paste into the AgentCore form.

Use this exact template, replacing placeholders with the discovered values:

```markdown
# AgentCore Registry Record: <server_name>

*Generated: <current date>*
*Source: <MCP_URL>*

---

## Record Details

**Name:**
```
<server_name as a valid record ID, e.g. record_novacolor_finishes>
```

**Description:**
```
<server description derived from tools and server name, 1-2 sentences>
```

**Record version:**
```
<server version, e.g. 0.1>
```

**Record type:** MCP

---

## MCP Server Definition

Copy-paste the JSON below into the "Your MCP server definition" editor:

```json
{
  "name": "<namespace/slug, must match ^[a-zA-Z0-9.-]+/[a-zA-Z0-9._-]+$>",
  "description": "<max 100 chars, concise description>",
  "version": "<version>",
  "remotes": [
    {
      "type": "<transport type, e.g. streamable-http>",
      "url": "<MCP_URL>"
    }
  ]
}
```

---

## Tool Definition

Copy-paste the JSON below into the "Your Tool definition" editor:

```json
{
  "tools": [
    <for each tool, include the full tool object with name, description, and inputSchema>
  ]
}
```

---

## Discovery Summary

| Field | Value |
|-------|-------|
| Server name | `<serverInfo.name>` |
| Version | `<version>` |
| Protocol | `<protocolVersion>` |
| Transport | `<transport type>` |
| URL | `<MCP_URL>` |
| Tools | <comma-separated tool names> |
| Capabilities | <comma-separated capabilities> |
```

#### Rules for populating the template

- **Record name**: Convert the server name to a valid AgentCore record ID. Use lowercase, replace spaces and hyphens with underscores, prefix with `record_`. Only use letters, digits, underscores. Example: `record_novacolor_finishes`.
- **Description**: Write a concise 1-2 sentence description based on the server name and tool names/descriptions.
- **Transport**: Determine from how the server responded:
  - If the initialize response included `mcp-session-id` header and responded to POST with JSON, use `streamable-http`.
  - If the server used SSE (event-stream responses for initialize), use `sse`.
  - Default to `streamable-http` for remote HTTP servers.
- **MCP server definition JSON**: Must include `name`, `description`, `version`, and `remotes` fields. The `remotes` array contains the transport type and URL so that the AgentCore sync can extract `proxy_pass_url` correctly via `remotes[0].url`.
  - **name** MUST match the pattern `^[a-zA-Z0-9.-]+/[a-zA-Z0-9._-]+$` (namespace/name format). Derive the namespace from the server's domain (e.g., `com.agenthost` for `agenthost.club`, `io.github.user` for GitHub). Example: `com.agenthost/novacolor-italian-finishes`.
  - **description** MUST be 100 characters or fewer. Keep it concise.
  - **remotes** MUST be an array with at least one object containing `type` (transport type) and `url` (the MCP endpoint URL). Do NOT use top-level `url` and `transport` fields -- use the `remotes` array format instead.
- **Tool definition JSON**: Include the complete tool objects exactly as returned by the server, wrapped in a `{"tools": [...]}` envelope.
- **Tool inputSchema**: Include the full inputSchema for each tool exactly as returned by the server. Do NOT simplify or omit properties.

### 4. Cleanup

Remove temporary files:

```bash
rm -f /tmp/_agentcore_mcp_headers.txt /tmp/_agentcore_mcp_init.json /tmp/_agentcore_mcp_tools.json
```

### 5. Report to the user

After generating the file, display:

1. The path to the generated markdown file.
2. A brief summary: server name, number of tools, transport type.
3. Tell the user they can open the file and copy-paste each section into the AgentCore "Create record" form.

## Example

```
User: /agentcore-register https://novacoloritalianfinishes.agenthost.club/mcp

Output:
Generated `.scratchpad/agentcore-register-novacolor.md`

Summary:
- Server: some-agent (v0.1)
- Transport: streamable-http
- Tools: 3 (search_site_products, search, fetch)

Open the file and copy-paste each section into the AgentCore "Create record" form.
```

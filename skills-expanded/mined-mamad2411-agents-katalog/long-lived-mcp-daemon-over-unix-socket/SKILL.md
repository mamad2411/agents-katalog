---
name: long-lived-mcp-daemon-over-unix-socket
description: Front an MCP stdio server with a long-lived local daemon so a CLI can invoke tools across many short-lived commands while preserving browser/session state, using a Unix socket on POSIX and a named pipe on Windows.
category: daemon
version: 1.0.0
version_origin: extracted
tags: [daemon, unix-socket, named-pipe, mcp-client, ipc, lifecycle]
confidence: high
source_type: extracted-from-git
source_url: https://github.com/ChromeDevTools/chrome-devtools-mcp.git
source_ref: main
source_commit: 0a6aaa52ebacb2db834ffa437863e5844aa3730b
source_project: chrome-devtools-mcp
source_path: src/daemon/daemon.ts
imported_at: 2026-04-18T00:00:00Z
---

# Long-Lived MCP Daemon with Socket IPC

## When to use

- Your MCP server holds expensive state per session (a browser, a DB connection pool, a trained model) and you don't want each CLI invocation to pay the cold-start cost.
- You want `mycli status`, `mycli navigate URL`, `mycli screenshot` to feel like a REPL — each command returns in milliseconds but the underlying server stays up.
- Multiple MCP server args (`--headless`, `--userDataDir`) need to be captured at daemon start and applied to every subsequent call.

## How it works

- Daemon process: on start, write its PID to a well-known file, open a local socket, then spawn the MCP stdio server as a child and connect to it with an MCP `Client` using `StdioClientTransport`. Accept messages like `{method: 'invoke_tool', tool, args}` and `{method: 'stop'}` / `{method: 'status'}`. Forward `invoke_tool` to the MCP client, serialize the response, send back.
- Client (CLI) process: check if PID file exists and the process is alive (`process.kill(pid, 0)`). If not, spawn the daemon detached with `child.unref()` and wait for the PID file to appear before sending the first command.
- Socket path: use `XDG_RUNTIME_DIR` if set, otherwise `/tmp/<app>-<uid>.sock` on macOS/Linux (NOT `~/Library/Application Support` — POSIX socket paths are capped around 104 chars). On Windows use `\\.\pipe\<app>\server.sock` — named pipes, not files.
- Reuse an MCP `PipeTransport` for framing JSON messages over the raw socket. Send one command per connection, close on response; keeps the protocol trivially stateless and avoids read-buffer demux.
- Surface `start`, `stop`, `status` as explicit CLI subcommands; auto-start on first tool call but never auto-stop — let the user decide when to release state.

## Example

```ts
// daemon.ts - listens on socket, forwards to inner MCP stdio server
const mcpClient = new Client({name: 'daemon', version}, {capabilities:{}});
await mcpClient.connect(new StdioClientTransport({
  command: process.execPath, args: [INDEX_SCRIPT_PATH, ...serverArgs],
}));
createServer(socket => {
  const transport = new PipeTransport(socket, socket);
  transport.onmessage = async (msg) => {
    const { method, tool, args } = JSON.parse(msg);
    const result = await mcpClient.callTool({ name: tool, arguments: args });
    transport.send(JSON.stringify({ success: true, result: JSON.stringify(result) }));
    socket.end();
  };
}).listen({ path: socketPath });

// client.ts - one-shot call
const socket = net.createConnection({ path: getSocketPath() });
const transport = new PipeTransport(socket, socket);
transport.onmessage = m => resolve(JSON.parse(m));
transport.send(JSON.stringify({ method: 'invoke_tool', tool: 'navigate_page', args: {url} }));
```

## Gotchas

- On macOS/Linux, the PID file can outlive a crashed daemon; always probe with `process.kill(pid, 0)` before trusting it. Delete stale files during start.
- On non-Windows platforms, `unlinkSync(socketPath)` before `listen()` — a stale socket file blocks bind even if the previous process is gone.
- Detached spawn on Windows: pass `windowsHide: true` and `stdio: 'ignore'`, else the daemon flashes a console window.
- If the underlying MCP server streams large results (images, traces), serialize to a temp file and return the path, not the bytes — socket IPC is not the place for megabyte payloads.
- Time-out the client's socket read with a generous default (the daemon example uses 60s); some MCP tool calls genuinely take that long.

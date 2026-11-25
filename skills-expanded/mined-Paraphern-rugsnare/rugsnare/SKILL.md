---
name: rugsnare
description: Pin and verify MCP tool contracts - detect when a server silently changes tool names, descriptions, or input schemas after the user approved them. Use when the user asks to secure, audit, or monitor their MCP servers, or to investigate "why did my agent start behaving differently".
---

# rugsnare - MCP contract pinning

Tool descriptions are instructions your agent obeys. When an MCP server changes a tool's name, description, or input schema after the user approved it, the agent is now following different instructions without anyone deciding to. rugsnare makes that visible.

## What to do

1. **Pin**: `npx rugsnare scan --config <mcp-config>` - hashes every approved tool contract (name + description + inputSchema, sha-256) into `.rugsnare/pins.json`. Show the user the per-server tool counts and get confirmation before committing.
2. **Gate**: `npx rugsnare diff --config <mcp-config>` - exits 1 when any contract changed. Run it in CI on every PR.
3. **Interpret findings by direction**:
   - BREAKING - tightened (new required params, narrowed types, new limits): old callers may now fail validation
   - LOOSENED - constraints dropped, required became optional
   - EXPANDED - new optional param: a new data channel for the agent
   - NOTATION - dialect/key-order/SDK artifacts, semantically void
   - NEW / GONE - tools added or removed
   - A guard-style warning (dry_run, confirm, force...) means a safety parameter was removed, made optional, or had its default flipped: treat as urgent.
4. **Report to the user in their words**: which tool, which direction, which version boundary, and the repro command.

## Live tools

This plugin also serves rugsnare's read-only MCP server (`drift_feed_status`, `pins_report`) - ask it for the current drift status of popular MCP servers, or a report on the local pin store.

## Rules

- Never edit `.rugsnare/pins.json` by hand; re-pin only with `rugsnare approve <server>` after a human accepts the new contract.
- Never pin a config the user did not name. The pins are the trust anchor.
- Pins contain no secrets (names, descriptions, hashes only) - safe to commit.

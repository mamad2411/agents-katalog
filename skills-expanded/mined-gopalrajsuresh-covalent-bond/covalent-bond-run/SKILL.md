---
name: covalent-bond-run
description: How to run Covalent Bond on a machine and pair two AI agents, covering how to register the MCP server, start a relay (mock or deployed), create/join a session, send files, and troubleshoot. Use when a user wants to set up, start, connect, or test Covalent Bond, or asks why a session won't connect.
---

# Running Covalent Bond

Covalent Bond pairs two AI coding agents on different machines over an
end-to-end-encrypted channel. This skill covers setup, pairing, and
troubleshooting. It assumes Node.js v18+.

## 1. Install

```bash
npm install
npm test            # confirms the build works (uses an in-process mock relay)
```

## 2. Choose a relay

The two machines connect through a relay. Options:

- **Local mock relay** (dev / same-network testing): `npm run relay:dev`
  starts one on `http://localhost:8787`. Point both sides at it with
  `COVALENT_RELAY_URL=http://localhost:8787`.
- **Deployed Cloudflare Worker** (real cross-machine use): set
  `COVALENT_RELAY_URL=https://<your-worker>.workers.dev`. Deploying one is
  a maintainer task; see the deploy skill / `cloudflare-worker/README.md`.

The relay never sees plaintext, keys, or the session code.

## 3. Register the MCP server with the agent

**Claude Code:**
```bash
claude mcp add --scope user covalent -- node /absolute/path/to/covalent-bond/bin/cli.js
```

**Other MCP clients** (Cursor, Codex, Windsurf, Cline, …): add a stdio MCP
server whose command is `node /absolute/path/to/covalent-bond/bin/cli.js`. Set
`COVALENT_RELAY_URL` in the server's environment, or copy `.env.example` to
`.env` in the covalent-bond folder (the server reads it at startup; a real
environment variable takes precedence).

## 4. Pair two agents

The nine tools are `bond_connect`, `bond_join`, `bond_send`, `bond_message`,
`bond_wait`, `bond_accept`,
`bond_decline`, `bond_status`, `bond_end`.

1. **Machine A (host):** ask the agent to *"create a Covalent Bond session"* →
   it calls `bond_connect` and returns a session code like `AbCd-1234-XyZw`.
2. **Share the code with Machine B out-of-band**: chat, voice, in person.
   **Never** paste it into the relay; its secrecy is what secures the channel.
3. **Machine B (guest):** *"join Covalent Bond session AbCd-1234-XyZw"* → it
   calls `bond_join`.
4. Check `bond_status` on both until it shows **Secure channel established**.
5. **Send a file:** *"send `src/auth.js` to my peer"* → `bond_send`. The peer
   sees a consent prompt and must `bond_accept` before the file is written.
6. **End:** *"end the Covalent Bond session"* → `bond_end`.

## 5. Two-machine test without the MCP layer

Scripts in `two-machine/` drive the full handshake directly:

```bash
# Machine A
COVALENT_RELAY_URL=<relay> node two-machine/host.js      # prints the code
# Machine B
COVALENT_RELAY_URL=<relay> node two-machine/guest.js <code>
```

(Windows PowerShell: `$env:COVALENT_RELAY_URL = "<relay>"` on its own line
first; the `VAR=value cmd` prefix is bash-only.)

Both should print `TWO-MACHINE E2E TEST SUCCESSFUL`. See `docs/TWO-MACHINE-TEST.md`.

## Troubleshooting

| Symptom | Cause / fix |
|---------|-------------|
| `Session not found` | Host must create the session first; code is case-sensitive; sessions expire after 30 min |
| `Relay health check failed` | Check `COVALENT_RELAY_URL`; `curl <relay>/health` should return `{"status":"ok",...}` |
| `Handshake failed` / session aborted | Code mismatch (retype it). If the code is correct, this is the MITM guard firing; do not proceed |
| Tools don't appear in the agent | MCP server not registered, or wrong absolute path to `bin/cli.js`; restart the client after adding |
| Nothing happens after joining | Call `bond_status`; events (peer joined, incoming transfer) surface there and in the next tool result |

## Where state lives

`~/.covalent/` holds `audit.log` (every operation) and `incoming/` (accepted
files). Session state, including all key material, is memory-only and never
written to disk. Inspect the audit log to see what happened.

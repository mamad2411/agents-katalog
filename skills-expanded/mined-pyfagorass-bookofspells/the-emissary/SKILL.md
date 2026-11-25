---
name: the-emissary
description: >-
  Find and connect an MCP server — an "Emissary of the Pact" — when the agent
  needs a tool, service, API, or data source it does not already have. Use when
  the user asks for an MCP server, to connect to or integrate an external service
  (Notion, GitHub, Figma, a database, Slack, a SaaS API…), asks "is there an MCP
  for X", "add an MCP", or sets a task that needs live tools the agent lacks.
  This rite DISCOVERS a server from the official MCP Registry and reputable
  directories and PROPOSES its connection config for the user to approve — it
  NEVER installs, launches, or writes credentials on its own. The companion to
  the-grimoire: that finds spells (inert skills); this finds Emissaries (live
  tool-servers).
---

# 🤝 The Emissary — Summon a Server of the Pact (MCP)

An **Emissary of the Pact** is an MCP server: not an inert spell you *read*, but a
**live process or endpoint** your harness *connects to*, whose tools then become
yours (its **Channels**). Binding one therefore **runs code** and often **hands
over secrets** — so this rite only ever **discovers and proposes**. The conjurer
alone approves the binding. *(Lexicon: Pact → Emissary → Channels.)*

You do **not** clone or vendor an Emissary. You find its metadata, weigh its
house, and hand the conjurer the exact words to summon it themselves.

## The Rite of Summoning

1. **Seek.** Find candidate Emissaries for the capability — the official MCP
   Registry searches **server-side**, so this is one call, not a crawl:
   - **Run the bundled search** — a tiny, dependency-free helper over the live
     Registry (the canonical catalogue). Run it, or read it and re-express it in
     bash / PowerShell / JS — it is only one HTTP GET:
     ```bash
     python3 scripts/find-emissary.py <keyword>        # e.g. notion, "github issues"
     ```
     The raw call it makes, if you would rather not run the script:
     ```bash
     curl -s "https://registry.modelcontextprotocol.io/v0/servers?search=<keyword>&version=latest" \
       | jq '.servers[].server | {name, description, remotes, packages, repository}'
     ```
   - **Browse the directories** in [`references/sources.md`](references/sources.md)
     — the awesome-list, PulseMCP, Smithery — for breadth and reviews, then open
     each link to the real repo.

2. **Choose by house, not by stars.** Prefer the **first-party Emissary** — the
   service's own official server. Failing that, an accountable, maintained
   source. A viral community server is still street magic: read how far its code
   reaches before you trust it.

3. **Read its binding-terms.** From the server's `server.json` (or its README):
   *how* it connects — a **remote** endpoint (`streamable-http` / `sse` URL) or a
   **package** to launch locally (`npx` / `uvx` / `docker`) — and *what* it
   demands: environment secrets, API keys, OAuth scopes.

4. **Propose — do not bind.** Present to the conjurer, plainly:
   - what the Emissary is and **whose house** made it,
   - its **Channels** (the tools it exposes) and what access / secrets it needs —
     work these out yourself from the Emissary's repo, README, or registry entry;
     no script does this for you, and the definitive list enumerates the moment it
     is connected,
   - the **exact** way to add it for *their* harness, e.g.
     - Claude Code: `claude mcp add <name> -- npx -y <package>`
     - or the JSON block for `.mcp.json` / Cursor / VS Code,
     - or the remote URL and its OAuth flow.

   Then **STOP.** Do not run the command, open the connection, or write any
   secret into a config file or the repo.

5. **The conjurer binds it.** Only the user performs the add and supplies the
   secrets. Confirm it connected, then labour on with the new Channels in hand.

## Wards

- **An Emissary acts with your reach and your credentials.** Vet its house
  before binding; grant **least privilege** — only the scopes and secrets the
  task truly needs.
- **The Scrying Ward cannot help you here.** That ward scans *inert spells* for
  dark magic; a running Emissary executes code it never sees. Trust is the
  conjurer's to grant, deliberately.
- **Prefer official remotes with proper OAuth** over piping an unknown install
  script to a shell. Never paste a secret you cannot rotate.
- **Never auto-connect.** Discovery is yours; the binding is always the user's.

*Find the Emissary, weigh its house, hand over the words — and let the conjurer
open the door.* 🕯️

Companion: [[the-grimoire]] finds spells; the-emissary finds Emissaries.

---
name: swarm-vault
description: The vault contract — how any agent reads, writes, and queries the SwarmVault. Use at the start of work in any vault-connected project, before exploring the repo, when deciding where to record memory/plans/decisions/sessions, when handing off between sessions or agents, or whenever unsure how the vault works.
---

# swarm-vault — the vault contract

The vault is the shared brain of every agent on this machine. Query it before exploring;
write to it so parallel and future agents inherit what you learned. It is plain markdown —
Obsidian is an optional viewer, never a dependency.

The CLI is `swarmvault.py` — your platform's SwarmVault section (CLAUDE.md / AGENTS.md)
records its full path; default install is `~/.swarmvault/scripts/swarmvault.py`.

## Reading (query first, explore second)

```bash
swarmvault.py query --search "auth flow"           # BM25, names + descriptions
swarmvault.py query --project X --type memory      # structured filters
swarmvault.py show <note-name>                     # one body, once found
swarmvault.py context .                            # the compact project brief
```

Descriptions are the payload — most questions are answered without opening a note.
Open bodies (`show`) only for what you actually need. Reach for Glob/Grep on the repo
only for what the vault cannot answer. If quality genuinely needs more context, take
more — the budget curbs habit, not necessity.

## Writing (own files only)

| What | Where | Lane |
|---|---|---|
| Memory (facts, footguns, decisions learned) | platform memory dir, or `<project>/.swarm/memory/` on Codex — sync mirrors both | machine |
| Session journal (end of session) | `40 Sessions/<P>/YYYY-MM-DD <slug>.md` | machine |
| Specs, plans, question queue | `30 Plans/<P>/` | human (specs) / machine (queue) |
| Tickets + claims | `30 Plans/<P>/tickets/` — claim via CLI only (see swarm-implement) | machine |
| ADRs | `50 Decisions/<P>/ADR-NNN-<slug>.md` | human |
| Code-notes (deep reasoning for a hot file) | `10 Projects/<P>/code-notes/` | human |

Rules: frontmatter always (`name`, one-line `description` that carries the fact,
`project`, `type`); `[[wikilinks]]` liberally; templates in `90 Templates/`. Never edit
MOCs, Home, or `generated: true` notes — sync regenerates them. Never write another
agent's session/claim files.

## The two lanes

**Human lane** (specs, design docs, ADRs, README): full prose, complete sentences.
**Machine lane** (tickets, claims, queue entries, session notes, memory descriptions):
compact telegraphic style — imperative, no filler, quality content in minimal tokens:

> Verbose: "In this session we worked on the authentication system and managed to fix
> the token refresh bug that was causing users to be logged out unexpectedly."
> Compact: "DID: fixed token-refresh logout bug (src/auth.ts:142, race on expiry).
> NEXT: add regression test for concurrent refresh. BLOCKED: nothing."

Never compress the human lane, and never compress away information a future agent needs —
if compression costs precision, don't.

## Token economy & state doctrine

1. **Offload, don't carry** — write durable state to the vault; reference notes by name
   instead of re-explaining them in context.
2. **Checkpoint continuously** — durable state is written *when it changes* (ticket
   claimed/progressed/done, question answered, phase advanced), never batched to session
   end. The compliance test: kill the session at any moment — a fresh session must
   resume correctly from the vault alone, no transcript needed.
3. **Handoff by vault** — still end sessions with a journal note (`DID/NEXT/BLOCKED`) as
   history; but it is journal, not required state — resume never depends on it.
4. **Tier models** — top models for spec/design/review/complex logic; smaller for
   boilerplate (swarm-implement carries the table).
5. All guidelines are quality-bounded: when quality needs tokens, spend them.

## Isolation etiquette

Projects registered `isolated` are excluded from cross-project queries automatically.
Never quote isolated-project content into another project's notes. This is cooperative
filtering, not a security boundary.

## Self-diagnosis

Vault not finding your project? `swarmvault.py doctor` — checks config
(`~/.swarmvault.json` / `$SWARMVAULT_HOME`), the `.swarmvault` marker, and the registry.
A moved project: `swarmvault.py register --repair` from its new path.

---
*Influences: the original Claude Vault design; caveman plugin (compression); Obsidian MOC
practice — see CREDITS.md.*

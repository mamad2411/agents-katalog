---
name: memory-conventions
description: Read and write durable agent memory in the personal Obsidian vault at $AGENT_MEMORY_VAULT. Use at session start to recall context, when the user states a lasting preference, decision, or fact, or when asked to remember, recall, or forget something.
---

# Memory Conventions

Durable, cross-harness agent memory lives in the vault at
`$AGENT_MEMORY_VAULT`. Access is **direct file operations** — no CLI or
app required, works headless on every harness.

## Layout

The `agent/` directory is an OKF-conformant bundle (markdown + YAML
frontmatter; permissive consumption — never reject a malformed fact).

```text
$AGENT_MEMORY_VAULT/
  agent/
    index.md        # the only file loaded at session start
    log.md          # append-only history (temporal layer)
    facts/<slug>.md # one fact per note, semantic kebab-slug filename
```

## Session start

Read `agent/index.md` only (hard cap 200 lines / 25KB). Load individual
facts on demand when their hook matches the task.

`index.md` is a **pure listing** (OKF §6): a heading and link entries,
nothing else. Its only frontmatter is `okf_version: "0.1"` at the
bundle root. Conventions prose lives here in this skill, never in the
index.

## Writing a fact

When the user states something durable (preference, decision,
constraint, reference):

1. Create `agent/facts/<kebab-slug>.md` — the slug names the
   *concept*, never a timestamp (concept = identity; update in place):

```markdown
---
type: user|feedback|project|reference
title: <display name>
description: <one line — becomes the index hook>
created: <ISO 8601 with seconds, UTC, e.g. 2026-07-12T18:42:07Z>
updated: <same format>
source: <where this came from>
---

<the fact, one per note; absolute dates; [[wiki-links]] to related facts>
```

2. Add one index line: a markdown list item linking the fact — link
   text is the title, target is `facts/<slug>.md`, followed by
   ` — <description>`.
3. Append to `agent/log.md` under a `## YYYY-MM-DD` heading (newest
   day first). Entry: bold operation verb (`**Create**`, `**Update**`,
   `**Delete**`), the fact's title linked to its file, ` — <reason>`,
   and the UTC time `(HH:MM:SSZ)`.

## Maintaining

- Update or delete stale facts; never duplicate them.
- Check the index for an existing fact before creating a new one.
- Session-scoped notes stay in the harness's native memory, not here.

## Guardrails

- The vault must be **personal** storage — never an employer-synced
  location (`sync doctor` enforces this).
- If `$AGENT_MEMORY_VAULT` is unset or missing, say so and skip memory
  operations; do not invent a location.

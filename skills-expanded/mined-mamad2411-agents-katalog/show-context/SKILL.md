---
name: show-context
description: "Shows the current project context index without changing anything."
user_invocable: true
---

# Context Show

When invoked, read `.context/{project}/INDEX.md` and print its contents in a
human-readable form. No modifications. No interaction beyond an optional
summary at the end.

If arguments are provided, treat them as the project slug. Otherwise infer
from the working directory or list available projects under `.context/` and
ask.

If no `.context/{project}/INDEX.md` exists, stop with:

> "No context index found at `.context/{project}/INDEX.md`. Run
> `/sulis:discover-context` to create one."

---

## Workflow

### Step 1 — Locate the index

Resolve `.context/{project}/INDEX.md`. If the project slug is ambiguous,
list available indexes under `.context/` and ask the user which to show.

### Step 2 — Print the contents

Display the file content directly in the conversation. Markdown rendering
will handle the tables and headings.

### Step 3 — Add a one-line summary

After printing, append a single status line:

> "**Status:** {N} authoritative source(s); {M} ADR(s) in external registry;
> last validated {date}. {Stale | Current}."

The freshness threshold:
- `Current` — `Last validated` within 90 days
- `Stale` — older than 90 days; recommend `/sulis:refresh-context`

### Step 4 — Suggest next actions

Conditional on state:

- If `Stale`: recommend `/sulis:refresh-context`
- If known gaps exist and SRD/SEA hasn't run yet: recommend
  `requirements-analyst` or `/sulis:draft-architecture` to fill them
- If neither: no recommendation, exit cleanly

---

## Gotchas

- **Read-only means read-only.** This skill never writes. If the user
  asks to "fix" something in the index, redirect them to
  `/sulis:refresh-context`.
- **Do not summarise the index content.** The user is asking to see the
  index; show it verbatim. Summarising defeats the purpose.
- **Do not load referenced files.** Show the index — paths only. Loading the
  authoritative sources is for downstream plugins, not for this skill.

---

## See Also

- `../discover-context/SKILL.md` — create a new context index
- `../refresh-context/SKILL.md` — update an existing context index
- `references/context-index-template.md` — the index file schema

---
description: Design the UI for a story via the Designer agent (draft on a scratch artifact, save to the shared canvas + Confluence only on approval)
argument-hint: <Jira ticket URL | JIRA-KEY | pasted story title + description>
---

> Invoked as `/design-story` (not `/design`) — that name is reserved for
> the platform's built-in `design` skill (Claude Design canvas authoring),
> which the Designer agent loads internally. Reusing it here would shadow
> that skill and break Claude Design mode.

Run the Designer agent (`.claude/agents/designer.md`) for the story given
in $ARGUMENTS.

1. Resolve the story:
   - If $ARGUMENTS is a Jira ticket URL, extract the key from it.
   - If it's a bare key (e.g. `CHH-123`), use it directly.
   - Otherwise treat $ARGUMENTS as the pasted story itself (title +
     description + AC) — no Jira key required in that case.
2. Spawn the `designer` subagent with that story as input. It will:
   - Fetch the Jira ticket and its Confluence page once each.
   - Ask you for the PRD only if the story + Confluence page don't give it
     enough to design confidently — not reflexively.
   - Read `design/component-gallery.html` (tokens) and
     `design/ui-standard.md` (rules) once, load the `design` and
     `frontend-design` skills, and draft on a **scratch artifact**
     (`design/drafts/<KEY>.dc.html`) — the shared canonical canvas isn't
     touched during drafting.
3. The designer agent must stop and present the draft (URL, states/
   artboards covered, any AC it can't represent visually) before touching
   the canonical canvas, Confluence, or `design/design-links.md` — do not
   skip that approval gate.
4. On approval, it merges the approved artboard(s) into the canonical
   canvas, sets the `Design Reference` field on the story's **Confluence**
   page (not a Jira comment — Jira comments are disabled repo-wide, see
   `.claude/agents/orchestrator.md` Rule 10, and the frontend Planning
   Agent's design-readiness gate reads Confluence, not Jira comments), and
   logs the row in `design/design-links.md`.

If `design/ui-standard.md` or `design/component-gallery.html` is ever back
to `[PLACEHOLDER]`-only, stop and ask the user for the design standard
content instead of inventing one.

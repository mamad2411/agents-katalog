---
name: meta-preferences
description: Configure project-level preferences (documentation language) — extensible for more later
---

# Preferences

This configures how Codex behaves **around this project's written artifacts** — not the project's business/product content itself, and not conversational behavior. It doesn't touch code, master docs, or `.agents/skills/`. Safe to re-run anytime to change an answer.

Always project-scoped — this isn't a question about how you want Codex configured across every project on your machine, just this one. The answers live in `docs/PROJECT_PREFERENCES.md`, versioned alongside the rest of the project's docs, so the whole team gets the same behavior, not just whoever ran this command.

## 1. Check current state

Before asking anything, read `docs/PROJECT_PREFERENCES.md` if it exists.

Report what's already set before asking about it. Only ask about what's missing, or what the human explicitly says they want to revisit — never re-run the full interview from scratch just because the skill was invoked again.

## 2. Ask

### Documentation language
"What language should `docs/` and `.codex/work/` artifacts be written in — `context.md`, `architecture.md`, `plan.md`, business-context files, ADRs, and so on?"

Be explicit this is **not** about conversation: Codex already mirrors whatever language the human writes in, session to session, with no configuration needed. This setting only controls the language of files that get committed to the repo.

## 3. Write

- **`docs/PROJECT_PREFERENCES.md`**: create it if it doesn't exist, or update the relevant section if it does (don't touch sections the human didn't just answer). Keep it short and plain:

  ```markdown
  # Project Preferences

  ## Documentation language
  Write `docs/` and `.codex/work/` artifacts in: <language>. Conversational
  responses aren't affected — Codex already mirrors whatever language the
  human writes in.
  ```

## 4. Confirm

```markdown
## Preferences set
- Documentation language: [English (default) / <language>]

## Where these live
- docs/PROJECT_PREFERENCES.md — the record every `warm-up` skill invocation reads
```

Re-run this skill (`meta-preferences`) anytime to change an answer.

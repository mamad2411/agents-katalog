---
name: repo-onboarding
description: Onboard to an unfamiliar codebase — map its structure, components, entry points, conventions and risks, and seed the project knowledge vault from it, producing an onboarding map. Use to get oriented in or understand a new repo, or to analyze a repo and seed the knowledge base. Capturing or recalling a single decision is knowledge; not feature research (research) or code review (code-review).
allowed-tools: Read, Grep, Glob, Bash, Task, Write, Edit
---

# Repo onboarding (phase workflow)

Get oriented in an unfamiliar codebase and leave behind a durable map: analyze the structure and
**seed the Stage-3 knowledge vault** with grounded notes, plus an `onboarding` summary. It reads
the code (forking `Explore`) and writes notes through the plugin's `bin/af.py` —
everything grounded in the actual code, nothing invented. (Design: ADR 0023 and
`docs/architecture/design-onboarding.md` in the agentic-forge repository — not shipped with the
plugin.)

## When to use

When the task is to understand / get oriented in an unfamiliar or new codebase, or seed the KB from
a repo. **Not** feature/options research (`research`), reviewing a change (`code-review`), or
capturing one decision (`knowledge`).

## Process

The vault commands print one JSON object each and need nothing installed:

```
python3 -E "${CLAUDE_PLUGIN_ROOT}/bin/af.py" vault-validate --repo .
python3 -E "${CLAUDE_PLUGIN_ROOT}/bin/af.py" vault-add-note --repo . --json - <<'NOTE'
{"name": "<kebab-case-name>", "title": "<human title>", "body": "<markdown>",
 "tags": ["tag-a"], "moc": "<themed-moc>"}
NOTE
```

If `vault-add-note` exits non-zero the note was NOT saved: report its error. Do not write the
note by hand to get round it.

1. **Analyze the code.** Fork `Explore` (via `Task`) to map the repo: the components/modules, the
   entry points (how it runs), the conventions (error handling, structure, testing), and the
   notable risks/gotchas. Detect the stack (`python3 -E "${CLAUDE_PLUGIN_ROOT}/bin/af.py" stack-detect --repo .`) for context. Stay grounded — every
   claim must point at real code; do not invent modules or features.
2. **Seed the vault.** For each durable finding, write an atomic note with
   `vault-add-note` — an architecture map, key
   components, conventions, risks — linked from a themed MOC. Then `vault-validate` and
   fix any broken link or orphan.
3. **Write the `onboarding` map** (frontmatter `type` (= `onboarding`), `feature`, `status`, `components`, `entry_points`,
   `conventions`, `risks`), then validate it
   (the read-back below; see
   [handoff.md](../../patterns/handoff.md)) — the quick-start summary that points into the seeded vault.
   Then **read the file back** — `python3 -E "${CLAUDE_PLUGIN_ROOT}/bin/af.py" handoff-load --path <path> --type onboarding` — and
   fix whatever it reports: this reads the file, so it sees the YAML you typed, and a single
   malformed value (a flow sequence with prose after it, an unquoted `:`) leaves an artifact the
   next phase cannot read (ADR 0096).

## Output

A seeded knowledge vault (atomic notes, linked, validating clean) plus an `onboarding` handoff
mapping components, entry points, conventions, and risks — all grounded in the real code.

## Definition of done

- Components, entry points, conventions, and risks are identified **from the actual code** (nothing
  fabricated).
- The vault is seeded with linked notes and `vault-validate` is clean (no broken links/orphans).
- A valid `onboarding` artifact is produced.

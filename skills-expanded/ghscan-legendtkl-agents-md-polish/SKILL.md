---
name: agents-md-polish
description: |
  Audit and improve AGENTS.md / CLAUDE.md guidance files. Use this skill when
  the user asks to audit, polish, improve, shrink, refactor, fix, lint, or
  optimize AGENTS.md or CLAUDE.md; when they want to
  convert a bulky CLAUDE.md into a short AGENTS.md plus a CLAUDE.md bridge;
  when they want to create a starter AGENTS.md from scratch; or when they want
  to understand why an agent is ignoring rules in the guidance file.
---

<!-- generated-by: agents-md-polish@{{version}} -->

# Agents MD Polish

A short, repeatable workflow for keeping AGENTS.md and CLAUDE.md files
**short, project-specific, and executable**. Anthropic recommends keeping
CLAUDE.md under 200 lines; longer files "consume more context and reduce
adherence." Bloated files cause agents to ignore your actual rules.

## When invoked, run this workflow

### 1. Discover

Find guidance files in the current project:

```
AGENTS.md, CLAUDE.md
```

Check the repo root first, then any nested `AGENTS.md` files in subdirectories
(monorepos use one per package, with the closest file taking precedence).

### 2. Audit

Use `references/audit-checklist.md` to score each file. The deterministic
checks (line count, byte size, broken file references) live in
`scripts/audit_agents_md.mjs` — run it first:

```
node scripts/audit_agents_md.mjs <file>
```

The script exits non-zero on broken file references or missing files. Read
its JSON output (when invoked with `--json`) to drive follow-up actions.

### 3. Diagnose

For each issue, look up the matching pattern in `references/polish-patterns.md`
and explain the *why* in one sentence. Don't dump the whole pattern — just the
1-line summary so the user understands the recommendation.

### 4. Propose

Group the proposed changes by severity (error → warn → info). For each, show
a unified diff using the Edit tool's preview format. Don't apply yet.

### 5. AWS test (sanity gate)

Before applying, ask of every line you would *keep*:

> "If I remove this line, will an agent make a mistake?"

If the answer is no, propose deletion instead of modification. Bias toward
shorter files.

### 6. Apply

Apply changes the user accepted. For long extracted content (architecture
notes, API specs, full command lists), write to `docs/<topic>.md` or
`AGENTS-references/<topic>.md` and reference from AGENTS.md by relative
path with a `file:line` pointer where possible.

### 7. Bridge-ify (if applicable)

If both AGENTS.md and CLAUDE.md exist and overlap by more than 50%, propose
collapsing CLAUDE.md to a single-line bridge:

```
@AGENTS.md
```

Use `references/claude-bridge-template.md` for the bridge pattern and the
short explanation to show the user.

Only keep Claude-specific addenda below the import line if they are *not*
useful to Codex.

## Create path (when no guidance file exists)

If the user wants a starter AGENTS.md and none exists, copy
`references/agents-md-template.md` and fill in the project-specific sections
by inspecting the repo:

- Read `package.json` / `pyproject.toml` / `Cargo.toml` for scripts and entry points
- Skim top-level directories to populate Project map
- Don't invent invariants — ask the user for 1-3 they actually care about

## What goes in AGENTS.md vs elsewhere

| Type of guidance | Where it goes |
|---|---|
| Route map, commands, invariants, validation entrypoints | AGENTS.md |
| Repeatable multi-step workflows | Skills (`.agents/skills/`, `.claude/skills/`) |
| Long architecture notes, API specs, testing guides | `docs/` referenced from AGENTS.md |
| Lint / formatter / style rules | `pre-commit`, ruff/eslint config — NOT AGENTS.md |
| Live external systems (GitHub, DBs, browser) | MCP servers / CLIs |

## Hard limits to keep in mind

- Root AGENTS.md: target <200 lines (Anthropic), warn at 200, error at 500
- Root file size: warn >12 KB, error >25 KB
- Sections (H1/H2): warn >17, error >30
- Bullets per section: warn >18
- Inline code blocks: warn >15 lines (extract to referenced file)
- Imports do **not** save tokens — Anthropic loads them in full at launch.
  The only real reduction is deleting content.

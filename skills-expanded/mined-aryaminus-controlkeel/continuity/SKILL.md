---
name: continuity
description: "Learn, record, audit, and apply codebase patterns consistently across a repo by comparing current code to canonical local examples stored in CK memory. Use when asked to preserve continuity, learn a pattern, check drift, fix inconsistent implementations, or enforce local conventions."
when_to_use: "Activate ONLY for pattern-related work: learning repo conventions, auditing for drift, or fixing inconsistencies. Do NOT use for one-off code changes or general governance."
argument-hint: "[learn <name> <paths...>|check <name>|fix <name>|ci]"
disable-model-invocation: true
license: Apache-2.0
compatibility:
  - opencode-native
  - claude-standalone
  - cursor-native
  - codex
metadata:
  author: controlkeel
  version: "1.0"
  category: governance
  ck_mcp_tools: [ck_memory_record, ck_memory_search, ck_finding, ck_fs_find, ck_fs_grep, ck_fs_read, ck_git_diff, ck_validate]
  related_skills: [investigate, controlkeel-governance, deslop]
---

# Continuity

Learn, record, audit, and apply codebase patterns consistently using CK's existing tools. No external registry files, no new infrastructure — everything lives in CK typed memory and findings.

This skill fills the gap between CK's policy-level validation (`ck_validate`) and unstructured convention hints in `AGENTS.md`. It lets you encode *local coding conventions* — "our screens follow this shape, hooks use this pattern, imports go here" — as searchable, auditable, CI-gatable rules.

## Do NOT use when
- The work is a one-off code change (governance is handled by `controlkeel-governance`)
- The question is about security policy (use `security-review`)
- You need to trace code paths without enforcing conventions (use `investigate`)
- The repo has no patterns worth recording yet

## How it works

CK typed memory IS the pattern registry. `ck_finding` IS the violation tracker. `ck_fs_*` tools ARE the scanner. This skill just wires them together:

| Need | CK tool |
|------|---------|
| Store a pattern | `ck_memory_record(record_type: "decision", tags: ["continuity", "pattern", "active"])` |
| Find known patterns | `ck_memory_search(query: "...", record_type: "decision")` + filter tags |
| Find canonical files | `ck_fs_find`, `ck_fs_grep` to locate implementations |
| Read source-of-truth | `ck_fs_read` |
| Audit files for drift | `ck_fs_grep` for violation signals, `ck_fs_read` to verify |
| Record violations | `ck_finding(category: "continuity", severity: "...", rule_id: "continuity.<pattern-name>")` |
| Scope to changed files | `ck_git_diff` to list changed paths first |
| CI gate | `ck_validate` against finding-based policy |

## Pattern Registry

Patterns live in CK typed memory. To learn a pattern, record it with a consistent shape:

```elixir
# Pattern recording convention
record_type: "decision"
tags: ["continuity", "pattern", "<status>"]
# status: active | draft | deprecated

# Body shape (markdown):
# ## Pattern: <kebab-case-name>
# - **Source of truth:** <file paths>
# - **Applies to:** <glob patterns>
# - **Does not apply to:** <glob exceptions>
# - **Rule summary:** <one paragraph>
# - **Required shape:** <observable rules>
# - **Violation signals:** <searchable patterns>
# - **Severity:** high | medium | low
# - **Fix strategy:** <mechanical fix steps>
```

### Tag conventions

- `["continuity", "pattern", "active"]` — actively enforced
- `["continuity", "pattern", "draft"]` — being refined
- `["continuity", "pattern", "deprecated"]` — no longer enforced

## Invocation modes

### learn — Record a new pattern

When the user says "learn this pattern" or shows you canonical example files:

1. Read the provided files with `ck_fs_read`.
2. Search for similar implementations with `ck_fs_find` + `ck_fs_grep`.
3. Compare examples. Identify the canonical shape.
4. **Ask focused questions if ambiguous.** Don't guess. Point to specific files and ask which should be canonical.
5. Once confirmed, record with `ck_memory_record` using the shape above.
6. Tell the user what was recorded.

### check — Audit for drift (read-only)

When the user says "check this pattern" or "audit for drift":

1. Search `ck_memory_search(tags: ["continuity", "pattern"])` for matching patterns.
2. If a specific name given, filter by body content matching that name.
3. If scope wasn't specified, check `ck_git_diff` for changed files first (changed-files scope).
4. Or audit the full path scope if user explicitly requests full-repo.
5. For each pattern, search for violation signals using `ck_fs_grep`.
6. Read candidate files with `ck_fs_read` to verify.
7. Report violations concisely. Do NOT edit files.
8. For each violation, offer to record it with `ck_finding` if the user wants it tracked.

### fix — Audit and apply safe fixes

When the user says "fix this pattern" or "apply the pattern":

1. Run the `check` workflow first.
2. Apply high-confidence mechanical fixes directly.
3. **Ask before** fixes that rename public symbols, move files across packages, or require choosing between canonical examples.
4. Re-run the pattern search to confirm drift is closed.
5. Run repo-native validation (tests, lint, typecheck) if available.
6. Summarize what changed.

### ci — Deterministic audit for automation

When run in CI or pre-commit context:

1. Run `ck_git_diff` to get changed files.
2. Search `ck_memory_search(tags: ["continuity", "pattern", "active"])`.
3. For patterns with `changed-files` scope, audit only changed files against violation signals.
4. For patterns with `full-repo` scope, audit the full scope.
5. Report violations as `ck_finding(category: "continuity", severity: rule_severity)`.
6. End with a stable summary line matching the pattern:

```
CONTINUITY_RESULT: pass|fail
PATTERNS_CHECKED: <n>
VIOLATIONS: <n>
```

## Operating principles

1. **Code wins over docs.** Start from actual implementations, not documentation.
2. **CK memory wins over inference.** Read recorded patterns before making claims. If memory contradicts current code, report the conflict.
3. **Do not invent canonical patterns.** If unsure which file is canonical, ask the user. Point to files, not abstract preferences.
4. **Record decisions.** After the user identifies canonical examples, save in CK memory so future sessions inherit it.
5. **Prefer narrow scope first.** Audit changed files or provided paths before scanning the whole repo.
6. **Separate detection from fixing.** First report violations. Then fix only what's clearly implied by pattern rules.
7. **Avoid shallow text matching.** Use `ck_fs_grep` to find candidates, but verify structure by reading relevant files.
8. **Respect baselines.** If a pattern has known legacy drift, don't report it as a new violation.

## Useful search tactics

```bash
# Find pattern candidates
ck_fs_find --query "ComponentName" --path lib/

# Search for violation signals
ck_fs_grep --query "import { useState }" --path lib/app/

# List changed files for CI scope
ck_git_diff --base-ref origin/main...HEAD

# Find related implementations
ck_fs_find --query "*.tsx" --path lib/app/screens
```

## Output style

Be direct and actionable. Never dump raw search results. Always distinguish:

- **Confirmed canonical:** file paths with evidence
- **Inferred but unconfirmed:** labeled as such
- **Violations that should be fixed:** specific files + issue + expected shape
- **Intentional exceptions:** known drift, not actionable
- **Open questions:** what needs human input

If no violations found, say:

> Continuity check passed for `<pattern>/<scope>`.

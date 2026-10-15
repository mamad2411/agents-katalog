---
name: assemble-panel
description: "Use when another skill or agent needs a review panel assembled, retained, or converged — invoked by /review-loop, /plan-review, and code-reviewer, not directly by users."
---

# Assemble Panel

Centralizes reviewer selection and loop governance. Callers invoke this via the Skill tool to get a panel and policy back — they handle dispatch themselves. This skill produces data. It never dispatches agents or modifies files.

## Integration Contract

Callers provide:
- `scope`: a plan file path OR a git diff (the artifact under review)
- `overrides` (optional): `{ include: [], exclude: [] }`

This skill returns (as structured text the caller parses):
- `panel`: ordered list of reviewer agent names
- `policy`: gate, cap, and the algebra below

If this skill is unavailable, callers fall back to `[technical-editor, code-reviewer]` with gate=P2, cap=3.

**Cross-tool note:** Codex/Cursor cannot invoke skills via the Skill tool. Read this file directly (`.claude/skills/assemble-panel/SKILL.md`) and apply the policy algebra inline.

## Policy Algebra (frozen — do not modify, version: 1)

```
DEFAULTS:
  gate    = P2                       # fix P0-P2, record P3+
  cap     = 3                        # max rounds before escalate
  always  = [technical-editor]       # expandable, never reducible

ASSEMBLE(scope: plan_file | diff):
  panel = always
        + select_by_scope(file_types(scope))
        + select_by_keywords(body(scope))
        + overrides.include
        - overrides.exclude            # cannot remove `always` members

RETAIN(reviewer, round_findings):
  keep(reviewer) while round_findings.any_above(gate)

EXPAND(panel, prior_scope, current_scope):
  new_coverage = file_types(current_scope) - file_types(prior_scope)
  panel += select_by_scope(new_coverage) when new_coverage

CONVERGE(round, panel, cap):
  APPROVE   when all(reviewer.done for reviewer in panel)
  ESCALATE  when round >= cap
  EXIT      when any(reviewer.verdict == DROP)
  continue  otherwise

ESCALATE_RECURRING(finding, rounds_present):
  finding.severity += 1 when rounds_present >= 2
```

## Scope-to-Reviewer Map

Used by `select_by_scope(file_types)`:

| File pattern | Reviewer |
|---|---|
| `.ts`, `.js`, `src/`, `tests/` | code-reviewer |
| `.yml`, `.github/workflows/` | code-reviewer, security-auditor |
| `.sh`, `scripts/`, `hooks/` | code-reviewer, security-auditor |
| `.md` (plans, ADRs, docs) | architect-reviewer |
| `*.css`, `*.tsx`, UI components | design-reviewer, accessibility-tester |
| `sync.sh`, `AGENTS.md`, `config.toml`, skills | codex-specialist |
| `*.pem`, `*.key`, secrets patterns | security-auditor |

When multiple patterns match, union all reviewers. Duplicates collapsed.

## Keyword-to-Reviewer Map

Used by `select_by_keywords(body)`:

| Keyword / phrase | Reviewer |
|---|---|
| "architecture", "ADR", "system design", "plan" | architect-reviewer |
| "security", "auth", "token", "PAT", "OIDC" | security-auditor |
| "WCAG", "accessibility", "a11y", "aria" | accessibility-tester |
| "UI", "component", "layout", "design system" | design-reviewer |
| "docs", "research", "ecosystem", "reference", "educational" | fact-checker |
| "Codex", "cross-tool", "sync.sh" | codex-specialist |

Keywords are case-insensitive substring matches against the scope body.

## Override Rules

- `overrides.include` appends reviewers unconditionally.
- `overrides.exclude` removes reviewers EXCEPT those in `always`. Attempting to exclude an `always` member is silently ignored.
- Invalid reviewer names are rejected with an error listing valid names.

## Failure Modes

- **Scope empty or unreadable**: return `always` panel only, warn caller.
- **No file types detected**: fall back to keyword matching only. If no keywords match either, return `always` panel.
- **Caller requests cap > 5**: clamp to 5. Non-negotiable ceiling.
- **Panel exceeds 5 members**: warn caller — likely a sign the change is too broad.
- **Reviewer unavailable at dispatch time**: caller skips that reviewer and notes the gap. This skill assembles; callers dispatch.

## Output Format

```
PANEL: technical-editor, code-reviewer, security-auditor
GATE: P2
CAP: 3
ALWAYS: technical-editor
NOTE: codex-specialist included — scope touches sync.sh
```

One `NOTE` line per non-obvious selection decision. Callers surface these in review summaries.

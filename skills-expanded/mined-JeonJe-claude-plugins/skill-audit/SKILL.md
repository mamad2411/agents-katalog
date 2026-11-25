---
name: skill-audit
description: "Use when the user explicitly asks to audit or quality-check Claude skills/commands for publish readiness (for example: 'skill audit', 'audit this skill', 'check skill quality'). Scores against Anthropic skill best practices and returns concrete fixes. Do not use for general code review, document polishing, or feature debugging."
---

# Skill Audit

Audit Claude skills and commands before sharing. Applies Anthropic skill best practices and reports quality, safety, and publish readiness.

Source of truth:
- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices

## Input
- `$ARGUMENTS`: Optional target name and/or flags.

## Argument Parsing Rules
Parse `$ARGUMENTS` in this order:
1. Detect supported flags first.
2. Remaining non-flag token (if any) is treated as target name.
3. If multiple non-flag tokens exist, join with spaces as the target name.

Supported flags:
- `--include-user-home`: Include `~/.claude/*` paths in audit scope.
- `--project-only`: Force project-only scope (default).

Conflict handling:
- If both flags present, `--project-only` wins.
- Unknown flags MUST be reported as warnings and ignored.

## Scope Defaults
Default behavior is privacy-safe for sharing prep:
- Scan project-local paths only: `.claude/skills/`, `.claude/commands/`

Optional expanded scan (explicit opt-in):
- `--include-user-home`: also scan `~/.claude/skills/`, `~/.claude/commands/`

## Use Cases

| Input | Scope | Output |
|---|---|---|
| `/skill-audit` | All project skills/commands | Summary table + prioritized fixes |
| `/skill-audit my-skill` | Single target (deep audit) | Detailed checklist + rewrite suggestions |
| `/skill-audit --include-user-home` | Project + user-level paths | Cross-scope quality report + conflict notes |

## Files
- **read**: `rubric/scoring.md` (6-category rubric + scoring consistency rules)
- **read**: `rubric/security-checks.md` (security/sharing checks + anti-patterns)
- **read**: `templates/output-format.md` (output format template)

## Grades
- **A (90-100)**: Ready to share
- **B (80-89)**: Share after minor fixes
- **C (70-79)**: Needs targeted rewrite
- **D (<70)**: Redesign before sharing

## Workflow
1. Discover targets from selected scope.
2. Detect naming/trigger collisions.
3. **Read** `rubric/scoring.md` and score with the 6-category rubric.
4. Apply anti-pattern deductions from `rubric/security-checks.md`.
5. Run security/share checks.
6. Verify score bounds (0-100). If out of range, clamp to 0-100 and report calculation error.
7. Report findings using `templates/output-format.md`.
8. If user requests fixes: apply → re-audit → verify score improved → repeat until grade A or user satisfied.

## Related Commands
- `skillbook`: usage stats and inventory context
- `doc-polish`: final documentation cleanup after content fixes

## Done When
- Score calculated per rubric and grade assigned for each target
- Summary table + Recommended Fixes output in priority order
- On fix request: apply fix → re-audit → confirm score improved
- Error: no skills/commands found at target path → ask user to verify path
- Error: rubric file missing → ask user to verify path
- Error: score out of range → clamp to 0-100 and report calculation error

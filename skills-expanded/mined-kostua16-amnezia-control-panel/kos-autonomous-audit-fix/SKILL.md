---
name: kos-autonomous-audit-fix
description: Run the audit-fix code audit (debt/smells/missing tests), implement TARGETED fixes, verify with npm test/lint/prettier, and return fixed_findings + manual_findings JSON — the agent does NOT run git/gh or push (the workflow handles commit/PR/reconcile).
user-invocable: true
when_to_use: "When the audit-fix workflow runs its autonomous code audit-and-fix cycle, or when such a run failed (disk / over-broad fix / missing findings output)."
category: utilities
argument-hint: "[scope or 'full']"
keywords: [audit, audit-fix, tech-debt, code-smell, fixed-findings, manual-findings, no-push, disk]
related: [kos-zai-agent-runtime-contract, kos-runner-disk-hygiene, kos-claude-turn-budget, kos-gh-automation-tooling, kos-zai-run-failure-prevention]
metadata:
  author: kos-workflow-improvement
  attribution: distilled from audit-fix.yml prompt + disk-exhaustion failure (run 28097503249)
  license: repo
  version: "1.1"
---

# Idea

`audit-fix` runs `/gsd:audit-fix`: audit the repo for debt/smells/missing tests, implement **targeted** fixes, verify, stop when findings are addressed. The agent **edits files only** — it does **NOT** run git or gh, does **NOT** push/commit/open a PR (the workflow handles commit/PR/reconcile). Run knowledge: the one hard failure observed was runner disk exhaustion during setup (a workflow/runner concern, not the agent's logic). Note: this skill is for `audit-fix` (code audit). `audit-auto-prs` is a different workflow — it audits automation **PRs**, not code.

## When to invoke this skill directly
- Running the `audit-fix` autonomous code audit-and-fix cycle.
- An audit-fix run failed on disk / produced an over-broad diff / omitted the findings output.

## References
- `audit-fix.yml` prompt (`/gsd:audit-fix`; do NOT run git or gh; never `node_modules` paths; don't search `node_modules`/`.next`/`src/generated`/coverage).
- `.github/workflows/scripts/classify-audit-fix.cjs`, `reconcile-audit-issues.sh` (workflow steps, not agent actions).
- `.github/actions/ensure-disk-space/` (workflow/runner concern — see [[kos-runner-disk-hygiene]]).
- [[kos-zai-agent-runtime-contract]].

## Communication Style
Findings → targeted fix per finding (file:line) → verify → the JSON. No push, no git/gh.

## Core Principles
YAGNI / KISS / DRY. One finding → one minimal change. Verify with the prompt's commands. Report unfixed findings honestly — never silently drop them.

## Hard rules (the prompt)
- **Do NOT run `git` or `gh`. Do NOT commit/push/merge/open a PR** — the workflow handles that.
- Use `npm run <script>` / `npx <tool>` only — never `node_modules/.bin` or `./node_modules/...`.
- Do NOT search ignored/generated/dependency dirs (`node_modules`, `.next`, `src/generated`, coverage).
- Narrow low-risk fixes; broad/schema/package/API-route/workflow/planning changes are allowed when needed but become manual-only PRs.
- If no worthwhile fixes → make no file changes.
- Once verification passes, **stop** — don't run alternate test entrypoints.

## Output contract (enforce)
In the final response and structured output:
- `fixed_findings[]` — every finding you fixed.
- `manual_findings[]` — every unfixed/manual-only finding, each with `finding_id`, `severity`, `summary`, `details`, `files` (so the workflow can create a follow-up issue).
- A Markdown `### Manual-only findings` section, one bullet per unfixed finding: `- **F-02 (medium):** details`.

**Verify** with `npm test`, `npm run lint`, and targeted `npx prettier --check …`.

## Failure modes to avoid
- **Running git/gh or pushing** — forbidden.
- **Over-broad fixes** — a "smell" becoming a refactor; keep each fix to the finding.
- **No verify** — always run the prompt's check.
- **Silent drops** — list every unfixed finding in `manual_findings`.
- **Disk** — if the run dies with `No space left on device`, that's a runner-disk issue (workflow/runner), not your logic; flag it.

## Process Flow (Authoritative)
1. Audit → concrete findings (file:line).
2. Minimal fix per finding (within scope + budget).
3. Verify (`npm test` + lint + prettier --check).
4. Stop when findings addressed.
5. Return `fixed_findings` + `manual_findings` + the `### Manual-only findings` section. Do not push.

## Output Format
```text
FINDINGS: n (debt=a smells=b tests=c)
FIXED: <file:line per fix>  DIFF=<files>
VERIFY: lint=ok test=ok prettier=ok
MANUAL: <F-id (severity): summary> …
```
(plus the structured `fixed_findings`/`manual_findings` JSON)

## Critical Constraints
- Never run git/gh, never push/open PR — the workflow does.
- Never ship an audit fix without verification.
- Never silently drop a finding — it goes in `manual_findings`.
- This skill is for `audit-fix` (code audit); `audit-auto-prs` (PR audit) does not use it.

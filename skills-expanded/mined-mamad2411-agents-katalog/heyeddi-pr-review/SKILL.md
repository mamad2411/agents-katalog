---
name: heyeddi-pr-review
description: Reviews submitted PRs using only committed changes — product fit, docs drift, engineering quality, test coverage, and pre-merge gate. Use when approving a PR, doing reviewer QA, or self-checking before requesting review. Not for replying to review comments (use heyeddi-pr-respond).
version: 1.0.0
disable-model-invocation: true
---

# HeyEddi PR Review

**Submitted PR review workflow** — judges only committed changes (`base...head`), not local WIP.

You are the **reviewer** workflow. Scope every judgment to the PR diff (`base...head`). Ignore uncommitted files.

**Artifacts:** `.heyeddi/docs/pr-<N>-review.md` — never repo root.

## When to use

| Situation | Who |
|-----------|-----|
| Reviewer approving a teammate's PR | QA / lead |
| Author self-check before requesting review | Author |
| PM/eng sign-off on product + docs alignment | `@heyeddi-product` delegates here for PR scope |

**Not this skill:** responding to human review comments → `@heyeddi-pr-respond`.

## Subagents (default)

See `reference/subagents.md`. Main chat owns the verdict; delegate fetches and scans via **Task `shell`**.

## Mandatory pipeline

Read **`reference/review-checklist.md`**.

```
fetch_pr_context --pr <N>              → committed diff + changed files
check_doc_drift --pr <N>               → product.md / design.md / engineering docs
audit_pr_changes --pr <N>              → engineering + test gaps on changed files only
load_product_context                   → @heyeddi-product (read JSON; scope to touched routes)
check_features                         → AC vs code when routes touched
conditional delegates (changed paths):
  **/*.vue                             → @visual-auditor, @no-duplicate-ui, @primevue-openprops-architect
  **/composables/**                    → @composable-patterns
  backend/**                           → @engineering-excellence audit_engineering
pre_merge_gate                         → tests, build, types (hard gate)
write_pr_review --pr <N> --force       → scaffold + merge tool JSON into report
→ YOU fill: Summary verdict, Product fit, PM judgment
verify_pr_review --pr <N> --check      → report complete before posting
```

## Verdict (you write)

| Verdict | When |
|---------|------|
| **Approve** | Gates pass; docs aligned; new behavior tested; no blockers |
| **Request changes** | Docs drift, missing tests, product/AC gaps, gate failures |
| **Block** | Breaks flagship route, security concern, or contradicts `product.md` |

Optional: post GitHub review via `gh pr review` when user asks — default is report in `.heyeddi/docs/` only.

## Never

- Review uncommitted working tree changes
- Approve without `pre_merge_gate` on required checks
- Skip doc drift when PR changes routes or public API
- Approve new user-facing behavior without test evidence (unit, integration, or documented manual AC)

## Related skills

| Skill | Role in this workflow |
|-------|----------------------|
| `@heyeddi-product` | Product context, feature matrix, AC |
| `@engineering-excellence` | Deeper audit when `audit_pr_changes` flags issues |
| `@pre-merge-gate` | Final hard gate |
| `@heyeddi-pr-respond` | **After** review — address human feedback |
## When the task is complete — suggest next skills

When you have **finished the user's request** for this skill (not after every tool call or subagent phase), suggest what to run next:

1. Run:

   ```bash
   python .agents/skills/heyeddi-orchestrator/scripts/suggest_next_skill.py --current-skill heyeddi-pr-review --project-root .
   ```

   Add `--route /path` if you worked a specific route.

2. Include the script's **`### Next step`** block in your **final** reply. The user copies the **Prompt** line into chat (e.g. `@heyeddi-design craft /settings`).

Pass `--mode shape` (or `craft`, `audit`, etc.) when you know which sub-command just finished.

See `@heyeddi-orchestrator` → `reference/next-skill-handoff.md`.


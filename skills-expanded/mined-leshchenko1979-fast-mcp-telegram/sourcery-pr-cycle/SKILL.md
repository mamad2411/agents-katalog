---
name: sourcery-pr-cycle
description: >-
  Runs the PR creation and Sourcery AI review loop until merge-ready: open PR
  with gh, poll checks and comments, fix blocking issues, push, re-request
  review, repeat. Use when the user asks to create a PR, run the Sourcery cycle,
  address Sourcery review comments, or get a branch merge-ready after review.
disable-model-invocation: true
---

# Sourcery PR Cycle

End-to-end loop: **open PR → Sourcery review → fix → push → re-review → repeat → merge**.

For **triage and status tables** on individual comments, read [sourcery-pr-review-analysis](/Users/leshchenko/.claude/skills/sourcery-pr-review-analysis/SKILL.md). This skill is the **workflow loop** only.

## When to use

- User asks to create a PR or run the Sourcery review cycle
- Post-implementation work is done and the branch needs merge readiness
- Sourcery left comments and the user wants fixes + another review pass

## Cycle checklist

Copy and track progress:

```
PR + Sourcery cycle:
- [ ] 1. Pre-push: exit tests green
- [ ] 2. Create PR (gh push + gh pr create)
- [ ] 3. Wait / poll Sourcery (checks + comments)
- [ ] 4. Triage comments; fix blocking issues
- [ ] 5. Pre-push: exit tests green again
- [ ] 6. Commit + push fixes
- [ ] 7. Request new Sourcery review
- [ ] 8. Repeat 3–7 until clean
- [ ] 9. Closeout + merge when ready
```

---

## 1. Pre-push gate (every push)

Run **exit tests/commands from the approved plan** before every commit and push. Do not push with failing exits.

If fixes changed behavior, re-run exits after fixes and before commit.

---

## 2. Create the PR

Use `gh` for all GitHub operations. Before creating the PR, gather branch state **in parallel**:

```bash
git status
git diff
git log --oneline -10
git diff main...HEAD   # or master — use repo default base
```

Check whether the branch tracks remote and is up to date.

**Push and create** (sequential):

```bash
git push -u origin HEAD

gh pr create --title "the pr title" --body "$(cat <<'EOF'
## Summary
- ...

## Test plan
- [ ] ...

EOF
)"
```

Return the PR URL to the user.

**Commit rules:** Only commit when the user asks. Never commit secrets (`.env`, tokens, `acl.dev.yaml` with real bearers).

---

## 3. Wait for / check Sourcery

Sourcery runs after the PR exists. Poll until the review finishes or stale.

**CI / check status:**

```bash
gh pr checks <N>
```

**Review comments** (issue-level, from `sourcery-ai[bot]`):

```bash
gh api repos/{owner}/{repo}/pulls/<N>/comments --jq '.[] | select(.user.login=="sourcery-ai[bot]") | .body'
```

**Grouped review body** (top-level suggestions):

```bash
gh api repos/{owner}/{repo}/pulls/<N>/reviews --jq '.[] | select(.user.login=="sourcery-ai[bot]") | .body'
```

Wait several minutes after triggering before expecting new results. Full fetch/triage commands: [reference.md](reference.md).

---

## 4. Triage and fix

**Default: always fix post-review blocking issues** unless the user explicitly narrows scope.

| Priority | Types | Action |
| -------- | ----- | ------ |
| 1 — Blocking | `bug_risk`, security, correctness | Always fix |
| 2 — Quality | `testing` on changed code | Fix when straightforward |
| 3 — Optional | `complexity`, `suggestion`, style | Fix only if user said "do all"; otherwise ask or skip with brief reason |

**Version bumps:** If Sourcery flags a version bump, **ask the user** before changing version files. Do not bump silently.

Use [sourcery-pr-review-analysis](/Users/leshchenko/.claude/skills/sourcery-pr-review-analysis/SKILL.md) to build a status table (Fixed / Not done / Skipped) before implementing.

After fixes, run **code-reviewer** (readonly) when the diff is non-trivial — aligns with [implementation-workflow step 5 closeout](.cursor/rules/implementation-workflow.mdc).

---

## 5. Commit and push fixes

Only when the user asked to commit:

```bash
git status
git diff
git log --oneline -5
git add <relevant files>
git commit -m "$(cat <<'EOF'
fix: address Sourcery review on <topic>

EOF
)"
git push
```

Re-run exit tests before push (step 1).

---

## 6. Request another Sourcery review

After pushing fixes, trigger a fresh review:

```bash
gh pr comment <N> --body "@sourcery-ai review"
```

Then return to **step 3** (poll checks and comments).

---

## 7. Repeat until merge-ready

Loop **3 → 4 → 5 → 6** until:

- `gh pr checks` are green (or only known/flaky exceptions the user accepts)
- All **blocking** Sourcery items are fixed or explicitly deferred by the user
- Exit tests pass on the final branch state

Optional refactors left open: document in PR comment or triage table with reason.

---

## 8. Phase close — merge

Merge when checks are green and blocking review items are resolved.

**Closeout** (matches [implementation-workflow step 5](.cursor/rules/implementation-workflow.mdc)):

| # | Check |
| - | ----- |
| 1 | Diff matches approved plan; no unapproved scope |
| 2 | Re-run exit commands on final state |
| 3 | Fix blocking findings only; no scope creep |
| 4 | Update docs / memory bank if the plan required it |

Merge via user-preferred method (`gh pr merge`, squash, etc.) when the user asks.

---

## Related skills

| Skill | Role |
| ----- | ---- |
| [sourcery-pr-review-analysis](/Users/leshchenko/.claude/skills/sourcery-pr-review-analysis/SKILL.md) | Triage tables, fetch patterns, categorization |
| [release-notes](.cursor/skills/release-notes/SKILL.md) | Version bump + release after merge (not part of this loop); before Telegram posts, see release-notes CI gate |
| [implementation-workflow](.cursor/rules/implementation-workflow.mdc) | Plan approval, exit tests, step 5 closeout |

## Additional resources

- [reference.md](reference.md) — gh command snippets and poll helpers

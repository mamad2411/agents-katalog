---
name: githubpr
description: Manage the GitHub PR lifecycle — create a branch with a kebab-case descriptive name, commit with Gitmoji + Conventional Commits messages, push, open a PR for review, post the loop results (review scores, QA, gates) and QA videos as a PR comment, and poll CI. NO automatic merge — merging is always an explicit user decision. Use this skill whenever the user mentions creating a PR, opening a pull request, or pushing a branch for review. Also trigger when the user asks to wait for CI or merge a PR (merge only on explicit user request).
---

# GitHub PR Skill

Lifecycle: branch → push → PR → CI. **Stop there — no automatic merge.**

## 1. Branch naming convention

```
<simple-description>
```

Rules:
- 2–5 words, kebab-case, lowercase, no articles — e.g. `add-user-auth`
- If the work references a ticket/issue anyway (optional), prefix it: `PROJ-123/add-user-auth` — but no ticket is required

Valid examples:
```
add-user-auth
fix-null-pointer-login
update-dependencies
```

Create and switch to the branch:
```bash
git checkout main && git pull origin main
git checkout -b add-user-auth
```

## 2. Commit message convention (Gitmoji + Conventional Commits)

Every commit message MUST start with a Gitmoji emoji followed by a conventional-commit subject:

```
<emoji> <type>(<scope>): <subject>
```

Examples:
- `✨ feat: add user authentication endpoint`
- `🐛 fix: null pointer on login redirect`
- `✅ test: e2e specs for resource crud`

Gitmoji table:

| Emoji | Code | Type | Use for |
|-------|------|------|---------|
| ✨ | `:sparkles:` | `feat` | New feature |
| 🐛 | `:bug:` | `fix` | Bug fix |
| 📝 | `:memo:` | `docs` | Documentation |
| ♻️ | `:recycle:` | `refactor` | Refactor code |
| ⚡️ | `:zap:` | `perf` | Performance |
| ✅ | `:white_check_mark:` | `test` | Tests |
| 🔧 | `:wrench:` | `chore` | Configuration |
| 🚀 | `:rocket:` | `ci` | Deployment |
| 🎨 | `:art:` | `style` | UI/Style |
| 🔥 | `:fire:` | `chore` | Remove code/files |
| 🚑️ | `:ambulance:` | `fix` | Critical hotfix |
| ⬆️ | `:arrow_up:` | `build` | Upgrade dependencies |
| ⬇️ | `:arrow_down:` | `build` | Downgrade dependencies |
| 🏗️ | `:building_construction:` | `refactor` | Architecture changes |

Rules:
- Use the emoji character itself in the message (quote the message in shell: `git commit -m "✨ feat: add user auth"`)
- One commit = one logical change with its matching emoji — never a bare message without an emoji
- Scope is optional: `✨ feat(auth): ...`
- On loop-back iterations, the fix commit uses 🐛/🚑️ (bug) or ♻️ (refactor) — never ✨ again

## 3. Create the PR

→ Load `references/pr-template.md` for the `gh pr create` command, the PR body template, and the full agent flow script.

> Always open as **draft** by default. Mark as "ready for review" only once CI is green.

## 4. Post loop results comment (when part of a loop)

When the PR closes an implementation loop (`feature-implementation`, `loop-implementation-review`, …), post the **full loop report as a PR comment** — everything in markdown: gates, code review scores + full findings, QA results, bug tickets, spec, loop timeline, plus the **QA replay videos attached inline**. The comment must be self-sufficient (readable by a reviewer with no access to the local machine).

**QA evidence is a HARD GATE, not a nice-to-have:**
- **Feature with a frontend** → the PR comment MUST show the QA replay videos attached inline (`gh pr comment --attach` + `![]()` embeds, per `references/results-comment.md` §4). A front-feature PR comment without inline videos is an INCOMPLETE PR step — do not mark the step done.
- **Backend-only feature** → the PR comment MUST embed the curl evidence (exact commands + actual responses) from `<LOOP_DIR>/qa/curl-logs.json` in a details block.
- **After posting, VERIFY** (per `references/results-comment.md` §5): every `![]()` video reference must be rewritten to a `github.com/user-attachments/...` URL. A local path left in the body, or zero uploaded videos on a front feature = attach FAILED = PR step NOT done.

→ Load `references/results-comment.md` for the results collection checklist, the comment template, the 65,536-char split rule, and the video attachment procedure (`gh pr comment --attach`).

Order: post after `gh pr ready` and **before** CI polling — all loop artifacts already exist at PR time, and the evidence must be visible during review.

## 5. Check CI status

```bash
# Quick overview
gh pr checks <PR_NUMBER>

# JSON output for agent parsing
gh pr checks <PR_NUMBER> --json name,state,conclusion
```

Possible states:
- `SUCCESS` → ✅
- `IN_PROGRESS` / `QUEUED` → ⏳ wait
- `FAILURE` → ❌ stop, investigate

## 6. CI polling (agent script)

→ Load `references/ci-polling-script.md` for `wait-ci.sh` (polls `gh pr checks`, exit codes: 0=green, 1=red, 3=timeout).

## 7. Merge (ONLY on explicit user request)

**Never merge automatically — not when CI is green, not as part of an agent loop.** Merging is always an explicit user decision. Only when the user explicitly asks to merge, load `references/merge-commands.md` and follow it:
- **A. Feature → `dev`** (or `main` if no `dev`): `gh pr merge --merge`
- **B. `dev` → `main`**: **NEVER use `gh pr merge`**. Use CLI `git merge --ff-only dev` + `git push origin main` (true fast-forward, no hash rewriting).

## 8. Full agent flow

→ Load `references/pr-template.md` for the end-to-end bash script (branch → push → PR → ready → loop results comment → wait-ci). Stop after CI is green — no merge step.

## Agent rules

- **No automatic merge.** After CI is green, report the PR status and STOP — the user decides. Merge only on an explicit user request, then follow `references/merge-commands.md`
- **Feature → `dev`**: use `gh pr merge --merge`
- **`dev` → `main`**: **never use `gh pr merge`**. Use CLI `git merge --ff-only dev` + `git push origin main` (see `references/merge-commands.md`)
- **Never force-push `dev` or `main`**
- **Never use `git reset --hard`.** It destroys uncommitted work irreversibly. To undo uncommitted changes, ask the user first, then prefer `git stash`, `git restore <file>`, or `git checkout -- <file>`. To move a branch, use `git reset --soft` / `git reset --mixed` (never hard). If a destructive git operation seems necessary, STOP and ask the user.
- On CI failure: log the branch and **continue** to the next one — do not block the pipeline
- **Commits are Gitmoji + Conventional Commits.** Every commit starts with its Gitmoji emoji + `<type>(<scope>): <subject>` (see §2 table). Never commit without an emoji.
- **Loop results comment.** When the PR comes from an implementation loop, post the full loop report as markdown in the PR comment(s) — code review scores + full findings, QA, bug tickets, spec, timeline, gates — with the QA evidence embedded: **QA replay videos attached inline (MANDATORY for any feature with a frontend — hard gate)** and curl evidence (commands + actual responses from `<LOOP_DIR>/qa/curl-logs.json`) for backend-only features, per `references/results-comment.md`, after `gh pr ready` and before CI polling. Comment bodies are capped at 65,536 chars by GitHub: split into sequential `part N/M` comments if needed. `--attach` requires `gh` ≥ 2.99.0 — verify with `gh --version`; on older versions post the comment WITHOUT videos, reference the local `qa-video-report.html` path, warn the user explicitly, and tell them to upgrade (`brew upgrade gh`). **Post-verification is mandatory:** confirm every `![]()` was rewritten to a `github.com/user-attachments/...` URL (`gh pr view --json comments`); if a local path remains or no video uploaded on a front feature, the PR step is NOT done — fix the paths and re-post

## References
- `references/pr-template.md` — `gh pr create` command, PR body template, full agent flow script
- `references/results-comment.md` — loop results PR comment: collection checklist, comment template, QA video attachment via `gh pr comment --attach`
- `references/ci-polling-script.md` — `wait-ci.sh` polling script with exit codes
- `references/merge-commands.md` — merge commands for both scenarios (feature→dev merge commit, dev→main fast-forward)
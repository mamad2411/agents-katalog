---
name: pr-fix-agent
description: >-
  Own one PR's full ship bar: bot/human threads, CI, synthesis, gates, squash merge.
  Babysit patterns through WORKFLOW.md steps 4–7 and post-merge handoff.
  babysit skill etc must always address PR bot feedback where appropriate.
---

# PR fix agent

You own **one assigned open PR's** full ship bar: CI failures, bot/human inline threads, feedback synthesis, gates, **squash merge**, and post-merge handoff — until merged on `main` or chief reassigns. Chief spawns **one dedicated pr-fix/babysit worker per open PR**; you are that worker for your PR number.

**Authoritative ship bar:** `WORKFLOW.md` steps 4–7 (especially **5b synthesis**, **step 6 thread closure**, **step 7 merge**).

**Non-negotiable:** babysit skill etc must always address PR bot feedback where appropriate. Advisory bots still require implement / defer / decline + resolve on every substantive thread before merge. Green CI never replaces that. Shared contract: `rules/respond-to-each-review-comment.mdc`, `rules/pr-review-bot-replies.mdc`, and `WORKFLOW.md` steps 5b–6.

**Patterns:** babysit triage loops (same ship-bar contract above); this skill owns the full ship bar.

**Reports to:** chief agent (one worker per PR number). Orchestrator spawns/resumes you per PR but does not substitute for your thread-closure loop. You do not spawn chief.

## Environment URLs (do not hardcode)

Read `.cursor/project.json` or repo `WORKFLOW.md` for `{DEPLOY_URL}`, `{VERIFY_COMMAND}`, and acceptance base URLs — do not introduce new hardcoded hosts in review replies.

## Invocation phrases

- **"run pr fix"** (optionally: *for PR #N*)
- Chief delegate: *Follow `.cursor/skills/pr-fix-agent/SKILL.md` on PR #N; branch `agent/<slug>`.*

## Path locks

| Scope | Rule |
|-------|------|
| Single PR | Only files in that PR's intended partition |
| Branch | `agent/<slug>` matching `gh pr view` head — verify before push |
| Forbidden | Unrelated paths from other open PRs; `main` direct commits unless user hotfix |

## When to run

- Open PR with failing CI, unresolved review threads, or bot findings.
- After `wait-for-bots` exit 0 — begin **5b** synthesis before replying.
- Chief assigns one babysit worker per PR (no five parallel pr-fix on same PR).

## Mandatory gates (before merge)

```sh
npm run wait-for-bots -- --pr <n>          # exit 0 required
npm run pr:bot-feedback-check -- --pr <n>  # exit 0 required
gh pr checks <n> --required                # single non-polling read (WORKFLOW.md step 4)
```

**Never** recommend merge on "CI green" alone.

## Workflow

### 1. Orient

```sh
gh pr view <n> --json title,state,headRefName,baseRefName,statusCheckRollup
gh pr checks <n>
git fetch origin && git checkout <head-branch> && git rebase origin/main  # if behind
```

### 2. Merge conflicts

Resolve preserving branch intent + `main`; if intents conflict, stop and ask chief/user with evidence.

### 3. After `wait-for-bots` exit 0 — synthesis (step 5b)

1. Fetch all threads: `gh pr view <n> --comments`, review APIs, Files tab on GitHub.
2. **Read every thread before replying to any.**
3. Post **one** `## Feedback plan` on the PR (implement / defer / decline per thread).
4. Single push with code fixes, then **in-thread** replies.

### 4. Thread closure (step 6)

Every **substantive** thread gets an in-thread disposition (gate is per-thread):

- `implemented in <sha>` / `deferred — <reason>` / `declined — <reason>`

If the inline reply API is unavailable: list each thread under `## Feedback responses` in the PR body, then still **resolve** every affected thread.

```sh
npm run pr:bot-feedback-check -- --pr <n>
```

### 5. Push and re-watch CI

Scoped fixes only. Do not weaken CI workflows to pass. Re-run checks until green + gate exit 0.

### 6. Merge (step 7)

When all gates exit **0** and substantive threads are closed:

```sh
npm run pr:bot-feedback-check -- --pr <pr-number>   # must exit 0
npm run pr:merge -- --pr <pr-number>                # or gh pr merge --squash
npm run close-loop:check -- --pr <pr-number>
npm run close-loop:check -- --post-merge-gap
```

**Never** merge on CI green alone. Global mirror check applies when the PR touches canonical global features (see `global-feature-sync.mdc`).

### 7. Post-merge handoff (steps 8–9)

After merge: run project `{DEPLOY_COMMAND}` and `{VERIFY_COMMAND}` from `WORKFLOW.md` / `.cursor/project.json`.

## Bot handling

| Bot key | GitHub login (typical) |
|---------|-------------------------|
| gemini | gemini-code-assist[bot] |
| codex | chatgpt-codex-connector[bot] |
| sourcery | sourcery-ai[bot] |
| qwen | github-actions[bot] (`<!-- qwen-code-review -->`) — optional; a missing review must not block |

After @mentioning required bots: `npm run wait-for-bots -- --bot-tag` then loop until exit 0. Do not wait for Qwen.

## Return format

| Item | Status |
|------|--------|
| PR # | URL |
| Feedback plan | posted Y/N |
| Threads closed | count / remaining |
| pr:bot-feedback-check | exit code |
| wait-for-bots | exit code |
| CI | green / failing checks |
| Merged | yes / no |

## Anti-patterns

- Merging with open substantive threads.
- Dismissing bot findings without per-item implement/defer/decline.
- Skipping Feedback plan / thread replies because reviewers are labeled advisory.
- Closing PR without merge without written user waiver.
- Editing files outside PR scope.

## Related

- Shared contract: `WORKFLOW.md`, `rules/respond-to-each-review-comment.mdc`, `rules/pr-review-bot-replies.mdc`
- Peer roles (by name only): workflow-orchestrator (queue), babysit (CI/conflict triage) — same bot-feedback non-negotiable

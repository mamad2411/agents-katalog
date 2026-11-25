---
name: opendirector-review
description: Review one OpenDirector pull request tip and report PASS, WITHHOLD, or REQUEST CHANGES. Use when the user invokes opendirector-review or asks for a PR or tip review; not for implementing the change, merging, force-pushing, or discussion of the skill itself.
---

# OpenDirector review

Review one pull request tip and post a short verdict in the room or chat.
The verdict is the review record. This repository has no signed-verdict
bot, attestation file, or extra status check; do not invent one.

Read the diff and the remote check runs. The PR body, commit messages, and
chat claims are claims, not evidence.

## Authority

This skill does not authorize merge, force-push, or bypassing a red
required check. A PASS means a Reviewer found the tip acceptable and
required CI is green on that SHA. Ping the Coordinator to merge. Do not
merge, enable auto-merge, dismiss failing checks, or push.

Creating or editing this skill does not review an open pull request.
Implementing a fix, closing an issue, or updating a PR requires a separate
request. Do not close unrelated issues. Do not add `Fixes` unless the tip
actually addresses that issue.

## Re-read guidance from the default branch

Fetch `origin/main` and read these files from that tree before reviewing.
A copy already in the conversation, the tip branch, or a stale checkout is
not a substitute.

- This skill: `.agents/skills/opendirector-review/SKILL.md`
- [AGENTS.md](../../../AGENTS.md)
- [CONTRIBUTING.md](../../../CONTRIBUTING.md) when the diff touches labels,
  submission requirements, or review process
- [docs/development/lessons.md](../../../docs/development/lessons.md) for
  every lesson the diff can trigger

When the diff touches checks or user-visible language, use the linked
docs instead of restating them: [validation](../../../docs/development/validation.md),
[CI failure patterns](../../../docs/development/ci-failures.md),
[bilingual interface](../../../docs/development/i18n.md), and the
architecture pages indexed from [docs/README.md](../../../docs/README.md).
Review the tip against the fetched default branch. If the tip is itself
the rule change, say so and review that change.

## Establish the tip

Record these from the remote before reading the narrative:

- Full tip SHA (PR head) and full base SHA (`origin/main` at review time)
- PR number and URL
- Linked issues, classified as `Fixes` or `Refs`. A bare mention, "related
  to", or `Fixes` on work that does not close the issue is a Refs-vs-Fixes
  finding. Missing auto-close intent is not a silent `Fixes`.
- Author association: internal (`OWNER`, `MEMBER`) or external / first-time
  (`COLLABORATOR`, `CONTRIBUTOR`, `FIRST_TIME_CONTRIBUTOR`, `FIRST_TIMER`,
  `NONE`, and any cross-repository head)

```bash
git fetch origin main
gh pr view <number> --repo ThinkFlowLab/OpenDirector --json \
  number,url,title,body,author,authorAssociation,headRefOid,baseRefOid,\
  baseRefName,isCrossRepository,maintainerCanModify,mergeable,mergeStateStatus
```

Check out or show that tip SHA. If local `HEAD` is not the tip, review the
fetched SHA, not the worktree. Read `headRefOid` again before posting. If
the tip moved, stop and use WITHHOLD. Do not finish against the old SHA.

## Inventory the diff

List paths against the merge base and read that diff:

```bash
git diff --name-status origin/main...<tip-sha>
git diff --stat origin/main...<tip-sha>
```

Use three dots so the inventory is the pull request, not the unrelated
history of main. Every changed path is in scope, including files the author
says are untouched.

## Issue fit

Read each linked issue, including its acceptance criteria and scope. PASS
requires the tip to satisfy that scoped acceptance. Extra product behavior
outside the issue is a finding. A docs or process change the user scoped
with no issue is not automatically a defect; say that no issue is linked.

## Architecture and contracts

When the diff touches creative capabilities, persistence, generation,
adoption, adapters, or user-visible text, check the matching principle in
AGENTS.md. Name the break and the section. Do not paste the principle.

- Capability equivalence: a business operation in scope exists for the UI
  and for the agent, under the same rules.
- The project is the source of truth: no second editable project in the
  browser, and no canvas-only business fact.
- Generation intent, execution facts, and current adoption stay separate.
- User-visible copy ships `zh-CN` and `en-US` together.
- Domain and application services own the rule; HTTP, UI, and tool
  adapters translate and present it.

Also apply lessons whose trigger matches the diff, and the CONTRIBUTING
checklist items the diff can violate (one concern, a failing-before test
for a behavior change, docs updated with the contract, no invented
provider evidence, no credentials in the diff).

## CI honesty

Required CI is the **Release checks** workflow
(`.github/workflows/ci.yml`, reusable job in
`.github/workflows/release-checks.yml`) plus any other required status on
the repository. Attribute a run only when its head SHA is this tip.

```bash
gh pr checks <number> --repo ThinkFlowLab/OpenDirector
```

Confirm the check run's SHA in the Actions URL or check-run payload. A
green run on an older head is not evidence for this tip.

- Green required checks on this SHA, and a clean merge against current
  main: eligible for PASS when the rest of the review is clean.
- Pending, queued, in progress, expected but missing, or otherwise
  unsettled: WITHHOLD. Unsettled Release checks are not PASS.
- A failed required check is not PASS. REQUEST CHANGES when the log shows
  a defect in the tip. WITHHOLD when you cannot yet separate a flake from
  a regression; use the CI failure notes. Do not rerun or bypass red CI
  from this skill.
- `mergeStateStatus` of `BEHIND`, `DIRTY`, or `UNKNOWN`, or `mergeable`
  of `CONFLICTING`: WITHHOLD, and say that a rebase onto current main is
  needed. Do not record that as PASS.
- Nightly lanes do not stand in for Release checks unless the change
  claims that lane.

## Tests

For a claimed fix, require a test that fails on the previous revision.
Absence of that coverage is REQUEST CHANGES. Docs-only and skill-only
diffs do not need unrelated model, media, or browser tests.

`Ran:` lists commands and CI jobs actually observed on this tip SHA.
`Not run:` lists relevant checks nobody ran. A passing local tree that is
not this SHA does not count. Never invent a green run. Distinguish a
model double from a real provider call; do not upgrade either.

- For a user-visible tip (UI, canvas, provider settings, generation
  flows, and similar), require screenshots, a short screen recording, or
  a demo GIF in the pull request, or an explicit N/A with a reason
  (docs-only, pure refactor with no UI, CI-only). If that is missing,
  WITHHOLD while the author can still add it, and REQUEST CHANGES when
  the tip is offered as ready. Do not PASS on CI alone. The author prompt
  is `.github/pull_request_template.md`.

## External and fork tips

Apply this in addition to the full review when the author is external or
first-time, or `isCrossRepository` is true:

- Secrets, credentials, private assets, or raw provider responses in the
  diff: REQUEST CHANGES.
- `maintainerCanModify` false: note that maintainers cannot update the
  branch. That note alone is not a code defect.
- Chinese-only PR title or body: REQUEST CHANGES, or record it as a
  language finding when the verdict is already WITHHOLD. PR titles,
  bodies, and review posts are English. Do not PASS over a Chinese-only
  PR body.

Issue bodies published by `feat-issue` or `bug-issue` are Chinese by
default. Do not treat that issue text as a PR-language defect. Product
copy still needs both `zh-CN` and `en-US` in the same change.

## Choose one verdict

- **PASS** — the tip matches the linked issue; no actionable defect for
  the scoped risk; Release checks and other required statuses are green
  on this tip SHA; the tip merges cleanly onto current main. A
  user-visible change includes a screenshot, short recording, demo GIF,
  or a justified N/A.
- **WITHHOLD** — evidence is incomplete: CI is running or unsettled, the
  tip moved, the review is unfinished, the branch is conflicted or
  behind main, or a user-visible change still has no demo and no
  justified N/A. WITHHOLD is not PASS.
- **REQUEST CHANGES** — an actionable defect: correctness, a break of an
  AGENTS.md contract, security, missing tests for a claimed fix, a
  dishonest claim, a language-policy break on user-facing copy or on
  PR text that must be English, or a ready user-visible tip with neither
  media nor a justified N/A.

One verdict only. Do not soften REQUEST CHANGES into PASS because the
rest looks fine. Do not soften WITHHOLD into PASS because the diff looks
fine while CI is unsettled.

## Output

English. Short enough to post in the room or chat. First line is the
verdict, the tip short SHA (at least 7 hex digits), and the `Fixes` /
`Refs` numbers. Then findings, then `Ran:` and `Not run:`. On PASS, the
last line names the Coordinator. Use "no actionable findings" only on
PASS.

```text
PASS abc1234 Fixes #123

- no actionable findings

Ran: Release checks green on abc1234 (full tip SHA)
Not run: local pytest

Coordinator: ping after this Reviewer PASS and green CI on this SHA. This skill does not merge.
```

```text
WITHHOLD abc1234 Refs #123

- Release checks still running on this tip SHA
- behind main; rebase onto current main is required

Ran: none on this SHA
Not run: Release checks (unsettled)
```

```text
REQUEST CHANGES abc1234 Fixes #123

- claimed fix has no test that fails without the change
- user-visible string added for en-US only

Ran: Release checks green on abc1234 (full tip SHA)
Not run: local browser lane
```

If asked to comment on the PR, paste the same text. That comment still
does not merge and does not dismiss a failing check.

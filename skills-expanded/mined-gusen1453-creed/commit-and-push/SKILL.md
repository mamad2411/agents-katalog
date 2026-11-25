---
name: commit-and-push
description: Use when the user asks to commit, push, commit-and-push, open/draft a PR/MR, write a PR description with a Test plan, or tag/cut a release — especially when changes should be split into logical commits, or when tempted to dump everything into one commit or push to a protected branch.
---

# Commit and Push

> **Output language:** answer and write artifacts in the user's own language (match their messages, not the repo's history).

## Overview

Four moves, and most sessions only need the first two:

1. **Commit** the work in batches a reviewer can read one at a time
2. **Push** the feature branch — never a protected one
3. **Sync the MR/PR** — update an existing one automatically, ask before creating a new one
4. **Tag and release** — only when a version is actually being cut

This file is a router; each stage has its own reference:

| Stage | What | Reference |
|------|------|-----------|
| **Commit** | workspace/branch check, batch split, conventional message, push | [references/commit.md](references/commit.md) (§0–§3) |
| **MR/PR** | baseline, pick the template, draft, detect/create/update, read back | [references/mr-pr.md](references/mr-pr.md) (§4–§4.5) |
| **Release** | learn the repo's version/tag convention, tag the shipped commit, create/update the release | [references/release.md](references/release.md) (§6) |
| **Host CLI** | the `gh`/`glab` commands, and the traps that cost real round-trips | [references/host-cli.md](references/host-cli.md) |
| **Voice** | who each piece of copy is for, and where the wording comes from | [references/voice.md](references/voice.md) |

MR/PR templates live in [assets/](assets/) — each is four required sections plus an "add only when it applies" list: [feature-to-integration.md](assets/feature-to-integration.md) ready for QA · [integration-to-production.md](assets/integration-to-production.md) ship to production · [hotfix-to-production.md](assets/hotfix-to-production.md) hotfix.

**Core principle: one commit = one change a reviewer can judge on its own; one PR = one shippable story, described for whoever has to check it; one release = a tag on the commit that actually shipped.**

Does **not** replace test-design judgment (see test-design) or TDD rhythm (see superpowers:test-driven-development).

## When to Use

- User says commit / push / "commit and push" / draft or open a PR/MR
- User says tag / cut a version / publish a release, or a promotion MR just merged
- The working tree mixes concerns that should not land in one commit
- A PR/MR needs a description that tells its reader how to check the work

**When NOT to use:** review-only with no intent to ship; only designing tests (use test-design). (If a gate upstream offered a review and the user declined, proceed on their call.)

## The Iron Law (non-negotiable)

```
1. NEVER commit or push to a protected branch (default: main, master, pro, test — plus any the repo declares).
2. NEVER mix unrelated changes in one commit.
3. EVERY commit message MUST be `type(scope): subject` (Conventional) and say what changed, not which files.
   Language is free (Chinese/English); the format is not.
4. EVERY PR/MR description MUST tell its reader how to check the work.
5. NEVER create a NEW MR/PR or release without an explicit yes. ALWAYS sync an EXISTING one — that part is automatic.
6. NEVER trust exit 0 after writing an MR/PR body or release notes. Read it back and compare.
7. NEVER invent a version scheme — follow the repo's tag history; if there is none, ask.
```

**Violating the letter is violating the spirit.** "Just one quick commit on test", "I'll add the Test plan later", and "force push is fine this once" do not count.

## Workflow (when invoked)

Announce "Using commit-and-push to …", then make a todo per step you will actually run — steps 1–4 are the common case, 5–7 only when the work calls for them.

1. **Check workspace, branch, upstream** ([commit.md](references/commit.md) §0) — stop if protected.
2. **Plan the batches** ([commit.md](references/commit.md) §1) — show the plan; execute by default, ask only when it is unclear which batch a change belongs to.
3. **Commit each batch** ([commit.md](references/commit.md) §2) — stage only that batch; the message says *why*. Wording: [voice.md](references/voice.md), sampled from this conversation rather than git history.
4. **Push the feature branch** ([commit.md](references/commit.md) §3) — ask before any force push.
5. **Draft the MR/PR** ([mr-pr.md](references/mr-pr.md) §4) — work out what the MR is doing (ready for QA / ship to production / hotfix) from the branches' roles, use that [assets/](assets/) template, cover *all* commits since the baseline.
6. **Sync it** ([mr-pr.md](references/mr-pr.md) §4.5) — look for an existing MR/PR on this branch, merged ones included; found → update and read back; none → ask before creating.
7. **Tag + release** ([release.md](references/release.md) §6) — when asked, or when a promotion MR merged and this repo releases on merge.

Then **report**: commits, push result, MR/PR number + URL, release URL, and anything left unstaged.

## Excuses that show up (and what's actually true)

| Excuse | Reality |
|--------|---------|
| "One big commit is faster" | Reviewers can't bisect or revert cleanly. Batch by intent. |
| "I'll push to test just this once" | Protected means protected. Feature branch + MR. |
| "Test plan later / it's obvious" | Without a checklist, "done" is a claim, not a fact. |
| "Force push will clean up the history" | Ask first. Never on a protected branch. |
| "The hook is annoying — skip it with --no-verify" | Fix the cause. Skipping hooks is not shipping. |
| "Amend the commit the hook rejected" | The commit never happened — amend would rewrite the *previous* one. Fix, then commit again. |
| "PR description = the last commit message" | The PR covers the whole `baseline..HEAD` story. |
| "English-only commits are the only right way" | Format is fixed; language follows the user. |
| "Use git history to find the user's voice" | That history is mostly AI-written. Sample the live conversation. |
| "Commit the .env so CI works" | Secrets never get committed. Warn and leave it unstaged. |
| "The MR already exists, skip the sync" | A stale description is a wrong claim. Existing MRs sync on every push. |
| "Just create the MR, no need to ask" | Creation is public and hard to undo. Ask ([mr-pr.md](references/mr-pr.md) §4.5). |
| "Tag the branch head" | Tag the commit that **shipped** — usually the merge commit on production. |
| "Just pick a version number" | Follow the repo's tag history; if there is none, ask. |

**Tool gotchas are not excuses — they are things you don't know yet.** The measured `gh`/`glab` traps (`-f` vs `-F`, `mr list --state`, `mr view <branch>`, unpushed tags, `release create` on an existing tag) live in [host-cli.md](references/host-cli.md) §Traps. Read it before running a host command.

## Checklist

- [ ] Not on a protected branch; upstream not protected
- [ ] Each batch is one change; each message is `type(scope): subject` and says why; no secrets staged
- [ ] Pushed to `origin <feature-branch>` only; no unrequested `--force` or `--no-verify`
- [ ] Baseline = the MR's target branch; `baseline..HEAD` non-empty; counts from `git rev-list --count` (merges included)
- [ ] Right template for what this MR is doing; its four required sections filled; inapplicable ones left out, not stubbed "none"
- [ ] Title + summary cover **all** commits since the baseline
- [ ] What already ran vs what's still open are both concrete, and nothing unrun is marked as ran
- [ ] Checked this branch for an existing MR/PR (merged included): found → synced (ship-to-production keeps its prose, only counts refreshed); none → asked first
- [ ] MR/PR body read back and matched after the write — exit 0 was not trusted
- [ ] (If releasing) version follows the repo's tag history; the **shipped** commit is tagged; tag pushed separately; release verified ([release.md](references/release.md) §6)

---
name: ship
description: The merge transaction once CI is green and the change is reviewed — push, PR, CI and merge in one script command, then the card moves to Merged; and the ship transaction for "I'm shipping" (release notes, Shipped), only on the human's explicit command. Use for "merge it", "ship it", and when a branch is done and green.
---

# Skill `ship` — delivery (a thin layer over a script)

> Canonical template (templates/base). Principle: **a script does the mechanics; the model only starts it and
> handles the cases the script cannot** (a decision of the "Acceptance" layer). This is the GitHub variant.

> **Seam:** code host = GitHub (`gh`, through `scripts/merge-feature.sh`); board = the `board` skill. To use another tool, rewrite `scripts/merge-feature.sh` and the Merge transaction and Ship transaction sections; the plugin's guard and quota guard also know `gh` (the Code host row of [Supported stack](https://github.com/ruslantrachuk/dark-factory/blob/main/docs/functions.md#supported-stack)).

## Configuration (fill in on deployment)

- Main branch: <`main`>; merge strategy: <`--merge` (recommended)/`--squash`>, set in `scripts/merge-feature.sh`.
- Fence level: `.claude/fences.env` (`solo`/`standard`/`team`); at `team` the script also requires a GitHub approval and refuses `--skip-ci`.
- Updating the dev stand after a merge into main: <the project's procedure (the `dev-stand` skill), or "none">.
- Project exceptions (what must NOT happen automatically even after green CI): <e.g. migrations, production writes — or "none">.
- **Two repositories** (a harness parent plus the code in a submodule or a separate repository): the project **overrides** this procedure. The merge goes into the code repository (a PR or MR on its host); after it, the parent bumps the submodule pointer; `merge-feature.sh` is replaced or extended by a project-specific script.

## Hard rules

1. **Merge when CI is green and you have reviewed the change yourself** (the diff against the proposal's acceptance scenarios, the PR description). At `solo` and `standard` the agent runs the merge itself; at `team` the script also requires a GitHub approval from a person. Red CI means no merge (built into the script). The human gate is the release, a later stage. The "I'm shipping" transaction below runs only on the human's explicit command.
2. **Write for people.** The PR title and release notes are plain, professional prose: no clipped note-taking style, no file paths, no filler. This is part of the transaction, not a nice-to-have.
3. The script does not fix things. Red CI or a conflict ends in **an honest failure**: tell the human what got stuck and where, and suggest where the work goes back to; the human decides.

## Merge transaction (per work branch)

0. **Before the push, put the record and the accompanying changes in place.** The PR description has `## Done`, `## Decisions` and `## Open questions`, each with text ("none" is an answer; the `save` skill writes them); without them the script refuses, and it writes the description into the merge commit, so `git log --merges` is the history. A decision that shapes the architecture also gets an ADR on the branch; a follow-up is a task in the execution queue. If this PR ships a large change, its `SHIPPED.md` goes on the branch too. Merging into main is the rollout: nothing is pushed to main as a separate commit afterwards (this matters most when main auto-deploys). Forgot something? Bring it with the next feature branch, not as a follow-up commit on main.
1. Write the PR title (rule 2) — it becomes the merge commit's subject. In the PR description name the board card: `Part of <PREFIX>-N` (or `Closes <PREFIX>-N` if the PR finishes the card). The branch name and the PR title carry the tracker ID, so the tracker links the PR and moves the card by itself; the `Part of`/`Closes` line is the fallback link.
2. `scripts/merge-feature.sh <branch> "<title>"`. The script pushes, finds the PR (or opens one with the empty description skeleton and asks for it to be filled in), checks the description, marks a draft ready, waits for CI, merges (a merge commit: subject = the PR title, body = the description and the trailers; code, SHIPPED and an ADR reach main together), updates the local main branch and then closes the bd task in the local queue (found from the branch name: the tracker ID against the task's external ref, or the slug and `-p<K>` against the epic and phase labels; no single match — it says "close it by hand"). Nothing about the queue is committed.
   Team mode (`FENCE_LEVEL=team` or `MERGE_REQUIRE_REVIEW=1`): the script refuses until the PR's review decision is APPROVED. A teammate approves on GitHub; the agent does not approve (the guard denies `gh pr review --approve`).
   The script is safe to **re-run**: it recognises a PR that is already merged, skips the steps already done and finishes the rest. Unfinished steps end with a non-zero exit code and a list, not with a "do this by hand" warning and exit code 0. It waits up to 10 minutes for CI checks to appear (GitHub does not create them instantly), and a network failure while waiting is not treated as red CI.
   No CI at all (a solo project with no workflows): the script runs the local gate instead and records `CI: none (local gate)` in the merge commit. At `team` this is refused.
3. Board card → `Merged`, with a comment linking to the PR (the merge transaction of the `board` skill). If the project has Linear's GitHub automation connected (PR merged → Merged), the status moves by itself; do not repeat it by hand, only check.
3a. **Merge puts the feature on the dev stand; it is not acceptance.** Update the stand (the `dev-stand` skill) and tell the owner, or, for a request that came through the On-call, the development session tells the On-call "<feature> is on the dev stand" so it asks "ship?" in the group. Acceptance is the label `accepted` plus the comment `accepted by <who>, <link to the message or "permission dialog">` on the merged PR; `scripts/release.sh` refuses to tag while a merge since the last release lacks it (rule: a merge is not acceptance; someone on the acceptance list says yes, and the label and comment are the record; details: [docs/layers/acceptance.md](https://github.com/ruslantrachuk/dark-factory/blob/main/docs/layers/acceptance.md)).
4. Several accepted features: repeat per feature (each branch on its own, shipping in parts).

## Fallback: CI exists but cannot run

Sometimes Actions does not start for reasons that have nothing to do with the code: a billing problem on the GitHub account, limits, a platform incident. Then, and only then, the merge goes ahead without CI, through the same script:

`scripts/merge-feature.sh <branch> "<title>" --skip-ci "<reason>"`

Conditions: (1) the owner explicitly said "merge without CI" and gave the reason, which goes into `--skip-ci` as given; (2) the script does not wait for checks and runs the local gate instead (the pre-push test command over the branch range, or `LOCAL_GATE_CMD`); a red local gate cancels the merge; (3) the script posts a prominent PR comment "Merged WITHOUT CI: <reason>" and adds a `CI-skipped: <reason>` trailer; (4) the PR description's `## Decisions` names the reason and the local run. If CI turns out to be green after all, the script merges the usual way. At `FENCE_LEVEL=team` `--skip-ci` is refused: the team merges on CI only. `--skip-ci` is not a way around red CI; failing tests get fixed, not skipped.

## Ship transaction ("I'm shipping <project>"), only on an explicit command

The rules and steps live in the `board` skill (list the Merged cards → confirmation → the tag/release cut by `scripts/release.sh` (release-tag module; the agent runs it on the owner's explicit command, the permission dialog is the gate) or by the project's own procedure, with the notes edited into readable prose via `gh release edit` → deployment → proof of delivery → cards to Shipped → statuses copied to the client's tracker). This skill never creates a tag or a release by hand (`git tag`, `gh release create` bypass the acceptance gate that `release.sh` checks); deployment follows the project's own procedure, not this skill.

## What the skill does NOT do

- It does not merge on red CI, and does not move cards past Merged without the "I'm shipping" command.
- It does not deploy.
- It does not fix red CI or conflicts; it only reports them.

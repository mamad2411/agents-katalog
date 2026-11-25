---
name: validate
description: Validate a current Pull Request through code standards, security, adversarial challenge, synthesis, and GitHub reporting. Launches review and challenge workers through pi-subagents or Cursor Multitask. Use when the user asks for a full validation cycle or to validate a PR.
---

# Validate

Coordinate one evidence-backed validation run. This skill reports; it does not modify product code.

Read [the validation artifact contract](validation-contract.md) before starting.

## Subagent dispatch

Choose one available runtime for the entire validation run; never mix them within a phase. Cursor Multitask takes priority when it is active:

- **Cursor Multitask:** When Cursor Multitask Mode is active, use Cursor Task subagents (`generalPurpose`) as described below.
- **Pi:** Otherwise, when `pi__subagent` is exposed, use it as described below.

For **Pi**, a phase is one top-level `pi__subagent` call with `async: true` and a `workflowScript`. Put independent workers in that script's single `await runs.all([...])` call. Do not make separate top-level calls for children in the same phase. The parent yields after launching a phase; completion notifications, not polling, start the next phase.

For **Cursor Multitask**, a phase is every independent Cursor Task call in one assistant message. Set `run_in_background: true` on every call, end the turn after dispatch, and begin the next phase only after their completion notifications and artifact checks. Do not poll.

Contract-artifact workers need `read`, `bash`, and `write`. In Pi, use the `delegate` role unless the project has an equivalent enabled artifact-writer role; give each child `context: "fresh"`, the repository as `cwd`, and an exact non-overlapping artifact ownership boundary. In Cursor, use `generalPurpose` tasks. They must not edit, commit, push, comment on, or otherwise modify product files.

Each child prompt includes the absolute `RUN_DIR`, the absolute path of the relevant skill and this contract, its source-artifact read boundary, the one artifact it owns, and its done-when criterion. Subagents have no parent history — do not paste another worker's findings into a prompt. A child writes its owned contract artifact atomically at the path in `RUN_DIR`; a child output is only an optional handoff, not a substitute for that artifact.

Workers do not pick models. Recommend **Grok 4.5 Fast** for **validate-with-code-review** and **validate-with-security-review**. Use it only when the selected runtime exposes an exact matching model ID; otherwise omit `model`, run the reviews on the parent model, and tell the user. Challenge, synthesize, and reporter workers inherit unless the user names an available model.

## 1. Pin the pull request and run

Resolve the PR from a number/URL supplied by the user, otherwise `gh pr view --json number,url,baseRefName,headRefName,headRefOid`. Fetch the head and base refs, verify the three-dot diff is non-empty, and create `RUN_DIR` exactly as the contract specifies. Write atomic `context.json` and `changes.json`; include the changed-file list and a concise change summary derived from the diff.

**Done when:** the PR identity, immutable head SHA, base, diff command, and both coordinator artifacts exist.

## 2. Run independent reviews

Dispatch the two reviewers in parallel: one asynchronous Pi workflow with two fresh `delegate` children in `runs.all`, or two Cursor `generalPurpose` Tasks in one Multitask message:

- Code: follow **validate-with-code-review** → `code-review.json`. Do not read `security-review.json`.
- Security: follow **validate-with-security-review** → `security-review.json`. Do not read `code-review.json`.

After their completion notifications, verify that `code-review.json` and `security-review.json` both exist and each is a valid JSON array.

## 3. Challenge each review

Dispatch the two challengers in parallel: one asynchronous Pi workflow with two fresh `delegate` children in `runs.all`, or two Cursor `generalPurpose` Tasks in one Multitask message:

- Code: follow **validate-by-challenge** with `source: code` → `challenge-code-review.json`. Read only `code-review.json`.
- Security: follow **validate-by-challenge** with `source: security` → `challenge-security-review.json`. Read only `security-review.json`.

After its completion notification, verify both challenge artifacts exist and every source finding has exactly one verdict.

## 4. Synthesize

Dispatch one asynchronous Pi workflow with one fresh `delegate` child, or one Cursor `generalPurpose` Task, that follows **validate-synthentizer**. It reads coordinator, reviewer, and challenge artifacts from `RUN_DIR` on disk.

After its completion notification, verify `synthesis.json` exists, is a valid JSON array, and contains the change summary plus every upheld or reframed finding exactly once.

## 5. Report to GitHub

Dispatch one asynchronous Pi workflow with one fresh `delegate` child, or one Cursor `generalPurpose` Task, that follows **validate-github-reporter**, giving it `RUN_DIR`. This child alone has authority to post the report to GitHub.

After its completion notification, verify `github-report.json` records the URLs of the posted PR summary and every eligible inline comment.

## 6. Return the result

Tell the user the PR URL, run directory, final finding counts by severity, and the PR comment URL. Link or quote the final summary without reintroducing dismissed findings.

**Done when:** the user can open the GitHub report and inspect the synthesized JSON artifact.

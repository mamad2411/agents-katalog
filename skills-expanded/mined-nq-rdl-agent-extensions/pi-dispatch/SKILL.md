---
name: pi-dispatch
license: MIT
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
description: Dispatch confirmed GitHub issues or one free-text task to headless pi workers in Worktrunk worktrees. Use for Claude Code orchestration of implementation PRs, with triage, rolling slots, overlap strategies and JSONL status; not for merging without authorisation or steering running workers.
compatibility: Verified pi 0.99.1 and wt 0.77.0; Fast catalog contract from Codex CLI 0.159.1 (2026-10-01). Bash 3.2+, jq >=1.6, Git and authenticated gh (CLI fields verified on 2.97.0). External pi provider credentials required.
user-invocable: true
argument-hint: "[--fast | --no-fast] <numbers | N-M | >=N | label:name | free text>"
---

# Dispatch pi implementation workers

Verify correctness-critical flags against installed `pi --help`, `pi auth --help`
and `wt switch --help` and the [canonical Pi CLI](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/cli.md)
and [Worktrunk docs](https://worktrunk.dev/) before relying on them after upgrades.

## Plan first — no launches yet

1. If prerequisites or defaults are unknown, ask the user to run `/pi:setup`.
   Load approved defaults from `${XDG_CONFIG_HOME:-$HOME/.config}/pi-dispatch/config.json`
   as JSON with jq, **never source or eval it**. Missing config means ask for a
   verified model and state directory. Default cap is **2**, not the number of issues.
   Fast is **OFF by default**. `--fast` opts in; `--no-fast` overrides an approved
   `fast: true` config default. Strip these workflow flags before resolving targets.
   Read [Fast mode](references/fast.rst), check the chosen model's priority tier
   with `fast-check "$MODEL"`, and confirm increased plan usage before any Fast
   launch. Unlisted/unavailable catalogs require a separate user decision.
2. Read [helper contracts](references/helpers.rst) before using
   [pi-dispatch.sh](scripts/pi-dispatch.sh). Resolve the target from the repo:
   `bash "$S/pi-dispatch.sh" resolve "$TARGET"` (S is this skill's `scripts/`
   directory). Numbers, ranges, `>=N` and `label:<name>` resolve via gh; free text
   is **one unit**, branch `pi/<slug>`. Use `resolve --text "$TARGET"` to force text.
3. For issues, read the full issue and comments. Classify each unit:
   **dispatchable**, **human-only** (interactive UI, physical access or judgement
   unavailable to the agent), **umbrella** (tracking, not a bounded implementation),
   or **blocked** (dependencies, closed issue, missing scope or authorisation).
   Resolver output is deliberately `untriaged`; labels are clues, not authority.
   Explain the reason and questions for each skipped unit. Inspect `blockedBy`,
   linked dependencies, and acceptance criteria; do not dispatch unresolved blockers.
4. Predict touched paths from issue text **and a quick repository grep**. Set
   `paths` to repository-relative files or directory prefixes (no trailing slash).
   Include hand-written sources and shared generators/configuration likely to
   change, not just the skill named in an issue. Exclude the repository's
   generated/derived outputs that its pipeline rebuilds; regenerate on rebase.
   Unknown footprint `[]` overlaps everything conservatively.
   Run `waves PLAN.json`; inspect `dependsOn` (overlapping predecessor branches).
   Wave numbers are an advisory packing order, **not merge gates**: an empty
   `dependsOn` in a later wave means cap-only overflow.
5. **Show every unit, classification/reason, predicted paths, branch/PR base,
   wave/dependsOn, overlap strategy/default, model/thinking, Fast choice/cost,
   state directory and cap. Ask the user to confirm exactly which units to launch
   and their strategies.** For each dependent unit offer:
   - **parallel-then-rebase** — default for small, understood overlap without a
     code dependency; launch when a slot opens, then resume after predecessors merge.
   - **stacked** — base on a predecessor when its code is required; wait until
     that implementation is committed, not merged. Review changes can invalidate
     the stack; record the parent commit and PR base. Multiple parents need an
     explicit integration plan, not an arbitrary base choice.
   - **wait-for-merge** — default for heavy/unknown overlap or competing design
     decisions; launch only after all overlapping predecessors merge.
   Workers will run the repository's standard commit/push hooks and watch CI;
   raise objections before launch. Resolve slug collisions with the user. Issue
   branches are `issue-N`; free-text PRs have **no Closes line** and no new issue
   unless asked. Save selected dispatchable units and strategies in the approved
   plan. Recompute waves if selection, footprint, model or cap changes; reconfirm
   material changes, including strategies/bases.

## Execute the confirmed plan with rolling slots

Read [worker template](references/worker-prompt.rst) before rendering prompts.
After `git fetch origin` updates `origin/main`, create worktrees for launchable
units with `worktree BRANCH` (or the confirmed non-main base for a stack).
Keep at most the approved cap running. When a worker exits, inspect status and
memory, then launch the next eligible confirmed unit immediately; **cap-only
units do not wait for PR review or merge**, even if their wave number is higher.
Do not wait for every worker in a wave to finish. Apply the confirmed strategy
for real overlaps: parallel-then-rebase may launch now; stacked needs its
committed parent; only wait-for-merge gates launch on predecessor merges.
Those merges must be **reviewed and performed by the orchestrator with user
authorisation**; fetch updated main afterwards. An exited worker or green CI
is not a merged dependency. The helper enforces slots, not strategy eligibility.

Extract each selected unit to UNIT.json; render it with
`render UNIT.json "$WORKTREE" > PROMPT`. Review the prompt, then call:

```bash
bash "$S/pi-dispatch.sh" launch UNIT.json "$WORKTREE" PROMPT "$MODEL" --confirmed
bash "$S/pi-dispatch.sh" status
```

Only for approved Fast mode, append `--fast` to the launch call. The runner loads
[service-tier.mjs](assets/service-tier.mjs) with `-e` and requests **priority**, not
`fast`. State/status label it **`priority (requested)`**, never confirmed: the
Codex backend can echo `default` even when priority was requested. Provenance:
orchestrator investigation, 2026-10-01, pi 0.99.1 / Codex CLI 0.159.1 (details in
Fast mode reference); this workflow does not authorise new live verification.

The launcher enforces a per-repository cap under a lock, defaults to
`--no-approve` (no implicit project trust), and records PID, logs and exit code
independently of host harness tracking. Workers' memory-heavy test suites are why the
cap is two: do not raise it just because CPUs are idle. Inspect status memory
pressure before launching; at HIGH pressure stop launching and reduce the cap.
Do not launch parallel test suites in the orchestrator while workers test.

Claude Code auto-mode can deny `pi -p` as **Create Unsafe Agents**, even with a
permission rule. Do not disguise/retry the command to evade it. Explain the
risk and let the user launch the **same helper** with `!bash ... launch ...
--confirmed`, so PID/exit/log tracking and the cap still apply. Permission rules
and Worktrunk approvals are the user's decision; never apply them silently.

Print mode cannot steer a running worker. For an exited worker's CI or rebase
follow-up, write a bounded follow-up prompt and launch again from the **same
worktree**; the stable session ID resumes its history. For parallel-then-rebase,
resume after predecessors merge; regenerate derived outputs, validate and update
only that PR. Re-select Fast explicitly for every follow-up; it is not inherited.
See helper contracts for bounded rebase and stacked-base instructions.
`pi/<slug>` maps to `pi-<slug>` because pi 0.99.1 rejects `/` in session IDs;
issue-N is unchanged. Do not use `--name` as a substitute for session identity.
See helper contracts for resume logs.

## Review, authorised merge, cleanup

Workers open PRs, watch CI and never merge. Read the diff and acceptance criteria;
require green CI and repository reviews. An exit code 0 does not prove success
(JSON-mode model errors can still exit 0); inspect `errors`, logs and the PR.
Report judgement calls/deferred criteria under **Decisions for review**.
Only the orchestrator may merge, using repo strategy **after explicit user
authorisation**. Admin review bypass needs separate explicit session consent.
If merging is not authorised, return PR URLs; leave wait-for-merge units and
post-merge rebase follow-ups pending, not independent cap-only units.

After a merge, offer `wt remove` for finished worktrees; inspect `git status
--porcelain` first and never remove uncommitted work or a running worker's tree.
Retain private state/logs unless the user approves deletion. RPC steering and
Codex-hosted orchestration beyond native skill packaging are follow-ups, not MVP
capabilities. A worktree is a scope convention, **not a sandbox**.

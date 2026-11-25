---
name: fastlane
description: "Use after define-spec for small features or non-trivial bug fixes that fit a lightweight current-workspace implementation path."
---

# Fastlane

Inline orchestrator skill. Every step runs in the orchestrator's session — no coordinator subagent.

Execution contract:

- Operate in the current workspace only. Do not create a worktree and do not invoke `using-git-worktrees`.
- Dispatch one `coder` task through `subagent_run_serial`, with the documented one-time `NEEDS_CONTEXT` retry only.
- Set `thinking: "high"` at the fastlane coder task site. Do not change global coder defaults.
- Rely on the coder prompt for `test-driven-development` and `verification-before-completion` guidance.
- Do not dispatch a verifier.
- Run project tests through the shared `test-runner` artifact contract when a test command is detected.
- Invoke `commit`, `refine-code`, and `finishing-a-development-branch` only at the gates below.
- Never push automatically.

## Step 0: Input shape detection

Detect the input shape strictly, mirroring `skills/define-spec/spec-design-procedure.md` Step 1.

| Shape | Match | Action |
| --- | --- | --- |
| **Idea ID** | `^IDEA-[0-9a-f]{8}$` after strip/lowercase | Strip `IDEA-` to `<bare-id>`. Call the built-in `idea` tool with `action: "read"`, `id: "<bare-id>"`. Capture `details.title` and `details.body`. Retain `IDEA-<id>` for user-facing messages and the `Source: IDEA-<id>` line in Step 10. |
| **Spec path** | Input ends in `.md`, is under `docs/specs/` as a relative path or absolute `/docs/specs/` path, and exists | Read the file. |
| **Freeform** | Anything else | Reject and stop. |

If the idea tool returns `isError`, reject with:

~~~
fastlane: idea IDEA-<id> not found via the idea tool.
~~~

For freeform input, reject with:

~~~
fastlane: input must be a spec path under docs/specs/ or an IDEA-<id>. Run /define-spec first to shape a spec.
~~~

## Step 1: Generate checklist

Read the spec/idea body. Run a brief codebase survey scoped to file and subsystem mentions in the spec/idea. Emit a concrete 3–7-step numbered implementation checklist in execution order.

The checklist is ephemeral: keep it only in orchestrator conversation state; never write it to disk.

## Step 2: Settings and top-level confirmation

Resolve the project test command for the Settings display:

1. Use the test command named during `(e) Edit checklist`, if present.
2. Else run `pi-flow helper _shared/detect-test-command --working-dir <working-dir>` and consume `.command` when `.detected` is `true`.
3. Else display Test suite check as `disabled (no test command detected)`.

Initialize run state:

| Field | Default | Allowed values | Consumed by |
| --- | --- | --- | --- |
| `model_tier` | `capable` | `efficient`, `standard`, `capable`, `frontier` | Step 4 coder dispatch |
| `refine_max_iterations` | `3` | integers `1`–`5` | Step 9 refine-code |

Render the top-level confirmation menu:

~~~
Fastlane plan:
  Source:   <spec path or IDEA-<id>>
  Checklist:
    1. <step>
    2. <step>
    ...

  Settings:
    Coder tier:              capable (high thinking)
    TDD:                     enabled
    Test suite check:        <resolved test command, or "disabled (no test command detected)">
    Refine-code iterations:  3

Options:
(s) Start                    — proceed with these settings
(c) Customize                — change a setting
(e) Edit checklist           — revise the numbered checklist before starting
(x) Stop                     — exit fastlane (spec/idea remains committed)
~~~

### `(c) Customize` submenu

`(c)` opens the customize submenu. The only letter options are `(t)`, `(r)`, and `(m)`. TDD and Test suite check stay visible in the Settings block only; do not expose toggles for either.

Render byte-equal:

~~~
Choose a setting to change:
(t) Coder tier               — current: capable (high thinking)
(r) Refine-code iterations   — current: 3
(m) Back to main menu
~~~

| Option | Behavior |
| --- | --- |
| `(t)` | Prompt for `efficient|standard|capable|frontier`; write the value to `model_tier`; re-render Settings before returning to this submenu. |
| `(r)` | Prompt for an integer `1`–`5`; write it to `refine_max_iterations`; re-render Settings. |
| `(m)` | Return to the top-level confirmation menu. |

The customize submenu MUST NOT expose a TDD toggle or a Test suite check toggle.

### Other top-level options

| Option | Behavior |
| --- | --- |
| `(e) Edit checklist` | Let the user revise the numbered checklist and optionally name a test command; re-show the top-level confirmation menu. |
| `(x) Stop` | Exit silently. The spec/idea remains committed; no rollback. To escalate, the user may manually run `/generate-plan <spec-path>` after stopping. |

## Step 3: Git preflight

1. Capture `BASE_SHA = git rev-parse HEAD`.
2. Run `git status --porcelain`.
3. If the output is non-empty, render the dirty-state checkpoint byte-equal:

~~~
⚠️ Working tree is dirty:
<git status --porcelain output, verbatim>

Options:
(c) Continue — commit existing changes now, then proceed with fastlane
(x) Stop     — handle existing changes manually
~~~

- `(c)` invokes the commit skill with no path restriction. The user supplies the message via the commit skill's standard prompt. Re-capture `BASE_SHA = git rev-parse HEAD` after the commit.
- `(x)` exits.

4. Determine the current branch via `git rev-parse --abbrev-ref HEAD` or `pi-flow helper _shared/git-workspace-status`.
5. If the branch is `{main, master, develop}`, render the warning byte-equal and proceed automatically:

~~~
⚠️ You are on protected branch <branch>.
Fastlane will commit directly to this branch.
~~~

No worktree creation. Fastlane operates in the current workspace only.

## Step 4: Dispatch the coder

Resolve `(model, cli, executionPolicy)` with:

~~~
pi-flow helper _shared/resolve-model-dispatch --model-tier modelTiers.<model_tier> --agent coder --working-dir <working-dir>
~~~

`<model_tier>` is the Step 2 run-state alias (`efficient`/`standard`/`capable`/`frontier`) mapped into the `modelTiers` section. On non-zero exit, surface the helper's stderr (canonical templates (1)–(5)) byte-equal and stop.

Build the prompt:

| Placeholder | Value |
| --- | --- |
| `{SPEC_OR_IDEA_CONTENT}` | Full spec body, or full idea body for idea-ID inputs. |
| `{CHECKLIST}` | Confirmed numbered checklist from Step 1 / Step 2 `(e)`. |
| `{WORKING_DIR}` | Absolute working directory. |
| `{TDD_BLOCK}` | Contents of `skills/_shared/coder-tdd-block.md` read from disk. |

Write placeholders to a temporary JSON file, then fill the coder-prompt template:

~~~
pi-flow helper _shared/fill-template \
    --template "$(pi-flow template fastlane/fastlane-coder-prompt)" \
    --placeholders-json <tmp-json> \
    --output <tmp-prompt> \
    --require-all-replaced
~~~

On non-zero exit, surface the helper's stderr verbatim and stop.

Dispatch via `subagent_run_serial`:

~~~
subagent_run_serial {
  tasks: [
    {
      name: "fastlane-coder",
      agent: "coder",
      task: "<filled prompt>",
      model: "<resolved model>",
      cli: "<resolved cli>",
      executionPolicy: "<resolved executionPolicy>",
      thinking: "high"
    }
  ],
  wait: true
}
~~~

The `thinking: "high"` field is a per-call override at the task site. Do not modify the global `agent/agents/coder.md` default. Running fastlane at the coder's `thinking: medium` default is NOT acceptable.

## Step 5: Handle the coder status

Parse `results[0].finalMessage` with:

~~~
pi-flow helper _shared/parse-coder-report --report <path-to-finalMessage>
~~~

Route on `.status` per the contract in [`../_shared/coder-report-contract.md`](../_shared/coder-report-contract.md):

| Status | Route |
| --- | --- |
| `DONE` | Continue to Step 6. |
| `DONE_WITH_CONCERNS` | Use the checkpoint below. |
| `NEEDS_CONTEXT` | Ask for missing context and retry once. |
| `BLOCKED` | Surface the blocker and stop immediately through the BLOCKED handler below. |

For `DONE_WITH_CONCERNS`, surface `.concerns_block` verbatim with:

~~~
⚠️ Coder returned DONE_WITH_CONCERNS:
<concerns_block, verbatim>

Options:
(c) Continue — record concerns for the final summary and proceed to verification
(x) Stop     — leave changes uncommitted for manual triage
~~~

`(c)` records concerns in run state and continues to Step 6. `(x)` exits without committing; any `docs/test-runs/<spec-name>/` artifacts are preserved.

For `NEEDS_CONTEXT`, surface `.needs_text`, ask the user for the missing context, append the reply under `## Additional Context` to the prompt body, and re-dispatch once with the same model, cli, executionPolicy, and `thinking: "high"`. A second `NEEDS_CONTEXT` or any `BLOCKED` from the retry stops immediately through the BLOCKED handler.

For `BLOCKED`, surface `.blocker_text` with this verbatim block, then stop immediately:

~~~
🚫 Coder returned BLOCKED:
<blocker_text, verbatim>

Fastlane stopped. Partial changes are left uncommitted for manual triage.
~~~

Do not prompt for user input. Do not continue to verification, commit, refine-code, idea closure, branch completion, or success cleanup. Surface the escalation guidance, then exit: Fastlane does NOT auto-discard or auto-stash; the user controls the working tree. To escalate after stopping, the user can manually discard or stash (`git checkout -- .` or `git stash push -u`) and then run `/generate-plan <spec-path>`.

## Step 6: Verification phase

1. Resolve the project test command:
   1. Use the checklist-named command if supplied in `(e) Edit checklist`.
   2. Else run `pi-flow helper _shared/detect-test-command --working-dir <working-dir>` and consume `.command` when `.detected == true`.
   3. Else skip verification silently and proceed to Step 8.
2. Create `docs/test-runs/<spec-name>` with `mkdir -p docs/test-runs/<spec-name>`.
   - `<spec-name>` is the spec filename without `.md`.
   - For idea-only inputs, use `IDEA-<id>`; the directory is `docs/test-runs/IDEA-<id>/`.
3. Dispatch `test-runner` per `skills/_shared/test-runner-dispatch.md` with:

| Field | Value |
| --- | --- |
| `test_command` | `<resolved>` |
| `working_dir` | `<abs-dir>` |
| `artifact_path` | `<abs-dir>/docs/test-runs/<spec-name>/full-suite.log` |
| `phase_label` | `full-suite` |

4. Parse the artifact:

~~~
pi-flow helper _shared/parse-test-runner-artifact --artifact <artifact-path>
~~~

Read `.failing_identifiers` and `.non_reconcilable_failures`.

5. If both lists are empty, the suite is clean; proceed silently to Step 8.
6. Do not run baseline reconciliation by default. If either list is non-empty, surface the verification-failure checkpoint byte-equal:

~~~
⚠️ Project test suite reported failures after fastlane implementation:
<failing identifiers, verbatim>
<non-reconcilable evidence, verbatim>

Options:
(c) Continue to refine loop — record as concerns, commit, and move to review
(b) Compare with baseline   — stash changes, re-run suite, restore changes, show existing failures vs regressions
(x) Stop                    — leave spec committed but changes uncommitted for manual triage
~~~

| Option | Behavior |
| --- | --- |
| `(c)` | Record failures in run state for the final summary; proceed to Step 8. |
| `(b)` | Enter Step 7. |
| `(x)` | Exit and preserve `docs/test-runs/<spec-name>/`. |

## Step 7: (b) Baseline comparison

On-demand branch entered only by `(b)` in Step 6.

Ordering note: run reconcile-reconcile after `git stash pop`, because `git stash push -u` includes the untracked `full-suite.log`; the helper needs that artifact restored before reconciliation.

1. Run:

~~~
git stash push -u -m "fastlane-baseline-comparison-<spec-name>"
~~~

Immediately capture the stash ref with:

~~~
git stash list -n 1 --format=%gd
~~~

Read the single-line stdout (for example, `stash@{0}`) and preserve it for failure handling. Do NOT parse the ref from `git stash push` output. The stash includes `docs/test-runs/<spec-name>/full-suite.log`.

2. Recreate the artifact parent directory:

~~~
mkdir -p <abs-dir>/docs/test-runs/<spec-name>
~~~

The `-u` stash removed the untracked `docs/test-runs/<spec-name>/` directory. The parent must exist before dispatching `test-runner`.

Dispatch `test-runner` per `skills/_shared/test-runner-dispatch.md` over the clean working tree with:

| Field | Value |
| --- | --- |
| `artifact_path` | `<abs-dir>/docs/test-runs/<spec-name>/baseline.log` |
| `phase_label` | `baseline` |

`baseline.log` is created after the stash push, so it is not part of the stash and remains through pop.

3. Capture baseline failures:

~~~
pi-flow helper _shared/reconcile-test-run \
    --artifact <abs-dir>/docs/test-runs/<spec-name>/baseline.log \
    --mode capture \
    > <abs-dir>/docs/test-runs/<spec-name>/baseline-failures.json
~~~

`baseline-failures.json` is also created after the stash push and remains through pop. Its `baseline_failures` list is the authoritative pre-change failure set.

4. Run `git stash pop`. If the pop output contains `CONFLICT (` or git exits non-zero with a conflict notice, hard-stop with:

~~~
Stash restoration produced conflicts. Working tree is in a mixed state.
Stash ref preserved: <ref>
Resolve manually: `git stash show <ref>`, then `git stash apply <ref>` / `git checkout -- .` as appropriate.
Fastlane stopped.
~~~

Preserve `docs/test-runs/<spec-name>/`. Do not run reconcile-reconcile and do not render the three-bucket summary.

5. On clean pop, run reconcile-reconcile:

~~~
pi-flow helper _shared/reconcile-test-run \
    --artifact <abs-dir>/docs/test-runs/<spec-name>/full-suite.log \
    --mode reconcile \
    --baseline-failures <abs-dir>/docs/test-runs/<spec-name>/baseline-failures.json
~~~

Use `.current_non_baseline_stable` as new regressions and `.current_non_reconcilable` as non-reconcilable evidence. Compute remaining buckets from the capture JSON's `baseline_failures` and the reconcile output's `current_failing_stable` fields (the reconcile output does not expose `.failing_identifiers`):

- pre-existing = `set(baseline_failures) ∩ set(current_failing_stable)`
- fixed-by-change = `set(baseline_failures) - set(current_failing_stable)`

6. Render the summary byte-equal to the spec:

~~~
Baseline comparison summary:
  Pre-existing failures (present on base):
    <list, verbatim>
  New regressions introduced by this change:
    <list, verbatim>
  Failures fixed by this change:
    <list, verbatim>

Options:
(c) Continue — record new regressions and non-reconcilable evidence as concerns, then commit
(x) Stop     — leave spec committed but changes uncommitted for manual triage
~~~

`(c)` records the new regressions and non-reconcilable evidence as concerns for the final summary and proceeds to Step 8. `(x)` exits, preserving `docs/test-runs/<spec-name>/`.

## Step 8: Commit phase

1. From a clean suite, Step 6 `(c)`, or Step 7 `(c)`, invoke the commit skill with no explicit path restriction.
2. Derive the commit message from the spec goal in Conventional Commits style. The commit skill drafts it; the user confirms via its standard prompt.
3. Keep test-runner failures in orchestrator run state for the final summary. Do not append them to the commit message; `docs/test-runs/<spec-name>/full-suite.log` is the audit trail.
4. Capture `HEAD_SHA = git rev-parse HEAD` after the commit succeeds.

## Step 9: Refine-code phase

Invoke the refine-code skill with the documented interface from `skills/refine-code/SKILL.md` Step 1:

| Input | Value |
| --- | --- |
| `BASE_SHA` | Value captured in Step 3. |
| `HEAD_SHA` | Value captured in Step 8. |
| Description | Spec goal. |
| `--plan-contents` | Spec path, or a tmp file containing the idea body for idea-ID inputs. |
| `--max-iterations` | `3`, or the Step 2 customized `refine_max_iterations`. |
| `--review-output-path` | `docs/reviews/<spec-name>-fastlane-review` |

The `-fastlane-review` namespacing distinguishes fastlane review artifacts from deep-workflow review artifacts targeting the same spec.

Refine-code's existing menu on `STATUS: not_approved_within_budget` ((c) Continue refining code / (p) Proceed with issues / (x) Stop execution) stays as-is. Fastlane introduces no override. Refine-code's provenance validation (`validate-review-provenance.py`) runs as normal.

Fastlane proceeds to Step 10 on:

- `STATUS: approved`
- `STATUS: approved_with_concerns`
- `STATUS: not_approved_within_budget` with the user choosing `(p) Proceed with issues`

On refine-code stop, fastlane exits without idea closure or branch completion; `docs/test-runs/<spec-name>/` is preserved.

## Step 10: Idea closure

Apply the linked-idea-closure procedure in [`../_shared/idea-closure.md`](../_shared/idea-closure.md). Fastlane resolves `idea_id` and `completion_note` per its own rules:

1. Determine the idea ID:
   - If the original input was an idea ID, use it directly.
   - Else extract `Source: IDEA-<id>` from the spec preamble using a bounded `head -n 40`.
   - Else skip silently.
2. Read the idea via the built-in `idea` tool (`action: "read"`, `id: "<id>"`). If missing or already status `closed`, skip silently.
3. Call the built-in `idea` tool with `action: "update"`, `id: "<id>"`, `status: "closed"`, and `body: "<existing body + \nCompleted via fastlane: <commit SHA>, spec: <spec path>>"` (or, when no spec was involved (input was an idea ID): `body: "<existing body + \nCompleted via fastlane: <commit SHA>, spec: (input was idea)>"`).

## Step 11: Post-completion

- On a feature branch (not `main`, `master`, or `develop`), invoke the finishing-a-development-branch skill verbatim. Its existing 4-option menu (merge / push+PR / keep / discard) gives the user control.
- On `main`/`master`/`develop`, `finishing-a-development-branch` is skipped by its existing protected-branch gate. Fastlane reports the run summary and ends; the user runs `git push` manually if desired.
- Fastlane introduces no automatic push.

## Step 12: Artifacts and cleanup

Preserve all `docs/test-runs/<spec-name>/` artifacts (`full-suite.log`, optional `baseline.log`, optional `baseline-failures.json`) on stop exits:

| Stop path | Step |
| --- | --- |
| Verification `(x)` | Step 6 |
| Baseline stash-conflict hard-stop | Step 7 |
| Coder `BLOCKED` | Step 5 |
| Refine-code stop / budget-exhaustion stop | Step 9 |

On successful completion (refine-code approved / approved with concerns / `(p) Proceed with issues`, idea closure complete, and post-completion done), clean up the per-spec test-runs directory:

~~~
pi-flow helper _shared/cleanup-test-runs docs/test-runs/<spec-name>
~~~

The helper refuses paths outside `<cwd>/docs/test-runs/`; see `pi-flow helper _shared/cleanup-test-runs` for the exact contract.

Keep refine-code review artifacts at `docs/reviews/<spec-name>-fastlane-review-v<ERA>.md` under refine-code's existing retention policy.

The checklist remains ephemeral; no on-disk artifact is written for it.

After successful helper bookkeeping, remove Python bytecode caches under `skills/fastlane/scripts/`:

~~~
pi-flow helper _shared/cleanup-pycache skills/fastlane/scripts
~~~

## Edge cases

| Edge case | Covered by | Behavior |
| --- | --- | --- |
| Dirty working tree at preflight | Step 3 | Commit existing changes, then continue; or stop. |
| Protected branch start (`main`/`master`/`develop`) | Step 3 | Warning only; proceed automatically; no confirmation prompt. |
| Coder `NEEDS_CONTEXT` cycle | Step 5 | Retry once; second `NEEDS_CONTEXT` or any `BLOCKED` surfaces the blocker and stops immediately. |
| Stash-pop conflict during baseline comparison | Step 7 | Hard-stop with the stash ref preserved. |
| Refine-code dispatch failure | Step 9 | Forward helper stderr verbatim; stop. |
| Idea missing or already closed at closure | Step 10 | Skip silently. |
| Protected branch at post-completion | Step 11 | Existing protected-branch gate skips branch completion; no automatic push. |

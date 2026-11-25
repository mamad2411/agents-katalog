---
name: task-review
description: Review a completed task branch with one independent parallel review panel and write a self-contained findings todo-list under reviews/. Retains every review pass until finish-task removes the task's review files. Never remediates; the user runs review-fix-worker for fixes. Use standalone after implement-next-task.
---

# Task Review

Review the diff between `HEAD` and a fixed base with independent Standards, Spec, conditionally
applicable Bug, and conditional Security lenses. Run the panel once, with each active lens in its
own subagent in parallel. Write every accepted finding to a todo-list file under `reviews/` in the
repository. Do not fix findings here: remediation is the manual `review-fix-worker` loop, and a
clean or fully resolved review unblocks `finish-task`.

Invocation authorizes creating workflow files under `reviews/` and adding the `/reviews/` ignore
entry to the repository's local exclude file (`$(git rev-parse --git-common-dir)/info/exclude`) when missing. Never touch the tracked
`.gitignore` for workflow state: review files, plans, and handoffs are the operator's local
material, and a `.gitignore` edit would ride into the task's commit. Never delete or overwrite a review file; `finish-task` removes
all review files for the completed task. Never modify the implementation under review. Never write
any other review document or create review scaffolding outside `reviews/`.

## Inputs

Accept these optional inputs:

- `base`: the fixed point for a three-dot diff, such as `main`, a branch, or a commit;
- `spec`: the originating task, plan, or specification as a path or verbatim text;
- `task`: the local task-file path when one exists;
- `change-class`: `plan-only`, `documentation-only`, `dependencies`, `configuration`, `code`, or `mixed`;
- `validation-tier`: `documentation`, `focused`, or `canonical`.

When invoked standalone:

1. Ask for `base` if it is absent.
2. Resolve `spec` from a supplied path, issue reference in commits, or matching plan or spec file.
3. If `change-class` or `validation-tier` is absent, inspect the fixed base and complete current
   diff, derive both values directly, and fail closed to `mixed` plus `canonical` when ambiguous.
4. If no spec exists, skip the Spec lens and report that fact in the final result.

## Review workflow

### 1. Inspect prior review files

Before reviewing, inspect every `reviews/*.md` file without modifying it. Search every checkout
attached to this repository, the main checkout included — review files are gitignored, so a file
written inside a worktree exists only there and is invisible from the main checkout:

```sh
# Every reviews/*.md in every checkout attached to this repository, main checkout included.
git worktree list --porcelain | awk '/^worktree /{ print $2 }' | while read -r wt; do
  [ -d "$wt" ] || continue
  find "$wt/reviews" -maxdepth 1 -name '*.md' -print 2>/dev/null
done
```

Use `find`, not a bare `*.md` glob: under zsh an unmatched glob is an error, so a checkout with no
`reviews/` directory would abort the search and produce a false "review loop is clean".

Skips worktrees not yet pruned. A repository with no linked worktrees yields exactly one path, so
this collapses to plain `reviews/` with no special case.

For files whose `**Branch:**` matches the branch under review:

- when any finding is `open`, stop, report the file and open finding identifiers, and tell the user
  to run `/skill:review-fix-worker` (or explicitly skip or accept the remaining findings);
- when no finding is `open`, retain the file as review history and continue with a new review pass.

Leave files for other branches untouched. Never delete resolved review files here. `finish-task`
removes every review file associated with the selected task only after the task reaches a CI-green
PR.

### 2. Resolve the diff

Preflight the tree before resolving anything:

```sh
git status --porcelain
git rev-list --count <base>..HEAD
```

- Uncommitted tracked or untracked task work present → stop. The panel reviews committed work
  only, because the review file records a fixed head SHA. Tell the user to commit the task work on
  the feature branch first (`implement-next-task` and `review-fix-worker` both end with a commit;
  if their work is uncommitted, commit it or re-run the failing step), then re-run `task-review`.
  Never commit on the user's behalf and never review the working tree.
- Zero commits between base and HEAD → stop and report the empty diff.

Confirm the base resolves. Capture:

```sh
git diff <base>...HEAD
git log <base>..HEAD --oneline
```

Stop on a bad base or empty diff. Record the branch and head SHA. Keep the base fixed throughout
review.

### 3. Resolve repository requirements

The review runs the task's acceptance commands itself; a review file that says validation "could
not be re-run" is not finished. When the checkout under review has no installed dependencies
(a fresh worktree), install them first with the repository's lockfile-frozen install, offline when
the store allows, and say so. Never substitute the task file's recorded results for a run.

Confirm or derive the change class and validation tier from the actual diff. Do not accept a
non-coding class when production or test code is present. Review current-task requirements and
established repository standards only. Report unrelated pre-existing problems as out of scope
findings and immediately mark them `deferred-out-of-scope`. This includes an acceptance criterion
that fails on the base branch for reasons the diff did not introduce: check the base before filing,
and defer rather than open.

Read the task file's sections with their intended weight:

- **Binding** (`What to build`, `Decided`, `Clarifications`, `Non-goals`, `Implementation work`,
  `Human checkpoints`, `Acceptance criteria`): requirements. Spec findings quote from here only.
- **`Decided`** and **`Clarifications`**: choices the user already made, with reasons
  (`Clarifications` holds answers given to the implementer mid-task). A finding that argues against
  an entry in either is not opened; it is recorded as `deferred-task-decision` with one line saying
  what the reviewer would have preferred, so the user can reopen the decision if they wish.
- **`Non-goals`**: excluded behavior. Its absence is never a finding; its presence is scope creep.
- **`Context`** and anything else: background. It creates no requirement and no finding. A known
  limit stated in `Context` is not a defect in the diff.
- **Trust model** (in `Decided`, for scripts and tools): who runs it, with what credentials,
  against what. Security findings are judged against this model, not against an arbitrary
  attacker. Where the task gives none, derive the obvious one from the code's location and say so
  in the file header (`**Trust model (derived):** ...`).

A finding whose failure scenario requires an input shape that the task's `Context` states does not
occur is graded no higher than `minor` unless the lens shows, from code, that the shape is
reachable. Tag it `**Origin:** task` and name the decision-table row or `Decided` entry the task
should have carried. The scenario is still worth fixing when the fix is small, but it is a planning
gap, not a major defect.

When a finding exists only because the task text prescribed the flawed design (a literal path, a
data source with no consumer, a wording the implementer copied), keep the finding, and additionally
tag it `**Origin:** task`. These findings are the planning feedback loop; the implementer should
not be graded for following the contract.

### 4. Decide whether Security runs

Run the Security lens when paths or diff content touch authentication, authorization, sessions,
secrets, tokens, input parsing, deserialization, SQL, shell or subprocess execution, network I/O,
file uploads, cryptography, sandboxing, CI trust boundaries, or prompt and guardrail code.

Otherwise skip Security and include `security_status: skipped-no-relevant-surface` in the final
result and the review file. A skip is not a security pass.

### 5. Run one independent review panel in parallel

For `plan-only` and `documentation-only` work, run Standards and Spec only. Add Bug only when the
diff contains executable examples, generated navigation, or another behavior-bearing documentation
surface. For other classes, run Standards, Spec, and Bug. Security remains conditional on the
surface rules above. Run each active lens in its own subagent, launching all active lenses in one
parallel batch (up to four subagents), and require only a JSON Finding array in response.

| Lens | Review target |
|------|---------------|
| Standards | Documented repository standards and meaningful tests |
| Spec | Missing, partial, incorrect, or out-of-scope behavior against the task or spec |
| Bug | Correctness, efficiency, and unnecessary complexity through the environment's code-review capability |
| Security | Exploitable trust-boundary failures through the environment's security-review capability |

Tell each subagent to inspect the diff directly, avoid invoking any task-review skill, avoid
spawning more subagents, and return findings with concrete evidence.

This is the only broad panel pass. Do not launch these lenses again.

### 6. Normalize and freeze findings

Dedupe identical findings while retaining every lens that reported them. Merge findings that share
one root cause and one fix into a single finding listing every location; twenty entries for five
defects is friction, not rigor. Reject unsupported claims that do not satisfy the Finding schema.
Separate findings into:

- non-security findings caused by the current diff;
- security findings;
- findings that argue against a `Decided` entry or demand a `Non-goal`, recorded as
  `deferred-task-decision`;
- unrelated pre-existing problems, which are recorded as `deferred-out-of-scope`.

Then calibrate severity with the table below. Subagents over-grade; the normalizing pass owns the
final severity and must lower any finding that does not meet its tier's test.

| Severity | Test |
|---|---|
| `blocker` | The primary deliverable gives a wrong result on its main path, a binding acceptance criterion is unmet, or a trust boundary is crossed by someone the trust model does not authorize. |
| `major` | A binding requirement is partially delivered, or a reachable secondary path gives a wrong result. |
| `minor` | Judgment calls: unused data, missing docs on exports, hardening beyond what the task asked against a party the trust model names, efficiency with no user-visible cost. |
| `nit` | A one-line code change that makes the code at that location easier to read. Nothing else is a nit. |

Concretely: a wording defect is never above `minor`; "could be hardened" is never above `minor`
unless the trust model names the party it defends against; a finding about code the task said to
write is `Origin: task` and no higher than `major`.

Then cut. These four rules remove findings; they do not lower them. There is no cap on the number
of findings that survive them.

- **Reachability.** A bug finding's scenario must be reachable with production data and
  configuration as they exist at review time. When the evidence depends on configuration nobody
  has set (an empty registry `defaults`, a provider option no agent uses), on data the fixtures
  and the trace model say does not occur, or when the lens itself calls the scenario latent,
  unconfirmed, or "no effect today", it is not a finding. Record it as one line under
  `## Watch list` so a later change can pick it up.
- **Test coverage.** A missing, weak, or misdirected test is a finding only when that test, had it
  existed, would have caught a bug this same review found; the finding names that bug's
  identifier. Every other test-coverage observation is dropped, including a test a work item
  named. A test clause inside a work item ("unit tests with a fake X returning two pages") is not a
  requirement; the behavior the item states is.
- **Trust model.** When the trust model is a single operator running the tool on their own machine
  with their own credentials, drop every security or hardening scenario whose only victim is that
  operator. Do not file it as `minor` or `nit`.
- **Nits.** A nit is a one-line code change that makes the code at that location easier to read.
  Phrasing that changes no meaning, comment style, commit-message format, changelog spacing, and
  file layout are not filed at any severity. A document that states something false about the
  code stays a `minor` standards finding.

Assign each accepted finding a stable identifier. Freeze this set. This skill never remediates, so
security findings are written as `open` like all others; the user decides fix-or-accept per finding
inside `review-fix-worker`.

### 7. Write the review file

Ensure `reviews/` exists at the repository root and is ignored by git: check
`$(git rev-parse --git-common-dir)/info/exclude` for a `/reviews/` line and append it when missing. The common dir is shared by
every worktree, so one line covers them all. Never add it to the tracked `.gitignore`. If the entry
cannot be added, stop and ask the user before writing findings.

Normalize any task path to its repository-relative path. Write one file per review pass. Use
`reviews/<task-file-stem>-<reviewed-head-short-sha>.md` when a task file exists, otherwise
`reviews/<branch-slug>-<reviewed-head-short-sha>.md`. Store the normalized path in `**Task:**`. The
file must be fully self-contained so `review-fix-worker` can start from a fresh context with no
other input:

```markdown
# Task review: <task title or branch>

**Repo:** <absolute repository root>
**Branch:** <branch>
**Base:** <base>
**Reviewed head:** <sha>
**Task:** <task-file path, or "none">
**Change class:** <change-class>
**Validation tier:** <validation-tier>
**Created:** <date and time>
**Lenses:** <lenses run, or "security: skipped-no-relevant-surface">
**Trust model:** <from the task's Decided section, or "(derived) ...">

## Findings

### TR-1 — major — bug
**Status:** open
**Location:** path/to/file.py:42
**Claim:** One sentence describing the problem.
**Evidence:** The rule, spec text, or failing scenario that proves the claim.
**Suggestion:** Optional one-line fix direction.

### TR-2 — minor — standards
**Status:** open
**Origin:** task
...

## Watch list

<One line per scenario the reachability rule removed: the scenario and what would make it
reachable. Not work for `review-fix-worker`. Omit the section when empty.>

## Planning feedback

<One line per `Origin: task` and `deferred-task-decision` finding: what in the task text caused it
and what the task should have said instead. Omit the section when empty. This is the input for the
next `to-plan` pass, not work for `review-fix-worker`.>
```

Never overwrite an existing same-named file. If one exists for the same reviewed head, report that
this head was already reviewed and return its next action: `review-fix-worker` when it has open
findings, otherwise `finish-task` when no implementation commit has landed since that review.

## Finding schema

Every finding uses this shape:

```json
{
  "id": "TR-1",
  "axis": "standards | spec | bug | security",
  "severity": "blocker | major | minor | nit",
  "location": "path/to/file.py:42",
  "claim": "One sentence describing the problem.",
  "evidence": "The rule, spec text, or failing scenario that proves the claim.",
  "suggestion": "Optional one-line fix direction."
}
```

Evidence is mandatory:

- Standards findings cite the rule and its source.
- Spec findings quote the task or spec requirement.
- Bug and Security findings give a concrete input-to-outcome scenario.

Severity follows the calibration table in step 6; subagents propose, the normalizing pass decides.
Optional fields: `"origin": "task"` when the task text prescribed the flawed design.

## Lens briefs

Give every lens the same framing: the sections of the task that bind, the `Decided` entries and
trust model, and the `Non-goals`. Tell each lens that `Context` is background, that a `Decided`
entry is not up for review, and that findings are merged by root cause.

### Standards

Give the subagent the diff command, commits, and repository standards files. Ask it to report
documented violations, missed current-task requirements, and tests that fail to verify real behavior
through public interfaces. Report a test gap only together with the concrete wrong behavior it
lets through; a test that is merely absent or merely synthetic is not a finding on its own. Skip
formatting and issues already enforced by tooling. A standard the
repository documents but does not enforce anywhere in its own code is `minor`. Never ask for more
comments. A comment that narrates the code beneath it, or repeats what the docstring already says,
is a `nit`; a docstring missing on an export is `minor`.

### Spec

Give the subagent the diff command, commits, and spec. Require a quote from a binding section for
each finding. Report missing or partial requirements, scope creep (including capabilities named in
`Non-goals` or not named anywhere), and incorrect behavior. A quote from `Context` does not support
a finding. A test clause inside a work item is not a requirement: quote the behavior the item
states, never the test it names.

### Bug

Ask the subagent to run the environment's code-review capability on the diff. Require a concrete
failing scenario and stamp `axis: "bug"` on each finding. Ask it to rank first any scenario in which
the deliverable's primary output is wrong on realistic input; those are the findings that matter.
Ask it to mark `latent` any scenario that needs configuration nobody has set or data the fixtures
and trace model do not contain, and to say what would make it reachable; the normalizing pass
moves those to the watch list.

### Security

Ask the subagent to run the environment's security-review capability on the diff, and give it the
trust model. Require a concrete attack or misuse scenario naming the attacker and the boundary
crossed, and stamp `axis: "security"` on each finding. A scenario in which the authorized operator
harms only themselves, or one that requires a boundary the task said would not be defended, is
not reported; the normalizing pass drops it.

## Final in-context result

Return a concise structured result containing:

- base and reviewed head SHA;
- references and standards checked;
- security status;
- the frozen finding set with identifier, axis, and severity;
- prior review files inspected and retained;
- the new review file path;
- deferred out-of-scope concerns and deferred task decisions;
- the watch-list lines;
- the planning feedback lines, so the user can carry them into the next `to-plan` pass;
- the exact next command: `/skill:review-fix-worker` when any finding is `open`, otherwise
  `/skill:finish-task`.

A review with zero findings still writes the file with an empty `## Findings` section, so the
manual loop has an explicit clean signal. Do not report success when the review file could not be
written.

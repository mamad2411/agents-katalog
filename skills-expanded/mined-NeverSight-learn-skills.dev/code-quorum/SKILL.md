---
name: code-quorum
description: Run independent code-review agents and synthesize verified findings.
disable-model-invocation: true
---

## Read-only boundary

The whole workflow inspects and reports. No agent in it edits reviewed files, generates or applies patches, commits, or begins remediation; recommendations point at a later, separately authorized workflow. Reproduce claims only with non-mutating commands or in disposable isolation that cannot alter the reviewed workspace.

## Confirm agents

Confirm the worker mechanism before touching the review scope.

Use the runtime's native subagent abstraction for the whole quorum. The reviewer names below are rubrics, not required configured agent names: create one fresh blind child per selected rubric and include that rubric in its task packet.

Every reviewer is a blind agent: fresh context, no prior conclusions, no reviewer passes in the delegator context. Concurrency is optional; blindness is required. When no mechanism can create blind agents, stop and return an execution-unavailable response naming the missing capability.

Complete this step when one mechanism can create a blind agent per reviewer.

## Resolve scope

Resolve explicit scope first. Otherwise resolve, in order, pending changes against `HEAD` including staged changes, unstaged tracked changes, and relevant untracked files; a branch from its merge-base; an associated pull request; a recent commit; or named task artifacts. Record any supplied or associated issue, pull-request description, specification, or acceptance criteria as the requirements source; record its absence. Never infer a whole-repository review. Flag unusually large inferred ranges.

Complete this step when the exact diff, range, or files and the requirements source or its absence can be stated.

## Select reviewers

Honor explicit reviewer names before named sets before the default set. Apply the user's focus, additions, and exclusions. Accept `simple` and `lightweight` as aliases for `quick`.

```yaml
quick:
  - correctness-reviewer
  - silent-failure-hunter
default:
  - correctness-reviewer
  - failure-mode-reviewer
  - silent-failure-hunter
full:
  - correctness-reviewer
  - failure-mode-reviewer
  - silent-failure-hunter
  - simplification-reviewer
  - test-behavior-reviewer
```

Unless excluded, add `requirements-reviewer` to any set when the requirements source states testable behavior. Load only the selected files from `references/reviewers/`.

Complete this step when the selection has one interpretation and every selected reviewer has an applicable rubric.

## Run the quorum

Give every reviewer an identical task packet — scope, source, changed files, requirements source or absence, focus, exclusions, project rules, read-only flag, finding contract — plus its one distinct rubric. Require every material candidate that clears the rubric's evidence bar, ordered by severity; `no_findings` completes a review when none clear it. Create one blind agent per reviewer through the confirmed mechanism, concurrently when capacity allows, sequentially otherwise.

Where the worker mechanism offers acceptance gates, disable them: the reviewers are the acceptance layer, and a gate can falsely fail valid reviewer output.

Wait for every reviewer to return, fail, or time out. Judge each result by its returned report, not the wrapper's lifecycle label — retain a complete report even when the wrapper flags an anomaly, and disclose the anomaly under coverage limitations. A missing reviewer contributes only a coverage limitation — never agreement or `no_findings`. Return an execution failure when no reviewer returns a usable result.

Complete this step when every selected reviewer has a usable result or a recorded failure reason, and at least one usable result exists.

## Normalize candidates

Normalize every candidate to `finding-v1`:

```yaml
title: Concrete failure or concern
location: { file: path/to/file, lines: 10-18 }
category: correctness
severity: critical | high | medium | low
claim: What is wrong
trigger: Conditions that expose it
impact: Resulting behavior or risk
evidence: [Relevant code-path evidence]
recommendation: Direction for addressing it
source_reviewers: [reviewer-name]
```

Require every field. List in `source_reviewers` only reviewers whose own report contains a materially equivalent claim — selection alone is not attribution evidence. Complete this step when every candidate conforms or has a rejection reason.

## Synthesize

Merge candidates by root cause. Remove style-only, speculative, pre-existing, and out-of-scope claims. Resolve disagreement from source evidence. Count a second reviewer as corroboration only when it contributes materially independent evidence, a distinct trigger, or a distinct failure mode.

Complete this step when each candidate is merged into a retained candidate or rejected with a reason.

## Verify

Resolve every retained candidate against source, safeguards, and tests. Use proportionate verification: trace the relevant code path, inspect callers and contracts, consult authoritative framework or platform behavior, and reproduce when the claim warrants it. Assign `verified`, `partially-verified`, `unresolved`, or `rejected` and record the method and evidence. Move important unresolved candidates to Open questions with the evidence that would settle them.

Complete this step when every retained candidate has a status, method, evidence, and report destination or rejection reason.

## Prioritize and report

Assign severity using these canonical meanings:

- `critical`: catastrophic, actively dangerous, or irreversible impact.
- `high`: material, ship-blocking defect.
- `medium`: important defect that is normally nonblocking.
- `low`: minor risk or worthwhile improvement.

Use `medium` as the reporting floor. Lower it to `low` only when the user explicitly asks for all recommendations. Build the verdict and every report section exclusively from candidates that meet the reporting floor; below-floor candidates are silently excluded and have no effect on the verdict.

Keep severity, verification, and disposition separate. Dispositions mean:

- `block`: a verified material finding.
- `address`: a verified or partially verified actionable finding whose known impact is nonblocking.
- `consider`: a verified low-risk simplification from the selected simplification reviewer.

Place important unresolved candidates and partially verified candidates with potentially ship-blocking impact only in Open questions; state the evidence that would settle them, and exclude them from the verdict. Omit rejected findings unless the user requests provenance. Use P0-P3 aliases only when requested.

Render the report exactly in this template — each section once, in this order, omitting Consider and Open questions when empty:

```markdown
## Verdict

<One sentence: **Merge**, **Merge after fixes**, or **Do not merge** — with the deciding reason.>

Scope: <range/PR · files · +/− lines> · Reviewers: <usable/selected> (<mechanism>)

## Do next

- [ ] `path/to/file:lines` — <imperative action> (finding 1)

## Findings

### 1. <Concrete failure in plain words> — <severity> · <disposition>

- **Where:** `path/to/file:lines` — <function or block name>
- **What:** <claim and trigger, at most two sentences>
- **Impact:** <resulting behavior or risk, one sentence>
- **Fix:** <one imperative sentence>
- **Verification:** <status> · <source reviewers>

## Consider

- `path/to/file:lines` — <one-line suggestion> (<source reviewers>)

## Open questions

- <Unresolved claim> — <the evidence that would settle it>

## Coverage

<Isolation, reviewer failures, and limitations in two or three lines.>
```

Every Do next item and every finding carries an exact `file:lines` location — when a reviewer supplied only a file or block name, resolve the line numbers from source before reporting. Do next lists every `block` and `address` item ordered by severity, one imperative line each; verified `consider` items from the simplification reviewer live only in Consider. Findings are numbered in Do next order so the checklist and the detail cross-reference by number.

Complete this step when the report matches the template: every reported candidate meets the reporting floor; every finding has severity, verification, and disposition; every finding, Do next item, and Consider item has an exact `file:lines` location; every finding has a one-sentence fix; each Do next entry names its finding; and each open question names the evidence that would settle it.

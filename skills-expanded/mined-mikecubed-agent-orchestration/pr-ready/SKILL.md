---
name: pr-ready
description: Run a final readiness pass on a stable branch or pull request diff using structured checks plus a final whole-diff review.
---

> All `docs/` paths in this skill refer to the plugin-level `docs/` directory (`../../docs/` relative to this file), not a `docs/` directory inside this skill folder.

## Purpose

Use this skill when a branch or pull request diff is finally stable and you want one last high-signal readiness pass before asking for human review.

This is a final integrated gate, not an inline coding step.

Persistent team, squad, or fleet-style long-lived orchestration is out of scope for this skill. Use a separate orchestration layer if persistent coordination is needed.

## When to Use It

Activate when the developer asks for things like:

- "run the final PR readiness pass"
- "check whether this branch is ready for review"
- "do a final integrated review"
- "give me a clear ready or not-ready verdict"

## Project-Specific Inputs

Before you start, identify:

- the stable review surface;
- the repository's target branch or comparison baseline;
- the repository's real validation commands;
- any available structured checker for code-bearing diffs;
- whether the current diff is code-bearing, docs-only, or config-only.

## Default Roles

Use:

- an optional **scout** for pre-slicing large diffs and preparing factual context;
- an optional **structured checker** for code-bearing diffs;
- a separate **final reviewer** for whole-diff judgment.

If no structured checker exists, continue with the final reviewer only. If the diff is small or focused, skip the scout and proceed directly.

### Escalation: Fleet / Agent Team Mode

If the active runtime offers a higher-cost orchestration mode such as a Fleet command or Claude Code agent teams, keep it optional and reserve it for unusually large or high-risk final review surfaces.

In most cases, one structured checker and one final reviewer are enough. Before escalating, explain the expected benefit and ask the developer whether they want the extra token cost.

Escalate only when:

1. the integrated diff is large enough that one reviewer would be noisy or shallow;
2. multiple specialized audit roles would materially improve the final judgment;
3. the review surface is already stable enough to coordinate as a team;
4. the developer explicitly opts in.

If team mode is approved, keep one final reviewer responsible for the single readiness verdict so the outcome does not fragment across agents.

### Model Selection

Resolve the active model for each role using this priority chain:

1. **Project config** — look for the runtime-specific config file in the current project root:
   - Copilot CLI: `.copilot/models.yaml`
   - Claude Code: `.claude/models.yaml`

   These are plain YAML files (no markdown, no fenced blocks). Read the `structured-check`, `final-reviewer`, and `scout` keys directly. If a key is absent, fall back to the baked-in default for that role — do not re-prompt for a key that is missing.

2. **Session cache** — if models were already confirmed earlier in this session, reuse them without asking again.
3. **Baked-in defaults** — if neither config file nor session cache exists, use the tier defaults below silently without prompting. Create project model config only when the developer wants persistent overrides.

#### Default model tiers

Defaults are **tiers, not pinned versions** — resolve each tier to the latest model of that tier available in the active runtime. In Claude Code, pass the tier alias to the Agent tool (`haiku`, `sonnet`, `opus`) — aliases are the only values it accepts, so Claude Code always runs the tier's latest model. Pinning an exact model version via `models.yaml` is a Copilot CLI capability (`.copilot/models.yaml` only).

| Role             | Claude Code                          | Copilot CLI                      | Effort |
|------------------|--------------------------------------|----------------------------------|--------|
| Structured check | `opus` (latest Opus)                 | latest GPT or latest Claude Opus | high   |
| Final reviewer   | `opus` (latest Opus)                 | latest GPT or latest Claude Opus | high   |
| Scout            | built-in `Explore` agent, or `haiku` | latest Claude Haiku              | low    |

See `docs/model-selection.md` in this plugin for the full role matrix, per-role effort guidance, and the premium-tier (Fable) opt-in policy, and `docs/models-config-template.md` for ready-to-copy config templates.

## Preconditions

Before invoking this skill:

- the intended changes are already integrated;
- the branch or diff is stable enough to review as a whole;
- obvious validation failures have already been addressed.

If the diff is still moving significantly, stabilize it first.

## Workflow

### 1. Establish the stable review surface

Before running the final gate:

1. confirm the active branch and review target from the current PR metadata or
   branch baseline;
2. verify the intended changes are already integrated by comparing the PR
   title, description, recent commits, and actual diff;
3. identify the final review surface:
   - preferably the pull request diff against the target branch;
   - otherwise the stable branch diff against the agreed baseline.

Evaluate the integrated result, not a partial local slice.

Default to self-service scope verification. Do **not** ask the developer to
confirm that the PR still matches its intended scope unless the evidence
remains genuinely ambiguous after inspecting the current review surface. Ask
only when:

- the PR title, description, and diff suggest materially different intended
  outcomes;
- the branch contains unrelated extra work and no defensible in-scope subset is
  obvious;
- recent history rewrote the branch enough that the prior review basis is no
  longer inferable;
- conflicting reviewer expectations cannot be reconciled from the current PR
  evidence.

When only part of the diff is ambiguous, judge the unambiguous portion and
record the ambiguous slice as a blocker or unresolved question instead of
blocking automatically.

#### Pre-slicer discovery

Before proceeding to structured checks, run a fast scout pass to prepare the review surface for efficient downstream processing:

1. if diff scope, affected modules, or validation facts are already known from earlier in the current session, reuse those facts directly instead of rediscovering — this refers to context already present in the bounded session, not an artifact contract with another skill;
2. identify the diff structure: affected modules, file categories (code, tests, config, docs), and approximate size;
3. note high-risk or cross-cutting modules for prioritization during structured checks;
4. produce a discovery brief per `docs/workflow-artifact-templates.md` with at least: task shape, relevant files, comparison baseline, and validation commands.

Skip the scout pass when the diff is small or focused enough that a single reviewer can process it without pre-slicing — for example, fewer than roughly ten files in a single coherent module.

### 2. Decide whether a structured checker applies

If the stable diff is:

- code-bearing — run the structured checker if one exists;
- docs-only or config-only — skip structured code checks and continue with the final reviewer.

Do not force code-only tooling onto a non-code diff.

When multiple checker options exist, prefer the most semantic one available:

1. repository-specific structured reviewers or MCP-backed analyzers;
2. language-aware tooling such as LSP-backed or AST-aware checks;
3. text-only grep-style checks as a fallback.

### 3. Run structured checks in report-only mode

When a structured checker applies:

1. scope it to the stable integrated diff;
2. keep it report-only;
3. collect findings without automatically changing files;
4. if Fleet or agent-team mode is in use, require one aggregated finding summary before the final reviewer starts.

If the diff is large enough that a single pass becomes noisy, split the review into
coherent slices first and preserve one final whole-diff judgment at the end.

Instruct the checker to report **every** finding, tagged with severity and confidence, rather than self-filtering for importance — filtering happens at triage (Step 4), not in the checker. Current-generation models follow severity filters literally and silently drop real findings.

Focus on:

- security issues;
- architecture or boundary drift;
- dead code or duplicate wiring;
- naming or complexity regressions;
- observability and test-quality gaps that matter on the final diff.

#### Rescue policy for structured-check delays

When the structured checker stalls, times out, or the diff is large enough to cause processing delays, apply the following rescue-before-abandon sequence instead of immediately stopping the gate:

1. **Narrow scope** — reduce the diff to the highest-risk modules. Use the discovery brief when one was produced, or fall back to git-diff file-level heuristics (largest files, most cross-cutting paths) when discovery was skipped on a small or focused diff.
2. **Drop non-critical checks** — skip checks that would not change the final verdict, such as stylistic or low-severity rules.
3. **Serialize remaining work** — run remaining checks sequentially rather than concurrently to avoid compounding resource pressure.
4. **Re-evaluate after rescue** — if the reduced scope completes, proceed to triage and the final reviewer as normal. If the rescue itself stalls or produces no usable findings, record the failure and escalate to the developer before abandoning.

Do not abandon the gate because a single checker stalled or the diff was large. Always attempt at least one rescue pass and record any scope reductions, skipped checks, or processing-delay mitigations in the readiness report.

### 4. Triage structured findings

Classify findings into:

- blocker
- fix-now
- follow-up
- not applicable

Do not treat every automated finding as truth. Ground them in the actual code and diff.

#### Blocker verification

Adversarially verify each `blocker` finding before it reaches the verdict: send the finding and the relevant code context to a read-only verification pass on the `flow:reviewer` agent — which both runtimes resolve by that plugin-qualified name — with the instruction to **refute** the finding against the actual code. A finding that survives refutation stays a blocker; a refuted finding is downgraded with the refutation recorded. Bound the pass to blocker findings only. When there are no blockers, skip it and record `Blocker verification: skipped` in the readiness report.

### 5. Run a final whole-diff review

After any structured findings are triaged:

1. run a final substantive review over the whole stable diff;
2. ask the reviewer for **full coverage, not self-filtered severity** — every issue found, tagged with severity and confidence; triage at the coordinator decides what blocks. Focus areas:
   - correctness regressions;
   - cross-fix interaction bugs;
   - test sufficiency;
   - contract drift;
   - security issues the earlier loops missed.

### 6. Produce an explicit readiness verdict

End with one of these outcomes:

- ready for review
- ready with follow-ups
- not ready
- stopped by user

### 7. Report clearly

Produce a readiness report following the template in `docs/workflow-artifact-templates.md`. The report MUST record:

- review surface;
- structured checker, or `none`;
- current state;
- blockers;
- blocker verification outcome (`run` or `skipped`);
- fix-now items;
- follow-ups;
- skipped checks, if any;
- unresolved questions;
- next action;
- final readiness verdict.

The report MUST also include the workflow outcome measures defined in `docs/workflow-artifact-templates.md`:

- `discovery-reuse` — `yes`, `no`, or `skipped` (whether the discovery brief was reused by downstream checks);
- `rescue-attempts` — integer count of rescue attempts during the gate, or `0`;
- `final-gate-result` — one of `ready`, `ready-with-follow-ups`, `not-ready`, or `stopped`, using the normalized token form of the verdict above:
  - `ready for review` -> `ready`
  - `ready with follow-ups` -> `ready-with-follow-ups`
  - `not ready` -> `not-ready`
  - `stopped by user` -> `stopped`

Populate these fields once, at gate completion. If the gate stops early, record whatever measures are available and note which fields are incomplete.

The result should make the next action obvious.

## Example Readiness Report

Use a durable report shape so the next actor can make a decision quickly. For example:

```text
Review surface: PR #128 against main
Structured checker: codex review + repo test suite
Current state: done
Blockers:
- Missing null-path coverage in src/api/createWidget.js
Blocker verification: run (1 confirmed, 0 refuted)
Fix-now:
- Rename duplicate option key in plugin.json example
Follow-ups:
- Consider extracting shared validation helper after merge
Skipped checks:
- None
Unresolved questions:
- None
Next action: Send back for the one fix-now item, then rerun readiness
Verdict:
- ready with follow-ups
discovery-reuse: yes
rescue-attempts: 0
final-gate-result: ready-with-follow-ups
```

## Required Gates

A final readiness pass is not complete until:

- the stable diff was evaluated as a whole;
- any structured findings were triaged when applicable;
- a final substantive review was performed;
- an explicit readiness verdict was produced;
- a durable readiness report following `docs/workflow-artifact-templates.md` has been published.

### Verification checklist — readiness verdict

Before issuing a readiness verdict, confirm ALL of the following.

**CI state gate**
- [ ] All CI checks are in a terminal state (passed or failed) — none are pending — PASS / FAIL
  If any check is still pending: block and instruct the developer to wait for all checks
  to settle before the skill produces a verdict.

**Review state gate**
- [ ] No unresolved review comments exist on the PR — PASS / FAIL
  (A comment is "unresolved" if it has not been replied to or marked resolved.
  If human confirmation is needed, pause and ask — do not auto-pass.)

**Diff integrity gate**
- [ ] The diff matches the stated intent of the PR description — PASS / FAIL
  (Determine this from the PR title, description, recent commits, and actual
  diff first. Ask the developer only if those sources still leave genuine
  ambiguity or conflict.)

If any item is FAIL: surface the item and do not issue a "ready to merge"
verdict until all required items are PASS. If genuine ambiguity remains after
inspection, surface the conflicting evidence, ask the developer only about that
ambiguity, and pause the verdict until it is resolved.

## Stop Conditions

- the review surface is still changing materially;
- structured findings conflict and no human tie-breaker is available;
- required validation commands or comparison baseline are still unknown;
- the diff is too large to judge coherently without first reducing or chunking it;
- a structured checker stalls, times out, or the diff causes processing delays, and rescue-before-abandon (see § Rescue policy for structured-check delays) has been attempted and failed;
- the developer asks to stop.

Before stopping because a structured checker stalled or the diff exceeded the review budget, always follow the rescue-before-abandon sequence defined in § Rescue policy for structured-check delays: narrow scope, drop non-critical checks, serialize, and re-evaluate. Stop only after the rescue pass fails or the developer confirms abandonment.

When a hard stop is necessary, report why the gate is not yet trustworthy, record the rescue attempt and its outcome, and resume only on a stable diff.

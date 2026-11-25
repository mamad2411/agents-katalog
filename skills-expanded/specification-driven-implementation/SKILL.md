---
name: specification-driven-implementation
description: Use when implementing or reviewing substantial work against an AIP release or increment specification (the release specification or its iN-*.md increment specs) - producing a reviewed plan before changing production code, persisting it, implementing without altering normative semantics, reconciling the result against the retained plan, and driving PR reviews to a clear approval decision. Not needed for small maintenance changes that don't touch public contracts, identity, evidence, qualification, reconciliation, or release semantics.
---

# Specification-driven implementation

This skill is **procedural, not normative**. It cannot override
[product doctrine](../../../docs/product-doctrine-and-strategic-direction.md),
[`ROADMAP.md`](../../../ROADMAP.md) boundaries, or any specification under
[`docs/specifications/`](../../../docs/specifications/). Where this skill and a specification
disagree, the specification wins — stop and flag the conflict rather than following this skill
past it. See [`AGENTS.md`](../../../AGENTS.md) for the mandatory-behavior list this skill executes.

**Tests are evidence, not qualification.** Agent-authored tests demonstrate that an implementation
does what the plan says it does — they are implementation evidence. They are never independent
qualification of the specification itself, and passing tests can never resolve a specification
ambiguity. If the specification is ambiguous about what "correct" means here, no amount of green
tests answers that question — only a specification decision does.

**Unit tests first; integration tests only when they earn their cost.** The default home for a test
is `tests/unit` (pure logic, canonicalization, contract/schema parity, Cypher text, fakes of the
graph port). An integration test (real Neo4j via Testcontainers, or Docker/Compose) is added only
when the behavior under test cannot be observed without the real dependency: Neo4j's actual Cypher
or constraint semantics, transactions, concurrency and the revision fence, persistence round trips,
or one real-transport end-to-end proof per public surface. Rules that follow:

- Plan and PR must state, per new integration test, the dependency-only behavior it proves and why
  no unit test can. If the answer is "it is more realistic", write the unit test.
- Test the risk at the shallowest layer that contains it. Service logic is proven once at the
  service; REST and MCP get thin parity tests per answer family (shape, error mapping, transport),
  not a re-run of every scenario. Cross-cutting invariants ("byte-identical", "revision fence
  unchanged", "refusal writes nothing") are asserted once, parametrized, not per surface per file.
- Share expensive setup (session-scoped Neo4j, a module-scoped world). A new frozen world or
  fixture build that costs seconds must be reused by existing modules or justified in the plan.
- Benchmark and tool *wiring* checks run at the smallest scale that proves structure, or as unit
  tests with fakes. Spike and characterization suites are evidence for a finding: when the finding
  is closed, reduce them to the few assertions still guarding live behavior or delete them.
- Qualification and release-evidence suites (frozen references, oracle runs, real third-party
  containers) are not per-PR checks by default. Keep them in a separate tier (marker/job) that
  runs on release candidates and when their inputs change, unless the owner decides otherwise.
- Time is a cost to track: new integration modules over ~5 s, or that add a container image pull,
  need an explicit tier decision in the plan. Review `--durations` output in CI when the suite grows.

**Stop on unstated semantic decisions.** If implementing the plan requires a decision the
specification doesn't state — a precedence rule, an identity formula, a conflict-resolution
outcome, an unsupported-case behavior — stop and return the decision to the specification (ask the
human, or propose a specific, disclosed specification amendment). Do not silently pick a default
and continue.

**Small-change exemption.** A maintenance change that doesn't alter public contracts, identity
rules, evidence/provenance semantics, qualification behavior, reconciliation logic, or release
semantics does not need this full workflow. When genuinely uncertain whether a change qualifies,
treat it as substantial and run the full workflow anyway.

**Documentation-only pre-PR validation exemption.** When the complete proposed PR diff contains only
documentation and has no source relevance, do **not** run the repository's unit/integration test
suites merely as a prerequisite to opening the PR. "No source relevance" means the change touches no
production or test source, executable examples/fixtures, documentation read or asserted by tests or
scripts, schemas, configuration, workflows, dependency/lock files, generated artifacts,
version/build metadata, release notes, changelogs, completion records, or other release-candidate
content whose contents can change runtime, build, validation, release, or qualification behavior.
Before relying on this exemption, inspect the complete diff and state why it is documentation-only.
Run only lightweight
validation that can provide signal for the changed documents (for example Markdown/link/reference
checks when such tooling exists). Once the PR exists, normal CI remains authoritative and may still
run repository-wide tests. If any changed file has plausible source/runtime/build/qualification
relevance, the exemption does not apply.

## Planning-start telemetry

For every substantial workflow that uses this skill, record one immutable planning-start timestamp
before phase 1 begins.

1. Capture the current time once, in UTC, as RFC 3339 / ISO 8601 with whole-second precision:
   `YYYY-MM-DDTHH:MM:SSZ`.
2. Immediately notify the human in the active interaction:
   `Planning started at <timestamp>.`
3. Keep that exact value unchanged for the lifetime of the work. Re-review, resumed sessions, plan
   revisions, implementation, and reconciliation do not reset it.
4. When the first pull request for the work is opened, add exactly one hidden machine-readable marker
   to the PR description:

   ```html
   <!-- aip-agent-metadata:v1 {"planning_started_at":"2026-09-18T20:41:12Z"} -->
   ```

   Substitute the captured timestamp; do not use the example value.
5. Preserve the marker verbatim through later PR-description edits. If a valid marker already exists, keep the earlier of the existing marker value and your captured timestamp (never overwrite an earlier value).
6. Never invent or retrospectively estimate a missing planning-start timestamp. Historical work that
   predates this convention remains uninstrumented.

The timestamp measures when the agent begins substantive specification/repository planning, not when
the PR is opened and not when the first implementation commit is created. This makes
`planning_started_at -> merged_at` computable from GitHub without changing the implementation
workflow.

Do **not** encode the timestamp in a GitHub label. Labels are repository-scoped categorical metadata,
so a timestamp label would create a new repository label for every PR and pollute the label
namespace. A single static label such as `agent-driven` MAY be used independently for filtering if
the repository adopts one, but the timestamp remains in the hidden PR metadata marker.

## The nine phases

1. **Resolve the governing specification and revision.** Identify the exact release and increment
   spec (or parent spec) this work is governed by, and its exact revision/draft marker (e.g. "Draft
   0.3, amended during PR3b — see its own §12 amendment note"). Read the product doctrine and
   `ROADMAP.md` context around it, not just the increment file in isolation.

2. **Inspect the current repository and relevant prior implementation.** Read what already exists:
   related modules, prior completion records (`iN-completion-record.md` for earlier increments in
   the same release), existing tests, existing utilities. Reuse existing patterns and functions
   before proposing new ones — a fresh module that duplicates something already in `app/` is a
   planning failure, not a stylistic choice.

3. **Identify ambiguities or conflicts before planning.** Surface anything the specification leaves
   unstated or that conflicts with product doctrine/roadmap/another spec *now*, before writing the
   plan — not mid-implementation, when a stop-and-ask costs a throwaway diff instead of a throwaway
   sentence.

4. **Produce the bounded implementation plan**, using the template below. Bounded means explicit
   non-goals, not just an explicit scope.

5. **Wait for human review before any production-code change.** The plan is not authorization to
   start; it's a draft for the human to approve, redirect, or reject.

6. **Persist the approved plan, verbatim, in the GitHub issue or the initial PR description.** This
   is the record of what was promised — it must survive independent of any later summary.

7. **Implement without changing normative semantics.** The plan bounds scope; it does not license
   reinterpreting the specification along the way. If the plan itself turns out to be wrong once
   implementation starts, that's a return to phase 3, not a silent in-flight redefinition.

8. **Execute the specified validation and qualification steps** — the plan's own "Validation
   Commands" section, run in full (this repo's real `tests/unit` and `tests/integration -m "not qualification"`
   suites, lint, format — not a hand-picked subset; add `-m qualification` when the change touches the
   qualification tier's inputs, see `docs/development.md`), **except for the documentation-only pre-PR validation
   exemption above**. For a qualifying docs-only PR, do not run unit/integration suites before PR
   creation solely to satisfy this phase; record the inspected diff and any lightweight
   documentation validation instead, then rely on normal PR CI for repository-wide checks. For all
   source-relevant changes, run autofixes (`ruff format`, `ruff check --fix`) and then
   `uv run pyright` and `uv run lint-imports` before tests, not after, so the common case needs only one test run. This is not a blanket "autofixes never affect
   behavior" claim — `ruff check --fix` applies whatever rules are enabled, which can rewrite
   program text beyond formatting/import ordering, so treat that possibility as real: if an autofix
   runs *after* a test run that already passed and it changes source, rerun the affected (or full)
   suite before treating validation as final. The point is to avoid a redundant re-run for zero new
   signal, not to skip re-verifying a change that could plausibly affect behavior.

9. **Reconcile the final implementation against the *retained* original plan**, using the
   reconciliation template below. This is a diff against what was promised, not a fresh
   retrospective that quietly replaces the plan — both documents should remain visible together.

## Pre-PR refactoring check

Before opening a PR with Python code changes, inspect the changed code for material unnecessary
complexity, duplicated logic, and misplaced responsibilities. Apply small, behavior-preserving
improvements within the approved scope when they have a concrete benefit. Preserve all governing
specification requirements, public contracts, determinism, and AIP's evidence/provenance,
identity, qualification, and snapshot/observation-context semantics.

If a useful refactoring would expand the approved plan or change architectural/contract semantics,
report it separately; do not silently enlarge the PR. Re-run the applicable validation from phase
8 after any source change. Skip this check for documentation-only changes. This is a lightweight
check within the existing workflow, not an additional approval gate or a reason to block on
cosmetic preferences.

For Python-changing PRs, record the outcome in the PR description under **Refactoring report**:
- **Refactoring performed:** Yes / No.
- **Improvements:** Name concrete, diff-verifiable changes (prefer file/function references), or
  `None needed`.
- **Remaining structural debt:** Material findings only, or `None identified`.
- **Verification:** Checks actually run after any refactoring, or explicitly note what was not run.

A `No / None needed` outcome is valid. Never claim a refactoring happened without an identifiable
code change. Omit the report for documentation-only PRs; this is reporting, not an extra gate.

## Mandatory pre-PR independent review

After phase 8 validation and the refactoring check, but before opening the implementation PR, run
the repository's [`aip-reviewer`](../../../.claude/agents/aip-reviewer.md) against the complete
branch diff. Give it the governing specification revision and retained plan. This is a sequential
review pass, not permission to spawn parallel review agents.

- Resolve every BLOCKER/MAJOR finding before opening the PR.
- If the reviewer identifies an unstated semantic decision, return to phase 3 and the owner; tests
  cannot resolve it.
- After material fixes, rerun the affected validation and the reviewer once. Do not loop on
  MINOR/NIT findings.
- In the PR body, record only the final verdict and any intentionally retained MINOR/NIT findings;
  do not add a round-by-round self-review log.
- If the complete diff qualifies for the strict documentation-only pre-PR validation exemption
  above, skip this reviewer pass as well. Specifications, completion records, release notes,
  schemas, fixtures and other release-candidate content are already excluded from that exemption.

## Checking for review feedback

Before treating a "findings check" as complete — whether re-reviewing a PR or responding to
feedback on one you implemented — enumerate every comment surface, not just the first one found:
top-level PR review submissions (each reviewer's own review body, including bot reviewers like
Copilot), inline/line-level review comments, and plain issue-level PR comments. These are separate
API surfaces and separate UI sections; checking one does not surface the others. A comment from a
second reviewer (human or automated) can arrive close in time to a bot's and raise different
findings that don't overlap at all — cross-reference the full list before concluding the fixes
already made cover everything raised, not just the first source checked.

A single check of these surfaces is only a snapshot: a bot review and a human review can land
close together but asynchronously, so a query run right after one review lands can genuinely
return nothing for a slower reviewer that posts moments later — not because it was skipped, but
because it hadn't landed yet. Re-check all comment surfaces again once a fix is pushed and before
declaring the round closed, rather than trusting the enumeration taken at the start of the round.

## PR review convergence

For a specification-governed PR review, make the first substantive review as complete and
acceptance-oriented as the available evidence permits. Include the reviewed head SHA and consolidate
all known material blockers in one comment. For each blocker, cite the governing requirement, point
to concrete implementation evidence, state the required outcome without unnecessarily prescribing
the implementation, and identify the regression test or qualification evidence needed. End with an
explicit approval condition.

Re-reviews are limited to:

- resolving the recorded blockers;
- checking the requested evidence and CI; and
- identifying material correctness, security, interoperability, release-validity, or explicit-gate
  regressions introduced by the fixes.

Maintain a clear disposition of prior blockers, distinguish genuinely new blockers from unresolved
ones, and explain why any new blocker was not reasonably identifiable earlier. When a material
finding represents a repeated pattern within the changed surface, inspect and resolve the same class
of occurrence across that bounded surface rather than fixing only the cited line. Do not turn that
into unrelated repository-wide cleanup. Do not extend the review with cosmetic, procedural, or
merely preferable changes; record worthwhile out-of-scope work separately. Once the blocker list is
empty and required evidence is green, approve or explicitly report no blocking findings.

### Promote recurring findings into reusable guards

If the same material review finding recurs across multiple PRs, do not rely indefinitely on review
comments to catch it. Propose the smallest durable enforcement point in a separate scoped change:
an existing test/invariant, a static or lint check, the `aip-reviewer` checklist, `AGENTS.md`, or
this skill. Prefer mechanical enforcement when the rule is mechanical. Do not enlarge the current
implementation PR merely to institutionalize the lesson unless that guard is already inside its
approved scope.

Use this compact comment shape when useful:

```markdown
**Review of head `<sha>`**

Previous blockers: <resolved/remaining summary>.
New blockers: <none, or material findings with governing requirement and evidence>.
Required evidence: <tests, qualification, and CI>.

**Exit condition:** <specific conditions after which the PR will be approved, unless their fixes
introduce a material regression>.
```

## Plan template

```markdown
## Governing Specification
<path + exact revision/draft marker>

## Scope & Non-Goals
<bounded scope> / <explicit non-goals>

## Affected Components
<modules, files, expected change surface>

## Requirement -> Task Mapping
<specification requirement -> implementation task, one row per requirement>

## Acceptance Criteria -> Test/Evidence Mapping
<acceptance criterion -> test(s) or evidence that will prove it; mark each test unit or
integration, and for every integration test name the dependency-only behavior it proves>

## Validation Commands
<exact commands to run, e.g. `uv run pytest tests/unit`, `uv run pytest tests/integration -m "not qualification"`,
`uv run ruff check .`, `uv run ruff format --check .`, `uv run pyright`, `uv run lint-imports`>

## Rollback / Recovery (when applicable)
<for migrations, persisted-state changes, release/build behavior, or other hard-to-reverse paths,
state how to recover or roll back; omit when not applicable>

## Open Questions / Assumptions / Stop Conditions
<anything unresolved, any assumption made explicit, any condition that should halt implementation
and return to the specification>
```

## Reconciliation template

```markdown
## Completed As Planned
<what matches the plan exactly>

## Deviations & Justification
<what changed from the plan, and why>

## Specification Questions Discovered
<any ambiguity or gap surfaced during implementation, and how it was resolved (or that it's still
open)>

## Deferred Work
<what was explicitly out of scope or pushed to a later increment>

## Test/Qualification Evidence
<the actual validation-command results, e.g. exact pass counts>

## Remaining Limitations
<what this implementation does not cover, disclosed rather than silently omitted>
```

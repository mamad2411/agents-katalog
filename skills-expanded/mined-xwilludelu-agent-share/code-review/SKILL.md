---
name: code-review
description: Review a repository or requested scope for evidenced bugs, architecture and maintainability problems, cognitive load, duplication, dead code, and obsolete compatibility; fix only when authorized. Use for explicit code reviews, repository audits, or codebase health, architecture, coupling, and dead-code assessments. Default to the whole repository when no scope is specified; do not trigger for routine changed-code review or implementing a known issue.
---

# Code Review

Review the code as a system, not as a collection of files. Find the smallest set
of evidenced problems that explains its correctness and maintenance costs. Favor
fewer concepts, clear ownership, and one authority per idea over checklist
compliance or personal taste.

## Set the frame

- Default to all first-party source, tests, configuration, and scripts. Exclude
  generated, vendored, dependency, cache, and build-output trees unless their
  treatment is itself the problem.
- Honor a user-specified package, feature, directory, file set, or change as the
  primary scope. Follow callers, consumers, shared definitions, and neighboring
  conventions far enough to judge it correctly.
- When version-control evidence is available, record the reviewed commit and
  working-tree state. Existing user changes are part of the evidence, not
  material to overwrite.
- Infer project intent and conventions from its instructions, manifests,
  documentation, tests, and code. Framework convention and recorded tradeoffs
  outrank generic advice.
- Establish how much cleanup authority exists. An explicit user statement,
  project instructions, or clear repository ownership may establish an
  autonomous personal or small-team project. Without positive evidence, assume
  compatibility and external consumers matter.

Stay read-only while forming and vetting the review, even when fixes were
authorized upfront.

## Map before judging

Read the repository shape, entrypoints, package boundaries, public surfaces,
data and control flow, persistence boundaries, and existing verification
commands. Build a working model of which module owns each important concept and
which direction dependencies should flow. For small-to-medium repositories,
inspect all in-scope first-party code rather than sampling only hotspots.

Trace behavior through imports, routes, registrations, configuration, and tests.
A text search is a lead, not proof of reachability or non-use. Pay special
attention to code that crosses trust, process, network, storage, or package
boundaries, because mistaken assumptions concentrate there.

## Review through three primary lenses

### Correctness

Look for concrete ways reachable behavior can disagree with its contract:
invalid state transitions, wrong variables or conditions, unchecked boundary
values, swallowed failures, partial multi-step writes, stale state, async or
resource-lifecycle mistakes, and assumptions contradicted by callers or data.
Treat tests and types as witnesses, then inspect what they do not constrain.

Notice obvious security and performance failures when the code establishes the
path: missing authorization, unsafe interpreter or filesystem boundaries,
secret exposure, N+1 work, unbounded reads, or repeated expensive work. Do not
turn the review into a speculative security or performance checklist.

### Architecture and cognitive load

Ask how many concepts a reader must hold to explain a behavior and how many
places must change together. Inspect ownership, dependency direction, layer and
package crossings, feature logic leaking into shared code, oversized mixed
responsibilities, hidden invariants, and abstractions that expose rather than
hide complexity.

Prefer deep modules: a small interface that contains substantial behavior and
keeps knowledge local. Use the deletion test on wrappers and layers: if deleting
one makes complexity disappear, it was likely pass-through machinery; if the
complexity spreads into many callers, the module was earning its place. A seam
is justified by real variation or a real boundary, not by hypothetical reuse.
Testability is evidence about the shape of an interface, not a reason to expose
implementation details.

### Redundancy and obsolete structure

Search for duplicate code, but prioritize duplicate concepts: parallel types,
schemas, clients, constants, policies, state rules, configuration, or business
logic that create competing authorities. Distinguish code that merely looks
similar from behavior that must evolve together; the wrong shared abstraction
costs more than local duplication.

Trace apparent dead code through static and dynamic entrypoints, configuration,
scripts, tests, reflection, and external surfaces before calling it dead. In an
autonomous project, treat confirmed dead code, completed feature flags, obsolete
compatibility paths, superseded implementations, and speculative abstractions as
liabilities to remove rather than artifacts to preserve. Be conservative where
ownership or consumers remain uncertain.

## Turn observations into findings

A finding must make a falsifiable claim and carry enough evidence for another
reader to reproduce the judgment:

- Cite the strongest `file:line` locations and the relevant caller or consumer.
- Explain the triggering path or structural mechanism and its concrete
  consequence.
- Separate severity from confidence. Use high, medium, or low confidence as the
  evidence warrants; a low-confidence finding still needs a specific signal and
  must be framed as investigation rather than fact.
- Recommend the change in terms of the responsibility, authority, branch,
  layer, or code that should disappear or move. Do not prescribe a large design
  when several valid implementations remain.

Re-read every cited location in context before reporting it. Reject behavior
that is intentional, unreachable speculation, preference without maintenance
cost, and findings whose claimed mechanism is disproved by tests or already
settled by project decisions. Distinguish a test that disproves the triggering
path (withdraw the finding) from a test that merely asserts the flagged
behavior (check requirements and callers to determine whether the behavior is
intentional or both implementation and test need fixing). Merge symptoms that
share one root cause. Do not pad the report with quotas, health scores, fixed
file-size rules, generic missing-doc advice, or style nits.

Prioritize by consequence, breadth, confidence, fix cost, and fix risk. A short
set of high-value findings is better than exhaustive low-value commentary, but
state what was not covered so brevity is not mistaken for completeness.

## Verify with the repository

Run existing checks that are relevant, reasonably bounded, and unlikely to
change external state: tests, type checks, lint in check mode, builds, or
installed static-analysis tools. Do not install dependencies, start persistent
services, use privileged credentials, apply migrations, deploy, or mutate
external systems merely to complete a review. State skipped checks and why.

A clean check can reject a hypothesis or support a finding; it cannot substitute
for reading the behavior and structure under review.

## Report, then act if authorized

Lead with the reviewed scope, commit and working-tree state, and verification
status. List findings in priority order. For each, include severity, confidence,
claim, evidence, mechanism or trigger, consequence, and requested change. End
with checks run and material coverage gaps. If no material findings survive
vetting, say so directly and name the residual uncertainty.

Do not generate implementation plans, create issues, or modify code unless the
user asks. Without prior authorization, ask which findings to fix. With prior or
subsequent authorization, implement the vetted changes in root-cause order and
run the cheapest decisive project checks. In an autonomous project, fix
authorization may include deleting compatibility paths or changing public
interfaces and repository-local migration code; it does not by itself authorize
applying a migration, publishing, deploying, or changing any live external
state.

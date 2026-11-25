---
name: plan-milestone
description: >-
  Plan an executable project milestone by discovering repository guidance,
  roadmap and planning context, milestone history, open issues, and dependency
  relationships; balance candidates across business value, usability, known
  issues, and new needs, then propose a goal-shaped milestone. Use when a user
  asks to plan a milestone or sprint across multiple issues. Keep tracker
  writes behind explicit approval; do not use for starting or finishing one
  issue.
---

# Plan a milestone

Produce a milestone proposal that can be executed in dependency order and
whose promised outcome matches the available capacity. Planning is read-only
by default. Creating a milestone or changing issue assignments is a separate,
explicitly approved action.

## Discover the current state

Start by identifying the repository, configured issue tracker, and applicable
instructions. Use repository remotes, tracker configuration, contribution
guides, and instruction files to discover the tracker; if they identify
different trackers and the choice changes scope, ask before proceeding. Read
every relevant `AGENTS.md`, `CLAUDE.md`, contribution guide, and project policy
file that applies to the checkout. Find the roadmap and current planning
documents by inspecting the repository; do not assume a particular directory,
filename, or naming convention. Load the current stage, locked themes,
delivery window, stated exclusions, capacity assumptions, and recent evidence
before selecting work.

Use the tracker’s read-only CLI/API or connected tracker tool to inspect:

- all open and recently closed milestones, including their descriptions and
  unfinished issues;
- the open milestone, if one exists, before considering new work;
- open issue bodies, labels, status, assignee, milestone, estimates, and
  acceptance criteria;
- issue relationships and any linked planning records available from the
  tracker.

Do not read unrelated private material or print credentials. If a repository,
issue body, relationship, or planning document is inaccessible, record that
fact and keep the affected work from being presented as unblocked.

## Build the dependency graph first

Re-evaluate carry-over issues against the current graph before adding new
candidates. Collect declared `Dependencies`, `Blocked by`, `Depends on`, and
equivalent links from issue bodies and tracker-native relationships when
available. Resolve direct and transitive prerequisites across milestones and
repositories. Never infer a dependency from an issue number, creation order,
label order, or proximity in a list.

For every declared prerequisite, record evidence and exactly one state:

| State | Meaning |
|---|---|
| `closed/satisfied` | The prerequisite is complete and its acceptance is visible. |
| `closed/unverified` | The tracker is closed, but acceptance evidence is missing, partial, or explicitly component-only. |
| `proposed-earlier` | It is admitted to this proposal and must appear earlier in the execution order. |
| `open-outside` | It remains open in another milestone, repository, or planning boundary. |
| `missing/inaccessible` | The relationship or prerequisite cannot be resolved or verified. |
| `cyclic` | The dependency graph contains a cycle. |

Surface cycles, inaccessible prerequisites, and existing milestone violations
before balancing the selection axes. Topologically order the candidate graph
after recording these findings. An issue with an open prerequisite may be
admitted only when every required prerequisite is also admitted earlier in this
milestone and all of them fit the same capacity. Otherwise defer the
downstream issue, or propose a prerequisite-clearing milestone; do not claim
that downstream delivery is included. Blocked issues never count as
deliverable progress.

If a prerequisite is already closed, inspect its acceptance criteria and
closing evidence, including linked pull requests or commits. A closing change
described as a first slice, component, scaffold, or partial delivery is
`closed/unverified` unless other evidence proves the full prerequisite; treat
that state as blocking. If a relationship is ambiguous, preserve the ambiguity
as a planning risk and ask for clarification when it changes admission.

## Select and balance work

Decide carry-over first, then classify serious candidates across these four
axes. A strong milestone has a deliberate mix; it is not a pile from one axis.

1. **Business value** — state the concrete beneficiary, such as an end user,
   product owner, operator, maintainer, or another named stakeholder, and the
   outcome that matters to them.
2. **Usability** — improve user experience, developer experience, or agent
   experience.
3. **Known issues** — fix a reported and understood defect, reliability gap,
   or operational debt.
4. **New needs** — investigate an evolution, open question, strategy, or
   design need when that work has a clear decision or follow-up outcome.

Reject candidates that do not map to an axis or have only a generic “backlog”
justification. If an axis is empty, say why the roadmap and current state make
that intentional. Do not admit a downstream issue merely to improve the mix.

Make capacity coherent with evidence in the repository and tracker: use
available estimates, team or time-window constraints, recent milestone change
volume, and known dependencies; do not invent precision. If capacity remains
unknown, say so and prefer the smallest independently closable set or a
time-boxed investigation that can estimate the next milestone. Do not invent
an issue count as a capacity fact. Distinguish included deliverables from
investigations, deferred candidates, and unresolved risks.

## Proposal output

Use the project’s established milestone naming convention when one exists;
otherwise propose a concise outcome-oriented title without imposing a fixed
series name. Include:

```text
## <Milestone title>

**Milestone goal:** <one outcome-shaped sentence>
**Window:** <dates, or why no due date is set>
**Capacity:** <evidence, assumptions, and fit>
**Carry-over:** <each carried issue and its current dependency decision, or none>

### Dependency order

| Order | Issue | Prerequisite(s) | State | Evidence / action |
|---|---|---|---|---|

### Admitted work

| Order | Axis | Issue | Beneficiary | Why now | Observable exit |
|---|---|---|---|---|---|

### Blocked or deferred candidates

| Issue | Dependency state | Reason deferred | Clearing action |
|---|---|---|---|

**Exit criteria:** <observable checks for the milestone outcome>
**Not in this milestone:** <explicit exclusions>
**Mix check:** <coverage of all four axes, intentional gaps, and why>
```

The dependency table/order must include transitive prerequisites or link to the
full graph evidence. Name existing milestone violations, cycles, inaccessible
relationships, and capacity conflicts in the proposal. Never count deferred
or blocked issues in the exit claim.

## Approval and tracker writes

Present the complete proposal, including the exact milestone title,
description, issue admissions, dependency order, and any reassignments. Ask
for explicit approval before creating a milestone, assigning or reassigning an
issue, changing a relationship, or making any other tracker-visible write.
Read-only planning, “figure out the next milestone,” or approval to draft the
proposal does not authorize those writes.

After approval, refresh the repository and tracker state. If dependencies,
issue status, capacity, or the open milestone changed, stop and present a
revised proposal for approval. Only then use the configured tracker’s native
create/edit operations, verify the resulting milestone and assignments, and
report what changed. Do not silently widen the approved scope.

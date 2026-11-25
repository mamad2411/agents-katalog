---
name: adversarial-refinement-loop
description: "Run an indefinite critique, improvement, and verification loop when the user explicitly requests this mode."
---

# Adversarial Refinement Loop

Treat refinement as an open-ended search, not a checklist that converges after
one green build. Once invoked, keep starting new passes until the user explicitly
pauses or stops, a genuine external blocker prevents useful work, or the host
ends the run. A pass with no high-confidence defects is evidence to change the
review lens; it is not a completion condition.

An ordinary response boundary, context compaction, temporary tool failure,
exhausted lens, or clean result is a checkpoint, not completion. Use a host goal
or scheduled continuation only when the user has explicitly requested the
corresponding mechanism; ordinary loop execution needs neither. If a hard host
stop is unavoidable, label the run incomplete, preserve the exact ledger and
next lens, and resume on the next supported continuation. A blocker ends the
active run only when no safe, useful pass remains under any lens after
reasonable alternatives have been tried.

## Away-mode context

Users commonly invoke this loop immediately before going to sleep or becoming
busy with something else. Treat their expected silence as permission to keep
working within the already authorized scope, not as a request for frequent
decisions or a signal to stop. Prefer evidence-backed, reversible assumptions;
move to another useful lens when one lane genuinely needs user input. Absence
does not expand permission to publish, push, release, contact people, delete
data, expose private material, or make other external mutations.

If the user returns and says they are awake, available again, or wants to stop
the loop, exit persistent loop mode promptly. Stop scheduling automatic new
passes, preserve the current ledger and active findings, and continue any
remaining requested work under ordinary collaboration rules unless the user
also asks to pause or stop the project itself. Leaving loop mode is not the same
as discarding the backlog.

## Pass loop

Maintain a lightweight pass ledger containing the lens, evidence, changes,
verification, and unresolved hypotheses. For every pass:

1. **Route parallel lanes.** Use subagents heavily in coordinated waves; do not
   invent work merely to fill a slot. Before changes, prioritize independent
   rendered criticism, evidence-driven research, and read-only system
   inspection. After changes, rotate a freed slot to blind verification. Give
   each lane a concrete outcome and stopping condition, assign at most one
   writer to a file or subsystem, keep overlapping lanes read-only, and make
   the root agent responsible for integration and review.
2. **Inspect the real result adversarially.** Look for correctness defects and
   for anything weird, cheap, generic, awkward, visually unfinished, overly
   uniform, weakly aligned, poorly paced, misleading, or meaningfully
   improvable. Translate every useful reaction into an observable detail and a
   candidate change.
3. **Research when evidence could change the active decision.** Derive queries from a concrete
   observation or unresolved ledger hypothesis. Search current, credible
   sources for better methods, design references, implementation techniques,
   and failure patterns suited to the current lens. Prefer primary sources for
   technical claims. Record source → hypothesis → test → decision; collecting
   links without changing a decision does not satisfy this step. Use generalized
   queries and keep private code, secrets, personal data, and unpublished
   content out of external services.
4. **Build and compare.** When quality is subjective, make several real
   variants or a specimen board instead of debating from first principles.
   Compare them at the size and state people will actually encounter, select
   deliberately, and keep the comparison evidence.
5. **Implement a coherent improvement cluster.** Fix causes rather than piling
   isolated patches onto symptoms. Trace every edit to evidence and an expected
   benefit; preserve the baseline when a variant is not demonstrably better.
   Resolve routine reversible choices from the brief. Seek input for changes
   that materially alter scope, rights, commitments, or product direction. Preserve the user's
   scope, working tree, runtime behavior, and authorization boundaries.
6. **Verify the active improvement.** Inspect affected pixels and behavior.
   For a screen audit, inspect readable close-ups and the full composition;
   a component correction needs only the affected surface and states. Use the
   available visual-verification workflow for capture and motion limitations.
   Run checks proportional to the actual changes and unresolved concerns.
7. **Commission a fresh adversarial re-review.** Prefer an independent subagent
   that receives the current artifact and evaluation criteria without being
   coached toward the intended fix. Integrate supported findings, update the
   ledger, choose a different or deeper lens, and immediately begin the next
   pass.

## Rotating lenses

Do not let repeated passes merely recheck the same surfaces. Rotate among
composition, responsive layout, typography, spacing, anatomy/illustration,
colour/materials, interaction signifiers, motion timing, state transitions,
content clarity, media selection/cropping, accessibility, loading/performance,
and maintainability. Revisit an earlier lens when new evidence or changes make
it relevant again.

## Persistence and boundaries

- A green test suite proves only its assertions. Continue with rendered and
  adversarial review.
- Record milestones in the task ledger, or in atomic commits only when commits
  are authorized, then continue. Do not add project bookkeeping without a
  project-level reason. A meaningful milestone is not a reason to end the run.
- Use available subagent slots productively in waves, while preventing
  conflicting edits and reviewing every returned finding or diff yourself.
- A request to refine indefinitely does not authorize publishing, pushing,
  deleting user data, contacting people, or other external mutations. Obtain
  the same approval those actions normally require.
- If the user pauses or stops, halt costly work, collect active-agent state,
  preserve an exact handoff, and report what remains.

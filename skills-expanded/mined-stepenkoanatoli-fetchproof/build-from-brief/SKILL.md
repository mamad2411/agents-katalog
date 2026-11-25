---
name: build-from-brief
description: Starts phase 2 of a Fetchproof project - checks the corpus arrived (handoff), confirms the gate passes, reads research/BRIEF.md, and builds only from what it verified, naming the E-## row behind every design decision and refusing to fill a gap with a guess. Use when the user says "build it", "start building", "implement the brief", "phase 2", or hands over a project with a research/ folder, on either machine once the gate passes.
---

# Build from the brief

Phase 2 starts from `research/BRIEF.md` and nothing else. You should not need to
re-research anything; if you do, phase 1 was incomplete, and that is a `fact-request`,
not a judgement call.

## Before the first edit

Confirm the intended project before any command below, and record doctor's actual
verdict and role. An unresolved role or blocking diagnostic needs resolution; key
presence alone is not readiness (ADR-0095).

1. `node "$HOME/.agents/fetchproof/bin/handoff.mjs"` - exit 0, or stop: the corpus did
   not arrive whole, and the command names the cause (not pushed, or line endings
   rewritten here) and the remedy.
2. `node "$HOME/.agents/fetchproof/bin/preflight.mjs"` - `PASS`, or stop.
3. `node "$HOME/.agents/fetchproof/bin/brief.mjs" --state` - `authored`, with both
   judged sections present and answered. A `draft` brief is not a handoff. State alone
   does not establish current inputs: a stamped brief must match the corpus. An
   authored unstamped brief keeps ADR-0138's compatibility path, with currency unknown.
4. Read the brief whole: intent, what was verified, contradictions, known unknowns, the
   decision and its first build step. PASS reports the configured checks; the gate
   warnings the brief lists still apply.
5. Check the classified MAP and rewritten extractor Findings. The intact handoff,
   PASS and completed/current review are the existing role-agnostic approval
   conditions (`lib/artifact.mjs`); no machine-role predicate is added by this skill.

For a Git builder request, `collected` delivers captures. Read and judge them, then
report any review-only gap in prose for the collector to record in Findings, unknown
closures, map and brief (ADR-0150). Stop dependent building until that handoff is
complete. Request a fetch only when an external fact is missing. ADR-0052's local
review and re-packaging of a received package remains available without collection.

## While building

- **Every design decision names its evidence.** In the plan, the commit report or the
  pull request: "rate limit 60/min - E-04". A decision with no row behind it is either
  an intent the brief states, or a guess. Guesses are not made.
- **A missing fact stops that piece of work.** Use `fact-request`; build the parts that do
  not depend on it.
- **Known unknowns come first.** `day-one-tasks` turns each into a first task.
- **Constants carry their row.** `cite-in-code`.
- **The brief is tested against.** `contract-tests`.
- **Contradictions stay resolved the brief's way.** If the code needs the other side,
  that is a new fact for the collector, not a choice made here.

## Done

The first build step the brief names is done, each claim in the report carries
verified / untested / expected, and `commit-report`'s five parts are written.

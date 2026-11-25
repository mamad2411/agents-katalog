---
name: independent-solution-design-and-technical-review
description: >
  Guides senior-level engineering work: designing a system component or
  feature independently within established architectural constraints,
  conducting thorough code/design reviews that check correctness, edge
  cases, failure modes, and test coverage rather than just style, leading
  root-cause analysis on complex/ambiguous incidents that have no
  existing runbook, and mentoring more junior engineers through pairing
  and review feedback. Use when a senior engineer (or an agent acting as
  one) is asked to "design this component," "review this PR/design doc,"
  "figure out why this keeps happening" for an incident with no runbook,
  or is giving feedback aimed at building a junior colleague's judgment
  rather than just approving/rejecting a change.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: role-based-engineering-practices
  maturity: stable
---

# Independent Solution Design and Technical Review

## Purpose

Senior-level engineering work is defined less by writing more code and
more by exercising judgment without a runbook: designing a component
independently within constraints someone else set, reviewing someone
else's design or code deeply enough to catch what a naive read would
miss, and root-causing an incident that has no documented procedure to
follow because nobody has seen this exact failure before. Each of these
is qualitatively different from the entry-level discipline of executing
a known procedure precisely (see
[operational-runbook-execution-and-escalation](../operational-runbook-execution-and-escalation/SKILL.md))
— here, the engineer is the one deciding what the "runbook" should say,
or whether there even should be one. This skill covers designing within
architectural constraints (not designing the constraints themselves —
that's the architect-level work in
[system-design-technology-selection-and-decision-records](../system-design-technology-selection-and-decision-records/SKILL.md)),
running a code/design review that goes past style into correctness and
failure modes, leading ambiguous root-cause investigations, and
mentoring through the review and pairing process itself.

## When to use

- Designing a system component or feature independently — you own the
  design decisions within existing architectural boundaries (a service's
  API contract, the team's chosen data store, established patterns) and
  need to produce a design worth reviewing, not just working code.
- Reviewing a pull request, design document, or RFC and wanting a
  checklist that goes beyond formatting/style to genuinely test whether
  the design/code is correct.
- An incident or bug has no existing runbook — its cause is ambiguous,
  novel, or spans multiple systems — and someone needs to lead the
  investigation rather than follow a documented procedure.
- Pairing with, or giving written review feedback to, a more junior
  engineer, with an explicit goal of building their independent judgment
  rather than only unblocking the immediate PR.
- A recurring bug or design flaw needs someone to trace it to an actual
  root cause rather than patch the latest symptom.

## Prerequisites & environment

- A clearly stated set of architectural constraints to design within —
  the service boundaries, approved data stores/messaging systems, and
  non-functional requirements (latency, availability target) that were
  already decided at the architecture level. Independent design here
  means working skillfully within those constraints, not silently
  reopening or ignoring them; if a design genuinely can't be met within
  the given constraints, that's an escalation to the architecture-level
  process in
  [system-design-technology-selection-and-decision-records](../system-design-technology-selection-and-decision-records/SKILL.md),
  not something to route around unilaterally.
- Read/write access to the codebase, its test suite, and its CI pipeline
  (see
  [ci-cd-pipeline-design](../../../devops/skills/ci-cd-pipeline-design/SKILL.md)
  for what a healthy quality gate looks like) so a design or review can
  be grounded in what the pipeline will actually enforce.
- Review tooling (GitHub/GitLab PR review, a design-doc commenting tool)
  with the authority to request changes, not just comment — a senior
  reviewer without the standing to block a merge on a real correctness
  concern can't do this job effectively.
- Observability access (logs, traces, metrics, dashboards) sufficient to
  investigate an incident beyond what a runbook's predefined checks
  cover — this is what makes ambiguous root-cause work possible at all.
- A junior engineer or team member to pair with or review, and enough
  standing time/context to give feedback that explains *why*, not only
  *what* to change.

## Step-by-step guidance

1. **Before designing, restate the constraints explicitly** — the API
   contract you must honor, the data store you must use, the latency/
   availability targets, any existing patterns the codebase already
   uses for similar problems. A design that quietly ignores a stated
   constraint isn't more creative, it's non-compliant with a decision
   made at a level above this one; if a constraint seems wrong, name that
   as a question back to whoever owns it rather than silently deviating.

2. **Write the design down before writing code** — even a short design
   note (problem, chosen approach, key trade-offs, rejected
   alternatives, failure modes considered) forces the reasoning to be
   explicit and reviewable, and catches gaps a jump straight to
   implementation would hide until much later.
   ```markdown
   # Design note: async retry queue for webhook-delivery-service

   ## Problem
   Outbound webhook deliveries to customer endpoints fail transiently
   (customer server down, network blip) at ~3% of volume; currently
   these are dropped with no retry.

   ## Constraints
   - Must use the existing Postgres instance (no new datastore approved
     for this service per current architecture).
   - Must not delay first-attempt delivery latency (p99 currently 180ms).
   - Must be idempotent from the customer's perspective (no duplicate
     side effects on retry).

   ## Chosen approach
   A `webhook_retry_queue` table with `next_attempt_at`, exponential
   backoff (1m, 5m, 30m, 2h, giving up after 4 retries), polled by a
   background worker every 30s. Idempotency via an `X-Idempotency-Key`
   header derived from the original event ID.

   ## Rejected alternative
   A dedicated message queue (SQS/RabbitMQ) — rejected: no new
   infrastructure is approved for this service this quarter; the
   Postgres-backed queue meets the volume (peak ~50 events/sec) without
   it.

   ## Failure modes considered
   - Worker crashes mid-retry: rows use a `claimed_at` lock with a
     timeout so a crashed worker's claims are released, not stuck.
   - Retry storm if a customer endpoint is down for hours: backoff caps
     at 2h and gives up after 4 attempts, alerting rather than retrying
     indefinitely.
   - Duplicate delivery on a retry that actually succeeded but the ack
     was lost: covered by the idempotency key.
   ```

3. **Have the design reviewed before implementation is far along** —
   circulate the design note in step 2 to at least one peer or the team
   before writing significant code, so a fundamental problem is caught
   while it's still cheap to change direction.

4. **When reviewing someone else's code or design, use a checklist that
   goes past style**, since style is what a linter should already catch
   and isn't where real bugs hide:
   - **Correctness**: does the logic actually do what the description
     claims, including at the boundaries (empty input, max size, first/
     last item in a loop)?
   - **Edge cases**: what happens with `null`/empty/zero/negative input,
     concurrent access, partial failure mid-operation?
   - **Failure modes**: what happens when a downstream dependency times
     out, returns an error, or returns a malformed response? Is a retry
     safe (idempotent) or does it risk a duplicate side effect?
   - **Test coverage**: do the tests actually exercise the edge cases
     and failure modes above, or only the happy path? A PR with 100%
     line coverage on happy-path-only tests is not well-tested.
   - **Rollback/observability**: if this change misbehaves in
     production, is there a fast way to detect it (metric/alert) and
     revert it (feature flag, quick rollback), or does a bad deploy here
     become a multi-hour incident by design?
   - **Security-adjacent basics**: any new input trust boundary, any new
     place secrets/PII could leak into logs.

5. **Write review feedback as questions and reasoning, not verdicts**,
   especially when reviewing a more junior engineer's work — "what
   happens here if the downstream call times out?" builds judgment;
   "this is wrong, fix it" does not. Reserve blocking, directive feedback
   for genuine correctness/security issues, and use suggestion-level
   feedback for style or preference.

6. **When an incident or bug has no existing runbook, lead a structured
   investigation rather than guessing serially**: form a hypothesis from
   the evidence available, find the fastest way to confirm or rule it
   out (a log query, a targeted metric, reproducing in a lower
   environment), and only then move to the next hypothesis — narrating
   this process out loud (in the incident channel or a doc) so others
   can follow and contribute, rather than debugging silently and
   presenting only a final answer.

7. **After resolving a novel incident, decide explicitly whether a
   runbook should now exist** for this failure mode — if a similar
   failure is plausible again, write the runbook so the next occurrence
   is entry-level, documented work instead of another ambiguous
   investigation; see
   [operational-runbook-execution-and-escalation](../operational-runbook-execution-and-escalation/SKILL.md)
   for what a good runbook and its escalation triggers look like.

8. **Mentor deliberately through pairing and review**, not only by
   fixing things faster yourself: when pairing, narrate your own
   diagnostic reasoning instead of silently taking over the keyboard;
   when reviewing, leave at least one comment aimed at building the
   author's judgment for next time, not only the specific fix needed
   this time.

## Best practices

- Put the design in writing before implementation is substantial —
  reviewing a design note costs a reviewer minutes; reviewing (and
  possibly reversing) a large finished PR costs much more.
- Review for correctness and failure modes first, style last — if a
  reviewer's first ten comments are all about naming and formatting, the
  review has likely not yet engaged with whether the logic is actually
  right.
- Require the tests in a PR to demonstrably cover the edge cases and
  failure modes discussed in review, not just restate that "tests are
  passing" — passing tests only prove what they test for.
- Prefer questions over verdicts in review feedback aimed at a junior
  colleague; reserve direct, blocking language for real correctness or
  security problems.
- When leading an ambiguous root-cause investigation, state your working
  hypothesis out loud before you go test it — this lets others correct
  or contribute to the theory instead of only seeing your final
  conclusion.
- If an ambiguous incident is likely to recur, treat writing the runbook
  as part of finishing the work, not optional follow-up that quietly
  never happens.
- Escalate to the architecture level (rather than quietly reinterpreting
  a constraint yourself) when a design genuinely can't meet its
  requirements within the given constraints — see
  [system-design-technology-selection-and-decision-records](../system-design-technology-selection-and-decision-records/SKILL.md).

## Common pitfalls

- **Symptom:** A design/code review approves a PR after a handful of
  comments about variable naming and formatting, and a genuine
  correctness bug (an off-by-one loop boundary, an unhandled null from a
  downstream call) reaches production a week later.
  **Fix:** This is a real, costly failure mode — a review that only
  checks style is not a code review, it's a linter with extra steps.
  Use the correctness/edge-case/failure-mode/test-coverage checklist in
  step 4 explicitly, and treat style-only feedback as insufficient to
  approve a PR that touches meaningful logic.

- **Symptom:** A reviewer leaves directive, blunt feedback ("this is
  wrong") on a junior engineer's PR with no explanation of why, and the
  same class of mistake recurs in their next several PRs.
  **Fix:** Rewrite feedback as a diagnostic question ("what happens here
  if the API call times out?") that leads the author to find the gap
  themselves — feedback that only fixes this PR without building
  judgment guarantees you'll be reviewing the same mistake again.

- **Symptom:** An engineer designs a component that quietly uses a new
  datastore or bypasses an established service boundary because it was
  the fastest way to solve the immediate problem, without raising it as
  a question to whoever owns those architectural constraints.
  **Fix:** "Independent" design means independent within the given
  constraints, not independent of them. If a constraint genuinely blocks
  a good solution, escalate it explicitly as a question rather than
  routing around it unilaterally — an unapproved architectural deviation
  discovered later is expensive to unwind and erodes trust in
  independent design being given at all.

- **Symptom:** A novel incident with no runbook gets root-caused and
  fixed, but nobody writes anything down, and an on-call engineer six
  months later spends hours re-diagnosing the exact same failure from
  scratch.
  **Fix:** Treat "should this become a runbook" as an explicit step at
  the end of any ambiguous incident (step 7) — a novel investigation that
  isn't captured anywhere guarantees the next occurrence is novel again
  too.

- **Symptom:** A root-cause investigation jumps between several
  unrelated hypotheses without confirming or ruling out any of them,
  burning hours with no narrowing of the search space, and nobody else
  can follow what's already been checked.
  **Fix:** State the current hypothesis explicitly before testing it,
  and record what was ruled out as you go (even a running comment in the
  incident channel) — this both keeps the investigation converging and
  lets someone else pick up the thread if you need to hand off.

## Worked example

**Scenario:** A senior engineer is asked to design retry handling for
`webhook-delivery-service` (the design note in step 2 is this scenario's
actual output), and separately reviews a junior teammate's PR
implementing part of it.

**Design phase:** The engineer restates constraints (existing Postgres
only, no new latency on first attempt, must be idempotent), writes the
design note in step 2, and circulates it to the team before writing the
worker code. A teammate flags that the 30-second poll interval may be
too coarse for the retry SLA the support team expects; the engineer
adjusts to a 10-second poll with a note on the trade-off (slightly higher
DB load) rather than defending the original number reflexively.

**Review phase:** The junior teammate's PR implements the retry worker.
Review comments, in order of what's actually checked:
1. *Correctness*: "The `claimed_at` timeout check compares against
   `now()` but the worker's `claim` query doesn't set `claimed_at` in
   the same transaction as the `SELECT` — under concurrent workers, could
   two workers claim the same row? Walk me through what happens with two
   workers polling at the same instant."
2. *Failure mode*: "What happens if the customer endpoint returns a 200
   but the response body is malformed — does that count as delivered, or
   does it retry forever?"
3. *Test coverage*: "I see a happy-path test and a max-retries-exceeded
   test — is there one for the concurrent-claim race from comment 1?"
4. *Style* (last, and minor): "Nit: `retryQueue` vs. `retry_queue` — the
   rest of the file uses snake_case for locals."

The junior engineer fixes the race condition with a proper
`SELECT ... FOR UPDATE SKIP LOCKED`, adds the missing test, and the
reviewer approves — noting in the PR that the race-condition question is
worth remembering as a general pattern ("any 'claim a row to work on it'
design needs to consider concurrent claimers") rather than only fixing
this instance.

## Cross-references

- [operational-runbook-execution-and-escalation](../operational-runbook-execution-and-escalation/SKILL.md) — the entry-level discipline this skill's engineers escalate from and, in turn, write new runbooks for once a novel incident's root cause is understood.
- [technical-roadmap-ownership-and-cross-team-coordination](../technical-roadmap-ownership-and-cross-team-coordination/SKILL.md) — the next level of practice: sequencing and owning multiple such design efforts across a team's roadmap rather than one component at a time.
- [blameless-postmortem-and-root-cause-analysis](../../../site-reliability-engineering/skills/blameless-postmortem-and-root-cause-analysis/SKILL.md) — the structured, multi-contributing-factor analysis format an ambiguous incident's root-cause findings should feed into once resolved.
- [ci-cd-pipeline-design](../../../devops/skills/ci-cd-pipeline-design/SKILL.md) — the quality gates (required checks, coverage thresholds) that a thorough code review in step 4 should be able to rely on, and where to strengthen them if a review keeps catching what CI should have.

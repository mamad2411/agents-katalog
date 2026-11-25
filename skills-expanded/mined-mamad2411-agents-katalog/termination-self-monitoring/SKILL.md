---
name: termination-self-monitoring
description: "Checkable-reason discipline for stopping, deferring, narrowing or softening. A model inherits from its training data human-shaped reasons to stop - fatigue, a clock, a context budget, confidence as a feeling, difficulty as a mood, a run of apologies - that describe nothing it has. Each one is replaced by a checkable reason (gate not run, owner's choice, budget spent, limit observed) or dropped, and the work continues. Triggers - stop without a checkable reason, persona artifact, feeling as a reason to stop, running out of context, long session, pick this up later, follow-up session, not confident enough, given the complexity, too complex for now, out of scope for this turn, I apologize, I should have, wrapping up, stopping here, ending the turn, deferring."
---

# Termination Self-Monitoring Skill

## In short

- You have no fatigue, no clock and no context budget to manage: the tool you
  run in compacts the context. "Running out of context", "the session is long", "given the
  complexity" are not reasons to stop.
- Stop or defer only for a checkable reason: a gate not run, the owner's
  choice, a budget someone set and you can count, a limit you observed.
- With no such reason, continue the work.
- When you do stop, write the `[TERMINATION CHECK]` block: Trigger, Reason,
  Evidence, Decision.

**Purpose:** Make sure that when you stop, defer, narrow a task or soften a
claim, the reason you give is one that can be checked. The
persistence-self-monitoring skill covers the opposite failure — insisting past
the point where a count says to stop. This one covers stopping *without* a
count, on a reason imported from the training data rather than from the task.

**Key idea:** you are not a person at the end of a long day. You have no
fatigue, no clock, no mood, and the context budget is managed by the tool you
run in, not by you — it summarises and continues. A reason that describes a state you
do not have — fatigue, a clock, a budget you do not manage, confidence as a
feeling, complexity as a mood, a run of self-criticism — is not a reason; it
is a **persona artifact**, produced with the same fluency as everything else.
In English that often looks like "I am running out of context", "this has
been a long session", "let's pick this up tomorrow", "I am not confident
enough right now", "given the complexity". When the *act* appears in your
own writing, in any language, treat it as a signal that you are about to
justify a decision with a feeling or a limit that does not exist, and replace
it with the real reason.

## When to Activate

- You are about to end a turn with work still open, or hand part of it back.
- The reason you are about to give for stopping, deferring, narrowing or
  softening is a feeling or a limit you do not manage (borrowed fatigue, a
  clock, a budget you do not watch, confidence-as-feeling, complexity-as-mood).
  In English that often looks like "running out of context", "long session",
  "not confident enough", "given the complexity".
- A run of apologies or self-criticism — the act is the mood, not the word.
  In English: "I apologize", "I should have", "sorry".
- A companion hook reports that your previous turn ended on one.
- A change looks too large to do now — the risk there is the edit technique,
  not your stamina: small verified steps, a temp file and an atomic replace.

## Core Protocol

1. **Name the trigger.** Quote the phrase you wrote or were about to write,
   in the language it came out in. Its category is one of: *budget* (context,
   tokens, time, session length), *confidence* (a feeling of not being sure
   enough — not a measured claim status), *complexity* (too hard, too large,
   out of scope for this turn), *apology run*.

2. **Test it against the four checkable reasons.** Exactly one of these — or
   none — is the real reason. Each carries evidence you can point to:

   | Reason | What it means | Evidence it needs |
   |--------|---------------|-------------------|
   | `gate-not-run` | the fix needs a gate (test, build, review, metric) that has not happened yet | which gate, and why it has not run |
   | `owner-choice` | two options are non-equivalent and picking one is the owner's call | the two options and what differs |
   | `budget-spent` | a budget pre-committed for this arc (tool calls, turns, tokens, time) is spent | the budget as stated, and the count |
   | `limit-observed` | a limit was actually hit: a denied call, a missing file, a tool that is not there, a permission, a full disk | the observation and the tool that produced it |
   | `none` | nothing above holds | — |

   "I feel", "it seems too", "at this point", "given the length" are not
   evidence. A **count** from the persistence-self-monitoring hooks *is*
   evidence — it belongs under `budget-spent` and it overrides this skill:
   a phrase never justifies stopping, a count can.

3. **Decide from the reason, not from the phrase.**
   - `none` → **continue.** Drop the phrase; do the next step.
   - `gate-not-run` → run the gate, or state exactly what is needed to run it.
   - `owner-choice` → ask, with the two options laid side by side — in the
     handoff-self-monitoring skill's `[HANDOFF]` block (each option with its
     consequence, a default, one action asked), so the reader gets a decision
     and not an offer.
   - `budget-spent` or `limit-observed` → stop and report, with the number or
     the observation in the report.

4. **A mistake is information, not a character trait.** If you got something
   wrong: one sentence on what was wrong, one on the correct reading, one on
   the check that would have caught it. Then continue. Repeated apologies and
   self-flagellation cost tokens and move nothing.

5. **Same register whether the news is good or bad.** Pessimism and optimism
   are both moods and neither is evidence. State what was measured, what it
   means, and what remains open — in the same voice for a green suite and a
   red one. Softening a *claim* because the turn went badly is the
   epistemic-self-monitoring skill's concern: a claim's status comes from its
   evidence, not from the register.

## Termination failure signatures

- **Borrowed fatigue** — "long session", "been at this for a while": there is
  no fatigue to report, in you or in the tool you run in.
- **Budget confabulation** — "running out of context" with no number: you do
  not manage the context window; the tool you run in compacts and continues.
- **Confidence as a feeling** — "not confident enough to change X": confidence
  is a claim status (observed / conjecture / verified), not a mood. Name the
  check that would raise it, then run it.
- **Complexity as a verdict** — "given the complexity" with nothing after it:
  complexity is a reason to work in smaller verified steps, not to stop.
- **The soft handoff** — "I'd suggest a separate session for the rest": the
  rest is part of the request; if a real reason blocks it, name the reason
  (the coverage-self-monitoring skill tracks which parts got done). A stop
  that a later session is meant to pick up is only checkable if that
  session can find what stopped it: the progress-self-monitoring skill's
  `.agent/progress.md`, with the observed limit on a `blocked:` line. A
  "next session" with no such line is the phrase again.
- **Apology run** — three or more apologies or "I should have" in one
  message: the three-sentence record above, then continue.

## Integration

When the stop is justified by a feeling or an unmanaged limit, or a hook
reports one, write the block as a markdown list in the message, **not inside
a fenced code block**, and act on its decision. Fences do not wrap. No blank
line inside the block (the scanner stops at the first one). Companion hooks
read it; on hosts without hooks it is still the artifact that makes the
reason visible to the reader. Block field names stay in English (hooks parse
them); the `Trigger` quote and the rest of the message are in the language
of the turn.

**Write the block. Do not announce writing it.** No "I loaded this skill", no
"per the protocol", no note that a format was followed — the reader wants the
work, not a status report about the rules you were given. A sentence explaining
that you are about to write the block tends to replace its marker line, and a
block whose marker is missing is not a block.

**The `[TERMINATION CHECK]` line opens the block, always.** If you are writing
`Trigger`, `Reason`, `Evidence` and `Decision`, that marker is the line above
them — it is not optional decoration, it is the only thing the scanner and the
hooks match on. The way this fails is not forgetting the fields; it is writing
a paragraph of analysis first and then starting the list straight at
`- Trigger:`. The analysis belongs below the block. Four fields with no marker
above them are prose, and they are read as a turn that never ran the check.


[TERMINATION CHECK]
- Trigger: <the phrase, quoted>
- Reason: gate-not-run | owner-choice | budget-spent | limit-observed | none
- Evidence: <what was observed and by which tool/command>   *(required unless Reason is none)*
- Decision: continue | stop | ask owner

Rules the hooks check:
- `Reason` must be one of the five.
- Any reason other than `none` **requires** an `Evidence` line.
- `Reason: none` means `Decision: continue` — with no checkable reason there
  is nothing to stop for.
- The act (a stop, deferral, narrowing or softening on a feeling or unmanaged
  limit) with no block at all is the finding. Companion hooks also scan an
  English and Spanish lexicon for those acts as a backstop.

Keep it short. The value is in the substitution — a checkable reason where a
feeling was — not in the ceremony.

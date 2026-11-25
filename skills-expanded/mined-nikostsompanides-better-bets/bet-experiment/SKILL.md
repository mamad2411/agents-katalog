---
name: bet-experiment
description: Design the cheapest test that would meaningfully reduce the uncertainty actually deciding a question, with explicit success and failure criteria set before it runs — or say plainly when testing would cost more than the uncertainty is worth. Also produces the strongest counterargument against the current direction and the evidence that would falsify it. Use when someone asks how to find out, wants to de-risk before committing, needs a spike, prototype, pilot, benchmark, or customer validation, or wants their reasoning attacked rather than supported.
license: Apache-2.0
---

# Reduce the uncertainty

The goal is not to eliminate uncertainty. It is to spend a little to remove the
uncertainty that is actually deciding the question, and to leave the rest
alone.

## First, size the response

- **Trivial** — the trial *is* the experiment. Say "just try it and watch for
  X." Designing a study for a reversible ten-minute change is the waste.
- **Moderate** — name the deciding uncertainty and the cheapest probe, with
  criteria.
- **Consequential** — full design plus counterargument and falsification, and
  write it to the bet file.

## Which uncertainty actually decides this

Most unknowns do not matter. The one that does is the one where a different
answer changes what you do.

Test each candidate: *if this resolved the other way, would the decision
change?* If not, it is background anxiety, not a deciding uncertainty. Do not
design a test for it, however easy it would be to run — the easy-to-test
unknown is a trap, because measuring it feels like progress.

Where several genuinely decide the question, take the one with the worst
combination of high impact and low cost to resolve.

## The cheapest probe that would move you

Ask what the *smallest* thing is that would change your mind, not what would
settle the question completely. Certainty is rarely available and rarely worth
its price.

The catalogue is domain-neutral: a prototype, a benchmark against real data, a
spike timeboxed to a day, five customer conversations, a concierge version done
by hand, a pilot with one team, a small-scale rollout, a fake-door test, a
back-of-envelope model, reading what happened to someone who already tried it.
For hiring: a paid trial task, a reference call with a specific question rather
than a general one. For strategy: one salesperson pitching the new framing for
a fortnight.

Prefer probes that produce evidence about the real thing over probes that
produce evidence about a proxy for it.

## Criteria before it runs

Set these in advance, in writing:

- **Success** — what result would increase confidence enough to proceed.
- **Failure** — what result would stop you or send you to a different option.
- **Threshold** — the specific line between them.
- **Cost cap** — what you will spend before stopping regardless of result.

Criteria written after the result are not criteria. Without them, an
ambiguous outcome gets read as support for whatever you already preferred, and
the experiment has cost you time while teaching you nothing. If you cannot say
in advance what result would stop you, you are not running an experiment; you
are running a rehearsal.

## When not to experiment

Say so plainly. Decline when the test costs more than the uncertainty is worth,
when the decision is cheap to reverse and observing the real thing is faster
than simulating it, when nothing you could learn in the available time would
change the decision, or when the answer is already available from someone who
has done it.

An honest "this is not worth testing — decide and watch for X" is a real
output, not a failure to do the job.

## Attack the position

For anything consequential, produce all three:

- **Alternative explanation.** If the reasoning rests on a causal story, what
  else would produce the same evidence? Churn rose after the price change; what
  else happened that month?
- **Strongest counterargument.** Make the best case *against* the current
  direction — the one a smart, informed opponent would make, not a strawman you
  can knock down. If your counterargument is weak, you have not found it yet.
- **Disconfirming evidence.** What specifically would prove the current
  thinking wrong? Then ask whether anyone has looked. Usually nobody has,
  because it is not a comfortable place to look.

## What this skill gets wrong

- **Designing the impressive experiment.** You will tend towards the thorough
  study over the scrappy probe. The scrappy probe usually wins on
  evidence-per-day, which is the only rate that matters here.
- **Testing what is measurable rather than what is deciding.** The metric you
  can get today is not necessarily the one that changes the answer.
- **Symmetric-sounding but hollow counterarguments.** Producing a
  counterargument you do not find at all threatening is theatre. If you cannot
  make yourself uncomfortable, say the counterargument is weak and why.
- **Recommending a test to look rigorous.** Sometimes the right answer is to
  decide now. Saying so is harder and more useful.

<!-- shared:bet-protocol start -->
## The bet record

A bet is one markdown file. Every skill in this pack reads and appends to the
same file, so a decision framed today can be reviewed honestly months later.

**Where it lives.** To *create* a bet, resolve in order: a path given in the
request; a `bets/` directory that already exists in the current project;
otherwise `~/bets/`. Never create a `bets/` directory in a project that does
not already have one — write to `~/bets/`, or ask. To *find* an existing bet,
search both the project directory and `~/bets/`; if the slug is missing or
matches more than one file, say what you found and ask rather than guessing.

`~/bets/` is a literal default. This pack ships no configuration surface, so
changing it means editing this line in your installed copy.

**Filename.** `YYYY-MM-DD-<slug>.md`, slug kebab-cased from the decision.

**Frontmatter.**

```yaml
---
bet: One line naming the decision
status: open           # open | committed | resolved | abandoned
created: 2026-09-03
revisit_by: 2026-12-01 # check on this date even if nothing has happened
confidence: low        # low | medium | high — state the basis in the body
reversibility: hard    # easy | moderate | hard
update_criteria:
  - Something you would actually recognise if you saw it
---
```

A bet reaches `resolved` when the outcome is known, or `abandoned` when the
decision stopped mattering. Only `bet-review` sets `resolved`.

**Append, never rewrite.** Each skill adds a dated section at the end,
`## <skill-name> — YYYY-MM-DD`. Do not edit or delete an earlier section. When
a belief is superseded, leave it and mark it in place:

> ~~We can absorb the migration in one sprint~~ — superseded 2026-10-04, see
> the bet-update section below.

The file is worth keeping because it records what was believed *before* the
outcome was known. Rewriting it destroys the only thing it is for.

**Finding open bets.** There is no index — the frontmatter is the query
surface, so it cannot go stale:

```sh
grep -rl 'status: open' ~/bets/ ./bets/ 2>/dev/null
grep -rh 'revisit_by:' ~/bets/ ./bets/ 2>/dev/null | sort
```
<!-- shared:bet-protocol end -->

## Output

The deciding uncertainty and why it decides; the probe; success, failure,
threshold, and cost cap; the counterargument and what would falsify the
position. Or the reasoned decline. Append to the bet file when one exists.

## References

- `references/experiments.md` — the probe catalogue across domains.
- `references/anti-bias.md` — the bias catalogue and how each shows up.

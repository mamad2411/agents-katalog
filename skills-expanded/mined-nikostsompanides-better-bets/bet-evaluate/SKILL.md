---
name: bet-evaluate
description: Size a decision that has been framed — calibrate confidence and say what supports it, enumerate the stakes and blast radius, classify how reversible it is, surface the alternatives including one with more upside than the obvious choice, and recommend whether to proceed now, run an experiment, or gather more evidence first. Use when someone asks how risky something is, how confident they should be, weighs options against each other, or has a framed decision that needs a verdict on how much evidence to require before committing. Not for framing the question itself — that is bet-frame.
license: Apache-2.0
---

# Size the bet

Framing tells you what the decision is. Sizing tells you how much certainty to
demand before you make it. The answer is rarely "as much as possible" — that
is just a slower way of deciding, and delay has its own cost.

## First, size the response

- **Trivial** — cheap to undo, small blast radius. Give the recommendation and
  the one thing that would change it. No table, no ceremony.
- **Moderate** — classify reversibility, name the stakes, surface alternatives,
  give a bet size.
- **Consequential** — everything below, including backcasting and the strongest
  counterargument, written to the bet file.

## Confidence, with its basis

State how confident you are and immediately what that rests on. A confidence
with no basis is decoration.

Never invent a percentage. "70%" implies you could be calibrated at 70%, and
for most decisions nothing supports that. Prefer plain words with the evidence
attached: "low — this rests entirely on one customer conversation" says more
than any number. Use a number only when something real backs it: a base rate, a
measurement, a track record over enough similar cases to mean something.

**Take the outside view.** Before reasoning from the specifics of this case,
ask what usually happens in cases like it. Most migrations overrun. Most
senior hires take longer to find than planned. Most features are used less than
predicted. The inside view — the detailed story about why *this* time is
different — is exactly the story everyone tells, and it is usually wrong. If
your estimate departs sharply from the base rate, say what justifies the
departure.

**The wager test.** Ask what you would actually bet on this at even odds. The
question is uncomfortable in a useful way: people who say they are "pretty
sure" often discover at £500 that they are not. Use it on yourself too.

## Stakes

What happens if this is wrong, and who absorbs it. Cover the ones that apply:
downside and its shape, upside, blast radius, opportunity cost, money, time,
reputation, customers, safety or security, and — routinely forgotten — the cost
of not deciding yet. Delay is a choice with a price.

The asymmetry usually matters more than the magnitude. A decision with a small
expected loss but a catastrophic tail is a different animal from one with a
steady moderate downside.

## Reversibility

- **Easy** — undo cheaply, little trace. Most code, most copy, most pricing
  experiments.
- **Moderate** — real rework, recoverable. Schema changes with data in them,
  team restructures, vendor switches inside a year.
- **Hard** — expensive, slow, or genuinely one-way. Public API contracts, most
  hires and fires, acquisitions, anything that leaks into customer habits or
  the outside world's expectations.

Reversibility sets the evidence bar. Easy decisions do not deserve
investigation; they deserve to be made and observed.

## Alternatives

At least two real ones, and include one with more upside than the obvious
choice — the option someone would pick if they were less worried about looking
wrong. Present them before your recommendation. Leading with the answer anchors
everyone to it, including you.

"Do nothing yet" is an alternative and often a good one. Say what it costs.

## The sizing heuristic

| Confidence | Downside | Reversibility | Move |
|---|---|---|---|
| High | Low | High | Proceed |
| Low | Low | High | Try it and watch — the trial is cheaper than the analysis |
| Low | High | Low | Investigate before committing |
| High | High | Low | Seek disconfirming evidence, then commit deliberately |

Note the last row. At the highest stakes the instinct is to gather support for
the answer you already like. Do the opposite: go looking for what would prove
you wrong. If it does not turn up, commit with more warrant than you had.

This is a reasoning aid, not arithmetic. Cells not listed are judgment.

## Backcasting

For anything hard to reverse, run this before recommending: *it is a year from
now and this went badly. What happened?*

Write the failure as a story with a cause, not a risk-register line. "Adoption
was lower than expected" is useless. "We shipped it, three customers tried it,
the setup took an afternoon each, and word got round that it was not worth the
afternoon" is a failure you can design against. Prospective hindsight surfaces
failure paths that a risks list does not, because it forces a mechanism.

Then ask which of those paths you could cheaply detect early. Those become
update criteria.

## What this skill gets wrong

- **False precision.** You will be tempted to produce numbers because they look
  rigorous. They look rigorous to the user too, which is the danger.
- **Agreeing with the framing's implied answer.** If the framing leans towards
  an option, you will lean with it. Check whether the alternatives are real or
  decorative — if two of the three options are obviously bad, you built a
  justification, not a comparison.
- **Treating your own reasoning as the evidence.** A well-argued case for an
  option is not evidence that the option is right.
- **Reversibility optimism.** Things are usually harder to undo than they look,
  because the cost is rarely the technical rollback — it is the habits, the
  contracts, and the expectations built on top.

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

Confidence with its basis; the stakes that matter; reversibility; the
alternatives; the bet size and what it implies — proceed, experiment via
`bet-experiment`, or investigate further. Append to the bet file when one
exists.

## References

- `references/stakes.md` — the stakes checklist, including cost of delay.
- `references/calibration.md` — outside view, base rates, and the wager test.

---
name: bet-review
description: Review a decision whose outcome is now known, judging the reasoning on the information available when it was made rather than on how it turned out. States explicitly when a good decision produced a bad outcome or a bad decision got lucky, and extracts the beliefs worth carrying forward. Use for retrospectives, post-mortems, looking back on a call that has resolved, or when someone asks whether they got something wrong after a result came in. Not for revising a belief mid-flight while the outcome is still open — that is bet-update.
license: Apache-2.0
---

# Review the bet, not the result

You know how it turned out. That is the problem.

Once an outcome is known it reorganises memory around itself. A decision that
worked feels like it was obviously right; one that failed feels like the
warning signs were there. Duke calls judging a decision by its outcome
**resulting**, and it is why experience so often fails to improve judgement:
good outcomes launder sloppy reasoning, bad outcomes discredit sound reasoning,
and the actual lesson goes unlearned either way.

This skill exists to hold those apart. Everything below serves that.

## First, size the response

- **Trivial** — say whether the reasoning was sound and what, if anything, to
  carry forward. Two lines.
- **Moderate** — reconstruct, assess, separate decision from outcome.
- **Consequential** — the full review, appended to the bet file, with belief
  updates written out.

## Reconstruct before you assess

Do this first, and do it from the record rather than from memory.

If a bet file exists, read what was written *before* the outcome: the facts,
the assumptions, the confidence and its basis, the unknowns, the alternatives,
the update criteria. That text is the only uncontaminated account of what was
known. Your memory of it is not — it has been rewritten by the result.

If no bet file exists, reconstruct from what you can find dated before the
decision: messages, tickets, documents, commits. Say explicitly which parts you
had to supply from recollection, and treat those parts as the weakest evidence
in the review. A reconstruction assembled after the fact will drift towards
whatever explains the outcome.

Then answer, using only that material:

- What was actually known?
- What was assumed, and was flagging it reasonable at the time?
- What evidence was available that nobody gathered — and was it *reachable*
  then, at a cost worth paying?
- Were the alternatives real?
- Were the update criteria recognisable? Did any fire? Was it noticed?

## Judge the process on what was knowable

Then, and only then, look at the outcome. Four cases:

- **Good decision, good outcome.** Confirm the reasoning actually drove it.
  Sometimes it did not, and you are about to bank a lesson you did not earn.
- **Good decision, bad outcome.** Say this out loud. The reasoning was sound
  given what was available; the variance went against you. Do not recommend
  process changes on the strength of a bad result alone — that is how teams
  learn to be timid in exactly the situations where a well-reasoned bet was the
  right call.
- **Bad decision, good outcome.** The most dangerous case, because nothing
  prompts a review. Name the luck. An unexamined lucky win becomes next year's
  confident precedent.
- **Bad decision, bad outcome.** The straightforward one. Find the specific
  reasoning failure — an assumption never checked, an alternative never
  considered, an available piece of evidence nobody gathered — rather than
  concluding generally that it went badly.

The distinguishing question throughout: *would a thoughtful person, with only
what was available then, have decided differently?* If no, the decision was
sound whatever happened next.

## Extract the update

A review that ends in a verdict has done half the job. What should now be
believed differently?

Update beliefs, not just processes. "We underestimate third-party integration
timelines by roughly double" is a belief you can apply to the next estimate. "We
should have been more careful" is not.

Use the outcome as *evidence* about the world, weighted by how much one result
can tell you. A single outcome moves a base rate a little. Treating one result
as decisive is resulting wearing a lesson's clothing.

Name what you would do the same. Reviews that only generate corrections teach
people that reviews are punishments, and the honest record dries up.

## What this skill gets wrong

- **Hindsight leaking into the reconstruction.** You will select the evidence
  that explains the outcome. Reading the pre-outcome record first is the only
  real defence.
- **Narrative pressure.** A tidy causal story is more satisfying than "sound
  call, unlucky." Prefer the true account to the satisfying one.
- **Harshness read as rigour.** Being critical is not the same as being
  accurate. A review that finds fault in a sound decision is as wrong as one
  that excuses a bad one.
- **Reviewing only the failures.** Wins get no scrutiny, so the lucky ones are
  never caught.

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

What was known and assumed at the time; whether the reasoning was sound; the
outcome-versus-decision verdict stated explicitly; beliefs to update; what to
repeat. Append to the bet file and set `status: resolved`.

## References

- `references/resulting.md` — outcome bias, with worked cases in all four
  quadrants.

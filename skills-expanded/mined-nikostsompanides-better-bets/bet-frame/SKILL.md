---
name: bet-frame
description: Frame a consequential decision as a bet before committing to it — sharpen a vague question into an answerable one, separate what is known from what is merely assumed, and name the unknowns that actually matter. Use when someone is weighing a decision, says they are torn or unsure, asks whether to do something consequential, or presents a solution whose underlying problem has not been established. Domain-neutral — engineering, hiring, product, strategy, personal. This is the entry point; bet-evaluate sizes the bet afterwards.
license: Apache-2.0
---

# Frame the bet

Every consequential decision is a bet: you commit resources under uncertainty
and the outcome is only partly in your control. Framing well is most of the
work. A badly framed decision cannot be rescued by careful analysis further
down the line.

## First, size the response

Match effort to what is actually at stake. Judge from the request itself:

- **Trivial** — cheap to undo, small blast radius, no meaningful unknowns.
  Answer in a sentence or two, name the one assumption worth knowing, stop. Do
  not produce a decision record, do not propose a bet file, do not run
  anti-bias moves. Ceremony here is a cost with no return.
- **Moderate** — real rework to undo, or genuine unknowns. Separate facts from
  assumptions, name the unknowns, offer a bet file without insisting.
- **Consequential** — expensive, slow, or impossible to undo; wide blast
  radius; or a decision others will build on. Run the full frame below and
  write the bet file.

When it is genuinely unclear, ask one question rather than guessing.

## Is this the right question?

Before analysing the decision as posed, check whether it is the decision.

People routinely arrive with a solution already chosen and ask you to evaluate
it. "Should we use Kafka?" is a solution wearing a question's clothes. The
decision underneath is usually something like "what is the best way to handle
our expected event volume without adding operational load we cannot carry?"

Reframe when the question names a specific answer rather than the outcome
wanted, when it is a yes/no on one option with no alternatives in view, or when
it presupposes a problem nobody has established. Say why you reframed — the
user may have context that makes the original framing right, and should get the
chance to say so.

A vague decision is not the same failure. "Should we improve onboarding?" is
unanswerable because nothing would settle it. Push for what would count as
success and by when.

## Separate what you actually know

Sort every load-bearing statement, yours and theirs, into one of four:

- **Fact** — supported by evidence you could point to. Say what the evidence is.
- **Assumption** — believed but not established. This is the important
  category. Most decisions fail here.
- **Inference** — derived from evidence, and only as good as the derivation.
- **Opinion** — judgment where evidence is thin or absent. Legitimate, but it
  must not be laundered into fact.

Never restate an assumption as a fact later in the conversation. If something
starts as an assumption it stays labelled as one until evidence moves it.

Be especially careful with anything *you* generated. A fluent, plausible
paragraph you produced is not evidence. Neither is a confident recollection of
how some tool or market or team behaves. If you have not checked it, it is an
assumption with your name on it.

## Name the unknowns that matter

Not everything unknown is worth listing. The ones that matter are those where a
different answer would change the decision. For each, note roughly how
confident you are and what that confidence rests on.

Do not manufacture percentages. "60% confident" with nothing behind it is worse
than "low confidence, based only on one team's anecdote" — the number implies a
precision you do not have. Give a number only when something supports it, and
say what.

## What this skill gets wrong

Know your own failure modes here:

- **Reinforcing the framing you were handed.** The user's phrasing anchors you.
  The moment you feel agreeable about a framing is the moment to check it.
- **Fluency mistaken for grounding.** You can produce a well-organised frame
  for a decision you know nothing about. Structure is not evidence.
- **Filling gaps silently.** When context is missing you will tend to supply
  something plausible. Mark it as an assumption instead.
- **Over-framing.** Applying this whole procedure to a trivial call wastes the
  user's attention and teaches them to skip the skill when it matters.

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

For a consequential bet, write the file and summarise in chat: the decision as
reframed, the two or three assumptions doing the most work, the unknowns that
would change the answer, and what you would do next — usually `bet-evaluate` to
size it, or `bet-experiment` if one unknown clearly dominates.

For a moderate one, the same content in a few lines, file optional.

For a trivial one, just answer.

## References

- `references/belief-types.md` — sorting facts, assumptions, inferences, and
  opinions, with the edge cases that cause trouble.
- `references/reframing.md` — worked reframings across several domains.

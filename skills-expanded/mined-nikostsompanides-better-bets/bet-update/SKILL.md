---
name: bet-update
description: Commit to a decision on the evidence available — recording confidence, what remains unknown, and what specifically would change your mind — and later, revise that belief when evidence actually arrives. Use when someone is ready to decide, asks what to do now, wants a decision written down, or brings new information bearing on a decision already made. Not for judging a decision after its outcome is known, which needs a posture that resists hindsight — that is bet-review.
license: Apache-2.0
---

# Commit, then revise

Two moments, one skill, because they share a file and a discipline: say what
you believe, say what would change it, and then actually change it when that
arrives.

Read which moment you are in. If there is no commitment yet, you are
committing. If a decision exists and new evidence has turned up, you are
revising. If the outcome is known and finished, this is the wrong skill —
`bet-review` handles that, because judging a decision after the fact needs an
active guard against hindsight that this skill does not carry.

## First, size the response

- **Trivial** — state the call and the one thing that would change it. Done.
- **Moderate** — the decision record below, minus the sections that would be
  empty.
- **Consequential** — full record, written to the bet file.

## Committing

Deciding under uncertainty is the normal case, not a failure. The job is to
commit honestly rather than to manufacture the confidence that would make
committing comfortable.

The record:

- **Decision** — what is being chosen, in one line.
- **Objective** — the outcome being optimised for. If this is fuzzy, the
  decision cannot be evaluated later.
- **Key facts** — what is actually established, with the evidence.
- **Key assumptions** — what is being taken on trust. The load-bearing ones.
- **Confidence** — and what it rests on. No bare percentages.
- **Open unknowns** — what remains unresolved and why it was acceptable to
  proceed anyway.
- **Stakes and reversibility** — carried from `bet-evaluate` if it ran.
- **Alternatives** — what else was considered and why it lost.
- **Update criteria** — see below. Not optional.
- **Recommendation** — what to do now, concretely.

## Update criteria are the point

The single thing that makes a decision revisable is having written down, before
the outcome, what would change it.

Each criterion needs to be recognisable. "If it does not work out" is not a
criterion. "If p95 is still above 400ms four weeks after the cache lands" is.
Write them so a person who has forgotten the reasoning could still tell whether
one has fired.

Cover three directions:

- What would **increase** confidence enough to invest further.
- What would **decrease** it enough to slow down or hedge.
- What would **invalidate** the decision outright and trigger a change of
  course.

Give at least one a date. Criteria that depend only on events never fire when
the event is quiet failure — nothing happening is itself information, and only
a date will surface it.

## Revising

When evidence arrives, do this in order, and do the first step before forming a
view:

1. **Read the recorded criteria before assessing the new evidence.** Reverse
   that order and you will find yourself deciding whether the evidence "really"
   counts based on whether you still like the decision.
2. **Say which criterion it meets, or that it meets none.** Evidence that fits
   no criterion is common and worth noting — it may mean the criteria were
   wrong, which is itself an update.
3. **Update the belief, or explicitly do not.** "This does not meet the
   threshold, holding" is a legitimate and underused outcome. Manufacturing a
   revision because new information arrived is as bad as ignoring it.
4. **Mark the superseded belief in place.** Never delete it. The old belief and
   the date it changed are the record.
5. **Rewrite the criteria if they proved unrecognisable.** Say why.

## What this skill gets wrong

- **Rescuing the original decision.** Once something is written down, you will
  tend to interpret ambiguous evidence as consistent with it. The recorded
  criteria exist to take that judgment away from you in the moment.
- **Confidence inflation on commit.** Committing feels like it requires
  conviction. It does not. Record the confidence you actually have.
- **Vague criteria.** Easy to write, useless later. If you cannot imagine
  recognising it, rewrite it.
- **Silent revision.** Quietly changing the belief and moving on destroys the
  trail. The trail is the product.

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

On commit: the decision record, and the bet file with `status: committed`.
On revision: a dated section naming the evidence, the criterion it met, the
belief before and after, and any criteria rewritten.

## References

- `references/decision-record.md` — the record format with a worked example.
- `references/update-criteria.md` — writing criteria that actually fire.

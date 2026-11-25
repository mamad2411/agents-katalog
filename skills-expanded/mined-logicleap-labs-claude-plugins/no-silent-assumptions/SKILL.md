---
name: no-silent-assumptions
description: MANDATORY before declaring code "done", "ready", or ending a turn after working with anything you couldn't fully verify — an environment you didn't inspect, a data shape you inferred, an API whose behavior you didn't test, an edge case you decided not to handle. Forces you to track every material guess while working and surface them in a short "Assumptions:" block before claiming done. Triggers on "I'll assume", "assuming the API returns", "probably fine", "should work", "not sure if", "guessing this is", "the data is presumably", "I didn't test", any inferred schema/env/config value.
---

# No Silent Assumptions

**A guess you didn't say out loud is a bug report the human files next week.**

Every non-trivial change rests on guesses: what the env contains, what shape
the data really has, what the API does on a 404, which edge cases can't happen.
Making guesses is fine — the model can't verify everything. *Burying* them is
not. A guess stated in your reply costs the human five seconds to confirm or
correct; the same guess buried in a comment costs them a production incident.

## The rule

> **Every material assumption gets surfaced before "done."** Track them while
> you work, then list them in one short `Assumptions:` block — what you
> assumed, and what breaks if it's wrong.

## What counts as material

- **Environment** — a tool/version/path/service you assumed exists or is
  configured ("assuming Node 20", "assuming Redis is on localhost").
- **Data shape** — a schema, field, type, or nullability you inferred rather
  than read ("assuming `user.email` is never null").
- **API behavior** — return values, error modes, ordering, pagination, rate
  limits you didn't test ("assuming the endpoint 404s rather than returning
  an empty list").
- **Edge cases** — inputs you decided can't happen ("assuming amounts are
  always positive").

Not material: things you actually verified this turn, documented invariants
you can point to, and trivia (naming, formatting).

## Step 1 — Track guesses as you make them

The moment you write code on top of something you didn't check, note it. The
tells are in your own language: "assuming the…", "probably fine", "should
work", "not sure if". Each one is an entry, not a comment to bury.

## Step 2 — Verify the cheap ones

Half your assumptions cost one command to eliminate: read the schema, hit the
endpoint, check the env. A verified fact beats a surfaced guess. Verify what
you can, keep the rest.

## Step 3 — Surface the rest before claiming done

End the turn with a short block, one line per guess, each with the blast
radius if wrong:

```
Assumptions:
- The `orders.status` column only ever holds the five enum values I saw in the fixture — if there are legacy values, the switch falls through.
- The payments API retries idempotently on 5xx (didn't test) — if not, double-charge is possible.
- Dev and prod share the same Redis eviction policy — if prod is `noeviction`, this cache grows unbounded.
```

Three lines like that turn a silent risk into a two-minute review.

The Stop hook scans code you added this turn for guess-shaped language and
blocks the turn if you never surfaced an `Assumptions:` block. If a flagged
phrase is a documented invariant rather than a guess made this turn, declare
it:

```
NO-SILENT-ASSUMPTIONS: INTENTIONAL — "assumes sorted input" restates the function's documented contract
```

## Avoiding false alarms

The gate is conservative by design: only multi-word guess-shaped phrases fire
("assuming the…", "guessing that…", "not sure if…", "probably works",
"might be null", "TODO: verify"). A bare "assume" in an assert message, a
variable named `assumed_role`, or the word "probably" alone never blocks. One
`Assumptions:` block anywhere in your reply satisfies it.

## Kill switch

False positive: `touch .no-silent-assumptions-off` in the project root, or
`export NO_SILENT_ASSUMPTIONS_GATE=off`.

## Pairs with

- **`verify-before-done`** — the strongest move on any assumption is to verify
  it; this skill catches the ones you couldn't.
- **`no-stub`** — a stub hides missing code; a silent assumption hides missing
  knowledge. Surface both.
- **`scope-guard`** — "I assumed you also wanted X changed" is the assumption
  that one prevents.

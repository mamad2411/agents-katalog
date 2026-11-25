---
name: learn
description: "Record mistakes and turn repeats or checks that did not hold into stronger prevention. Use after review findings, reverts, red gates on merged code and owner corrections."
---

# Learn from outcomes

At adoption level 3 or above, after fixing a review finding, after a revert, after a gate goes red on merged code,
or when the owner corrects you, run:

`node scripts/tbs/learn.mjs add --class <short-kebab-kind> --where <file-or-area> --source <source> --evidence "<sha, PR or log line; disposition>"`

Sources: `review-finding`, `revert`, `gate-red-after-merge`, `owner-correction`. The hook records `hook-block` and `revert` itself (at level 3 or above);
do not duplicate it. Keep evidence short and free of secrets. Never rewrite or delete old entries.
Routine also records findings routed to an issue or an owner decision.

Run `node scripts/tbs/learn.mjs --due` at session start and `--recurred` after shipping a check.
For each due class, draft prevention on a branch for the owner to accept. Prefer architecture, then types,
a lint with a useful fix, tests, hooks or gates; use docs for remaining judgment. A review miss gets a seeded
eval case and a measured review pass. Prove the check red on the original mistake and green on the fix.
Never merge the draft yourself.

At adoption level 4, the owner may not be around to accept a draft or answer a question. Do not wait: park
that item (keep its branch, pushed only if the project's rules already allow it, and note the branch and
your recommendation where the project keeps owner questions) and
work on what does not need them, such as other due classes, outcomes to record and checks to prove red.
Absence is never acceptance: the draft stays unmerged and the answer stays pending until the owner gives it.

After the owner accepts and ships the check, add a row to the shipped-enforcers table with the class,
enforcer id and actual UTC ship timestamp. That row links the class to its enforcer.
Future mistake records may also name the check with `--enforcer <id>`; those still count as recurrences.
A later entry for that class returns it to due with “check did not hold”; strengthen the check and repeat.
See the enforcers template for the precise table format and journal storage. Never mark a draft shipped.

Run `node scripts/tbs/learn.mjs sync` after recording outcomes so the shared local journal is appended to
`learn.file` (default `docs/trust-before-scale/lessons.jsonl`) for the normal commit. Review the added entries.

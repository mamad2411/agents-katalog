---
name: ledger-report
description: "Mastery map for this project: which areas of the codebase are defended, which are thin. Run it at a commit, a pull request, or on request. (decision-ledger)"
allowed-tools:
  - Bash
  - Read
---

# ledger-report

The map of what this project's decisions rest on. Report at moments the user already stops at: a commit, a pull request, or an explicit request. **Never mid-task.**

```bash
for p in ~/.claude/skills/decision-ledger/bin/ledger \
         ~/.claude/skills/ledger-report/bin/ledger \
         .claude/skills/ledger-report/bin/ledger \
         .agents/skills/ledger-report/bin/ledger; do
  [ -x "$p" ] && LEDGER="$p" && break
done

$LEDGER report      # the map
$LEDGER askable     # concepts due for a revisit here
$LEDGER personal    # what the user has defended across projects
```

The list covers both ways this can be installed: `install.sh`, which lays down the whole repo, and a skills registry, which copies this directory alone.

## Present a map, not a curve

A rising line invites optimisation and becomes exactly the engagement metric this project exists to reject. A map answers the only useful question: where am I thin?

```
Mastery map: 24 decisions tracked, 21 days

  auth/          ██████░░░░  2 of 5 defended     <- thinnest area
  data-model/    █████████░  4 of 5, 1 decayed
  ui/            ██████████  7 of 7
  jobs/          ████░░░░░░  2 of 5, 1 unknown

  Transfers observed: 2 (session-storage, cache-invalidation)
```

Add at most one factual, non-judgemental line:

> Since last week, `auth/` grew by 340 lines while two of its decisions remain undefended.

Then stop. No advice, no nudging, no offer of a lesson, no encouragement. The information is the product, and anything appended to it reads as a verdict on the person.

## Language

Every sentence describes **the project**, never the developer.

- Say: "`auth/` has two decisions with nothing on record."
- Never: "you don't understand auth."

The distinction is not cosmetic. It decides whether this is a map someone consults or a rating they resent, and a rating ends up in a performance review, which is the failure mode the whole design avoids. There is deliberately no global score for the same reason: aggregating across areas produces a number that rates a person.

## After an audit, say what the map is not

When `report` prints that the decisions came from an audit, repeat it in your own words before showing anything else. An audit goes looking for what nobody arbitrated, so the first map is a picture of where it pointed, not of what the person knows.

Left unsaid, a screen of empty bars reads as "you don't know your own project", which is a verdict on a person and the exact misuse this whole design exists to prevent. It is also simply wrong: the decisions that were already defended were never asked about, so they are not in the file.

> Five decisions, all from the audit. It went looking for what had no entry, so this is where it pointed, not a score. `boundaries/` is the one you corrected me on.

Where the audit recorded real knowledge, such as a `partial` earned by correcting the auditor or a convention the user could justify, name it. It is the part that makes the rest credible.

## Decay

Confidence decreases in areas left untouched. Someone who has not opened a module in three months understands it less well than they did. Default half-life is 90 days of no activity in the area.

A decayed concept becomes askable again, and that is a feature, not a gap to apologise for: it is spaced retrieval, and re-answering correctly is a stronger signal than the first answer was. If the user reads decay as backsliding, say plainly that an index which only ever rises is a badge.

## At a pull request

The report is a mirror, never a gate. State what is undefended in the diff, and let them through:

> 340 lines added, 2 decisions in `auth/` with nothing on record. Opening the PR.

If the ledger is empty because the project predates it, do not report zeros. Point at `/ledger-audit` instead, which reconstructs the decisions already made.

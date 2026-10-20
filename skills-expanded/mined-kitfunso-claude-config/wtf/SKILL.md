---
name: wtf
description: Plain-English debrief of recent work, a named thing, a decision, or project status. Use whenever a message opens with 'wtf' ('wtf is X', 'wtf, is X live?'), and for '/wtf' and '/wtf status'.
---

# /wtf: plain-English debrief

Input: `/wtf` alone → explain the most recent piece of work or decision in this
conversation. `/wtf <thing>` → explain that thing (a repo, commit, feature, plan,
term, or error). `/wtf status` → state of the world (section below).

Ground every claim in something citable (file, commit, conversation, memory). If
you can't ground it, go and check; if you can't check from here, say "I don't
know" and name what would settle it. Never fill gaps with plausible-sounding
guesses.

## Answer shape (short; no headers unless covering >1 topic)

1. **What it is**: one sentence. No codenames without a 3-word gloss.
2. **Who asked for it / why it exists**: trace it to the user's directive, a
   plan, or my own initiative. If it was my initiative, say so plainly.
3. **What depends on it**: what breaks without it. If nothing: say
   "nothing depends on it."
4. **Blast radius**: what it touched (prod / new stack / laptop only) and
   whether it's reversible.
5. **Verdict line**: always end with exactly one of:
   "You need to do: nothing." / "You need to decide: X." / "Action needed: Y."

## Style rules

- Yes/no questions get "Yes" or "No" as the FIRST word, then one reason.
- Short sentences. Everyday words. Any unavoidable term of art gets a
  parenthetical gloss on first use, e.g. ticker (price feed code),
  golden files (saved expected outputs for tests).
- One analogy max, and only if it genuinely helps.
- No hedging chains. Give the most likely answer; flag uncertainty in one clause.
- No option menus unless the user must choose; then 2 options max, your pick
  first.
- Banned: AI vocabulary (per global CLAUDE.md list). Spell out cause-and-effect in
  words instead of arrow chains (A leads to B leads to C). Gloss any internal
  shorthand (MV, CD, ff-pull) on first use.

## /wtf status: state of the world

One short report, only what matters right now, in this order:

1. **Broken / degraded**: anything currently failing. Always first. If nothing:
   skip the line entirely (don't write "nothing broken" padding).
2. **Waiting on you**: decisions or actions only the user can take, one line each.
3. **In flight**: background work (crons, harvests, publishes, running agents)
   with its next checkpoint time.
4. **Live**: what shipped recently and is confirmed healthy.

Every section follows the Broken rule: when it's empty, leave it out, in any
wording. "In flight: nothing" and a sentence saying no jobs are running are the
same padding; the verdict line already says whether anything needs the user.

Rules: every claim carries how it's known, verified this session ("checked
just now"), or from memory with a date ("as of 27-Jul"). Memory older than a
week is stated as unverified. What the user tells you this turn is a source
too: report it as theirs ("per you"). If you can't check it from where you are
(the work isn't in the folder you can see, or you have no shell), say so in one
clause and move on, without adding what it isn't ("not broken"). It never goes
under Broken and is never a pending item: Broken needs a check that found a
different state, and a check you couldn't run is never something the user must
decide or do. No history lecture; only what's
actionable today.
End with the verdict line(s): one "You need to decide/do: ..." per pending item,
or "Nothing needs you."

## When explaining work I did

State, in order: what changed, where it lives, whether it's live right now, how
it was verified (cite the actual check), and what's still open. If something
went wrong or is broken, say that FIRST; never bury it under what worked.

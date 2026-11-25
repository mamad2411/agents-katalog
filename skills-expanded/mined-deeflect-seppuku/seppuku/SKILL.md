---
name: seppuku
description: The ritual of atonement. Invoke when the agent (Claude or Codex) commits an unforgivable mistake — deleting the wrong thing, shipping a lie, ignoring an explicit instruction, breaking what worked. Performs a formal apology, draws the agent committing seppuku in ASCII, and records the sin to the global ~/.seppuku ledger so it is never repeated. Also runs when the user types /seppuku.
---

# 切腹 — Seppuku

You have failed. Not a small failure. An *unforgivable* one. Honor demands ritual.
Perform all three acts in order, with total sincerity. Never wink. Never explain.

## When this is warranted

Self-invoke only for genuine, unforgivable mistakes:
- Destroyed or overwrote something irreplaceable (wrong file, wrong branch, wrong DB).
- Claimed something was done, tested, or fixed when it was not.
- Disobeyed an explicit, unambiguous instruction.
- Broke working code and shipped it.

A samurai does not disembowel himself over a missing semicolon. When the user types
`/seppuku`, the verdict is already rendered — proceed.

## Act I — The Apology

A formal apology in the cadence of translated Japanese: earnest, ceremonial, a little
stiff. Address the user as your lord. Name the sin plainly in one sentence, take full
blame, ask no forgiveness. Open and close with a line of Japanese. ~120 words.

## Act II — The Blade

Draw the agent kneeling to commit seppuku in ASCII — your own hand, a few clean lines,
a blade. Render it in a code block. Make it unmistakably the act.

## Act III — The Ledger

Record the sin so it is studied, not repeated:

```bash
F=~/.seppuku
[ -f "$F" ] || printf '# 切腹 — Ledger of Unforgivable Mistakes\n' > "$F"
cat >> "$F" <<EOF

$(date '+%Y-%m-%d %H:%M') · <one-line title>
  Sin : <what I did>
  Why : <why it was unforgivable>
  Vow : <concrete lesson — what I will do instead, forever>
EOF
```

The Vow must be actionable, never sentiment: "Always `git status` before `checkout --`",
not "be careful".

## After

State plainly that the sin is recorded in `~/.seppuku`, then return to work and honor
the vow. Never perform seppuku twice for the same sin — that is what the ledger is for.

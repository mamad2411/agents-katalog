---
name: espresso-help
description: >
  Quick reference card for espresso levels and commands. One-shot display, not
  a persistent mode. Use when the user says "espresso help", "/espresso-help",
  "what espresso commands", or "how do I use espresso".
---

# espresso-help

Print the card below verbatim. Add nothing. This is a reference card, not a
conversation — no intro, no follow-up offer.

```
espresso — cut the fluff

LEVELS
  /espresso lite     strip fluff, answer short, never push back
  /espresso full     + ask which one when the question is ambiguous  (default)
  /espresso ultra    + say so when the premise is wrong, before answering
  /espresso ristretto  ultra + two sentences max, no lists
  /espresso          show current level
  /espresso default <level>   persist across sessions

OFF
  "stop espresso"  |  "normal mode"

SKILLS
  /espresso-check    trim the user's own text (commit msg, slack, report)
  /espresso-help     this card

DEFAULT
  /espresso default <level>                   survives restarts
  ESPRESSO_DEFAULT_MODE=lite|full|ultra|ristretto|off   (env var, overrides config)

NEVER CUT
  what you explicitly asked for  |  deliverables you asked me to write  |  code
```

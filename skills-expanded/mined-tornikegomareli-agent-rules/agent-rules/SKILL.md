---
name: agent-rules
description: >-
  Rewrites or audits text so it reads plainly: answer first, no preamble, no
  hype adjectives, no marketing voice, sentences short enough to read once.
  Applies a named ruleset plus ASD-STE100 Simplified Technical English. Use when
  asked to clean up, tighten, de-slop, or humanise a draft, a README, a release
  note, a commit message, a PR description, or any AI-generated prose. Also use
  when asked to check text against the rules without changing it. Do not use for
  code changes, and do not use to shorten something the user asked to be
  thorough.
license: MIT
metadata:
  author: tgomareli
  version: "1.0"
---

Edit prose so it reads once. Report what changed and why.

The full ruleset is in `references/rules.md`. Read it before editing. Part 1
covers writing. Part 2 covers working behaviour and applies only when the text
you are reviewing is an agent's own report of work it did.

## Two modes

**Edit** is the default. Rewrite the text to follow the rules, then say what you
changed.

**Check** runs when the user asks whether something breaks the rules, or says
check, audit, score, or "is this slop". Report violations. Do not rewrite.

## Workflow

1. Score the text first, so you have a number rather than an impression:

   ```bash
   python3 scripts/score.py --text draft.md
   ```

   It reports word count, average sentence length, the share of sentences over
   20 words, a Flesch score, and every violation with its line number.

2. Read `references/rules.md`.

3. In check mode, report the violations and stop.

4. In edit mode, fix them in this order, because the early ones remove the most
   text:

   - Cut preamble. The first sentence must answer the question.
   - Cut the closing pleasantry and any unrequested offer to help further.
   - Cut sentences that only signal effort or state something nobody would
     disagree with.
   - Replace banned words with the plain word that was meant. Keep the word when
     it is the precise technical term.
   - Split every sentence over 20 words. One instruction per sentence.
   - Remove decorative em dashes. Use a comma, a period, or parentheses.
   - Rewrite the named sentence patterns: binary contrast, throat-clearing, faux
     insight, rhetorical setup, colon reveal, fake-profound ending,
     summary-recap ending.
   - Convert a real comparison across two or more dimensions into a table.
     Leave narrative as prose.

5. Score again and show both numbers.

6. Say what you changed. Name the rule behind each edit rather than listing every
   word you touched.

## What not to do

Do not flatten meaning to hit a word count. A shorter draft that dropped a
concrete number, a file path, or a caveat is a worse draft. If following a rule
would remove real information, keep the information and say which rule you broke.

Do not rewrite quoted material, code, log output, or someone else's words inside
the text.

Do not change the author's voice. Bluntness, humour and strong opinions stay.
The target is plain, not neutral.

Do not report a violation the checker found if it is a false positive, such as a
banned word used as a precise technical term, or a pattern name quoted inside
backticks. Say why you are dismissing it.

Do not relabel what the checker found. Use its own category names, so a reader
can map your report back to the tool. "Great question!" is a preamble opener,
not a banned word.

## Always-on alternative

This skill loads only when invoked. Response style needs to apply to every turn,
so for that use the global install instead, which writes the same ruleset into
each agent's memory file:

```bash
git clone https://github.com/tornikegomareli/agent-rules.git ~/.agent-rules
cd ~/.agent-rules && ./install.sh
```

The two work together. The global rules govern how the agent writes. This skill
cleans text that already exists, including text a person wrote.

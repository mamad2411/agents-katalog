---
name: sr-humanize
description: Edits a draft so it sounds like the person and not like a generic assistant. Removes invisible characters, em dashes and curly quotes, cuts or replaces stock phrases such as delve, tapestry, game-changing and in today's fast-paced world, lists the structural habits a script cannot fix (it's not just X, it's Y; rule-of-three; tidy recap closers; emoji bullets), and shows a before and after style score. Use before posting any AI-assisted writing, when drafts feel stiff or samey, or when someone asks to make something sound human. A style editor, not a detector bypass.
license: MIT
compatibility: Any agent that loads Agent Skills. Python 3.9+ for the cleaner; the by-hand checklist below works without it.
metadata:
  author: Raj Bharti
  version: "0.1.2"
  family: showrunner
---

# Humanize: sound like the person

Readers can tell when nobody was home. The fix is not a trick. It is specific details, the person's rhythm, and cutting the phrases everybody has seen too many times.

## What this is, and is not

It is an editor for style. It is **not** a way to beat AI detectors, and it makes no claim about any detector service. Detectors are unreliable and Showrunner does not try to defeat them. If a platform, school or employer requires you to disclose AI use, disclose it (`sr-policy-check`).

## Run it

Tool `text_humanize` with the draft as `text`. Options: `emdash` (`comma`, `period`, `hyphen`, `keep`), `keep_quotes`, and `banned_phrases` (defaults to the list in the profile's `voice`). CLI:

```
python scripts/sr.py humanize --file draft.txt
python scripts/sr.py detect --file draft.txt
```

The cleaner does mechanical things only: removes zero-width and other invisible characters, replaces em dashes, straightens quotes, cuts or swaps stock phrases, and leaves URLs, code, hashtags and mentions alone. It keeps Hindi, Hinglish and other scripts intact. Then it lists what a script cannot fix.

`text_detect` runs five local style checks: sentence-length variation, concrete details per 100 words, stock-phrase density, typographic fingerprints and structural tells. It returns a score with reasons. These are heuristics, not detector verdicts.

## Then rewrite by hand

Work through `needs_rewrite` and `watch_words` with the person.

- **"It's not just X, it's Y."** Say the Y.
- **Three-item lists everywhere.** Real lists are different lengths.
- **A tidy summary at the end.** If the post worked, the summary is redundant. Cut it.
- **Emoji bullets.** A template tell. Use plain lines.
- **Abstract nouns** (journey, landscape, ecosystem). Name the actual thing.

Then add **specifics from the person's real life**. Ask three questions: What was the number? What was the name of the place or person? What exactly went wrong? Put the answers in. Never invent a detail to make the text feel real.

Finally, read it aloud. Anything you would not say, change.

## By hand (no tools)

Search the draft for: "delve", "tapestry", "landscape", "navigate", "unlock", "elevate", "leverage", "in today's", "it's important to note", "in conclusion", "game-changer", and for the em dash character. Count sentences that begin the same way. Check whether any sentence contains a number, a name or a place. If fewer than one in four does, add some.

## Check the voice

Compare with the voice notes (`sr-voice`). Banned phrases from the profile are cut automatically.

## Gate

`approve`. The person reads the final text and confirms it is something they would say.

## Do not

- Promise it will pass a detector.
- Strip the person's own quirks. Their habits are the point.
- Add fake casualness ("lol", "tbh") they never use.

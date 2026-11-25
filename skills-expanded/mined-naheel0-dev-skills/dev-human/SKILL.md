---
name: dev-human
description: >-
  Strip the machine fingerprint out of any dev.to draft - em dashes, AI slop
  words, invisible watermark characters - and score it against a five-check
  detection panel before it goes out. Use before any dev.to article is shown
  to the user.
---

# dev-human

Two tools live in this folder and they both actually run. Use them. Do not
eyeball this.

```
python3 humanize.py draft.txt --report   # clean it, show what changed
python3 detect.py draft.txt              # score it, five checks
python3 detect.py before.txt after.txt   # prove the delta
```

Both read `slop.json`, which is the lexicon: 100+ stock words and phrases
with plain-English replacements, 17 invisible character classes, 11
typographic substitutions, and 11 structural tells. It is meant to be
edited. If the user has a word they always use that the lexicon strips,
remove it from the file.

## What gets fixed automatically

**1. Invisible characters.** Zero-width spaces and joiners, word joiners,
soft hyphens, byte-order marks, Unicode tag characters, non-breaking and
narrow spaces. A keyboard does not produce these. They survive copy-paste,
they are invisible in every editor, and they are the single most mechanical
thing in generated text. `humanize.py` deletes every one, including any
remaining Unicode format character it does not have a name for.

**2. Typography.** Em dash to comma, en dash to hyphen, curly quotes to
straight, ellipsis to three dots, bullet character to hyphen. The em dash
pass is the one that matters: it collapses ` — ` to `, ` and then cleans up
the double punctuation that leaves behind.

**3. The slop lexicon.** delve, leverage, robust, seamless, crucial,
tapestry, testament to, moreover, "in today's fast-paced world", "let that
sink in" and the rest, each swapped for a plain word, with capitalisation
preserved and URLs left untouched.

## What does NOT get fixed automatically

Structural tells get **flagged, not rewritten**, because changing the shape
of a sentence needs judgement:

- "It's not just X, it's Y" and "not only X but also Y"
- Rule-of-three triads
- Rhetorical one-word question lines: "The result?"
- Rocket, fire, bulb, sparkle and dart emoji
- Hashtag walls
- Reflex engagement bait: "Thoughts?", "Agree?", "Who else?"
- Uniform sentence length and uniform bullet length
- Code blocks without surrounding context (every snippet needs intro text)

That list is your job. Rewrite each flagged line by hand, keeping the
meaning, then re-run `detect.py`. This is the part that moves the score from
REVIEW to PASS, and it is the part a script cannot do.

## The five checks

`detect.py` scores five signals 0-100, higher is more human:

| check | what it measures | machine looks like |
|---|---|---|
| BURSTINESS | sentence-length variation | every sentence the same length |
| SPECIFICITY | numbers, names, concrete markers per 100 words | abstract nouns, no figures |
| SLOP DENSITY | lexicon hits per 100 words | stock vocabulary |
| FINGERPRINT | invisible chars, em dashes, curly quotes per 1k chars | typographically perfect |
| VOICE | contractions, person, structural tells | no contractions, staged reveals |

The verdict weights the mean at 60% and the **weakest single check** at 40%,
because a detector only needs one signal to fire. PASS needs an overall of
70+ with no check below 55.

## Say this honestly

These are five local heuristics modelled on the signals public detectors
key on. They run entirely on the user's machine and nothing is uploaded.
They are **not** GPTZero, Originality, Copyleaks, Winston or Turnitin, they
do not call those APIs, and they cannot promise those verdicts. Fixing what
they measure does tend to move those numbers, because they are measuring the
same underlying things. That is the claim. Do not make a bigger one on the
user's behalf, and do not tell a user their text is undetectable.

## Order of operations

1. `humanize.py draft.txt -o clean.txt --report`
2. Read the structural flags. Rewrite those lines yourself.
3. `detect.py draft.txt clean.txt` to show the before and after.
4. If the verdict is not PASS, fix the weakest check named in the output and
   go again. Two rounds is normal. Five means the draft was written by
   formula, and the fix is a different draft, not more passes.
5. Show the user the cleaned text and the score. Never the score alone.
6. After publishing, record the `human_score` in `~/.claude/devto/log.md`
   for that post. `/dev-learn` uses it to track whether humanized drafts
   outperform non-humanized ones.

## Self-improvement: slop learning

`slop.json` does **not** auto-expand — slop words are voice-specific. After
several `humanize.py --report` runs, note which slop words keep reappearing.
Add them manually to `slop.json` replacements, or remove words the user
consistently re-adds. Run `dev-learn.py status` to review current coverage.

## dev.to-specific notes

- dev.to articles are long-form (800–2,500 words). The lexicon and checks
  are the same as `li-human`, but length targets differ: aim for 1–3 min
  read for reach, 4–7 min for depth.
- Code blocks are expected on dev.to; they don't count as slop. But every
  code block needs context text before it.
- YAML front matter (`title`, `tags`, `canonical_url`, `cover_image`,
  `series`, `ai_disclosure_level`) is structural, not prose — leave it alone.

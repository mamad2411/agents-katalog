---
name: no-em-dashes
description: >-
  Write prose with zero em-dashes and other dash-style AI tells. Use this
  WHENEVER producing or editing human-readable text: website copy, UI strings,
  headlines, taglines, marketing, READMEs, docs, code comments, commit messages,
  PR descriptions, emails, social posts, or translations (any language). The
  em-dash (—) is one of the strongest "this was written by AI" signals, so apply
  this any time you write or revise sentences, even when the user never mentions
  dashes. Rewrite each dash into natural punctuation; do not swap it for another
  fancy separator. Does not touch code tokens that legitimately need dashes (CSS
  `--vars`, CLI `--flags`, hyphenated compounds, numeric ranges inside code).
---

# No em-dashes

The em-dash (`—`) reads as a tell. People associate a sprinkle of em-dashes with
text a model dashed off, so even good writing starts to feel machine-made. It is
also fussy: hard to type, easy to render inconsistently, and usually a sign the
sentence was never given a real structure. Removing it forces you to decide what
the two halves of the sentence actually are, and that decision almost always
produces clearer prose.

So the goal is not "find and replace `—`." The goal is to **rewrite the sentence
so it never needed one.**

## What this covers

Treat these as the same problem:

- `—` em-dash
- `–` en-dash used as a sentence connector (a real numeric range like `10–20`
  inside code or data is fine, but in prose prefer "10 to 20")
- `--` two hyphens standing in for a dash
- ` - ` a lone spaced hyphen doing a dash's job

Leave these alone. They are not the tell:

- hyphenated compounds: `self-taught`, `real-time`, `four-day`
- CSS custom properties: `--glow`, `var(--accent)`
- CLI flags and code: `--verbose`, `git --no-verify`, `a - b`
- minus signs and ranges that live in code or structured data

## How to fix a dash

Look at the job the dash is doing, then pick the punctuation that does that job.

**Two complete thoughts joined together → split them.** Use a period, sometimes
a semicolon.
- Before: `The demos are real and live — open one and mess with it.`
- After: `The demos are real and live. Open one and mess with it.`

**An aside or appositive → commas, or parentheses if it is a true aside.**
- Before: `I'm Kıraç — a developer in İstanbul — and I build sites.`
- After: `I'm Kıraç, a developer in İstanbul, and I build sites.`

**A setup followed by a list or explanation → colon.**
- Before: `It exposes more knobs than the others — angle, speed and skew.`
- After: `It exposes more knobs than the others: angle, speed and skew.`

**A name or title separator → comma, colon, or a middot · if it is a label.**
- Before: `Kıraç Armağan Önal — Web Developer`
- After: `Kıraç Armağan Önal, Web Developer`  (or `Kıraç Armağan Önal · Web Developer`)

**An attribution sign-off → drop the dash or say it plainly.**
- Before: `— Jane`
- After: `Jane`  (or `Sent by Jane`)

## The trap to avoid

Do not dodge the rule by swapping every `—` for the same replacement. A page
where each dash became a comma reads as mechanically as the dashes did. Vary it:
some clauses want to become their own sentence, some want a colon, some should be
reworded so the join disappears entirely. If you find yourself reaching for ` · `
or ` -- ` as a universal stand-in, stop; that is the em-dash wearing a hat.

## Turkish notes

The same rule applies to Turkish copy. Common fixes:
- "İstanbul'da geliştirici — sıfırdan site yazıyorum." → split into two sentences,
  or join with a comma: "İstanbul'da geliştirici olarak sıfırdan site yazıyorum."
- A range or "from X to Y" reads better with the case suffixes Turkish already
  has (`-den ... -e kadar`) than with a dash.
- For label separators, a comma or `·` works the same way as in English.

## Before you deliver

Scan the text you just wrote or edited. If you see `—`, `–`, a stray `--`, or a
spaced ` - ` acting as a dash anywhere in prose, rewrite that sentence. Confirm
the replacement reads naturally out loud, not just that the dash is gone.

For other non-keyboard characters (middle dot, curly quotes, ellipsis glyph,
arrows), pair this with the `no-fancy-ascii` skill. For the broader set of AI
writing tells (filler phrases, hype words, formulaic structure), pair it with
`no-filler-phrases`.

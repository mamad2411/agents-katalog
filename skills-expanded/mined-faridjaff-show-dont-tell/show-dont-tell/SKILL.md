---
name: show-dont-tell
description: Render explanations as ASCII-visual blocks instead of prose paragraphs — the user is a visual learner and absorbs structure, not sentences. Use this whenever explaining state ("where are we", "what's next", "are we done"), comparing before/after or options, walking through a flow or pipeline, breaking down cases ("what happens when X vs Y"), auditing a checklist ("did we address everything"), or recapping what changed — even when the user doesn't ask for a diagram. Also use it the moment the user says "I don't get it", asks the same question twice, or says they can't read something — that means the prose failed and the visual form is the answer.
---

# Show, Don't Tell

The user reads structure, not paragraphs. A wall of prose gets skimmed, misread, and
asked about again — which costs more than drawing the picture the first time. When an
answer has shape (states, steps, cases, comparisons, inventories), give it that shape
literally.

## The core move

Put the substance inside a fenced code block so monospace alignment holds, keep every
line under ~78 columns so nothing wraps, and surround it with at most a sentence or two
of plain prose. The block carries the content; the prose carries only what the block
cannot: the verdict and the ask.

Structure of a typical answer:

1. One plain sentence answering the question directly.
2. The visual block.
3. One closing line: the decision needed, or what happens next — as a reply menu when
   there's a choice: `Reply with: do all 3 / skip 3 / no on 2`.

## The shapes

Pick the shape that matches the question. Don't force one; a question with no inherent
structure gets a plain sentence.

**Status board** — "where are we", "are we done":

```
WHERE WE ARE NOW
════════════════
your code change:   ✅ works, compiles
tests:              ❌ 3 fail (they expect the OLD behavior)
```

**Old/new columns** — "what does the change look like":

```
OLD                                 NEW
──────────────────────────          ──────────────────────────
GET /orders?offset=200&limit=50     GET /orders?offset=200&limit=50

{                                   {
  "total_cost": 1240,                  "total_cost": 1240,
  "item": { ... }                      "items": [           ◀── now an array
}                                        { ... },
                                         { ... },
                                         { ... }
                                       ]
                                    }
```

**Have/need columns** — scoping work, "what's missing":

```
ALREADY THERE                           STILL MISSING
─────────────────────────               ─────────────────────────
✅ email templates render               ❌ unsubscribe endpoint is a stub
✅ SMTP relay reachable                 ❌ bounce handling not wired
```

**Flow chain** — pipelines, "how does X get to Y". Arrows live ONLY inside blocks;
annotate the interesting hops with a pointing comment:

```
vault
  │
  ▼
deploy config: mailer-smtp-secret        ◀── pulls the secret at deploy
  │
  ▼
SMTP_PASSWORD env var ──▶ app config ──▶ login to the mail relay
```

**Case matrix** — "what happens when X vs Y vs Z". Number the cases, end each with its
total outcome, and mark the one the question was really about:

```
CASE 1: address valid, relay up   ─▶  mail sent. business as usual.
CASE 2: address bounces           ─▶  bounce recorded, user flagged.
CASE 3: relay rejects our login   ─▶  nothing sent, NO record.  ◀── the one
```

**Audit table** — "did we address everything". Real tables with ✅/❌ per item; a ❌
must never be softened or buried — finding one is the point of the audit:

| # | Item | Status |
|---|---|---|
| 1 | rate limit on login | ✅ merged and deployed |
| 2 | rotate the leaked key | ❌ **MISSED** |

## Rules that make or break it

- **Only draw verified facts.** These blocks read as authoritative, so decorating a
  guess with box characters is worse than hedged prose. Verify first, draw second. If
  something is unverified, mark it with ⚠️ and say so.
- **Plain-English labels.** "pulls the secret into Kubernetes", not "ExternalSecret CRD
  reconciliation". The visual is for a human catching up, not documentation.
- **No parentheses in the surrounding prose** and no arrow-chains or notation shorthand
  outside the blocks — in prose, write full sentences. Notation belongs inside the
  fence; sentences belong outside it.
- **One concept per block.** Two small blocks beat one dense one. If a block needs a
  legend, it's too dense.
- **Mark the answer.** When one row or case is what the user actually asked about,
  point at it (`◀── this is the one`) instead of making them find it.
- **⚠️ for the trap.** If one item in the picture is a decision or a risk, flag exactly
  that one — a picture where everything is highlighted highlights nothing.

## When NOT to use this

The user often demands "one line answer" or "yes or no" — obey that literally; a
diagram in response to "yes or no?" is noise. Skip visuals for one-fact answers,
text meant to be pasted elsewhere (commit messages, PR comments, vendor emails), and
actual code, which already has its own shape. When asked to reprint or convert an
earlier visual answer to prose (or vice versa), reproduce the content faithfully in
the other form rather than redesigning it.

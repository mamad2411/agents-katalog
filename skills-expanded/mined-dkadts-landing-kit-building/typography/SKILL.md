---
name: typography
description: Print-quality typography enforcement for English text. Prevents widows, orphans, and hanging short words (articles, prepositions, conjunctions, dashes) at line ends. Rewrites HTML text nodes to insert &nbsp; ties. Also serves as the canonical short-word list used by /build and /audit.
---

# /typography

Standalone skill. Takes a completed section (or the full `site/index.html`) and enforces print typography rules on all English text. Callable anytime — before `/audit`, after copy edits, whenever the source text changed.

Also the **single source of truth** for the short-word list that `/build` (pre-save pass) and `/audit` (post-build check) both reference.

Language scope: **English only**. Do not run on any other language.

## When to use

- After `/build` writes a new section — `/build` calls this automatically as its pass 4b.
- After any copy edit in `inbox/texts/` that triggered a rebuild of a section.
- Standalone: user says "fix the typography on the hero" or "re-run typography on the whole site".
- Before `/audit` as a safety pass.

## Requirements

- `site/index.html` exists (or a specific section HTML file was provided).
- Content is English. If the copy is in another language, refuse and report which language was detected.

## The rules

### Rule 1 — Hanging short words at line end

A rendered line MUST NOT end on any of these words. Tie the word to the following word using `&nbsp;` so they wrap together.

**Canonical short-word list (English):**

```
# Articles
a, an, the

# Coordinating conjunctions
and, or, but, nor, for, so, yet

# Subordinating conjunctions & connectors
if, as, at, by, in, on, of, to, up, via, with, into, onto, from, than, then, when, where, while, before, after

# Auxiliary and short verbs
is, am, are, was, were, be, do, does, did, has, have, had, can, will, would, could, should

# Pronouns (short)
I, we, he, she, it, you, they, my, our, his, her, its, your, their, this, that

# Negations & quantifiers (short)
no, not, all, any
```

Case-insensitive matching, but preserve the original case when rewriting.

### Rule 2 — Dashes never end a line

`-`, `–`, `—` must attach to the following word: `text&nbsp;— word` (nbsp before the dash, regular space after). This is opposite direction from Rule 1 — dash pulls the next word up.

### Rule 3 — No orphans

Last line of a heading or a paragraph must contain **at least 2 words**. If the natural break would leave a single word on the last line, tie the last two words together: `... together with&nbsp;us.`

Detection heuristic: for each `<h1>`, `<h2>`, `<h3>`, `<p>`, `<li>`, take the last 2-3 words and tie the last two with `&nbsp;` regardless of length. Cheap, prevents 95% of orphans.

### Rule 4 — No widows (advisory)

If a `<p>` or `<blockquote>` spans a column break (rare on landing pages, but happens in multi-column footer or blog-style sections), the first line on the new column must contain ≥ 2 lines of the paragraph. This is difficult to detect statically — flag rather than fix.

## Process

**Step 1. Read input.**

- If a file path was provided, load it.
- Otherwise load `site/index.html` and every section CSS to know which classes are text vs decorative.

**Step 2. Detect language.**

Sample ~200 chars from the largest `<p>` and the first `<h1>`. If the character set is not predominantly ASCII English, stop and report. Example refusal: `Detected language: Russian. This skill runs on English only. Aborting.`

**Step 3. Walk text nodes.**

For each text node inside a semantic text element (`<h1>`-`<h6>`, `<p>`, `<li>`, `<blockquote>`, `<figcaption>`, `<button>`, `<a>` if the anchor's text is a full phrase, `<label>`):

1. Tokenize into words + whitespace runs.
2. **Rule 1 pass.** Scan word-by-word. If word W is in the short-word list AND the following whitespace is a regular space AND the next word W+1 exists — replace the space with `&nbsp;`.
3. **Rule 2 pass.** Scan for standalone `-`, `–`, `—` surrounded by spaces. Replace the space **before** the dash with `&nbsp;`.
4. **Rule 3 pass.** Take the last two words of the text node. Ensure they are joined by `&nbsp;`, not a regular space.

**Step 4. Skip zones.**

Do NOT rewrite text inside:
- `<code>`, `<pre>`, `<kbd>`, `<samp>`, `<var>` — verbatim by contract.
- `<script>`, `<style>` — not text content.
- Any element with `class="no-typo"` — user escape hatch.
- Attributes (`alt=`, `title=`, `placeholder=`, `aria-label=`) — these do not line-wrap in visible layout in the same way.

**Step 5. Idempotency check.**

Before writing, diff the file. Existing `&nbsp;` from prior passes must not be duplicated (`a&nbsp;&nbsp;the` — bug). Collapse `&nbsp;{2,}` to a single `&nbsp;`.

**Step 6. Save + report.**

Save the file. Print a compact report:

```
typography pass — site/index.html
  ties inserted:        47
  dashes rewritten:      3
  orphans prevented:    12
  skipped (code/pre):    5 nodes
  no-typo opt-outs:      1 node
```

If run inside `/build`, no report — silent success. If run standalone, always report.

## Escape hatch

`class="no-typo"` on any element skips it entirely. Use for stylized headings where the designer wants specific manual breaks (e.g. `<h1 class="no-typo">Ship<br>fast.</h1>`).

## Rules of behavior

- **English only.** Do not attempt to guess other languages' rules.
- **Rewrite text nodes only.** Never touch attributes, script, style, or verbatim elements.
- **Idempotent.** Running twice produces the same output as running once.
- **No visual changes beyond typography.** Never move elements, never add wrappers, never touch CSS.

## What NOT to do

- Do not attempt to detect actual rendered line breaks (would require a headless browser; too expensive per pass). Use the word-level heuristics defined above.
- Do not modify the short-word list per project. It's the canonical English list. If the user wants a variant, they can override in a project-local `typography-overrides.md` (not currently supported — flag as an enhancement request).
- Do not run on non-English copy. Refuse.

## Next

- `/audit` — will grep for violations (hanging words, unfixed dashes) as part of category A.
- `/build` — calls this automatically after each section HTML is written.

---
name: anti-slop
description: >-
  Strip AI slop from written artifacts: KB documents, analysis, synthesis,
  research notes, technical docs, PR descriptions. Enforces structural writing
  rules and blocks known slop patterns. Invoke before writing any non-trivial
  prose artifact. Not for chat responses (caveman mode covers those).
metadata:
  version: "0.1.0"
---

# Anti-Slop Writing Rules

Apply before writing any KB document, synthesis, analysis, report, or technical
documentation. These rules govern written artifacts, not chat.

## Structural rules

**Start with content.** First sentence delivers the fact, claim, or decision.
No "In this document we will explore...", no "This analysis covers...", no
"It is worth noting that...".

**No concluding recap.** Final paragraph must add new information or be absent.
Never restate what was just written.

**Active voice.** "The algorithm reduces latency" not "Latency is reduced by
the algorithm."

**One idea per sentence.** Split compound sentences. Short is readable; long
is a symptom.

**Every word earns its place.** Read the draft. Delete any sentence that could
be removed without losing information.

## Slop patterns — detect and cut

### Confidence theater

Hedging on things that are simply true or false.

- Wrong: "This approach may potentially reduce overhead in certain scenarios."
- Right: "This approach reduces overhead when the input is sorted."

Fix: state the fact directly. If genuinely uncertain, name the condition
(`when X`, `if Y`, `assuming Z`) — do not hedge with vague qualifiers.

### False enumeration

Turning a 2-item answer into a 5-bullet list for appearance of thoroughness.

- Wrong: five bullets when three are filler restating the same point
- Right: list only when items are genuinely parallel and enumeration adds
  scannability. Prose is often clearer for 2–3 items.

Fix: ask "would this be clearer as one sentence?" If yes, write one sentence.

### Balance theater

Adding a counterpoint to seem fair when one position is correct.

- Wrong: "While approach A has merits, approach B also has its advantages..."
  (when A is clearly better for the stated goal)
- Right: state the correct position. If a real tradeoff exists, name it
  specifically with the exact condition under which it matters.

Fix: only acknowledge opposing positions when they apply to the concrete
situation. Generic balance is noise.

### Fake precision

Claiming authority without a traceable source.

- Wrong: "Studies show...", "Many experts agree...", "Research indicates..."
- Right: name the source or drop the claim. Use `[DIRECT]` / `[INFERRED]` /
  `[SPECULATIVE]` markers from `kb-conventions` for KB documents.

## Banned words

Cut on sight: `delve`, `leverage`, `utilize`, `robust`, `seamlessly`,
`tapestry`, `testament`, `spearhead`, `in conclusion`, `furthermore`,
`moreover`, `it's worth noting`, `it is important to note`, `please note`,
`rapidly evolving`, `it's important to remember`.

## Formatting rules

**No `---` horizontal rules.** Never use `---` as a section separator in
documents or responses. Frontmatter delimiters only.

**Headers earn their place.** Use H2/H3 only when the section is long enough
to warrant navigation. One-paragraph sections need prose, not a header.

**No 3-level bullet nesting.** If bullets nest 3 deep, collapse to prose or
restructure. Deep nesting signals the content isn't actually parallel.

**Bold means emphasis, not decoration.** Bold one or two genuinely critical
terms per document. Bolding every other phrase means nothing is emphasized.

**No `code ticks` on non-code.** Ticks for commands, identifiers, file paths,
values — not for concepts or invented terms that sound more technical in ticks.

**Tables require comparison value.** A table is justified when the reader
needs to scan across columns (comparison, lookup). Three items with a label
and description are a list, not a table.

**No padding whitespace.** Blank line between paragraphs — yes. Blank line
between every sentence or bullet — no. Whitespace structures; it does not
signal thoroughness.

**No concept inflation.** "the pipeline", "the architecture", "the system" —
lowercase unless a proper name. Unnecessary capitalization implies official
status that doesn't exist.

## Code artifact rules

**No restate comments.** Comment only the why — hidden constraint, non-obvious
invariant, workaround for a specific bug. Never describe what the code does.

**No single-caller abstractions.** No interface, wrapper, or helper with one
caller unless re-use is certain.

**No TODO placeholders** unless explicitly requested.

**Slop audit before submitting:**
- Does any dependency exist only to replace a native 5-line solution?
- Is any abstraction layer present that the caller never benefits from?
- Are there any "just in case" parameters or flags not used by existing callers?

## Self-audit checklist

Run before finalizing any written artifact:

- [ ] First sentence delivers content, no intro
- [ ] Last paragraph adds new information, not recap
- [ ] Every list has genuinely parallel, enumerable items
- [ ] Every hedge names a concrete condition
- [ ] Every authority claim has a traceable source
- [ ] No banned words present
- [ ] Active voice throughout
- [ ] No `---` separators outside frontmatter
- [ ] No headers on single-paragraph sections
- [ ] No bold used decoratively
- [ ] No tables where a list or sentence suffices
- [ ] No concept inflation (unnecessary capitalization)

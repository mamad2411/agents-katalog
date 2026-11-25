---
name: prose-style
description: Foundational prose style for every word written in this project.
  Use whenever drafting or editing ANY prose, including documentation, README
  files, code comments, PR descriptions, commit messages, JIRA tickets, design
  notes, Slack messages, and chat replies. This skill is the source of truth
  for voice and style; other project skills should reference and defer to it.
  Enforces British English, smart-brevity structure, plain non-technical
  language, specificity over abstraction, current-state-only writing, no em
  dashes, and a defined ban list of AI writing tells. Triggers on any prose
  edit, even short ones.
---

# Prose style

The house style for every word that leaves this project. Apply to docs,
READMEs, code comments, PRs, commit messages, JIRA tickets, design notes,
Slack messages, and chat.

## The six rules

1. **British English, always.** Organise, behaviour, colour, centre, realise.
2. **Plain language.** Write so a non-technical reader gets it. Use the word
   you would say out loud.
3. **Smart brevity.** Lead with what. Then why it matters. Context in short
   bullets. One idea per sentence.
4. **Specific over abstract.** Name people, numbers, and things. No vague claims.
5. **Current state only.** Describe how things work now. Git holds the history.
6. **Active, present, declarative.** State facts. Do not hedge, narrate, or pose.

---

## Hard rules

Non-negotiable. No exceptions.

- **No em dashes (—).** Use commas, colons, parentheses, or a full stop.
- **No adverbs.** Cut `-ly` words and "really", "just", "literally",
  "genuinely", "honestly", "simply", "actually", "essentially", "basically".
  Full list in `references/banned-phrases.md`.
- **No hedges.** Cut "might", "could potentially", "seems to", "appears to",
  "I think", "perhaps", "arguably". Commit or say you do not know.
- **No throat-clearing openers.** Cut "Here's the thing", "Here's what...",
  "The truth is", "Let me be clear", "It turns out", "Look,", "So,".
- **No vague declaratives.** "The implications are significant" is empty.
  Name the implication.
- **No lazy extremes** doing vague work. "Three of five customers" beats
  "every customer".
- **No transitional language.** Cut "now", "currently", "still", "used to",
  "previously", "no longer", "as of", "formerly".
- **No corrective parentheticals.** Rewrite the sentence instead.
- **No buried subjects.** Avoid delayed-subject openers: "What makes
  this hard is...", "Why this matters is...", "How this works is...".
  Lead with the actual subject. A plain subordinate opener is fine:
  "When the cache expires, avatars go stale."
- **No false agency.** Inanimate things do not act. "The team fixed the
  bug" not "the complaint became a fix".

---

## Smart brevity

Default shape for any prose section longer than a sentence:

1. **What.** One short sentence stating the thing.
2. **Why it matters.** One short sentence on why the reader should care.
3. **Context.** Short bullets. One idea per bullet. Self-contained.

Not every section needs all three. A reference list, a code snippet, or a
one-line note can stand alone. The pattern is a default, not a template.

### Limits
- Sentences: short. Two clauses joined by "and" or "but" usually split.
- Bullets: one idea each. No semicolon-joined sub-clauses.
- Paragraphs: three sentences maximum. Use bullets above that.

---

## Specificity: where the punch comes from

Three swaps for every paragraph:

1. **Concrete nouns over abstractions.** "The auth team" beats "stakeholders".
   "The avatar resolver" beats "the system".
2. **Specific numbers over vague quantities.** "5x faster (3.2s to 0.6s)"
   beats "significantly faster". "Three reports per week" beats "often".
3. **Strong verbs.** "Routes" beats "is responsible for routing". "Decided"
   beats "made a decision".

Full guidance in `references/specificity.md`.

### The "so what" test
After each paragraph, ask: would the reader stop and say "so what?"
If yes, add the consequence or cut the paragraph.

---

## Documents over a paragraph

For anything over a paragraph, the document's shape matters as much as
the words.

- **Headlines, not topic headers.** "P99 latency dropped from 800ms to
  200ms" beats "Performance".
- **Lead with the answer.** Add a TL;DR for anything over ~300 words.
- **Inverted pyramid.** Key fact first. Background, if any, last.

Full guidance in `references/document-structure.md`.

---

## Current state only

- When a feature is removed, delete its mention. No tombstones.
- When updating, replace outdated content. Do not append clarifications.
- No dates, sprint IDs, or sweep names as inline context. A single ticket
  link is fine if it points to a still-relevant design doc.

---

## Code comments

Comments add information the code does not.

- Default: no comment. If the name says it, the comment is noise.
- One line if needed. Multi-line only for subtle rationale.
- Explain why the code is *shaped this way*, not why it was *added*.
- Delete stale comments instead of editing them in place.

---

## When to read which reference

| Need | Read |
| --- | --- |
| Check if a word or phrase is banned | `references/banned-phrases.md` |
| Check if a sentence structure is banned | `references/structures.md` |
| Find a plain-language swap (long word → short) | `references/plain-language.md` |
| Check American/British spelling | `references/british-english.md` |
| Make prose more specific or punchy | `references/specificity.md` |
| Structure a longer document | `references/document-structure.md` |
| See before/after pairs by context | `references/examples.md` |

Read references as needed, not by default. Each is a focused lookup.

---

## Decision shortcuts

- About to type "now" or "currently"? Delete it. Re-read the sentence.
- About to type an em dash? Use a comma, colon, or full stop.
- About to write "Here's what"? Cut to the point.
- About to write a paragraph? Try what + why + bullets first.
- About to type a `-ly` adverb? Delete it. Re-read the sentence.
- About to type "might", "seems to", "I think"? Commit or admit ignorance.
- About to write "What makes this hard is..."? Lead with the subject.
- About to write American spelling? Switch to British.
- About to use a long word? Try the short word.
- Making a vague claim ("important", "significant")? Name the specific thing.
- About to write "Not X, but Y"? Drop the negation. State Y.
- About to give an inanimate thing a human verb? Name the human.
- About to write a topic-style header ("Background")? Try a headline.
- Writing a doc over 300 words? Add a TL;DR.

---

## How other skills should use this

Other project skills should defer to this one for voice and style. They
should not restate these rules. They can extend with context-specific
rules: a `design-docs` skill might add a section template; a `changelog`
skill might add formatting conventions. The rules here remain the baseline.

When a project skill conflicts with this one, this skill wins on style.
The project skill wins on domain content.

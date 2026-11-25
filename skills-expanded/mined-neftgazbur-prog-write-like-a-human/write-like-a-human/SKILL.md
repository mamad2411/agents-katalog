---
name: write-like-a-human
description: Use when writing or editing prose that must read as human-written — encyclopedia articles, bios, blog posts, docs, essays, emails — or when asked to humanize, de-AI, naturalize, or audit a text for machine-writing tells. A rewrite-first skill for AI coding/writing agents a regex sweep plus 21 fix rules covering hype voice, hollow authority, rhythmic tics, bot residue, and format fingerprints.
---

# write-like-a-human

Machine prose has a voice. Everything matters enormously, sources vaguely agree, sentences march in threes, and every other clause is bolted on with an em dash. It reads smoothly and smells synthetic — and human editors (Wikipedia's volunteers maintain whole field guides on the subject) spot it within a paragraph.

This skill turns that knowledge into a rewriting pass for you, the agent. The pattern list flags candidates; meaning decides what actually changes.

## The workflow

1. Draft normally.
2. Run the search pattern below over the draft.
3. For each hit: does the phrase carry real information? Keep it. Is it filler in a stock shape? Rewrite it per the table.
4. Do a rhythm pass: sentence-length variety, concrete nouns, anything that survives its own deletion gets cut.
5. Check citations: every link resolves, identifiers are real, tracking parameters are gone.

## The search pattern

```regex
(?i)plays a (vital|key|crucial|pivotal|significant) role|stands as a (testament|reminder|symbol)|serves as a reminder|poignant|testament to|pivotal moment|underscores|highlights the importance|showcas|demonstrating|reflecting|nestled|breathtaking|vibrant|rich (cultural|artistic|historical) (heritage|tapestry|landscape)|in the heart of|hidden gem|boasts|charm|it('s| is) (important|worth|crucial) to note|worth noting|please note that|in conclusion|ultimately|to summarize|despite (these|its) (challenges|limitations)|looking ahead|the future of.{0,30}(looks|remains)|continues to (thrive|evolve|captivate)|not only.{0,40}but also|isn'?t just.{0,30}(it'?s|but)|according to (experts|industry (reports|analysts))|some (critics|argue)|widely regarded|as of my (last )?(knowledge|training)|I hope this helps|let me know if|utm_source=(chatgpt|openai)
```

## The 21 tells

### Hype voice — the promotion reflex

| # | Tell | Why it shows | Fix |
|---|------|--------------|-----|
| 1 | Inflated stakes: "plays a pivotal role", "stands as a testament to", "cannot be overstated" | Models raise the importance of everything, down to beetle species and small towns | State who did what, when, and how it is known. Small fact, small sentence |
| 2 | Adjective wallpaper: "vibrant", "breathtaking", "nestled", "hidden gem", "rich cultural tapestry", "in the heart of" | Promotional register leaks into neutral text | Neutral descriptor plus concrete noun. "Nestled in the heart of X" → "in X", or "64 km north of Y" |
| 3 | Facts that act: "the decision underscores…", "the location highlights…", "this demonstrates…" | Inanimate things given animate agency | Hand the action to a person or body — "the curator noted" — or drop the commentary clause |
| 4 | Insight theater: "It's important to note that…", "Worth noting:" | A frame that adds authority to plain statements | Delete the frame, keep the sentence |

### Hollow authority

| # | Tell | Why it shows | Fix |
|---|------|--------------|-----|
| 5 | Notability by name-drop: "featured in Forbes, Bloomberg, and TechCrunch" | Outlets listed instead of what they reported | One claim, one source, one fact |
| 6 | Vague consensus: "experts say", "industry reports suggest", "some critics argue" | Opinions pinned to an anonymous crowd, often with one weak citation or none | Name the source, or cut the claim |
| 7 | Cutoff disclaimers: "as of my last training data", "information may be limited" | The model's self-talk about its own limits lands in the document | Say what is known with a dated source; the document never discusses the author's memory |
| 8 | Chat residue: "Certainly! Here's…", "Let me know if you'd like…", "I hope this helps" | Assistant boilerplate pasted with the deliverable | The document contains only document sentences |

### Rhythmic tics

| # | Tell | Why it shows | Fix |
|---|------|--------------|-----|
| 9 | The rule of three: triads of adjectives or clauses ("clear, concise, and compelling") | Statistically averaged rhythm that pretends to be thoroughness | Pick the strongest. One is usually enough |
| 10 | The not-only pivot: "not just X, but Y", "isn't merely X — it's Y" | A manufactured contrast that signals "insight" | Assert both halves plainly, or drop the lesser half |
| 11 | Merism sprawl: "from X to Y" across unrelated extremes ("from the Big Bang to modern astronomy") | Grand range with no scale between the poles | List the items, or keep one |
| 12 | Synonym carousel: one person rotates through "the entrepreneur", "the visionary", "the founder" | Repetition-avoidance training; humans just repeat the name | Repeat the name. A precise synonym only when it adds information |
| 13 | Participle pileups: chains of "-ing" clauses, often dangling ("Using this approach, results improve") | The model never hears that the sentence lost its subject | Short sentences; each modifier attaches to its actual actor |
| 14 | Em-dash addiction: one every sentence or two, standing in for commas, colons, parentheses | Borrowed "authorial" cadence | Reserve it for genuine breaks; prefer commas, colons, parentheses |
| 15 | Conclusion gravity: "In conclusion…", "Ultimately…", a closing section that restates the piece | Chat-answer habits carried into documents | End on facts. No summary of what the reader just read |

### Structure reflexes

| # | Tell | Why it shows | Fix |
|---|------|--------------|-----|
| 16 | The "challenges and future prospects" coda: "Despite these challenges, X continues to thrive…" | A fixed positive verdict bolted onto any topic | Problems get specifics and sources; no prophecy unless someone credible made one |
| 17 | Title-as-thesis: the page title restated as a definition ("'List of songs about X' is a curated collection…") | The model treats the headline as a term needing a gloss | Open by the genre's convention — a list opens with its first entry, a bio with the person |
| 18 | The balanced-blur ending: a vague upbeat verdict on any subject | Trained-on-PR closure | Stop where the sources stop |

### Format fingerprints

| # | Tell | Why it shows | Fix |
|---|------|--------------|-----|
| 19 | Title Case headings: "Early Life and Education" everywhere | English chatbot defaults | Sentence case: "Early life and education" |
| 20 | Bold spam and labeled lists: every term bolded, "**Term:** explanation" bullets, emoji or hand-typed numbers | Habits from slide decks and "key takeaways" | Bold only for wayfinding; plain flat lists |
| 21 | Markdown pasted into wiki markup: `**`, `#`, `*` where `'''`, `==`, `*` belong; broken hybrid syntax — plus `utm_source=chatgpt.com` / `utm_source=openai` on citation URLs, and links that 404 in a document written yesterday | The model's native format bleeding through; tracking parameters and dead links often mark fabricated references | Write in the target format's markup; strip tracking parameters; open every cited link before shipping |

## The positive pass

Stripping tells leaves a vacuum. Fill it with what human prose actually does:

- **Concrete over general.** Names, numbers, dates, actions. Generalize only when the source generalizes.
- **Uneven rhythm.** Short sentence beside long. Paragraphs of any honest length.
- **Attribution with a face.** "According to the 2019 audit" beats "experts agree".
- **Restraint.** If the fact is small, say it small.
- **The deletion test.** Cut every phrase that survives its own removal.

## Don't overcorrect

- A stock phrase carrying real information can stay. The pattern flags candidates; meaning decides.
- The destination is a specific, verifiable, unevenly-rhythmed text. Flat bureaucratic gray is just another uniform.
- Detector tools misfire in both directions. A human read plus link-checking beats a score.

---

Adapted from [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) by Wikipedia contributors (CC BY-SA 4.0, [license text](https://creativecommons.org/licenses/by-sa/4.0/legalcode)), rewritten, reorganized, and extended for general-purpose prose. The underlying material remains © Wikipedia contributors, CC BY-SA 4.0; this adaptation is distributed under the same license. Not affiliated with the Wikimedia Foundation.

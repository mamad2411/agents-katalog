---
name: writing-hooks
description: Craft invisible openers, False-Summit retention bridges, 90/10 Socratic generation gaps, and Peak-End closers in any language. Sub-skill: load only when routed from the hook-everything entry skill, not for general writing or editing.
---
# Writing Hooks & Long-Form Retention Architecture

Most writing advice focuses only on the first sentence. In practice, reader drop-off often spikes around **Paragraph 3** (working heuristic, verify with your own data) when the opener's tension evaporates into background filler, and at **the first H2 heading** when the article turns into a dry textbook list.

Use this guide to engineer continuous, invisible pull from the first word to the final period.

---

## Phase 1: Openers That Bypass the Reader's Shield

Never start with a macro-generalization ("Since the dawn of...", "In modern software development..."). Select an opener chord (`skills/hook-compounding`) that pairs immediate tension with a **Trust Damper**:

1. **In-Medias-Res + Pratfall (`M2` + `M20`)** drops into a specific moment where a capable narrator hit an unexpected wall:
   - *"I deleted the production database at 4:55 PM on a Friday. Nobody noticed until Monday morning, which was somehow worse."*
2. **Asymmetric Anomaly + Boundary (`M4` + `M15`)** pairs two verifiable facts that violate expectations, and states who cares:
   - *"Our slowest API endpoint had zero database queries, twelve lines of Python, and cost us $4,100 a month in idle worker timeouts."*
3. **Inoculated Counter-Thesis (`M21` + `M3`)** validates the reader's current default belief, then shows the exact measurement where it breaks:
   - *"Everyone tells you to index foreign keys first. On tables with fewer than 50 distinct values, that index makes Postgres 3x slower."*

---

## Phase 2: Surviving Paragraph 3 (The "No-Backstory" Bridge)

Writers often ruin a strong opener by retreating into 300 words of history (`"Before I explain how we fixed the database, let's review the history of our company's architecture..."`). That kills momentum immediately.

- **The 150-Word First Payoff Rule** delivers one concrete, usable insight or forensic clue within the first 150 words before giving any background context.
- **Flashback by Necessity Only** introduces background details *only* at the exact sentence where the reader needs that detail to understand the next action.

---

## Phase 3: Mid-Piece Retention Mechanics (Keeping Readers Through 2,000+ Words)

### 1. The "False Summit" Turn (Mid-Article Re-Hook)
Around the 40% mark of an article or case study, readers think they have figured out the whole answer and prepare to close the tab.
- **Execution** Solve the initial problem cleanly at the 40% mark, then immediately reveal the **Second-Order Consequence** that the obvious fix created.
- *Example* - `"Adding the local LRU cache dropped median latency from 310ms to 12ms. We celebrated on Thursday. On Friday morning, our memory usage hit 98% because every user's session object held a reference to the entire tenant graph."`

### 2. The 90/10 Socratic Generation Gap (Slamecka & Graf 1978)
Instead of stating your thesis and then listing 3 supporting bullets (which puts the reader into passive skimming mode), **invert the order**:
- Lay out Clue 1 and Clue 2 side-by-side so the reader's brain connects the dot half a second before your next sentence confirms it (`M11`). When readers generate the conclusion themselves, they experience a rush of personal insight and stay locked in.

### 3. Assertion-Tension Subheads & Caption Hooks
- **Ban Textbook Subheads** Never use one-word labels (`Background`, `Implementation`, `Results`, `Conclusion`). Write every H2/H3 as a declarative assertion or an unresolved tension (`Why the 30-second timeout made the outage twice as long`).
- **Hook Skimmers in Captions (`M27`)** Write every code-block comment, table header, and image caption as a self-contained insight so a skimmer who scrolls down to look at a diagram gets pulled back into the prose.

---

## Phase 4: Pacing Architecture by Length

| Piece Length | Hook & Payoff Rhythm | Structural Rule |
|---|---|---|
| **Short-Form (`< 300 words`)** *(Emails, Social Posts, Release Notes)* | **Single Chord**: 1 sharp opener (`< 20 words`) -> 1 concrete mechanism/example -> 1 immediate takeaway or micro-action. | Zero section headings, zero throat-clearing, zero summary closer. |
| **Medium-Form (`300 - 1,200 words`)** *(Blog Posts, Case Studies, Memos)* | **3-Chord Arc**: Opener Chord -> First Payoff at word 150 -> False-Summit Turn at word 500 -> Peak-End Closer. | Include at least 1 visual eye-brake (table, diff, or numbered forensic trace) around the midpoint. |
| **Long-Form (`1,200 - 4,000+ words`)** *(Deep Dives, Whitepapers, Guides)* | **Rotated Chord Sequence**: Rotate `Chord 3 -> Chord 5 -> Chord 1 -> Chord 4` across major sections. Close every open loop within 250 words before opening the next. | Audit in 300-word blocks (`anti-slop` Rule 71) so the prose never degrades into repetitive LLM filler in the second half. |

---

## Phase 5: Peak-End Closers (Fredrickson & Kahneman 1993)

Never end with a summary paragraph that starts with `"In conclusion"` or repeats what the reader just read. End at the highest point of utility:
- **The 60-Second Diagnostic Closer** gives the reader one exact command, search query, or mental check they can run in the next 60 seconds to see if they have the same issue.
- **The Resonant Artifact Closer** ends on a concrete physical detail that encapsulates the lesson (`"I still keep a yellow sticky note taped to my monitor bezel: check the hostname before you hit enter."`).

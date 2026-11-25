---
name: technical-tutorial
description: "Draft technical tutorials that teach through code. Combines SPIN storytelling arc with DO→NOTICE→CODE→NAME pedagogy loop, prerequisite tracking, beat/artifact sync, exercise design, Bragi prose gate, and voice calibration. For tutorials where the reader builds a working thing, not just reads about one."
license: MIT
metadata:
  openclaw:
    emoji: "\U0001F9EA"
---

# Technical Tutorial

Draft technical tutorials where the reader builds a working thing. Articles argue a thesis; tutorials build a capability. This skill enforces both a narrative arc (SPIN) and a cognitive arc (DO→NOTICE→CODE→NAME) so the reader feels the problem before they solve it and names the concept only after they've built it.

Inherits: Bragi prose gate, voice calibration, SPIN arc, visual injection, beat mapping from `article-draft`. Inherits: DO→NOTICE→CODE→NAME loop, prerequisite chain, Starting State Rule from aegir's `lesson-generator` and `outline-writer`.

---

## Step 0: Inputs

Before drafting, you need:

1. **Topic brief** — what the reader will be able to DO after completing this tutorial (not what they'll "understand"; what they'll build, run, or use)
2. **Prerequisite inventory** — what the reader knows coming in (languages, tools, concepts they already have)
3. **Companion artifact type** — notebook / repo / CLI tool / none. Determines how code cells are structured.
4. **Voice target** — which register(s) to blend (see Voice Calibration below; default ratio differs from articles)
5. **War story inventory** — real incidents, CVEs, production failures, named people. Not hypotheticals.

If any of these are missing, do an elicitation pass before drafting. Do not draft from a topic name alone.

---

## Phase 1: Learning Arc

The tutorial has two parallel arcs. SPIN provides the emotional arc (tension → resolution). DO→NOTICE→CODE→NAME provides the cognitive arc (experience → understanding). They run simultaneously.

### The Dual Arc

| SPIN Phase | Cognitive Phase | What Happens |
|------------|----------------|--------------|
| **Situation** | DO, NOTICE | Reader encounters the thing (war story, demo, broken output). Reader observes a pattern ("wait, the lengths are different"). No labels yet. |
| **Problem** | NOTICE, CODE | Reader's observation sharpens into a specific pain. Reader starts building something to investigate. |
| **Implication** | CODE | Reader's code reveals the scope of the problem. Each cell makes the situation worse. This is where alarm lives. |
| **Need-Payoff** | CODE, NAME | Reader builds the solution. Concepts get their proper names only after the reader has already built the thing that implements them. |

### DO→NOTICE→CODE→NAME (mandatory per concept)

Every concept in the tutorial, at every scale, follows this loop:

| Stage | What Happens | Modality |
|-------|-------------|----------|
| **DO** | Experience it. See it, hear it, run it. No labels yet. | Sensory/interactive |
| **NOTICE** | Guided observation. "What did you notice?" Pattern recognition prompts. | Reflective |
| **CODE** | Build, modify, break. Change parameters, swap implementations. | Tactile/code |
| **NAME** | Formalize. Give it its proper name. Connect to theory. Define it. | Symbolic |

Rules:
- **NAME always comes last.** The reader builds the concept before they learn its name. "A Beta distribution" is never introduced before the reader has seen the shape, played with the parameters, and intuited what it does.
- **DO is never skipped.** Every concept starts with experience, not definition.
- **Each stage projects into at least 2 modalities** (visual + code, code + prose, etc.)

### Concept Primitives

A concept primitive is the smallest unit where confusion is possible. Decompose every concept into primitives. Each primitive gets its own DO→NOTICE→CODE→NAME loop.

- Good primitive: "E→F has no black key between them" (one learnable fact)
- Bad primitive: "The W-W-H-W-W-W-H pattern" (compound; decompose into W, H, why that sequence)

Test: "Could someone be confused about this?" If yes, it's not a primitive yet. Keep decomposing.

---

## Phase 2: Prerequisite Chain

Every section declares three things:

1. **What the reader has built** — functions, classes, mental models, earned jargon from prior sections
2. **What this section adds** — the new capability, concept, or artifact
3. **What the reader can do after** — the concrete thing they couldn't do before this section

### The Starting State Rule

The first section begins by establishing what the reader walks in with (from the prerequisite inventory in Step 0). Every subsequent section begins by using something the reader built in a prior section.

Pattern: `their_function(args) → result → "but notice [gap]"`

Never recap. Use. Run their code. Then reveal the gap that motivates the next concept.

### No Forward References

If a section references a concept the reader hasn't built yet, restructure. Discovery order beats logical order. If the reader needs B to understand A, teach B first. If A and B are mutually dependent, break the cycle by teaching a simplified version of one.

### Jargon-Earning Order

Track every technical term:

```markdown
| Term | Introduced | Earned By |
|------|------------|-----------|
| codepoint | Section 2 | comparing len() of two identical-looking strings |
| homoglyph | Section 3 | seeing Cyrillic с next to Latin c in hex |
| skeleton normalization | Section 5 | building normalize_for_scan() and seeing regex matches recover |
```

No term is used before it's earned. If you need a term early, restructure so the earning happens first.

---

## Phase 3: Beat Map + Artifact Sync

Every section has an emotional beat (from article-draft) AND a companion artifact (code cell, function, output).

### Beat Map

Map every section to an emotional beat. Adjacent sections cannot have the same beat.

**Building tension (first half, SPIN Situation→Problem→Implication):**
- Curiosity ("huh, what's this about")
- Unease ("wait, something's off")
- Alarm ("oh shit, it's worse than I thought")

**The Turn (midpoint, SPIN Implication→Need-Payoff transition):**
- Agency ("I can do something about this")

**Building competence (second half, SPIN Need-Payoff):**
- Competence ("I built a thing and it works")
- Mastery ("I can break my own thing and fix it")
- Resolve ("I know what to do next")

**Closing:**
- Resolution (callback to the opening, now transformed by what the reader built)

### Artifact Sync

Every beat maps to a companion artifact. The artifact IS the beat; it's not decoration.

```
Beat 1: CURIOSITY  → Cell: two identical-looking strings, different lengths
Beat 2: UNEASE     → Cell: inspect_string() reveals hidden codepoints
Beat 3: ALARM      → Cell: real CVE reproduced in 4 lines
Beat 4: AGENCY     → Cell: reader builds encoder
Beat 5: COMPETENCE → Cell: reader builds detector
Beat 6: MASTERY    → Cell: reader tries to defeat their own detector
Beat 7: RESOLVE    → Cell: normalization neutralizes everything
```

Rules:
- **Adjacent beats must differ emotionally** (inherited from article-draft)
- **Adjacent cells must build on each other** (inherited from aegir)
- **Every beat has a cell.** No prose-only sections longer than two paragraphs without a runnable artifact.
- **Every cell has a beat.** No code blocks without narrative context. If you can't name the emotional beat, the cell is filler.

---

## Phase 4: Visual Injection Protocol

Three layers inherited from article-draft, plus a fourth for tutorials.

### Layer 1: Data visuals (charts, screenshots)
- Place AFTER the claim they support, not before
- Caption must state what the reader should see, not just label the axes
- Max 2 data visuals per section

### Layer 2: Architecture diagrams (SVG)
- One hero diagram per tutorial (the "big picture")
- Place at the SPIN transition (end of Situation or start of Need-Payoff)
- Dark theme. Minimal color palette (2-3 colors max). No gradients unless they encode data.

### Layer 3: Interactive elements
- Max 1-2 per tutorial. Use where static fails.
- Best for: parameter exploration, distributions updating in real time, before/after toggles
- Every interactive MUST have a static fallback

### Layer 4: Expected output (tutorial-specific)
- The reader needs to see what correct output looks like BEFORE they run their own code
- For every code cell where the output matters, show the expected result
- Format: screenshot, inline code block, or assertion that prints a success message
- This is the tutorial equivalent of "data visuals": it builds confidence that the reader is on track

### Injection checklist
For each visual, answer:
1. What concept does this support?
2. What should the reader notice first?
3. What's the caption? (Complete sentence, not a label)
4. Does removing this visual weaken understanding? (If no, cut it.)

---

## Phase 5: Bragi Prose Gate

These 28 rules are enforced DURING drafting, not on review. Tutorials don't get a prose pass because they're "educational." Internalize them.

### Hard bans (zero tolerance)
1. **No em dashes (—).** Use colons, semicolons, commas, parentheses, or separate sentences.
2. **No AI vocabulary blocklist words.** Additionally, align with, bolstered, crucial, delve, emphasizing, enduring, enhance, fostering, garner, highlight (as verb), interplay, intricate/intricacies, key (as adjective), landscape (abstract), load-bearing, meticulous/meticulously, pivotal, showcase, tapestry (abstract), testament, underscore (as verb), valuable, vibrant.
3. **No performative honesty.** "Being honest:", "To be frank:", "The truth is:"
4. **No self-referential pivots.** "This is where things get interesting"
5. **No inflated significance framing.** "Marking a pivotal moment", "setting the stage for"

### Structural bans
6. **No hedging then inflating.** "Though limited, it contributes to the broader..."
7. **No punchy fragment marketing copy.** "One encoder. Every format."
8. **No tricolon/pentad enumerations for rhythm.** Escalation test: each item must add a NEW dimension or sharpen the existing one.
9. **No rhythmic parallel construction closers.** End with a concrete claim.
10. **No challenges-and-future-prospects formula.** Name the problems. Skip the sandwich.

### Word-level bans
11. **No elegant variation.** Same thing, same word.
12. **No copula avoidance.** "Serves as", "stands as" → just say "is."
13. **No dismissive 'with' framing.** Don't reduce complex features to prepositional afterthoughts.
14. **No vague attribution.** Name the source or cut the claim.
15. **No false ranges.** "From X to Y" only with an actual spectrum.

### Analysis bans
16. **No superficial participle analysis.** Don't append gerunds to stated facts.
17. **No hedging with 'not' lists.** Say what the thing IS.
18. **No colon-into-bold-statement.** Formatting is not argumentation.
19. **No promotional puffery.** Cut every adjective that doesn't distinguish.
20. **No notability assertion sections.** Show the work.

### Rhythm and structure bans
21. **No blunt fragment negation.** "A review tool. Not a generator." → use a comma or restructure.
22. **No wall-of-text paragraphs.** One thought per visual unit.
23. **No full-clause linking.** Links highlight the operative noun/concept.
24. **No mirrored affirmation pairs.** "X is real. So is Y." Cut the mirror.

### Cross-model LLM signatures
25. **No "not just X, but also Y" constructions.**
26. **No restating the obvious.** Trust the reader.
27. **No bare conjunctions as standalone paragraphs.** "But." alone is an LLM rhythm trick.
28. **No emotional cliche templates.** "A mix of [emotion] and [emotion]." Replace with specific, embodied detail.
29. **No staccato data-point mic drops.** Fragment lists of stats as closers are the most recognizable GPT-4o signature in technical writing. Data belongs in the argument, not arranged as a curtain call.

### Pelekification (do MORE of these)

- **Break line after standalone statements that land.** The break IS the emphasis.
- **Colon extension for earned continuation.** "The idea was right: I use it every day."
- **Ellipsis for hesitation and self-correction.** "was...Experimental."
- **Ellipsis as sentence binder.** Two sentences joined by `...` when the second deflates or undercuts the first.
- **Semicolons in extended lists.** When items are closer to clauses than words.
- **Semantic punctuation.** Period→colon when explaining. Period→semicolon when paralleling. Period→ellipsis+"But" when contradicting with hesitation.
- **Bold for argumentative weight, not decoration.** Bold the words that carry the claim.
- **Annotations as cross-references.** `<Annotation>` connects ideas across articles.
- **Prosodic awareness.** Alliteration and sibilance are good. Sound matters.
- **Decorative sentences earn their placement.** Needs buildup. After the argument, not before.
- **Section headers at argument pivots.** Not topic boundaries. Where the argument turns.
- **Typographical weight escalation at pivots.** line break < italic < blockquote < bold.

---

## Phase 6: Voice Calibration

### Three registers to blend

**Register A: Frustrated Engineer (Mickens)**
- Escalating specificity. Start general, narrow to a specific log line, narrow to a specific token.
- Real terror underneath the laughs.
- Hyperbolic analogy that clarifies.
- USE FOR: war stories, "this is bad" revelations, the moment the reader sees the scope of the problem

**Register B: Self-Deprecating Narrator (Sedaris)**
- Be harder on yourself than anyone else in the story.
- Mundane details elevated to absurdity.
- Weight at the end.
- USE FOR: "I thought I understood this, then...", personal anecdotes, the opening hook

**Register C: Respectful Tour Guide (Paul Ford)**
- Direct address that dignifies the reader. Never talk down.
- Sustained genuine curiosity about the subject matter.
- Humor in the juxtaposition: rigorous material described by someone who finds parts of it absurd.
- USE FOR: concept explanations, code walkthroughs, "here's how it works" sections, exercise framing

### Tutorial voice rules
- **Default ratio: 25% Register A, 25% Register B, 50% Register C.** Tutorials weight toward tour guide because you're teaching, not arguing. Articles default to 40/30/30.
- Technical deep dives within tutorials: bias toward C+A (tour guide + frustrated specificity)
- War story openings: bias toward A+B (Mickens + Sedaris)
- Exercise framing: pure C (Paul Ford)
- NEVER use all three in the same paragraph. One register per paragraph, blend across sections.

---

## Phase 7: Exercise Design

Every major section (each SPIN phase) ends with at least one exercise. Exercises follow a three-tier pattern.

### Exercise tiers

**Verify** — confirms understanding. The reader runs something on known input and checks output.
- "Run `inspect_string()` on this tool description. How many invisible characters does it find?"
- Expected output provided. The reader compares. If it matches, they understood.

**Extend** — builds capability. The reader modifies what they built to handle a new case.
- "Modify `encode_zwc()` to use tag characters instead of zero-width spaces."
- Starter code provided. Solution in a collapsed cell. The reader attempts before checking.

**Break** — builds adversarial intuition. The reader tries to defeat their own system.
- "Write a string that passes your `detect_stego()` function but still contains a hidden payload."
- No expected output. The reader discovers gaps in their own detector. This is where the deepest learning happens.

### Exercise rules
- **At least one exercise per SPIN phase.** No phase without hands-on work.
- **The final exercise is always "use this on your own real thing."** Not a toy example. The reader runs their detector on their own MCP tool descriptions, their own SKILL.md files, their own npm packages. They leave with a result that matters to them.
- **Every exercise has success criteria.** What does "done" look like? An assertion that passes, a specific output, a comparison to expected.
- **Build-a-toy exercises** (from aegir): at least one per tutorial. Interactive, dopamine payoff, combines multiple concepts from the tutorial into one playable thing.
- **Exercises build on each other.** Exercise 3 uses the function the reader built in Exercise 2. No standalone throwaway exercises.

### Exercise format
```markdown
### Exercise: [Title]

**Tier**: Verify / Extend / Break
**Uses**: [functions/concepts from prior sections]
**Adds**: [new capability after completion]

[Task description — 2-3 sentences max]

```python
# --- YOUR CODE BELOW ---

```

<details>
<summary>Solution</summary>

```python
# Solution code
```

</details>

**Success**: [what "done" looks like — assertion, output, comparison]
```

---

## Phase 8: Draft Execution

With all the above internalized, draft in this order:

1. **Write the opening war story.** This anchors everything. A specific incident, a specific failure, a specific feeling. Register B (Sedaris). The reader encounters the problem (DO) before they know what it is.
2. **Establish the prerequisite state.** What does the reader have? What can they run right now? This is one paragraph, not a section.
3. **Write the SPIN transitions.** The questions that move the reader from Situation → Problem → Implication → Need-Payoff. Each transition is a natural question the reader is asking.
4. **Fill each section following dual-arc alignment.** SPIN phase determines the emotional beat. DO→NOTICE→CODE→NAME determines the cognitive sequence. Every section has prose AND a companion artifact.
5. **Write exercises at each SPIN boundary.** Verify after Situation (did they observe correctly?). Extend after Problem (can they build the tool?). Break after Implication (can they defeat their own tool?). Build-a-toy in Need-Payoff (combine everything).
6. **Write the capstone exercise.** "Use this on your own real thing." No toy data. Their data. Their tools. Their risk.
7. **Write the circular close.** Callback to the opening war story. The same situation, now transformed by what the reader built. They can detect what they couldn't see before.
8. **Run Bragi gate.** Search the draft for every banned pattern. Fix them. Non-negotiable.
9. **Run prerequisite audit.** Verify no forward references. Every concept built before used. Every term earned before named.
10. **Read aloud test.** Does any sentence make you cringe? Cut it. Does any paragraph feel like filler? Cut it. Does any exercise feel like busywork? Cut it or upgrade it.

---

## Review Mode

When reviewing an existing tutorial draft (not drafting from scratch), run these passes in order. Output a structured review report.

### Pass 1: Bragi Scan

Search the entire draft for violations of the 29 prose rules. For each violation:

```
[BRAGI] Line ~N: "<offending text>"
  Rule: <rule name>
  Fix: <specific rewrite>
```

### Pass 2: SPIN + Cognitive Arc Audit

Identify where each SPIN phase lives and verify DO→NOTICE→CODE→NAME alignment:

```
[SPIN] Situation: lines N-M (or MISSING)
  DO→NOTICE→CODE→NAME: [which stages present]
[SPIN] Problem: lines N-M (or MISSING)
  DO→NOTICE→CODE→NAME: [which stages present]
[SPIN] Implication: lines N-M (or MISSING)
  DO→NOTICE→CODE→NAME: [which stages present]
[SPIN] Need-Payoff: lines N-M (or MISSING)
  DO→NOTICE→CODE→NAME: [which stages present]
[SPIN] Solution first appears: line N — BEFORE/AFTER Implication
```

Flag any concept that skips DO (starts with definition) or skips NAME (never formalized).

### Pass 3: Prerequisite Audit

Verify the prerequisite chain is intact:

```
[PREREQ] Section N uses "<term/function>" — first built in Section M: OK/VIOLATION
[PREREQ] Forward reference: Section N uses "<concept>" before it's introduced in Section M
[PREREQ] Jargon violation: "<term>" used in Section N, earned in Section M (N < M)
```

Zero forward references. Zero jargon violations. If any exist, the structure must be reordered.

### Pass 4: Artifact Sync

Verify every beat has a companion artifact and every artifact has a beat:

```
[SYNC] Beat N (CURIOSITY): Cell present — YES/NO
  Cell does: <what it runs/shows>
  Beat alignment: <does the cell's output create the right emotion?>
[SYNC] Orphan cell: Cell at line N has no corresponding beat
[SYNC] Prose desert: Lines N-M (>2 paragraphs) with no runnable artifact
```

### Pass 5: Exercise Coverage

```
[EXERCISE] SPIN Situation: Verify exercise — YES/NO
[EXERCISE] SPIN Problem: Extend exercise — YES/NO
[EXERCISE] SPIN Implication: Break exercise — YES/NO
[EXERCISE] SPIN Need-Payoff: Build-a-toy — YES/NO
[EXERCISE] Capstone ("use your own data"): YES/NO
[EXERCISE] Exercises chain: YES/NO (each builds on prior)
[EXERCISE] Success criteria present: N/N exercises
```

### Pass 6: Voice Analysis

Sample 5 representative paragraphs. For each, identify the register (A/B/C/mixed) and flag:
- Adjacent paragraphs with same register (monotone risk)
- Paragraphs blending all three registers (muddy voice)
- Sections where register doesn't match content type
- Overall ratio deviation from 25/25/50 target

### Review Output Format

```markdown
# Tutorial Review: <title>

## Summary
- Bragi violations: N
- SPIN + cognitive structure: OK / NEEDS WORK
- Prerequisite chain: OK / N VIOLATIONS
- Artifact sync: OK / N ORPHANS, N DESERTS
- Exercise coverage: N/5 required types
- Voice consistency: OK / ISSUES

## Critical (fix before publish)
<items>

## Major (fix for quality)
<items>

## Minor (nice to have)
<items>
```

---

## Anti-patterns (things this skill prevents)

- **Definition-first openings.** "Steganography is the practice of..." No. Show the attack. Let the reader feel the problem. THEN name it.
- **Concept before code.** Never introduce notation, terminology, or theory before the reader has built something that demonstrates it.
- **Orphan code blocks.** A code cell with no narrative context. Every cell has a beat; every beat has a cell.
- **Prose deserts.** Three paragraphs of explanation with no runnable artifact. If you can't make it runnable, it's not a tutorial; it's an article. Use article-draft.
- **Busywork exercises.** "Print the length of this string." If the exercise doesn't build capability or reveal something surprising, cut it.
- **Forward references.** "We'll see later why this matters." No. Restructure so it matters now.
- **Toy-only exercises.** Every tutorial must end with "use this on your own real thing." Toy data teaches mechanics; real data teaches judgment.
- **Monotone voice.** Three sections in a row with the same register. Blend across sections; vary the emotional texture.
- **Skipping DO.** Every concept starts with experience. If the reader's first encounter with an idea is a definition, the tutorial has failed at that concept.
- **The "I'll explain it twice" trap.** State it once. Show it in code. The code IS the second explanation. Don't write the same idea in prose twice.

---

## Appendix: Quick Reference

### Dual arc check
- [ ] SPIN arc present (Situation → Problem → Implication → Need-Payoff)
- [ ] Solution appears AFTER Implication section
- [ ] Every concept follows DO→NOTICE→CODE→NAME
- [ ] No concept starts with definition (DO is never skipped)
- [ ] NAME always comes after CODE

### Prerequisite check
- [ ] Starting state documented (what reader has coming in)
- [ ] Every section declares what it adds and what reader can do after
- [ ] Zero forward references
- [ ] Jargon-earning order complete (no term used before earned)
- [ ] Opening move uses something from prior section, not recap

### Beat + artifact check
- [ ] Every section has an emotional beat
- [ ] Adjacent sections have different beats
- [ ] Every beat has a companion artifact (code cell, function, output)
- [ ] Every artifact has a beat
- [ ] No prose desert (>2 paragraphs without runnable artifact)

### Exercise check
- [ ] At least one exercise per SPIN phase
- [ ] Verify, Extend, and Break tiers all represented
- [ ] At least one Build-a-Toy exercise
- [ ] Capstone exercise uses reader's own real data
- [ ] Exercises chain (each builds on prior)
- [ ] Every exercise has success criteria

### Visual check
- [ ] Every visual supports a specific concept
- [ ] Every visual has a caption (complete sentence)
- [ ] Expected output shown before reader runs their own code
- [ ] 1 hero SVG per tutorial
- [ ] Interactive elements have static fallbacks

### Voice check
- [ ] Default ratio: 25% A / 25% B / 50% C
- [ ] One register per paragraph
- [ ] No all-three-registers paragraphs
- [ ] War stories use A+B; concept explanations use C; exercises use C

### Bragi check
- [ ] Zero em dashes
- [ ] Zero blocklist words
- [ ] Zero performative honesty
- [ ] Zero self-referential pivots
- [ ] Zero puffery
- [ ] Zero restating the obvious
- [ ] Zero "not just X, but also Y"
- [ ] Zero staccato data-point mic drops
- [ ] Parallel structures pass escalation test
- [ ] Pelekification patterns actively used

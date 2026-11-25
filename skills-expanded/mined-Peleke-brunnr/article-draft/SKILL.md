---
name: article-draft
description: "Draft technical articles with narrative structure, visual injection, and prose quality enforcement. Combines SPIN storytelling, engagement science, Bragi prose gate, and comedy-writer voice calibration for articles that are rigorous AND readable."
license: MIT
metadata:
  openclaw:
    emoji: "\u270D\uFE0F"
---

# Article Draft

Draft technical articles that tell a story, not a lecture. This skill enforces narrative structure (SPIN arc), prose quality (Bragi gate), engagement science (sensory hooks), and voice calibration (irreverent but substantive) at draft time so review passes catch less garbage.

## Step 0: Inputs

Before drafting, you need:

1. **Editorial map** — what the article covers, what it claims, what evidence supports each claim
2. **Visual inventory** — screenshots, charts, diagrams available for injection
3. **War stories** — specific anecdotes, incidents, real data (not hypotheticals)
4. **Voice target** — which register(s) to blend (see Voice Calibration below)

If any of these are missing, do an elicitation pass before drafting. Do not draft from an outline alone.

---

## Phase 1: SPIN Arc

Map the article to SPIN (Rackham). The solution does NOT appear until the Need-Payoff phase. The audience must feel pain BEFORE seeing the solution.

| Phase | Function | Reader's internal question |
|-------|----------|---------------------------|
| **Situation** | Establish shared reality | "Yeah, I know this" |
| **Problem** | Name the specific pain | "Oh god, yes, this sucks" |
| **Implication** | Show what the pain costs | "Wait, it's THAT bad?" |
| **Need-Payoff** | Present the solution + proof | "OK, show me" |

Rules:
- Solution does NOT appear before the Implication section. Period.
- Each phase transition is a natural question the reader is asking
- The Situation phase is max 2 paragraphs. Do not over-explain what people already know.
- The Problem phase uses a specific war story, not an abstract description

---

## Phase 2: Beat Map

Map every section to an emotional beat. Adjacent sections cannot have the same beat.

**Tension building (first half):**
- Intrigue ("huh, what's this about")
- Recognition ("oh I know exactly what this is")
- Discomfort ("oh no, I do this too")
- Empathy ("I feel seen")

**The Turn (midpoint):**
- Respect ("but there's a way")

**Conviction building (second half):**
- Clarity ("oh, I see how this works")
- Insight ("wait, THAT'S what's actually happening?")
- Relief ("this is solvable")
- Confidence ("I could do this / I believe this works")

**Closing:**
- Resolution (callback to the opening war story, now resolved)

---

## Phase 3: Visual Injection Protocol

Every article has three visual layers. Plan injection points during outlining, not after drafting.

### Layer 1: Data visuals (charts, screenshots)
- Place AFTER the claim they support, not before
- Caption must state what the reader should see, not just label the axes
- Max 2 data visuals per section. If you need more, the section is too long.

### Layer 2: Architecture diagrams (SVG)
- One hero diagram per article (the "big picture")
- Place at the SPIN transition (end of Situation or start of Need-Payoff)
- Pipeline/flow diagrams: left-to-right or top-to-bottom, never circular unless the loop IS the point
- Dark theme. Minimal color palette (2-3 colors max). No gradients unless they encode data.

### Layer 3: Interactive elements (d3.js, animations)
- Max 1-2 per article. These are expensive; use them where static fails.
- Best for: distributions updating in real time, graph traversals, parameter exploration
- Every interactive MUST have a static fallback (PNG) for non-JS contexts
- Place after the reader has built intuition, not as the introduction to a concept

### Injection checklist
For each visual, answer:
1. What claim does this support?
2. What should the reader notice first?
3. What's the caption? (Must be a complete sentence, not a label)
4. Does removing this visual weaken the argument? (If no, cut it.)

---

## Phase 4: Voice Calibration

### Three registers to blend

**Register A: Frustrated Engineer (Mickens)**
- Escalating specificity. Start general, narrow to a specific system, narrow to a specific log line, narrow to a specific token.
- Real terror underneath the laughs. The joke works because the problem is genuinely absurd.
- Hyperbolic analogy that clarifies, not obscures.
- USE FOR: war stories, failure descriptions, "the state of the industry" sections

**Register B: Self-Deprecating Narrator (Sedaris)**
- Be harder on yourself than anyone else in the story.
- Mundane details elevated to absurdity. The joke is in the precision, not the exaggeration.
- Weight at the end. Laugh for 2,000 words, then one sentence that hits.
- USE FOR: personal anecdotes, "how I got here" sections, the opening hook

**Register C: Respectful Tour Guide (Paul Ford)**
- Direct address that dignifies the reader. Never talk down.
- Sustained genuine curiosity about the subject matter.
- The humor is in the juxtaposition: rigorous science described by someone who finds parts of it absurd.
- USE FOR: technical explanations, architecture walkthroughs, "how it works" sections

### Voice rules
- Default ratio: 40% Register A, 30% Register B, 30% Register C
- LinkedIn-facing articles: bias toward A+B (war stories + self-deprecation)
- Technical deep dives: bias toward C+A (tour guide + frustrated specificity)
- NEVER use all three in the same paragraph. One register per paragraph, blend across sections.

---

## Phase 5: Bragi Prose Gate (applied at draft time)

These 28 rules are enforced DURING drafting, not on review. Internalize them.

### Hard bans (zero tolerance)
1. **No em dashes (—).** Use colons, semicolons, commas, parentheses, or separate sentences.
2. **No AI vocabulary blocklist words.** Additionally, align with, bolstered, crucial, delve, emphasizing, enduring, enhance, fostering, garner, highlight (as verb), interplay, intricate/intricacies, key (as adjective), landscape (abstract), load-bearing, meticulous/meticulously, pivotal, showcase, tapestry (abstract), testament, underscore (as verb), valuable, vibrant.
3. **No performative honesty.** "Being honest:", "To be frank:", "The truth is:" — if you have to announce you're being honest, cut the announcement.
4. **No self-referential pivots.** "This is where things get interesting" — just make the point.
5. **No inflated significance framing.** "Marking a pivotal moment", "setting the stage for", "evolving landscape" — name the specific consequence or delete.

### Structural bans
6. **No hedging then inflating.** "Though limited, it contributes to the broader..." — if it's minor, say it's minor and move on.
7. **No punchy fragment marketing copy.** "One knowledge base, every agent surface." — technical articles aren't ad copy.
8. **No tricolon/pentad enumerations for rhythm.** "Fast, reliable, scalable, secure, and observable" — itemize what matters, not what sounds balanced. **Escalation test**: each item must either add a NEW dimension or sharpen the existing one. Think improv: "yes, and..." is the whole point. "Every time. From scratch. Forever." passes (frequency → mechanism → time horizon: each sharpens). "Fast, reliable, scalable" fails (three synonyms for "good"). Stop at three.
9. **No rhythmic parallel construction closers.** "Decisions tied to outcomes, updated by evidence, grounded in practice" — end with a concrete claim.
10. **No challenges-and-future-prospects formula.** "Despite challenges, the future looks promising" — name the problems and skip the sandwich.

### Word-level bans
11. **No elegant variation.** If you mean the same thing, use the same word. Do not cycle through synonyms.
12. **No copula avoidance.** "Serves as", "stands as", "represents a" — just say "is."
13. **No dismissive 'with' framing.** "A demo with persistence" — don't reduce complex features to prepositional afterthoughts.
14. **No vague attribution.** "Experts argue", "Industry reports suggest" — name the source or cut the claim.
15. **No false ranges.** "From X to Y" only when there's an actual spectrum.

### Analysis bans
16. **No superficial participle analysis.** "...creating a lively community", "...further enhancing its significance" — if you stated a fact, stop. Don't append a gerund.
17. **No hedging with 'not' lists.** "Not X. Not Y. Not Z." — say what the thing IS.
18. **No colon-into-bold-statement.** "The question: **How do you...**" — formatting is not argumentation.
19. **No promotional puffery.** "Groundbreaking", "renowned", "boasts a", "showcasing" — cut every adjective that doesn't distinguish this subject from any other.
20. **No notability assertion sections.** Don't build a section whose purpose is arguing the subject deserves attention. Show the work.

### Rhythm and structure bans
21. **No blunt fragment negation.** "A review tool. Not a generator." → "A review tool, not a generator." Period-then-"Not"-fragment is fake emphasis. Use a comma or restructure.
22. **No wall-of-text paragraphs with multiple beats.** 3+ sentences carrying independent weight = break at thought boundaries. One thought per visual unit. If a paragraph has multiple beats, decompose it.
23. **No full-clause linking.** Links highlight the operative noun/concept, not entire clauses. `[functional programming](url)` not `[here's an article about functional programming](url)`.
24. **No mirrored affirmation pairs.** "X is real. So is Y." False equipoise through parallel "is" constructions. Cut the mirror; say what you mean directly.

### Cross-model LLM signatures (sourced from LAMP corpus + Wikipedia:Signs of AI writing)
25. **No "not just X, but also Y" constructions.** "Not only a framework, but also a philosophy." LLMs use this to sound balanced while saying nothing. Subsumes "It's not...it's..." variants.
26. **No restating the obvious.** If you stated a fact, don't re-explain it in different words. LAMP corpus confirmed this across GPT-4o, Claude, and Llama: "redundant clarifications making implied information explicit." Trust the reader.
27. **No bare conjunctions as standalone paragraphs.** "But." alone on a line is an LLM rhythm trick. The conjunction performs a turn the prose hasn't earned. Integrate the turn into the sentence.
28. **No emotional cliché templates.** "A mix of [emotion] and [emotion]", "a sense of [noun] grew in the pit of", "the weight of [abstract noun]." Cross-model signatures identified by LAMP. Replace with specific, embodied detail.
29. **No staccato data-point mic drops.** "Sixty-seven kilobytes. Thirty-two tools. 2.3 out of 5." Fragment lists of stats used as closers are the most recognizable GPT-4o signature in technical writing. The data belongs in the argument, not arranged as a curtain call. If a section needs a closer, close on the *insight*, not a remix of the numbers. Doubly banned with a trailing aphorism: "The numbers were always there. Somebody had to count them."

### Pelekification (do MORE of these)

These aren't bans. They're the patterns that make the writing land. Encode as positive directives.

- **Break line after standalone statements that land.** "was the exploration." gets its own line. The break IS the emphasis. Don't dilute it with continuation.
- **Colon extension for earned continuation.** "The idea was right: I use it every day." The colon says "and here's the proof." Use it where the first clause earns the second.
- **Ellipsis for hesitation and self-correction.** "was...Experimental." The ellipsis performs the thinking. Use sparingly; it's a precision tool.
- **Ellipsis as sentence binder.** Two sentences that could stand alone get joined by `...` when the second deflates, recontextualizes, or quietly undercuts the first. "It doesn't encode hidden data or exploit an obscure Unicode plane...it just breaks pattern matching." No space before the resumption. The ellipsis replaces a period+capital with a breath that says "and the punchline is." Non-standard; very Peleke.
- **Semicolons in extended lists.** When list items are closer to clauses than words, or when the rhythm wants a significant pause between items, use semicolons over commas. "The payload was too large; the IDs were opaque; thirty percent of the rules were irrelevant." The semicolon says "these are parallel but independent weights."
- **Semantic punctuation.** Period→colon when explaining. Period→semicolon when paralleling. Period→ellipsis+"But" when contradicting with hesitation. Punctuation carries structural meaning; use it.
- **Bold for argumentative weight, not decoration.** Bold the words that carry the claim: **structured data** would have been **cheaper and more reliable**. Not every noun. Not headers-in-prose. The words the reader's eyes need to land on.
- **Annotations as cross-references.** Use `<Annotation>` to connect ideas across articles and projects. The annotation enriches without interrupting flow.
- **Prosodic awareness.** Alliteration and sibilance are good. Sound matters. When a sentence sounds right spoken aloud, it reads right silently.
- **Decorative sentences earn their placement.** "They're autocomplete in a nice outfit" is good writing. But it needs buildup. Without earned context, standalone observations read as filler. Place them after the argument, not before.
- **Section headers at argument pivots.** Not at topic boundaries. The header marks where the argument *turns*, not where the subject changes.
- **Dialogue as blockquote.** Character speech gets visual weight. Blockquotes for dialogue, not just for pull-quotes.
- **Typographical weight escalation at pivots.** line break < italic < blockquote < bold. Deploy weight at pivots, not decoratively.
- **Self-aware rule violations.** When you deliberately break a Bragi rule, acknowledge it inline. Recruit the reader as co-conspirator.

---

## Phase 6: Engagement Hooks

From engagement science (Warnick et al., 2018): named characters create 2.5x more neural engagement than abstractions. Circular stories are 22% more memorable than linear ones.

### Required elements
- **Named protagonist by paragraph 3.** Not "developers" or "teams." A specific person (can be the author) with a specific problem.
- **Protagonist appears 3+ times by name.** Thread them through the article.
- **Circular close.** The ending callbacks to the opening. The war story that opened the piece resolves (or deepens) at the end.
- **Code before formula.** Show the output, THEN explain the math. Never introduce notation first.
- **One "holy shit" data point per section.** Not buried in a table. Called out in prose. ("56% of all mistakes were repeats.")

### Engagement budget per article
- 1 war story opening (required)
- 3-5 data callouts (bold or standalone line)
- 2-4 code blocks (real output, not pseudocode)
- 1 circular close (required)
- 0-2 footnotes for technical asides that would break flow (Roach technique)
- 0 open-question closers ("What's your version of this?" is LinkedIn distro copy via LinWheel, NEVER article prose. Articles end with resolution or forward motion, not audience prompts.)

---

## Phase 7: Draft Execution

With all the above internalized, draft in this order:

1. **Write the opening war story first.** This anchors everything. Get the specific anecdote, the specific failure, the specific feeling. Register B (Sedaris).
2. **Write the SPIN transitions.** The questions that move the reader from Situation → Problem → Implication → Need-Payoff.
3. **Fill each section.** One register per paragraph. Inject visuals at planned points.
4. **Write the circular close.** Callback to the opening. The same situation, now transformed by what the reader knows.
5. **Run Bragi gate.** Search the draft for every banned pattern. Fix them. This is non-negotiable.
6. **Caption every visual.** Complete sentence stating what the reader should see.
7. **Read aloud test.** Does any sentence make you cringe? Cut it. Does any paragraph feel like filler? Cut it. Does the piece work without any single section? If yes, that section is filler. Cut it.

---

---

## Review Mode

When reviewing an existing draft (not drafting from scratch), run these passes in order. Output a structured review report.

### Pass 1: Bragi Scan

Search the entire draft for violations of the 28 prose rules. For each violation found, output:

```
[BRAGI] Line ~N: "<offending text>"
  Rule: <rule name>
  Fix: <specific rewrite>
```

Priority order: em dashes first (easiest to grep), then blocklist words, then structural patterns.

### Pass 2: SPIN Audit

Identify where each SPIN phase lives in the current draft. Report:

```
[SPIN] Situation: lines N-M (or MISSING)
[SPIN] Problem: lines N-M (or MISSING)
[SPIN] Implication: lines N-M (or MISSING)
[SPIN] Need-Payoff: lines N-M (or MISSING)
[SPIN] Solution first appears: line N — BEFORE/AFTER Implication
```

If the solution appears before Implication, flag it as a structural problem.

### Pass 3: Engagement Audit

Check for required engagement elements:

```
[ENGAGE] Named protagonist: YES/NO — first appears line N
[ENGAGE] Protagonist reappears: N times (need 3+)
[ENGAGE] Circular close: YES/NO
[ENGAGE] Code before formula: YES/NO (or N/A)
[ENGAGE] "Holy shit" data points: N found (need 1+ per section)
```

### Pass 4: Voice Analysis

Sample 5 representative paragraphs. For each, identify the register (A/B/C/mixed) and flag:
- Adjacent paragraphs with same register (monotone risk)
- Paragraphs blending all three registers (muddy voice)
- Sections where register doesn't match content type (e.g., Register B on architecture walkthrough)

### Pass 5: Visual Injection Opportunities

For articles that will include visuals, identify:

```
[VISUAL] Line ~N: "<claim or data point>"
  Type: chart / screenshot / SVG / d3.js / code block
  What it should show: <description>
  Caption draft: <one sentence>
```

Also flag: sections longer than 500 words with no visual break.

### Pass 6: Staleness Check

Flag any claims that reference specific numbers, tool counts, PR counts, test counts, or version numbers. These go stale fast.

```
[STALE?] Line ~N: "<claim>"
  Verify: <what to check and where>
```

### Review Output Format

```markdown
# Article Review: <title>

## Summary
- Bragi violations: N
- SPIN structure: OK / NEEDS WORK
- Engagement score: N/5 required elements
- Voice consistency: OK / ISSUES
- Visual opportunities: N identified
- Staleness risks: N flagged

## Critical (fix before publish)
<items>

## Major (fix for quality)
<items>

## Minor (nice to have)
<items>

## Suggested visual injection points
<items>
```

---

## Anti-patterns (things this skill prevents)

- "Let me explain the architecture" opening (Register C without a war story setup = lecture)
- Visuals dumped at the end instead of injected at claim points
- Prose that passes spell check but reads like ChatGPT (Bragi gate catches this)
- Articles that explain what something IS but never show what it DOES (code-before-formula rule)
- Humor that tries too hard (the truth is funny enough; describe it precisely)
- Articles with no named protagonist (abstractions don't engage)
- Open-question closers in articles ("What's your version?" belongs in LinkedIn distro, not here)
- Prose that restates what was just said in different words (trust the reader)

---

## Appendix: Quick Reference

### SPIN check
- [ ] Solution appears AFTER Implication section
- [ ] Each phase transition is a question the reader is asking
- [ ] War story in the Problem phase (not abstract)

### Beat check
- [ ] Adjacent sections have different beats
- [ ] Turn (midpoint) is identifiable
- [ ] Closing callbacks to opening

### Visual check
- [ ] Every visual supports a specific claim
- [ ] Every visual has a caption (complete sentence)
- [ ] Max 2 data visuals per section
- [ ] 1 hero SVG per article
- [ ] Interactive elements have static fallbacks

### Voice check
- [ ] One register per paragraph
- [ ] No all-three-registers paragraphs
- [ ] Default ratio appropriate for article type

### Bragi check
- [ ] Zero em dashes
- [ ] Zero blocklist words (including load-bearing, meticulous, bolstered)
- [ ] Zero performative honesty
- [ ] Zero self-referential pivots
- [ ] Zero puffery
- [ ] Zero blunt fragment negation ("Not X." standalone)
- [ ] Zero wall-of-text paragraphs (one beat per visual unit)
- [ ] Zero full-clause links (operative word only)
- [ ] Zero mirrored affirmation pairs
- [ ] Zero "not just X, but also Y"
- [ ] Zero restating the obvious
- [ ] Zero bare conjunction paragraphs
- [ ] Zero emotional cliché templates
- [ ] Parallel structures pass escalation test (new dimension OR sharpen)
- [ ] Open-question closers saved for LinWheel, not in article

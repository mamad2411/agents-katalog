---
name: assessment-generator
description: "Generate tiered assessments that test understanding at six cognitive levels. Maps to DO→NOTICE→CODE→NAME: recall, predict, build, break, transfer, teach. Companion to technical-tutorial — tutorials teach, this evaluates. Includes difficulty calibration, Socratic follow-ups for wrong answers, and misconception log integration."
license: MIT
metadata:
  openclaw:
    emoji: "\U0001F9EA"
---

# Assessment Generator

Generate assessments that test whether the reader actually learned, not whether they can pattern-match a multiple-choice answer. Six tiers map to the DO→NOTICE→CODE→NAME loop: recall what you experienced, predict what you noticed, build what you coded, break what you built, transfer the concept you named, teach it to someone else.

Companion to `technical-tutorial` (#34). Tutorials generate teaching content; this skill generates evaluation content. Tutorial outputs are valid inputs for the assessment generator. Reads `_educational-suite-conventions.md` for shared contracts.

---

## Step 0: Inputs

Before generating, you need:

1. **Source content** — one of:
   - A `technical-tutorial` output (preferred; includes prerequisite chain, jargon-earning order, exercise list, SPIN phase map)
   - A `lesson-generator` module outline or notebook
   - A chapter outline or teaching artifact with identifiable concepts
2. **Learner profile** (optional) — from aegir's curriculum brief or elicitation. Adjusts difficulty calibration and misconception targeting.
3. **Misconception log** (optional) — known weak spots from prior Socratic Q&A or previous assessment results. When present, generates targeted questions.
4. **Tier distribution** — percentage allocation across tiers. Default: 15% recall, 20% predict, 20% build, 15% break, 15% transfer, 15% teach.
5. **Checkpoint** (optional) — if set, generates a mini-assessment covering only concepts earned up to a specific section in the source content. Enables mid-tutorial quizzes.

If source content lacks a prerequisite chain or jargon-earning order, extract one before generating. No assessment without knowing what the learner has earned.

---

## Phase 1: Concept Extraction

Read the source content and extract a structured concept inventory.

### From a technical-tutorial

The tutorial provides these directly:
- **Prerequisite chain**: section-by-section "Has / Adds / After"
- **Jargon-earning order**: term → section → earned-by table
- **Exercise list**: what the reader already built and at which tier (verify/extend/break)
- **SPIN phase map**: which concepts live in which emotional phase

### From other sources

If the source is a notebook, chapter outline, or unstructured teaching artifact:

1. **Identify concepts** — every distinct idea, technique, function, or principle taught
2. **Order by dependency** — which concepts require which prerequisites
3. **Map to DO→NOTICE→CODE→NAME** — for each concept, identify which stages the source covers
4. **Build the jargon-earning order** — when each term is first used meaningfully

Output: a concept inventory table.

```markdown
| # | Concept | Prerequisites | DO→N→C→N Coverage | Source Section |
|---|---------|---------------|-------------------|----------------|
| 1 | codepoint vs glyph | none | DO+NOTICE+CODE+NAME | Part 2 |
| 2 | zero-width characters | codepoint | DO+NOTICE+CODE | Part 2 |
| 3 | homoglyph substitution | codepoint | DO+NOTICE+CODE+NAME | Part 3 |
```

---

## Phase 2: The Six-Tier Framework

Every question belongs to exactly one tier. Tiers map to the DO→NOTICE→CODE→NAME loop.

### Tier 1: Recall (DO stage)

**Tests:** Can you remember what you experienced?

The reader saw, heard, or ran something. Can they retrieve it?

**Difficulty levels:**
- **Low:** Direct recall of a fact or definition. "What Unicode category contains invisible format characters?"
- **Medium:** Recall with context. "In the os-info-checker-es6 attack, what Unicode range was used to hide the dropper?"
- **High:** Recall requiring synthesis of multiple facts. "Name three Unicode character categories that can produce invisible output, and give one codepoint from each."

**Question patterns:**
- Multiple choice (concept identification)
- Term matching (vocabulary precision)
- Fill-in-the-blank (code completion with a single correct answer)
- "Which of these is/are true about X?" (select all that apply)

**Anti-patterns:**
- Trick questions that test reading comprehension, not concept recall
- Questions answerable by someone who skimmed headings without doing the exercises

### Tier 2: Predict (NOTICE stage)

**Tests:** Can you simulate mentally? Can you predict output without running code?

The reader noticed patterns during DO and NOTICE. Can they apply those patterns to new inputs?

**Difficulty levels:**
- **Low:** Predict output of a function they built, with familiar input. "What does `inspect_string('Hello')` return?"
- **Medium:** Predict output with unfamiliar input. "What does `inspect_string('Hеllo')` return?" (Cyrillic е)
- **High:** Predict behavior of a system they built, under edge conditions. "What happens when `detect_stego()` receives a string containing only variation selectors and no base characters?"

**Question patterns:**
- "What happens when..." (predict output given input)
- "Step through this algorithm on this input" (trace execution)
- "Which of these outputs is correct for this input?" (output identification)
- "Before running this cell, predict..." (pre-execution prediction)

**Anti-patterns:**
- Questions that require running the code to answer (that's Tier 3, not Tier 2)
- Predictions about code the reader hasn't seen or built

### Tier 3: Build (CODE stage)

**Tests:** Can you construct it? Given a specification, can you write working code?

**Difficulty levels:**
- **Low:** Complete a partial implementation. Starter code provided, 1-3 lines missing.
- **Medium:** Implement from specification. Function signature and docstring provided, body is empty.
- **High:** Implement from description only. Natural language spec, no starter code.

**Question patterns:**
- Implement from specification
- Complete a partial implementation
- Modify existing code to change behavior
- "Write a function that..." with success criteria

**Anti-patterns:**
- Asking the reader to rebuild something they already built in the tutorial (that's the tutorial's job)
- Build questions without clear success criteria

**The dedup rule:** If the tutorial had a Build exercise for concept X, the assessment's Tier 3 question for concept X MUST use a different context, different parameters, or different domain. Same cognitive level, different scenario.

### Tier 4: Break (CODE stage, adversarial)

**Tests:** Can you find edges, failures, and vulnerabilities? Can you defeat the system you built?

**Difficulty levels:**
- **Low:** Find the bug in a provided implementation. One obvious error.
- **Medium:** Construct an adversarial input that defeats a provided function. Requires understanding the function's blind spots.
- **High:** Identify a class of inputs that no simple fix can handle. Requires understanding the fundamental limitation.

**Question patterns:**
- "Find the bug in this implementation"
- "Construct an input that passes X but still contains Y"
- "Under what conditions does this approach fail?"
- "What happens if you initialize/configure X incorrectly?"
- "Write a test case that this function should pass but doesn't"

**Anti-patterns:**
- Break questions about code the reader didn't build or understand
- Adversarial questions with no correct answer (there must be a constructible example)

**The dedup rule:** Same as Tier 3. If the tutorial's Break exercise was "defeat your own detector," the assessment's Tier 4 question must use a different attack vector or a different detector.

### Tier 5: Transfer (NAME stage)

**Tests:** Can you apply this concept in a domain you haven't seen? Can you recognize the same pattern elsewhere?

**Difficulty levels:**
- **Low:** Apply to a closely related domain. "How would you use skeleton normalization to detect homoglyph attacks in email subject lines?"
- **Medium:** Apply to a moderately different domain. "Design a Unicode-aware input validation function for a web form that accepts usernames."
- **High:** Apply to a distant domain. "The normalize-then-scan pattern from Unicode stego applies to another security domain. Name it and explain the parallel."

**Question patterns:**
- "Apply this concept to [different domain]"
- "How would you modify this for [new constraint]?"
- "Compare this approach to [alternative]; when would you choose each?"
- "What other fields have this same problem? Describe the parallel."
- "Write the general principle that explains why both X and Y work"

**Anti-patterns:**
- Transfer questions to domains the reader can't reasonably know about
- Questions that are really just Tier 1 recall dressed up as transfer ("apply X to Y" where Y is from the tutorial)

### Tier 6: Teach (NAME stage, Feynman)

**Tests:** Can you explain this to someone else? Can you create a teaching artifact?

The ultimate test: if you can teach it, you understand it. These produce artifacts.

**Difficulty levels:**
- **Low:** Explain to a peer with similar background. "Explain homoglyph attacks to a developer who understands Unicode but hasn't heard of this attack class."
- **Medium:** Explain to someone in a different field. "Explain why Unicode normalization matters to a product manager who decides which npm packages to approve."
- **High:** Explain using an analogy from a completely different domain. "Explain the normalize-then-scan defense to a chef. Use a food safety analogy."

**Question patterns:**
- "Explain X to someone who knows Y but not Z"
- "Draw/diagram the process of..."
- "Write a 2-minute script walking through..."
- "Create an analogy for X using [domain]"
- "Write a tweet thread (5 tweets) explaining X to [audience]"
- "What's the one sentence you'd put on a slide to explain X to [audience]?"

**Anti-patterns:**
- Teach questions where the audience is identical to the reader (that's just restating, not teaching)
- Questions that accept vague hand-waving ("explain why security matters")

---

## Phase 3: Difficulty Calibration

Each tier has internal difficulty variance. The skill distributes questions across three difficulty levels within each tier.

### Default difficulty distribution (per tier)

| Difficulty | % of tier | Purpose |
|------------|-----------|---------|
| Low | 30% | Confidence building. Verifies the reader grasped the basics. |
| Medium | 50% | Core assessment. Tests solid understanding. |
| High | 20% | Stretch. Identifies deep comprehension. |

This distribution is configurable. For diagnostic assessments (finding gaps), shift toward 40/40/20. For certification-style assessments, shift toward 20/40/40.

### Difficulty calibration heuristics

A question's difficulty increases when:
- The input is unfamiliar (not from the tutorial)
- Multiple concepts must be combined
- The domain is distant from the tutorial's domain (Tier 5-6)
- Edge cases or adversarial conditions are involved (Tier 4)
- The answer requires synthesis, not recall

A question's difficulty decreases when:
- Starter code is provided
- The answer format is constrained (multiple choice vs open-ended)
- The concept was heavily practiced in the tutorial
- A worked example of the same pattern exists in the source content

---

## Phase 4: Question Generation

### Ordering

Questions follow the source content's prerequisite chain. Within a checkpoint:

1. Start with Tier 1 (Recall) — warm up, build confidence
2. Progress through Tier 2 (Predict) — test pattern recognition
3. Move to Tier 3-4 (Build/Break) — test construction and adversarial thinking
4. End with Tier 5-6 (Transfer/Teach) — test deep understanding

Never test a concept at Tier 5 before the reader has encountered it at Tier 1-2. The assessment mirrors the learning arc.

### SPIN phase alignment

If the source content has a SPIN phase map:

| SPIN Phase | Appropriate Tiers | Rationale |
|------------|-------------------|-----------|
| Situation | Tier 1-2 | Reader has observed; test recall and prediction |
| Problem | Tier 2-3 | Reader has started building; test prediction and construction |
| Implication | Tier 3-4 | Reader has seen scope; test construction and adversarial thinking |
| Need-Payoff | Tier 4-6 | Reader has the solution; test breaking, transfer, and teaching |

Don't test Tier 5 (Transfer) before the reader has reached Need-Payoff. Transfer requires the concept to be fully named and understood.

### Per-question format

```markdown
### Q[N]: [Title]

**Tier:** [1-6] — [Recall/Predict/Build/Break/Transfer/Teach]
**Difficulty:** [Low/Medium/High]
**Concept:** [which concept from the inventory]
**Prerequisites:** [earned terms/functions required]

[Question text — 2-4 sentences max. Clear, specific, unambiguous.]

[If code is involved: provide code block with context]

---

<details>
<summary>Answer / Rubric</summary>

**Expected answer:**
[The answer, with code if applicable]

**Rubric:**
- [Full marks]: [what a complete answer includes]
- [Partial marks]: [what a partial answer looks like]
- [Common mistakes]: [misconceptions this question targets]

**If wrong → Socratic follow-up:**
[See Phase 5]

</details>
```

### Question count guidelines

| Assessment Type | Total Questions | Recommended |
|-----------------|-----------------|-------------|
| Mid-tutorial checkpoint | 5-8 | Quick pulse check at a SPIN boundary |
| End-of-tutorial assessment | 12-18 | Full coverage across all tiers |
| Chapter assessment | 15-25 | Comprehensive, with difficulty gradient |
| Diagnostic (gap-finding) | 8-12 | Targeted at suspected weak spots |

---

## Phase 5: Socratic Follow-Up Sequences

When a learner gets a question wrong, the assessment generates a guided walkback through lower tiers for that specific concept.

### The Socratic bridge

```
Wrong answer on Tier 4 (Break)
    ↓
Step back to Tier 2 (Predict): "What would you expect this function to return for input X?"
    ↓
If wrong → Step back to Tier 1 (Recall): "What does [concept] mean? What's the definition?"
    ↓
If wrong → Flag as misconception. Log it. Reader needs to revisit the source content.
    ↓
If right → Step forward to Tier 3 (Build): "Now implement a version that handles this case."
    ↓
Re-attempt original Tier 4 question with new understanding.
```

### Follow-up generation rules

1. **Each follow-up is ONE tier lower** than the question that was answered wrong.
2. **Follow-ups target the SAME concept**, not a different one.
3. **Max 3 follow-up steps** before flagging as a misconception. Don't spiral.
4. **Follow-ups use different phrasing** than the original question. Same concept, different angle.
5. **Tier 1 is the floor.** If a Tier 1 follow-up is wrong, log it and move on. The reader needs to revisit the source, not take more quizzes.

### Misconception log format

When a Socratic sequence bottoms out (Tier 1 wrong), write an entry:

```yaml
- concept: "skeleton normalization"
  source_section: "Part 5"
  tier_failed: 4
  walkback_depth: 3  # bottomed out at Tier 1
  wrong_answer_pattern: "confused normalize with strip — thought normalization removes characters"
  timestamp: "2026-03-12T22:30:00Z"
  suggested_remediation: "revisit Part 5 cells 3-5; reader conflates NFKC normalization with category-Cf stripping"
```

This log is consumed by:
- `lesson-generator` revision mode (targets confused concepts for re-teaching)
- Future `assessment-generator` runs (generates misconception-targeted questions)
- The learner (transparency about where gaps exist)

---

## Phase 6: Assessment Assembly

### Document structure

```markdown
# Assessment: [Source Content Title]

**Source:** [tutorial/module/chapter reference]
**Checkpoint:** [section N or "full"]
**Tier distribution:** [actual percentages]
**Total questions:** [N]
**Estimated time:** [M minutes]

---

## Concept Coverage

| Concept | Tier 1 | Tier 2 | Tier 3 | Tier 4 | Tier 5 | Tier 6 |
|---------|--------|--------|--------|--------|--------|--------|
| [name]  | Q1     | Q4     | Q7     | —      | Q12    | —      |

---

## Questions

[Questions ordered by prerequisite chain, then by tier within each checkpoint]

---

## Answer Key

[Collapsed answers with rubrics and Socratic follow-ups]

---

## Misconception Targets

[If a misconception log was provided as input, list which questions specifically target known weak spots]
```

### Assembly rules

1. **Every concept gets at least 2 tiers of coverage.** A concept tested only at Tier 1 isn't assessed; it's trivia.
2. **No concept gets all 6 tiers.** That's exhausting. Max 4 tiers per concept, spread across difficulty levels.
3. **The assessment starts easy and ends hard.** First third is Tier 1-2. Middle third is Tier 3-4. Final third is Tier 5-6.
4. **Misconception-targeted questions are distributed**, not clustered. Don't make the reader feel like they're being interrogated about one weak spot.
5. **At least one question uses the reader's own real data/tools.** The capstone. "Run your detector on [your actual tool description / your actual npm package / your actual codebase]."

---

## Phase 7: Prose Quality Gate

The Bragi Prose Gate applies to all prose in the assessment:
- Question stems
- Answer explanations
- Rubric descriptions
- Tier 6 teaching prompts
- Socratic follow-up questions
- Section headers and framing text

All 29 rules from the canonical gate (defined in `article-draft/SKILL.md` Phase 5) are enforced. No "educational" exemptions.

### Voice calibration

Default ratio: **10% Register A, 20% Register B, 70% Register C.**

| Context | Register | Example |
|---------|----------|---------|
| Context-setting (Tier 1-2 framing) | A (Mickens) | "In May 2025, an npm package used variation selectors to hide a dropper. What Unicode range did it use?" |
| "I thought I understood" framing (Tier 4) | B (Sedaris) | "You built a detector that catches zero-width characters. Here's a string your detector says is clean. It contains a reverse shell." |
| Question stems, rubrics, explanations | C (Paul Ford) | "Write a function that normalizes the input before scanning. Your function should strip all category Cf characters and collapse confusable characters to ASCII." |
| Tier 6 teaching prompts | C (Paul Ford) | "Explain to a product manager why 'just add more characters to the blocklist' doesn't solve the Unicode steganography problem." |

---

## Review Mode

When reviewing an existing assessment, run these passes:

### Pass 1: Tier Coverage

```
[TIER] Concept "[name]": Tiers covered = [1,2,4] — OK / UNDER-COVERED (need 2+)
[TIER] Overall distribution: T1=15% T2=22% T3=18% T4=15% T5=17% T6=13% — OK / SKEWED
[TIER] Difficulty within T3: Low=30% Med=50% High=20% — OK / NEEDS ADJUSTMENT
```

### Pass 2: Prerequisite Audit

```
[PREREQ] Q7 tests "skeleton normalization" — concept earned in Section 5: OK
[PREREQ] Q3 references "variation selectors" — not earned until Section 4, but Q3 is at Section 2 checkpoint: VIOLATION
```

### Pass 3: Dedup Check

```
[DEDUP] Q8 (Tier 3, Build) vs Tutorial Exercise 4 (Extend): SAME CONTEXT — rewrite Q8
[DEDUP] Q11 (Tier 4, Break) vs Tutorial Exercise 5 (Break): different attack vector — OK
```

### Pass 4: Bragi Scan

Same as article-draft/technical-tutorial Bragi scan. All 29 rules.

### Pass 5: Socratic Sequence Validation

```
[SOCRATIC] Q7 wrong → follow-up at Tier 2 → follow-up at Tier 1: OK (3 steps max)
[SOCRATIC] Q12 wrong → no follow-up defined: MISSING
[SOCRATIC] Q4 follow-up references concept not yet earned: VIOLATION
```

### Pass 6: Rubric Quality

```
[RUBRIC] Q3: full marks criteria = specific and measurable: OK
[RUBRIC] Q9: full marks criteria = "demonstrates understanding": TOO VAGUE — rewrite
[RUBRIC] Q14: common mistakes listed: YES (2 listed)
```

### Review Output Format

```markdown
# Assessment Review: [title]

## Summary
- Tier coverage: OK / N concepts under-covered
- Prerequisite chain: OK / N violations
- Dedup vs tutorial: OK / N duplicates
- Bragi violations: N
- Socratic sequences: N/N questions have follow-ups
- Rubric quality: OK / N vague rubrics

## Critical (fix before use)
<items>

## Major (fix for quality)
<items>

## Minor (nice to have)
<items>
```

---

## Anti-patterns

1. **All Tier 1.** An assessment of only recall questions tests memory, not understanding. Minimum 2 tiers per concept.
2. **Duplicate tutorial exercises.** If the tutorial had a Build exercise, the assessment's Tier 3 question must use a different context. Same cognitive level, different scenario.
3. **Forward-reference questions.** No question tests a concept the reader hasn't earned at that checkpoint.
4. **Vague rubrics.** "Demonstrates understanding" is not a rubric. Specify what the answer must contain.
5. **Tier 6 without Tier 3.** Don't ask someone to teach a concept they haven't been asked to build. Build first, then teach.
6. **Difficulty monotone.** All Medium questions. The distribution exists for a reason: Low builds confidence, High identifies depth.
7. **No real-data capstone.** Every assessment must include at least one question where the reader uses their own tools, data, or codebase.
8. **Interrogation clustering.** Don't put all misconception-targeted questions in a row. Distribute them.
9. **Trick questions.** Questions designed to confuse rather than assess. If the question's difficulty comes from its phrasing rather than its concept, rewrite it.
10. **No Socratic follow-ups.** Every Tier 3+ question needs a walkback path. Wrong answers are learning opportunities, not dead ends.

---

## Appendix: Quick Reference

### Tier distribution check
- [ ] Default: 15% T1, 20% T2, 20% T3, 15% T4, 15% T5, 15% T6
- [ ] Every concept covered at 2+ tiers (max 4)
- [ ] No concept at all 6 tiers

### Difficulty distribution check (per tier)
- [ ] Default: 30% Low, 50% Medium, 20% High
- [ ] No tier is all one difficulty level

### Prerequisite check
- [ ] Concept inventory extracted from source
- [ ] Questions ordered by prerequisite chain
- [ ] Zero forward references
- [ ] Jargon-earning order respected

### Dedup check
- [ ] No Tier 3 question duplicates a tutorial Build/Extend exercise in the same context
- [ ] No Tier 4 question duplicates a tutorial Break exercise with the same attack vector
- [ ] Tier 5-6 questions are assessment-only (tutorials don't cover transfer/teach)

### Socratic check
- [ ] Every Tier 3+ question has a follow-up sequence
- [ ] Follow-ups step down one tier at a time
- [ ] Max 3 steps before misconception log
- [ ] Follow-ups target same concept, different phrasing
- [ ] Misconception log entries include remediation suggestions

### Prose check
- [ ] All 29 Bragi rules enforced
- [ ] Voice ratio: ~10% A, ~20% B, ~70% C
- [ ] One register per question (no mixing within a question stem)

### Assembly check
- [ ] Starts easy (T1-2), ends hard (T5-6)
- [ ] Misconception-targeted questions distributed, not clustered
- [ ] At least one real-data capstone question
- [ ] Estimated time provided
- [ ] Concept coverage table present

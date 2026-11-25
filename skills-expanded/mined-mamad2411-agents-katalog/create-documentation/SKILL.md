---
name: create-documentation
description: >
  Generate reader-centered documentation aligned with the Diátaxis framework
  and optimized for cognitive load management. Creates tutorials, how-to guides,
  explanations, and reference documentation with multi-layer quality validation.

  PROACTIVELY activate for: (1) Write tutorials for learning new skills,
  (2) Create how-to guides for specific tasks, (3) Write explanations for
  understanding concepts, (4) Generate reference documentation for APIs or
  features, (5) Document systems, features, or processes, (6) Create user
  guides or onboarding documentation.

  Triggers: "write documentation for", "create docs", "document this",
  "write a tutorial for", "how-to guide for", "explain [concept]",
  "reference documentation for", "API docs for", "user guide for",
  "document the", "create documentation"
---

# Create Documentation

Generate high-quality, reader-centered documentation using Diátaxis framework alignment and cognitive load optimization.

## Purpose

This skill produces documentation that serves readers effectively by:

- **Diátaxis alignment** — Matching content structure to reader intent (learning, doing, understanding, or lookup)
- **Cognitive load management** — Minimizing extraneous load, managing intrinsic complexity, maximizing schema-building
- **Reader persona adaptation** — Tailoring voice, depth, and structure to Anxious Novice, Developer, or Scanning Executive
- **Multi-layer validation** — Verifying structure, content, and reader experience before publication

## When to Use

**Ideal for:**
- User-facing documentation (tutorials, guides, onboarding)
- API and technical reference documentation
- Concept explanations for technical or non-technical audiences
- Feature documentation requiring multiple reader perspectives
- Documentation that must serve readers at different expertise levels

**Avoid when:**
- Internal notes or scratch documentation (no structure needed)
- Highly specialized domain requiring SME validation first
- Legal or compliance documentation (requires legal review)
- Marketing copy (different skill set)
- Documentation requiring real-time data or dynamic content

## Workflow

### Step 1: Document Type Classification

Determine which Diátaxis quadrant fits the reader's needs:

```
Reader's Primary Need → Document Type
─────────────────────────────────────
"Teach me to do X"           → Tutorial
"Help me accomplish Y"       → How-To
"Help me understand Z"       → Explanation
"What are the options for W" → Reference
```

**Decision Tree:**

| Question | Yes Answer | No Answer |
|----------|------------|-----------|
| Is the reader trying to LEARN something? | Continue below | How-To or Reference |
| Is it learning by DOING (practical)? | Tutorial | Explanation |
| Does the reader have a SPECIFIC task? | How-To | N/A |
| Is the reader LOOKING UP information? | Reference | N/A |

**Output:** `doc_type` (tutorial | how_to | explanation | reference)

**Load:** `@references/tutorial-framework.md`, `@references/howto-framework.md`, `@references/explanation-framework.md`, or `@references/reference-framework.md` based on type.

---

### Step 2: Reader Analysis & Confidence Loop

Build a complete reader profile through iterative refinement. Do not proceed until confidence reaches threshold.

**Confidence Loop Logic:**

```
confidence = 0.0
iterations = 0

WHILE confidence < 0.85 AND iterations < 3:

    1. ASSESS what we know about the reader:
       - expertise_level: novice | intermediate | expert
       - persona: Anxious Novice | Developer | Scanning Executive
       - prior_knowledge: What they already know
       - reading_context: Where/how they'll read this
       - success_definition: What "done" looks like for them

    2. IDENTIFY gaps in reader understanding:
       - Unknown expertise level?
       - Unclear persona fit?
       - Missing context about prior knowledge?
       - Undefined success criteria?

    3. RESOLVE gaps:
       IF user available:
           Ask specific clarifying questions
       ELSE:
           Make explicit assumptions with confidence scores
           Document assumptions in output

    4. RECALCULATE confidence based on profile completeness

    iterations++
```

**Reader Dimensions:**

| Dimension | Question | Impact |
|-----------|----------|--------|
| `expertise_level` | How much do they already know? | Vocabulary, depth, assumed knowledge |
| `persona` | What's their emotional/practical state? | Voice, structure, pacing |
| `prior_knowledge` | What specific knowledge do they have? | What to explain vs. assume |
| `reading_context` | How/where will they read? | Length, structure, format |
| `success_definition` | What does success look like for them? | Scope, endpoints |

**Output:** Complete reader profile with confidence >= 0.85

**Load:** `@references/reader-personas.md`

---

### Step 3: Cognitive Load Planning

Design for optimal information absorption given the topic and reader.

**Three-Load Assessment:**

| Load Type | Assessment | Optimization |
|-----------|------------|--------------|
| **Intrinsic** | How complex is this topic inherently? | Sequence, chunk, scaffold |
| **Extraneous** | What presentation overhead can we eliminate? | Remove noise, co-locate info |
| **Germane** | How can we help build lasting understanding? | Examples, connections, reflection |

**Load Strategy by Document Type:**

| Type | Intrinsic | Extraneous | Germane |
|------|-----------|------------|---------|
| Tutorial | Manage carefully | Minimize aggressively | Maximize |
| How-To | Assume away | Eliminate | Optional (via links) |
| Explanation | Embrace complexity | Minimize | Maximize |
| Reference | Minimal per entry | Near zero | N/A |

**Output:** Cognitive load strategy document

**Load:** `@references/cognitive-load.md`

---

### Step 4: Structure Selection

Select and customize document skeleton based on type and reader profile.

**Process:**

1. Load appropriate skeleton from `@templates/document-skeletons.md`
2. Adapt sections based on reader persona:
   - Anxious Novice: Add verification, recovery paths, reassurance
   - Developer: Strip to essentials, ensure copy-paste ready
   - Scanning Executive: Add "why" sections, connections, depth options
3. Plan navigation aids (TOC for >500 words, cross-references)
4. Determine appropriate length based on reading_level:
   - Grade 8: Max 1500 words
   - Grade 12: Max 3000 words
   - Professional: As needed, chunked appropriately

**Output:** Customized document structure/outline

**Load:** `@templates/document-skeletons.md`

---

### Step 5: Content Generation

Write documentation following the selected structure, type-specific patterns, and style guidelines.

**Type-Specific Patterns:**

| Type | Pattern | Key Characteristics |
|------|---------|---------------------|
| Tutorial | Step-by-step learning | Verification after each step, worked examples, recovery paths |
| How-To | Task completion | Imperative verbs, copy-paste ready, minimal context |
| Explanation | Understanding | Multiple perspectives, "why" focus, connections |
| Reference | Information lookup | Consistent entries, complete coverage, self-contained |

**Style Application:**

1. Apply voice appropriate to persona (from `@references/style-guide.md`)
2. Use sentence length appropriate to reading_level
3. Handle technical terminology per audience expertise
4. Format code blocks for copy-paste readiness
5. Use callouts sparingly and purposefully

**Content Quality During Writing:**

- [ ] One concept per sentence/step
- [ ] Active voice preferred
- [ ] Second person for instructions ("you")
- [ ] Terms defined on first use
- [ ] Examples are realistic and minimal

**Output:** Draft documentation

**Load:** `@references/style-guide.md`, appropriate framework reference

---

### Step 6: Multi-Layer Validation

Validate documentation across three layers to ensure quality.

#### Layer A: Meta-Cognitive Self-Audit

Audit your own reasoning and assumptions before validating the document.

**Checklist:**
- [ ] Reasoning chain is traceable (each claim has foundation)
- [ ] Assumptions are inventoried and documented
- [ ] Confidence levels are calibrated appropriately
- [ ] No logical leaps without explanation
- [ ] Document type correctly identified and consistent
- [ ] Structure matches skeleton for this type
- [ ] Title accurately reflects content and type
- [ ] Section flow is logical

**Load:** `@references/self-audit-protocol.md#reasoning-chain-audit`, `@references/self-audit-protocol.md#assumption-inventory`, `@references/checklists.md#layer-a-structural-validation`

#### Layer B: Reader Persona Simulation

Simulate reading the document as each relevant persona.

**For Developer persona:**
- [ ] Scan pattern works (code blocks → headings → bold → prose)
- [ ] Code is copy-paste ready
- [ ] Prerequisites are upfront
- [ ] Can skip to what they need

**For Anxious Novice persona:**
- [ ] Every step is explicit
- [ ] Verification points are clear
- [ ] Recovery paths exist for mistakes
- [ ] No assumed knowledge beyond prerequisites

**For Scanning Executive persona:**
- [ ] Key questions are answerable (What? So what? Now what?)
- [ ] Tradeoffs are visible
- [ ] Recommendations are clear
- [ ] Impact is quantified where possible

**Load:** `@references/reader-personas.md`, `@references/checklists.md#layer-b-content-validation`

#### Layer C: Experience Validation + Mode Boundary Audit

Verify document serves readers well from their perspective.

**Persona Alignment Check:**
- [ ] Primary persona needs met
- [ ] Voice consistent with persona expectations
- [ ] Cognitive load appropriate for audience
- [ ] Entry/exit points clear

**Mode Boundary Reasoning Audit:**

Detect implicit transitions between documentation modes that confuse readers.

1. **Map each section's mode** (learning | doing | looking up)
2. **Identify all transitions** between modes
3. **Verify markers** for each transition (explicit signals)
4. **REASON through each transition:** Why is this mode shift necessary? Is the reader prepared?
5. **Check for red flags:**
   - Sudden jargon increase
   - Unexplained prerequisites mid-document
   - "Obviously" or "Simply" language
   - Explanation content in how-to
   - Instructions in explanation

**Load:** `@references/checklists.md#layer-c-experience-validation`, `@references/checklists.md#mode-boundary-reasoning-audit`

---

### Step 7: Final Polish & Self-Audit

Ensure completeness, coherence, and publication-readiness.

**MECE Verification:**

| Check | Question | If Fails |
|-------|----------|----------|
| Mutually Exclusive | Do any sections overlap? | Merge or delineate |
| Collectively Exhaustive | Are there gaps in coverage? | Add missing content |

**Orphan Concept Detection:**

- [ ] All technical terms defined or linked
- [ ] No broken references to undefined concepts
- [ ] No forward references without eventual fulfillment

**Promise Verification:**

- [ ] Title delivers what it promises
- [ ] All "What You'll Learn" items taught
- [ ] All stated outcomes achievable

**Final Readability Pass:**

- [ ] Read-aloud test (mark stumbles)
- [ ] Heading scan test (structure clear from headings)
- [ ] "Can I find X?" test (information findable)
- [ ] Paragraph length audit (max 5 sentences)

**Output:** Publication-ready documentation

**Load:** `@references/self-audit-protocol.md`

---

## Output Format

```markdown
# [Document Title]

## Metadata
- **Type:** [Tutorial | How-To | Explanation | Reference]
- **Audience:** [expertise_level], [persona]
- **Reading Level:** [grade_8 | grade_12 | professional]
- **Estimated Read Time:** [X minutes]

---

[Document content following selected skeleton and type-specific structure]

---

## Quality Attestation

- **Diátaxis alignment:** Confirmed [type]
- **Cognitive load optimized:** Yes
- **Validation layers passed:** A, B, C
- **Reader profile confidence:** [X.X]
- **Assumptions made:** [List if any]
```

---

## Quality Gates

Before completing documentation:

- [ ] Document type correctly classified (single Diátaxis quadrant)
- [ ] Reader profile complete with confidence >= 0.85
- [ ] Cognitive load strategy documented and applied
- [ ] Layer A (Meta-Cognitive Self-Audit) passed
- [ ] Layer B (Reader Persona Simulation) passed
- [ ] Layer C (Experience + Mode Boundary) validation passed
- [ ] Mode boundary reasoning audit passed with explicit reasoning
- [ ] MECE verification completed
- [ ] Style guide compliance verified
- [ ] All examples tested/verified

---

## Parameters

| Parameter | Default | Options | Description |
|-----------|---------|---------|-------------|
| `doc_type` | auto_detect | tutorial, how_to, explanation, reference | Diátaxis document type |
| `topic` | — | (required) | What to document |
| `audience.expertise_level` | intermediate | novice, intermediate, expert | Reader's technical expertise |
| `audience.persona` | auto_detect | anxious_novice, developer, scanning_executive | Reader persona |
| `reading_level` | grade_12 | grade_8, grade_12, professional | Complexity/vocabulary level |
| `confidence_threshold` | 0.85 | 0.0-1.0 | Minimum confidence before proceeding from Step 2 |
| `include_examples` | true | true, false | Include worked examples |
| `validation_depth` | standard | quick, standard, comprehensive | How thorough to validate |

---

## References

This skill uses the following reference files:

| Reference | Purpose |
|-----------|---------|
| `@references/reader-personas.md` | Three reader persona definitions and selection guide |
| `@references/cognitive-load.md` | Cognitive load theory and documentation strategies |
| `@references/style-guide.md` | Writing style, voice, and formatting standards |
| `@references/tutorial-framework.md` | Tutorial-specific guidance and patterns |
| `@references/howto-framework.md` | How-to guide specific guidance |
| `@references/explanation-framework.md` | Explanation documentation guidance |
| `@references/reference-framework.md` | Reference documentation guidance |
| `@references/checklists.md` | All validation checklists (Layers A, B, C + Mode Audit) |
| `@references/self-audit-protocol.md` | MECE verification and final audit protocol |
| `@templates/document-skeletons.md` | Ready-to-use templates for all four types |

---

## Examples

**Example 1: Tutorial Request**

```yaml
request: "Create a tutorial for setting up Firebase authentication"

analysis:
  doc_type: tutorial (learning by doing)
  expertise_level: novice
  persona: anxious_novice (worried about breaking things)
  reading_level: grade_12

workflow:
  step_1: Classified as Tutorial (learning-oriented, practical)
  step_2: Reader profile - novice, anxious, needs reassurance
  step_3: High germane load, low extraneous, managed intrinsic
  step_4: Tutorial skeleton + extra verification steps
  step_5: Write with reassuring voice, explicit steps
  step_6: All three layers validated
  step_7: MECE verified, no orphans

output: Step-by-step tutorial with verification at each step,
        recovery paths for common errors, "What You've Learned" summary
```

**Example 2: How-To Request**

```yaml
request: "How-to guide for resetting a user's password"

analysis:
  doc_type: how_to (task completion)
  expertise_level: intermediate
  persona: developer (needs it done fast)
  reading_level: professional

workflow:
  step_1: Classified as How-To (task-oriented)
  step_2: Reader profile - competent, time-pressured
  step_3: Minimal all loads, optimize for speed
  step_4: How-To skeleton, stripped to essentials
  step_5: Imperative verbs, copy-paste commands
  step_6: Layers A and B focus (C lighter for practitioners)
  step_7: MECE verified

output: Numbered steps with prerequisites, copy-paste commands,
        result verification, troubleshooting section
```

**Example 3: Explanation Request**

```yaml
request: "Explain how database indexing works"

analysis:
  doc_type: explanation (understanding)
  expertise_level: intermediate
  persona: scanning_executive (wants to understand deeply)
  reading_level: grade_12

workflow:
  step_1: Classified as Explanation (understanding-oriented)
  step_2: Reader profile - curious, wants depth
  step_3: Higher intrinsic OK, maximize germane (connections)
  step_4: Explanation skeleton with multiple perspectives
  step_5: Include why, analogies, related concepts
  step_6: Full validation with mode audit
  step_7: MECE verified, connections documented

output: Concept explanation with multiple mental models,
        practical grounding, related concepts section
```

**Example 4: Reference Request**

```yaml
request: "Generate API reference for the configuration options"

analysis:
  doc_type: reference (information lookup)
  expertise_level: expert
  persona: developer (looking up specific info)
  reading_level: professional

workflow:
  step_1: Classified as Reference (information-oriented)
  step_2: Reader profile - expert, needs quick lookup
  step_3: Near-zero extraneous, minimal intrinsic per entry
  step_4: Reference skeleton with consistent entry format
  step_5: Complete entries, no narrative, all options documented
  step_6: Focus on consistency and completeness
  step_7: MECE verified, index complete

output: Alphabetically organized reference with consistent
        entry format, parameter tables, minimal examples, full index
```

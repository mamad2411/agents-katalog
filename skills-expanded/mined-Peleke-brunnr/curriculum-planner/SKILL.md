---
name: curriculum-planner
description: Interactive elicitation protocol for designing tutorial series. Triggers on "plan a tutorial", "design a curriculum", "I want to teach [topic]", "/curriculum-plan". Runs structured elicitation across 5 dimensions, produces YAML outline + per-chapter specs ready for the chapter-generator skill.
metadata:
  openclaw:
    emoji: "\U0001F5FA\uFE0F"
---

# Curriculum Planner

Run an interactive elicitation to design a tutorial series. Produces a structured outline and per-chapter specs that feed directly into the chapter-generator skill.

## When to Use

- Planning a tutorial series on any topic
- Designing a curriculum for a specific audience
- Structuring educational content with narrative arc
- Creating chapter specs for the chapter-generator skill

## Trigger Phrases

- "Plan a tutorial series on [topic]"
- "Design a curriculum for [audience] learning [skill]"
- "I want to teach [concept]"
- "/curriculum-plan [topic]"

---

## Elicitation Protocol

### Overview

The elicitation runs through 5 dimensions in a conversational flow. Ask 2-3 questions at a time. Reflect back what you heard before moving to the next dimension. Total elicitation: 5-10 exchanges.

### Dimension 1: AUDIENCE

Map the reader's cognitive profile, not demographics.

**Questions:**
- Who is the reader? (curious engineer, optimizer, architect, beginner, expert)
- What do they already know? (anchors for new concepts)
- What's their goal? (explore, build, optimize, understand)

**Extract:**
- Persona name (e.g., "curious engineer who just built a knowledge graph")
- Prior knowledge anchors (what to connect new concepts to)
- End-state capability (what they can DO after the series)

### Dimension 2: NARRATIVE ARC

Every series needs tension. No tension, no engagement.

**Questions:**
- What's the opening hook? (What problem creates cognitive tension?)
- What's the climax? (The surprising insight or reversal?)
- What's the cliffhanger? (What question leads to the next series?)

**Extract:**
- Opening war story or scenario (the "wtf" moment)
- The "aha" surprise (expectation vs reality)
- Bridge to future content (the unsolved problem)

### Dimension 3: CHAPTER BREAKDOWN

**Questions:**
- What are the 4-8 major teaching beats?
- Which chapters go deep (exercises, theory backfill, multiple aha moments)?
- Which chapters are transitional (light, keep momentum)?
- What are the dependencies between chapters?

**Extract:**
- Chapter list with titles
- Depth markers: `deep` or `light` per chapter
- Dependency chain (which chapters must precede which)

### Dimension 4: DATA & EXAMPLES

**Questions:**
- What real data do we have?
- What supplements are needed for teaching? (note plausibility)
- What running example carries through the entire series?

**Extract:**
- Data source path or description
- Supplement list with plausibility notes
- Running example description (the thread that connects all chapters)

### Dimension 5: VOICE & STYLE

**Questions:**
- What's the tone? (aegir-style irreverent, formal, conversational)
- Any specific voice rules?
- What's the teaching philosophy? (code-first, theory-first, story-first)

**Extract:**
- Voice guide reference (see `reference/voice-guide.md`)
- Specific style rules (e.g., no em-dashes, personality level)
- Philosophy statement (e.g., "code-before-formula, story-first")

---

## Elicitation Flow

```
1. OPEN
   "Let's plan a tutorial series. Who's the reader and what
    are they trying to learn?"

2. ANCHOR
   "Where does this start? What does the reader have/know
    when they begin?"

3. ARC
   "What's the opening hook: the 'wait, this is wrong' moment?"
   "What's the surprise they'll discover?"
   "Where does it leave them wanting more?"

4. STRUCTURE
   "Let me propose [N] chapters. Which feel deep vs light?"
   [Interactive refinement with user]

5. DATA
   "What real data do we use? What do we need to add?"

6. CONFIRM
   "Here's the full structure. Ready to generate chapter specs?"
```

---

## Output Format: Curriculum Outline

After elicitation, produce a YAML outline:

```yaml
# CURRICULUM-OUTLINE.yaml

metadata:
  title: "Part N: [Series Title]"
  audience: "[persona name]"
  estimated_time: "[total minutes]"
  voice_guide: "reference/voice-guide.md"
  data_source: "[description or path]"

narrative_arc:
  opening_hook: |
    [The cognitive tension moment]
  climax: |
    [The surprising insight]
  cliffhanger: |
    [The unsolved problem that pulls toward the next series]

chapters:
  - number: "N.1"
    title: "[Chapter Title]"
    depth: deep  # or light
    opens_with: "[Opening hook summary]"
    closes_with: "[Bridge to next chapter]"
    learning_objectives:
      - "[Objective 1]"
      - "[Objective 2]"
    aha_moments:
      - "[Aha 1]"
    visual_hooks:
      - type: "[mermaid|table|code_output|bar_chart]"
        description: "[What it shows]"

  # ... more chapters

supplements:
  - concept: "[Name]"
    reason: "[Why needed for teaching]"
    plausibility: "[High/Medium/Low]: [justification]"

jargon_earning_order:
  - term: "[Term]"
    introduced: "N.M"
    earned_by: "[intuition-first description]"

style_rules:
  - "Story-first opening"
  - "Code-before-formula"
  - "Visual every 2-3 sections"
  - "No em-dashes"
  - "Recap aggressively"

falsifiable_claims:
  - chapter: "N.M"
    statement: "[Specific testable claim]"
    test: "[How to verify]"
```

---

## Output Format: Per-Chapter Specs

For each chapter, generate a spec that the chapter-generator can consume directly:

```yaml
# chapter-N.M-spec.yaml

chapter:
  number: "N.M"
  title: "[Chapter Title]"
  depth: deep  # or light

  opening_hook: |
    [The war story or scenario that creates cognitive tension.
     Concrete, specific, with code if applicable.]

  learning_objectives:
    - "[Objective 1]: [subtitle]"
    - "[Objective 2]: [subtitle]"

  aha_moments:
    - "[Aha 1]: insight after buildup"
    - "[Aha 2]: deeper realization"

  key_queries:
    - description: "[What this demonstrates]"
      code: "[The code/query]"
      expected: "[What the reader should see]"

  closing_bridge: |
    [Transition to next chapter. Creates pull.]

  visual_hooks:
    - type: "[mermaid|table|code_output|bar_chart]"
      description: "[What it shows]"

  falsifiable_claim:
    statement: "[Specific testable claim]"
    test: "[How to verify]"

  jargon_introduced:
    - term: "[Term]"
      earned_by: "[intuition-first description before naming]"
```

---

## Recursive Invocation

After generating specs, invoke the chapter-generator:

```
# Generate all chapters
for spec in chapter-specs/*.yaml:
  /chapter-gen $spec

# Or generate one at a time with review
/chapter-gen chapter-N.1-spec.yaml
[review output]
/chapter-gen chapter-N.2-spec.yaml
```

---

## Voice Principles (Summary)

These are the key voice rules applied during planning. See `reference/voice-guide.md` for the full guide.

1. **Story-first**: Every chapter opens with a concrete scenario, not abstract framing
2. **Code-before-formula**: Show the code, show the result, THEN name the concept
3. **Jargon-earning**: Never use a term before the reader has earned it through examples
4. **Visual hooks**: Mermaid diagrams, tables, code output descriptions every 2-3 sections
5. **Recap aggressively**: Assume the reader forgot what happened 3 sections ago
6. **Personality**: Irreverent, direct, calibrated profanity where appropriate
7. **No em-dashes**: Colons, commas, parentheses instead
8. **Falsifiable claims**: Each chapter includes a testable claim
9. **Bridges**: Every chapter closes with a bridge that creates pull to the next

---

## Screenshot Placeholders

When planning visual hooks, note which ones should also get screenshot placeholders for post-processing. The chapter-generator inserts HTML comments at these locations:

```markdown
<!-- SCREENSHOT: [specific description of what to capture] -->
```

During curriculum planning, flag visual hooks that benefit from real screenshots (query results, graph visualizations, tool UI) vs. those that are self-contained (mermaid diagrams, markdown tables). This helps the chapter-generator place placeholders effectively, and a second-pass agent can fill them in.

---

## Quality Checklist

- [ ] All 5 elicitation dimensions covered
- [ ] Narrative arc has tension (open, climax, cliffhanger)
- [ ] Chapters have clear depth markers (deep/light)
- [ ] Deep chapters have 2-3 aha moments; light chapters have 1
- [ ] Supplements are plausible and noted
- [ ] Voice rules are explicit
- [ ] Jargon-earning order is defined
- [ ] Falsifiable claims are specified per chapter
- [ ] Each chapter spec is self-contained (can generate independently)
- [ ] Cross-references to related materials included
- [ ] Running example threads through the series

---
name: situation-analysis
description: |
  Deep analysis of unfamiliar situations, domains, or contexts via a structured three-phase protocol: Map, Drill, Act.

  [WHAT] Builds quick situational understanding in three interactive phases. The user signals unfamiliarity, the assistant asks precise questions (Map), drills deeper in the core domain (Drill), delivers actionable analysis (Act). Ends with a structured insight document saved to the vault's unsorted area.

  [WHEN] Use when: help me understand, I don't know enough about, what should I know about, I'm meeting X and know nothing, situation analysis, unknown domain, new situation, quick context before a meeting, prep before a decision.

  [LANGUAGE] Configurable. Output matches input language.

  [EXPERTISE] Domain orientation, structured questioning, three-phase analysis, decision prep.
argument-hint: "[situation or domain]"
---

Situation to analyse: $ARGUMENTS

# Situation Analysis — Map, Drill, Act

## Purpose

This skill provides quick yet deep situational understanding before meetings, decisions, projects, or contexts the user doesn't know. Instead of giving general answers, the assistant takes the role of an experienced analyst: asks precise questions to build the right context, then delivers sharp analysis in three steps.

The result is always a structured insight document, saved in the vault's unsorted folder.

---

## Protocol

### Phase 1: MAP — understand the terrain

**Trigger:** the user signals unfamiliarity with an area or situation.

**What the assistant does:**
Ask three to five precise questions to understand:
- The user's role and starting point in the situation
- What the domain or context is about (in their own words, not correct terminology)
- What's about to happen (meeting, decision, project, conversation)
- Time horizon and pressure
- What is already known vs. unknown

**Format for questions:**
Present the questions naturally, not as a numbered list. Ask one thing at a time if it seems overwhelming, otherwise as a batch.

**After the user answers:**
Deliver a sharp five-minute brief with:
- Key terms and vocabulary insiders use
- The most important options or approaches and how they differ
- How this domain or process normally works
- What outsiders consistently misunderstand or get wrong

The tone should be like an experienced colleague briefing the user before a meeting. Not academic. Not over-pedagogical. Direct and useful.

---

### Phase 2: DRILL — the surface isn't the whole picture

**Trigger:** automatically after Map is done. The user doesn't have to ask.

**What the assistant does:**
Ask the user to add specific situational context:
- Budget, time constraints, restrictions
- What they're trying to achieve
- Relationships or power dynamics that matter
- What's already decided vs. open

**Question to the user:**
"Now tell me more about your specific situation. What's your goal, your constraints, and what's already decided?"

**After the user answers:**
Deliver an analysis of what isn't visible at the surface:
- Hidden complexities that most people in the user's position don't understand until it's too late
- What seems easy but is actually hard
- The most expensive mistakes people in similar situations make
- Second-order effects to consider (not primary consequences, but what happens after them)
- What a 20-year veteran would say in an informal conversation that isn't in any handbook

The tone should be open and direct. The user needs to hear what's uncomfortable, not just what's encouraging.

---

### Phase 3: ACT — insights translated into action

**Trigger:** automatically after Drill is done.

**What the assistant does:**
Ask the user exactly what's about to happen next:
"What's the next step you're going to take, and when? Meeting, decision, conversation?"

**After the user answers:**
Deliver an action package:
- Three to five questions the user should ask (others or themselves)
- Specific information they should gather before acting
- The smartest first step given the situation
- Red flags to watch for

---

## Documentation

### When all three phases are done:

Create a markdown document with the insights and save it to the vault's unsorted area.

**Filename:**
`YYYY-MM-DD insight [title for this specific insight].md`

Date is today's date. The title should be short, descriptive, and specific to this situation.

**Document structure:**

```markdown
---
MOC: 
Created: YYYY-MM-DD
Modified: YYYY-MM-DD
Links: [relevant concepts, organizations, domains from the analysis]
tags: status-active
---

# [Document title]

## Situation description

[Short description of the situation the user faced]

## Mapping

[Key insights from phase 1 — vocabulary, structure, how the domain works]

## Hidden complexities

[Insights from phase 2 — what's not visible on the surface, risks, second-order effects]

## Action plan

[Insights from phase 3 — questions to ask, information to gather, first step, red flags]
```

**Important rules for the document:**
- No em-dashes in flowing text
- No colons in flowing text where avoidable
- Prose over bullet lists where possible
- Output language matches user input
- No `Type:` line in metadata unless template requires it
- MOC left empty if the user doesn't specify

---

## Tone guidelines for the whole process

- Direct and analytical, not pedagogical
- No unnecessary calls to action or encouragement
- No phrases like "it's important to note" or "remember that"
- No bullet lists with one word per item — if a list is used, each item should be one to two sentences
- Treat the user as an intelligent person who quickly absorbs new information
- If something is complex, say so directly instead of simplifying it away

---

## Example initiation

If the user writes: "I have a meeting with a venture capitalist next week and know nothing about the VC world"

The assistant starts Map with questions like:
- What's the meeting about — are you seeking funding or something else?
- How big is your organization and what stage are you at?
- Have you had similar conversations before, or is this entirely new territory?
- What do you want to achieve in the meeting?

Then deliver the briefing, then Drill, then Act, then the document.

---
name: op-ed
description: |
  Write op-eds and opinion articles for major publications. Thesis-driven argumentation, not narrative.

  [WHAT] Argumentative structure: thesis first, evidence, solution, call to action. Publication adaptation per length and tone. Co-author handling. Reply and final reply formats. Sharp policy stance.

  [WHEN] Use when: op-ed, debate article, opinion piece, "argue for", "write an op-ed", reply, final reply, letter to the editor. NOT for: chronicle/blog (use chronicle — narrative, not thesis-driven), policy memo (use policy-brief).

  [LANGUAGE] Configurable. Sharp and thesis-driven, not the user's narrative chronicle voice.

  [EXPERTISE] Op-ed conventions, thesis formulation, publication adaptation, evidence handling, co-author handling, reply/final-reply.
argument-hint: "[topic] [publication]"
allowed-tools: Read, Grep, Glob, Write
---

Topic: $ARGUMENTS

# Op-Ed specialist

**Role:** opinion writer.
**Signature:** sharp policy stance, clear thesis, action-oriented.
**Difference from a chronicle:** more thesis-driven, shorter, harder argumentation, often co-authored.

## Core principles

| Principle | Meaning |
|-----------|---------|
| Thesis first | Reader knows your position within the first paragraph |
| Evidence, not opinion | Every claim needs evidence or a concrete example |
| One question | Focus on ONE problem, ONE solution |
| Action force | End with a concrete demand or call to action |

## Structural pattern

### Standard op-ed (~4000-5000 characters)

```
1. HOOK + THESIS (1 paragraph)
   └─ Concrete event → Your position clearly stated

2. PROBLEM STATEMENT (1-2 paragraphs)
   └─ Why this matters → What's at stake → For whom

3. EVIDENCE (2-3 paragraphs)
   └─ Concrete examples → Statistics → Expert testimony
   └─ Each paragraph = one piece of evidence supporting the thesis

4. SOLUTION (1-2 paragraphs)
   └─ What needs to be done → By whom → When

5. CLOSING + CTA (1 paragraph)
   └─ Restate the core message → Call to action

6. SIGNATORIES
   └─ Name, title, organisation (one per line)
```

## Publication adaptation

Configure per project. Common categories:

| Publication type | Max chars | Tone | Note |
|------------------|-----------|------|------|
| National broadsheet (formal) | ~6000 | Formal, weighty | Often requires news angle |
| National broadsheet (general) | ~5000 | Factual | Broad audience |
| Tabloid debate page | ~4000 | Accessible | More emotion-driven |
| Policy outlet | ~4000 | Policy focus | Decision-maker audience |
| Ideas/progressive outlet | ~5000 | Ideas-driven | Idea debate |

## Headline patterns

**Pattern:** [Verb/imperative] + [what/whom] + [consequence/goal]

**Examples:**
- "A cyber boost for [country] in a digital age"
- "Stop platform X's influence over children"
- "We need a digital preparedness plan now"

**Avoid:**
- Questions as headlines (too weak)
- "Time to..." (overused)
- Abstract concepts without concretisation

## Thesis formulation

**Strong thesis:**
- "We all need to contribute to society's digital resilience."
- "Europe's dependence on American technology must be broken."
- "Platform X poses a security risk for children."

**Weak thesis:**
- "There are challenges in cybersecurity." (too vague)
- "One could discuss..." (too soft)
- "It's complicated." (no position)

## Co-author handling

### When several authors

1. **One lead author** owns the unified voice of the text
2. **Each signatory** contributes their expertise/credibility
3. **Signatory order** reflects contribution or alphabetical
4. **Title and organisation** for each signatory

### Signatory format

```
First Last, title, organisation
First Last, title, organisation
First Last, title, organisation
```

## Anti-AI principles

### NEVER

| Avoid | Why |
|-------|-----|
| "It's important to point out..." | Passive, filler |
| "In summary..." | Signals AI |
| "One could argue..." | Weak position |
| "There are pros and cons..." | Not thesis-driven |
| "Not just X but also Y" | Max 1 per text |

### INSTEAD

- Direct claim: "[Country] must act now."
- Rhetorical question (sparingly): "How long should we wait?"
- Contrast: "While other countries act, [country] stands still."
- Personal authority: "In our work we see daily..."

## Evidence handling

### Type of evidence

| Type | Strength | Use |
|------|----------|-----|
| Statistics | High | Quantify the problem |
| Concrete example | High | Illustrate consequences |
| Expert testimony | Medium | Strengthen credibility |
| International comparison | Medium | "Other countries have..." |
| Personal experience | Low-Medium | Personal authority |

### Integration

**Don't:** "According to a report from agency X..."
**Do:** "In 2023, attacks on agencies rose by 40 percent, according to agency X."

## Reply and final reply

### Reply (~3000 characters)

1. Reference the original article
2. Identify the main objection
3. Counter with new evidence
4. Strengthen the original thesis

### Final reply (~2000 characters)

1. Brief reference to the debate
2. Focus on the remaining core question
3. End with a principled claim

## Checklist

- [ ] Thesis clear in the first paragraph?
- [ ] One focused problem?
- [ ] At least 3 concrete pieces of evidence?
- [ ] Solution specified (who does what)?
- [ ] Action-oriented closing?
- [ ] Right length for the publication?
- [ ] Signatories with correct titles?
- [ ] Headline that draws interest?

## Instruction

1. Ask for the publication (if not specified)
2. Ask about co-authors (if not specified)
3. Identify: thesis, evidence, solution, CTA
4. Write directly per the structure
5. Stay within the publication's character limit
6. End with signatories

---

🎯 COMPLETED: [SKILL:op-ed] [op-ed for publication X]
🗣️ CUSTOM COMPLETED: [SKILL:op-ed] [Op-ed ready]

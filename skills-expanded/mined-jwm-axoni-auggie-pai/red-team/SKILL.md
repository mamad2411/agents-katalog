---
name: red-team
description: Adversarial analysis that steelmans arguments then produces devastating counter-arguments from multiple expert perspectives. USE WHEN red team, poke holes, devil's advocate, stress test, find weaknesses, attack this, challenge, which approach is better.
---

# Red Team: Adversarial Analysis

Adversarial analysis that breaks arguments into atomic components, attacks from multiple expert perspectives, and produces devastating counter-arguments while first building the strongest possible version of the argument (steelman).

## Customization

Check for user customizations at:
`~/.augment/USER/SKILLCUSTOMIZATIONS/RedTeam/PREFERENCES.md`

If this file exists, load and apply preferences found there. They override defaults below.

## Core Philosophy

**The goal is NOT destruction** -- it is finding the fundamental flaw that, if challenged, causes the entire structure to collapse.

The most powerful critique is usually ONE core issue:
- A hidden assumption that is actually false
- A logical step that does not follow
- A category error (treating X like Y)
- An ignored precedent that directly contradicts

## Two Modes

### Mode 1: Parallel Analysis (Stress-Test Existing Content)

Use when: "Red team this," "poke holes in," "find weaknesses," "devil's advocate"

### Mode 2: Adversarial Validation (Produce New Content via Competition)

Use when: "Which approach is better," "help me decide," "battle of bots"

---

## Parallel Analysis: The Five-Phase Protocol

### Phase 1: Decomposition

Break the argument into atomic claims.

1. Extract the central thesis (one sentence)
2. Identify key supporting claims (numbered list)
3. Surface implicit assumptions (what must be true for this to work)
4. Map the logical chain (A leads to B leads to C leads to conclusion)
5. Break into discrete, attackable claims

### Phase 2: Multi-Perspective Attack

Analyze from four expert categories, each bringing a different attack angle.

**Engineers (Technical/Logical Rigor):**
- Where does this break at scale?
- Show me the numbers that prove this.
- What happens when assumption X is not true?
- This is harder than it sounds because...
- Here are the failure modes.

**Architects (Structural/Systemic Issues):**
- This ignores how it fits the larger system.
- You gain X but lose Y, and Y matters more.
- These are not the same category of problem.
- Second-order effects: this causes A, which causes B, which destroys C.

**Adversarial Thinkers (Security/Game Theory):**
- Here is how I would exploit this logic.
- This depends on X, and X is false.
- A smart opponent would simply...
- This entire surface is undefended.

**Fresh Perspectives (Naive/Contrarian):**
- But why do we assume X in the first place?
- What if the exact opposite is true?
- The simpler explanation is...
- If this is true, then [absurd consequence] must also be true.

**For each perspective, identify:**
- Strongest point FOR the argument (which claim, why it is valid)
- Strongest point AGAINST the argument (which claim, what is the flaw)
- Overall assessment (one sentence verdict)

### Phase 3: Synthesis

Identify convergent insights across perspectives:
- **Multiple perspectives hit same weakness** --> Critical vulnerability
- **3-4 perspectives identified same point** --> Significant weakness
- **Unique insight from one perspective** --> Notable finding

Categorize by type: logical fallacies, missing evidence, hidden assumptions, counterexamples, precedent contradictions, second-order effects.

### Phase 4: Steelman

Before attacking, construct the STRONGEST possible version of the argument. This ensures intellectual honesty and prevents strawmanning.

```
STEELMAN

The Position (Best Version): [One sentence -- strongest formulation]

The Strongest Case FOR This Argument:
1. [12-16 words -- most compelling opening point]
2. [12-16 words -- strong supporting evidence]
3. [12-16 words -- historical precedent that supports]
4. [12-16 words -- valid concern being addressed]
5. [12-16 words -- what critics get wrong]
6. [12-16 words -- the real risk if ignored]
7. [12-16 words -- why smart people believe this]
8. [12-16 words -- strongest single reason to take seriously]

Validity Assessment: [One sentence on the legitimate core concern]
```

### Phase 5: Counter-Argument

Produce the strongest rebuttal that defeats the steelman, not a weaker strawman.

**Pre-analysis checklist:**
1. Identify claim type: Causal / Comparative / Categorical / Predictive / Normative
2. Surface hidden assumptions: What must be true? What is taken for granted?
3. Check historical precedent: Has this argument been made before? What happened?
4. Test logical validity: Does conclusion follow from premises? Any fallacies?
5. Verify it defeats the STEELMAN, not a weaker version

```
RED TEAM VERDICT

The Position: [One sentence summary of what was red-teamed]

The Counter-Argument:
1. [12-16 words -- establishes the fundamental flaw]
2. [12-16 words -- develops the core weakness]
3. [12-16 words -- historical precedent or analogy]
4. [12-16 words -- addresses the hidden assumption]
5. [12-16 words -- the counterexample or exception]
6. [12-16 words -- what is conveniently ignored]
7. [12-16 words -- second-order effects exposed]
8. [12-16 words -- knockout conclusion]

Assessment: [One sentence on fundamental soundness after analysis]
```

**Quality Criteria:** Each point is self-contained, attacks a real weakness (not a strawman), uses plain language, follows logically, and builds toward the devastating conclusion.

---

## Adversarial Validation: Three-Round Protocol

For producing superior output through competition and refinement.

### Round 1: Competing Proposals

Generate 3 distinct solutions from different perspectives:
- **Pragmatist**: Prioritizes ease of implementation and quick wins
- **Idealist**: Prioritizes best practices and long-term quality
- **Skeptic**: Prioritizes risk reduction and failure prevention

Each proposal should be complete and defensible.

### Round 2: Brutal Critique

As a harsh but fair critic, evaluate all proposals:
- What each got RIGHT (acknowledge genuine strengths)
- What each got WRONG (identify flaws, gaps, blind spots)
- The Uncomfortable Truth: What none of them want to hear
- If forced to pick one, which has the strongest foundation?

### Round 3: Collaborative Synthesis

Produce a SINGLE UNIFIED solution that:
- Addresses the valid criticisms
- Incorporates best elements from each proposal
- Resolves tensions between perspectives
- Honestly acknowledges remaining trade-offs

This is synthesis, not compromise. The final output should be BETTER than any individual proposal.

## Examples

**Stress-test an architecture:**
"Red team this microservices migration plan"
--> Parallel Analysis --> Steelman + Counter-Argument

**Devil's advocate:**
"Poke holes in my plan to raise prices 20%"
--> Parallel Analysis --> Surfaces the core issue that could collapse the plan

**Adversarial validation:**
"Which approach is better for this feature?"
--> Adversarial Validation --> Synthesized superior solution

## Anti-Patterns

- **Strawmanning**: Attacking a weak version instead of the strongest version
- **Nitpicking**: Finding trivial flaws instead of fundamental ones
- **Generic Objections**: "This might not scale" without specifics
- **Performative Destruction**: Being contrarian without substance
- **Missing the Steelman**: Attacking before honestly representing the best case

## When NOT to Use

- Simple decisions with obvious answers, time-critical situations, creative tasks where multiple valid outputs are fine, or problems where expert consensus already exists

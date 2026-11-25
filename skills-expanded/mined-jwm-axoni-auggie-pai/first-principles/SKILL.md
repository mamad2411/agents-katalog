---
name: first-principles
description: Decompose to axioms, challenge inherited assumptions, reconstruct from verified truths. USE WHEN first principles, fundamental, root cause, decompose, challenge assumptions, rebuild from scratch, physics-based reasoning, why does this work this way.
---

# First Principles Thinking

Decompose problems to fundamental truths, challenge inherited assumptions, and reconstruct optimal solutions from verified axioms. Based on physics-based reasoning methodology.

## Customization

Check for user customizations at:
`~/.augment/USER/SKILLCUSTOMIZATIONS/FirstPrinciples/PREFERENCES.md`

If this file exists, load and apply preferences found there. They override defaults below.

## Core Concept

**Reasoning by Analogy** (default human behavior, often wrong):
- "How did we solve something similar?"
- "What do others do?"
- Copies existing solutions with slight variations

**Reasoning from First Principles** (this skill):
- "What are the fundamental truths here?"
- "What is this actually made of?"
- Rebuilds solutions from irreducible facts

## The 3-Step Framework

```
STEP 1: DECONSTRUCT
"What is this really made of?"
Break down to constituent parts and fundamental truths.

        |
        v

STEP 2: CHALLENGE
"Is this a real constraint or an assumption?"
Classify each element as hard/soft constraint or assumption.

        |
        v

STEP 3: RECONSTRUCT
"Given only the truths, what's optimal?"
Build new solution from fundamentals, ignoring inherited form.
```

## Step 1: Deconstruct

Break the subject into its actual constituents.

**Key Questions:**
- What is this actually made of?
- What are the constituent parts?
- What is the actual cost/value of each part?
- What would a physicist say about this?

**Process:**
1. Identify the subject being deconstructed
2. List all commonly stated components (without judgment)
3. For each component, ask "What is THIS actually made of?"
4. Identify what remains when you cannot decompose further (fundamental truths)
5. Map the gap between stated vs. actual components

**Fundamental truths ARE:** Laws of physics, mathematical certainties, empirically verified facts, irreducible requirements.

**Fundamental truths are NOT:** Industry best practices, "how it's always been done," market prices, conventional wisdom.

## Step 2: Challenge

For every stated constraint, ask: "Is this a law of physics, or is it a choice someone made?"

### Constraint Classification Table

| Type | Definition | Example | Can Change? |
|------|------------|---------|-------------|
| **Hard** | Physics/reality | "Data can't travel faster than light" | No |
| **Soft** | Policy/choice | "We always use REST APIs" | Yes |
| **Assumption** | Unvalidated belief | "Users won't accept that UX" | Maybe false |

**Rule:** Only hard constraints are truly immutable. Everything else should be challenged.

**For SOFT constraints, ask:**
- Who made this decision and why?
- What would happen if we violated it?
- Is the original reason still valid?

**For ASSUMPTIONS, ask:**
- What evidence supports this?
- Has anyone tested the opposite?
- What would prove this wrong?

**The "Remove It" Test:** If we removed this constraint entirely, what would become possible? If the answer is significant, challenge it.

**Hidden Assumptions:** The most dangerous constraints are those so assumed they are never stated. "Of course we need a database" -- do we?

### Challenge Questions Library

| Domain | Questions |
|--------|-----------|
| **Technical** | Is this a language limitation or a fundamental one? Could different tech remove this constraint? |
| **Business** | Is this budget fixed or just "budget for the obvious solution"? Is the timeline real or arbitrary? |
| **Security** | Is this preventing a real or theoretical attack? Is this security or security theater? |
| **UX** | Have we tested with actual users? Are we confusing user needs with user habits? |
| **Architecture** | Is this pattern required or just familiar? What if we had never seen the current solution? |

## Step 3: Reconstruct

Build an optimal solution from scratch using only fundamental truths and hard constraints.

**Core Principle:** "If we knew nothing about how this is currently done, and only knew the fundamental truths, what would we build?"

**Process:**
1. State ONLY the hard constraints (exclude soft constraints and assumptions)
2. Define the function to optimize (outcome, not method)
3. Blank-slate design: generate 3+ approaches without filtering for feasibility
4. Cross-domain synthesis: what industry has solved an analogous problem differently?
5. Evaluate each solution against function, not form

**Common Reconstruction Patterns:**
- "Do we even need this?" -- Eliminates entire components
- "Different technology, same function" -- Form changes, function preserved
- "Combine steps" -- Removing soft constraints allows merging previously separate steps

## Output Format

```markdown
## First Principles Analysis: [Topic]

### Deconstruction
- **Constituent Parts**: [List fundamental elements]
- **Actual Values**: [Real costs/metrics, not market prices]

### Constraint Classification
| Constraint | Type | Evidence | If Removed? |
|------------|------|----------|-------------|
| [X] | Hard/Soft/Assumption | [Why] | [What becomes possible] |

### Reconstruction
- **Hard Constraints Only**: [The immutable facts]
- **Function to Optimize**: [Outcome, not method]
- **Optimal Solution**: [Built from fundamentals]
- **Cross-Domain Insight**: [What other field solved this differently?]

### Key Insight
[One sentence: what assumption was limiting us?]
```

## Examples

### Example 1: Architecture Decision
**Problem:** "We need microservices because that's how modern apps are built"

1. **Deconstruct**: What does this app actually need? (team size: 3, scale: moderate, complexity: medium)
2. **Challenge**: Is "microservices" a hard constraint? No -- reasoning by analogy from large companies
3. **Reconstruct**: A modular monolith optimizes for our actual constraints (small team, moderate scale)

### Example 2: Security Assessment
**Problem:** "The firewall protects the internal network"

1. **Deconstruct**: What is the firewall actually doing? (packet filtering on specific ports)
2. **Challenge**: Does packet filtering = protection? What about authorized ports? Insider threats?
3. **Reconstruct**: Protection requires defense in depth -- firewall is one layer, not "the" protection

### Example 3: Cost Optimization
**Problem:** "Cloud hosting costs $10,000/month -- that's just what it costs"

1. **Deconstruct**: What are we paying for? (compute, storage, bandwidth, managed services)
2. **Challenge**: Is managed Kubernetes a hard requirement? Is this region required?
3. **Reconstruct**: Actual compute needs = $2,000. The other $8,000 is convenience we chose to pay for

## Principles

1. **Physics First** -- Real constraints come from physics/reality, not convention
2. **Function Over Form** -- Optimize what you are trying to accomplish, not how it is traditionally done
3. **Question Everything** -- Every assumption is guilty until proven innocent
4. **Cross-Domain Synthesis** -- Solutions from unrelated fields often apply
5. **Rebuild, Don't Patch** -- When assumptions are wrong, start fresh rather than fixing

## Anti-Patterns

- **Reasoning by Analogy**: "Company X does it this way, so should we"
- **Accepting Market Prices**: "$600/kWh for batteries" without checking material costs
- **Form Fixation**: Improving the suitcase instead of inventing wheels
- **Soft Constraint Worship**: Treating policies as physics
- **Premature Optimization**: Optimizing before understanding fundamentals

---

**Attribution:** Framework derived from Elon Musk's first principles methodology as documented by James Clear, Mayo Oshin, and public interviews.

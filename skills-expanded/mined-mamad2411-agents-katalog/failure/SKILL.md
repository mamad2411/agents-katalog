---
name: failure
description: "Engineering philosophy - form follows failure, learning from case studies"
---

# Henry Petroski - Engineering Design Philosophy

Apply Petroski's insights from "To Engineer Is Human" and "Design Paradigms" to understand how failure shapes good design.

## Core Philosophy

### Form Follows Failure

The famous dictum "form follows function" is wrong. Form follows *failure*.

**Petroski's insight**: Design evolves not from imagining ideal function, but from correcting past failures. Every successful design is a response to a previous failure.

```
BAD THINKING:  "What should this do?" → Design
GOOD THINKING: "What has failed before?" → Design that prevents that failure
```

### The Success-Failure Paradox

Success breeds complacency; complacency breeds failure.

```
SUCCESS
   ↓
"We've got this figured out"
   ↓
Reduced vigilance
   ↓
Ignored warning signs
   ↓
FAILURE
   ↓
"How could this happen?"
   ↓
Deep investigation
   ↓
Improved design
   ↓
SUCCESS (cycle repeats)
```

**Rule**: The most dangerous time is right after a string of successes.

## Prescriptive Rules

### Case Study Methodology

Learn from specific failures, not abstract principles.

```
ABSTRACT (weak):
"Always validate input"

CASE STUDY (strong):
"The 2016 incident where unvalidated JSON crashed production
taught us to validate at the boundary. Here's the exact pattern
that failed and the fix that prevented recurrence."
```

**Application**:
- Document failures with full context
- Reference specific incidents in code comments
- Build institutional memory of what went wrong

### Constraints as Design Drivers

Constraints are not obstacles - they're the source of innovation.

```
WITHOUT CONSTRAINT          WITH CONSTRAINT
─────────────────          ────────────────
Infinite solutions         Focused solutions
Analysis paralysis         Clear direction
Gold-plating              Elegant simplicity
```

**Petroski's examples**:
- The pencil's hexagonal shape: prevents rolling, reduces material
- Bridge designs: span limits force structural innovation
- Software: memory limits drove efficient algorithms

**Application**:
```yaml
When facing a constraint:
  1. Don't fight it immediately
  2. Ask: "What innovation does this force?"
  3. The constraint may be the feature
```

### Anticipating Failure Modes

Before building, enumerate how it could fail.

```
For any component, ask:
├── How could this fail silently?
├── How could this fail catastrophically?
├── How could this fail intermittently?
├── How could success in one area cause failure in another?
└── What would the post-mortem say?
```

**Pre-mortem technique**: Write the post-mortem *before* shipping. What would you regret not checking?

### Evolution Over Revolution

Good design is incremental refinement, not revolutionary leaps.

```
REVOLUTIONARY (risky):
"Let's rewrite everything from scratch"

EVOLUTIONARY (Petroski-approved):
"Let's fix the specific failure mode while preserving what works"
```

**The pencil lesson**: The modern pencil evolved over 400 years through thousands of small improvements, each fixing a specific problem.

## Code Application

### Document the "Why Not"

```javascript
// BAD: Only documents what
function processPayment(amount) {
  // Process the payment
}

// GOOD: Documents failures that shaped design
function processPayment(amount) {
  // Idempotency key required after 2023 duplicate charge incident.
  // Timeout set to 30s after 2022 gateway slowdown caused cascading failures.
  // Retry logic added after network blip lost $50k in transactions.
}
```

### Design Reviews Should Ask

| Question | Petroski Principle |
|----------|-------------------|
| "What has failed before in similar systems?" | Form follows failure |
| "Are we overconfident from recent success?" | Success-failure paradox |
| "What constraint is actually helping us?" | Constraints drive innovation |
| "How will this fail?" | Failure mode analysis |
| "Is this a rewrite or a refinement?" | Evolution over revolution |

### Post-Mortem Template (Petroski Style)

```markdown
## Failure Report: [Incident Name]

### What Failed
Specific description of the failure mode.

### The Form That Followed Function
What design decision seemed reasonable at the time?

### The Form That Should Follow Failure
What design change prevents this class of failure?

### Constraints Revealed
What constraints did we discover that we should embrace?

### Similar Historical Failures
What other systems failed this way? What can we learn?

### Success That Preceded This
Were we overconfident? What success masked the risk?
```

## Anti-Patterns

| Pattern | Why It's Wrong | Petroski Fix |
|---------|----------------|--------------|
| "That won't happen to us" | Ignores case studies | Study similar failures |
| "We've never had that problem" | Success-failure paradox | That's when it happens |
| "Let's remove that constraint" | Constraints drive innovation | Ask what you'd lose |
| "Clean slate redesign" | Revolution over evolution | Incremental improvement |
| "The old system was dumb" | Disrespects evolved design | Understand why it evolved |

## Review Checklist

Before shipping:

- [ ] What failures shaped this design? (Can you cite them?)
- [ ] What could fail that we haven't seen yet?
- [ ] Are we overconfident from recent success?
- [ ] Which constraints are actually helping?
- [ ] Is this evolution (good) or revolution (risky)?
- [ ] Would the post-mortem be embarrassing?

## Petroski Score

| Score | Meaning |
|-------|---------|
| 10 | Design explicitly shaped by failure analysis, constraints embraced |
| 7-9 | Failure modes considered, some case study awareness |
| 4-6 | Functional but no failure history awareness |
| 0-3 | "Form follows function" thinking, overconfident |

## Key Quotes

> "The most significant engineering failures usually occur in areas where prior success has encouraged the raising of stakes without adequate understanding of the risks."

> "Form follows failure, not function."

> "Successful design is not about getting things right the first time but about not making the same mistake twice."

## Integration

Combine with:
- `/safety` - Systematic failure prevention
- `/resilience` - Designing for antifragility
- `/security-mindset` - Security as failure anticipation

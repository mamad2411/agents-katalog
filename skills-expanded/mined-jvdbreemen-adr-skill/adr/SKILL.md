---
name: adr
description: 'Architecture Decision Record management. Creates, maintains, and enforces architectural decisions. Ensures code changes align with documented decisions. Includes anti-rationalization guards and verification gates.'
license: MIT
---

# ADR Skill: Architecture Decision Records

## Overview

Systematic creation, maintenance, and enforcement of Architecture Decision Records (ADRs). ADRs document significant architectural choices with context, alternatives considered, and consequences. They are living documentation that helps current and future developers understand why the system is built the way it is.

## When to Use

### Automatic Triggers

Use this skill **automatically** when:

- **Code review or PR analysis** -- verify changes align with existing ADRs
- **Major code changes** -- check if a new ADR is needed
- **Architecture planning** -- document decisions before implementation
- **Refactoring proposals** -- validate against existing decisions or create new ADR
- **Technology selection** -- choosing libraries, frameworks, protocols, storage

### Explicit Requests

Activate when user mentions:
- "Create an ADR", "Document this decision", "Architecture decision"
- "Why did we choose...", "Alternatives considered"
- "Should we switch from X to Y"

### Decision Triggers

Create a new ADR when a decision:
- Has **long-term impact** on architecture
- Affects **multiple components** or modules
- Involves **trade-offs** between viable alternatives
- **Constrains future** development choices
- Addresses a **significant technical challenge**
- **Changes existing** architectural patterns

### Do NOT Create ADR For

- Bug fixes that don't change architecture
- Refactoring maintaining same structure
- Configuration changes
- Documentation updates
- Minor features within existing patterns
- Temporary workarounds or experiments

---

## Anti-Rationalization Guards

AI agents find excuses to skip rigorous documentation. Catch yourself.

| Thought | Reality | Required Action |
|---------|---------|-----------------|
| "This decision is obvious" | Obvious to you now, not to someone in 6 months | Document it. Include the "obvious" reasoning |
| "There's only one option" | You haven't looked hard enough | List at least 2 alternatives, even if clearly inferior |
| "I'll document it later" | You won't. Context fades fast | Write the ADR now, mark as Proposed |
| "It's just a library choice" | Libraries shape architecture for years | ADR if it affects >1 component |
| "The code speaks for itself" | Code shows WHAT, never WHY | ADR captures the WHY |
| "This is temporary" | Nothing is more permanent than a temporary solution | Document the intent to replace, with criteria |
| "Everyone knows this" | New contributors don't. Future-you doesn't | Write for the person who joins next month |
| "The PR description covers it" | PR descriptions are buried in git history | ADR is discoverable, indexed, and referenced |
| "I already explained this in chat" | Chat is ephemeral | If it mattered enough to discuss, it matters enough to record |
| "This is too small for an ADR" | Check the triggers above. If it fits, write it | Trust the triggers, not your instinct to skip |

**The test:** If removing this decision would confuse a future developer, write the ADR.

---

## Verification Gates

Every ADR must pass these gates before acceptance. Do not mark an ADR as Accepted until all gates clear.

### Gate 1: Completeness

```
- [ ] Problem statement explains WHAT and WHY
- [ ] Decision is a clear, unambiguous statement
- [ ] At least 2 alternatives documented with pros/cons
- [ ] Each rejected alternative has "Why Not Chosen" with specific reasoning
- [ ] Consequences section has both positive AND negative items
- [ ] Risks identified with concrete mitigations
```

**Fail condition:** Any unchecked item. No exceptions.

### Gate 2: Evidence

```
- [ ] Claims are backed by measurements, not adjectives
      ("saves 5KB RAM" not "saves memory")
- [ ] Constraints are verified, not assumed
      ("ESP8266 has 40KB RAM" not "limited memory")
- [ ] Trade-offs are quantified where possible
      ("~10% more code verbosity" not "slightly more verbose")
- [ ] Implementation references exist (file paths, code examples)
```

**Fail condition:** Any vague claim without supporting evidence. Go measure.

### Gate 3: Clarity

```
- [ ] A developer unfamiliar with the project can understand the core trade-off
- [ ] Technical terms are explained on first use
- [ ] No jargon without definition
- [ ] Code examples demonstrate the pattern (not just describe it)
- [ ] Negative consequences are honest, not minimized
```

**Fail condition:** Read the ADR as if you've never seen the codebase. If anything is unclear, rewrite.

### Gate 4: Consistency

```
- [ ] No contradiction with existing accepted ADRs
- [ ] If superseding, old ADR is updated (status only, not content)
- [ ] Related ADRs are cross-referenced
- [ ] File naming follows convention: ADR-XXX-kebab-case-title.md
- [ ] Added to docs/adr/README.md index
```

**Fail condition:** Contradicts existing ADR without superseding it, or missing from index.

---

## ADR Template

```markdown
# ADR-XXX: [Concise Decision Title]

**Status:** Proposed | Accepted | Deprecated | Superseded by ADR-XXX
**Date:** YYYY-MM-DD
**Decision Maker:** [Agent | User: Name | Team Discussion]

## Context

### Problem Statement
[What problem are we solving? What is the situation?]

### Constraints
[Hardware, memory, security, compatibility, budget, timeline]

## Decision

[Clear statement of the choice made]

### Why This Choice
[Reasoning. Reference measurements and evidence.]

### Implementation Summary
[High-level description of how this is implemented]

## Alternatives Considered

### Alternative 1: [Name]
**Description:** [What is this alternative?]

**Pros:**
- [Specific benefit]

**Cons:**
- [Specific drawback]

**Why Not Chosen:** [Clear, evidence-based explanation]

### Alternative 2: [Name]
[Same structure. Minimum 2 alternatives required.]

## Consequences

### Positive
- **[Category]:** Specific benefit with evidence

### Negative
- **[Category]:** Specific drawback, why accepted

### Risks & Mitigation
- **Risk:** [Description]
  **Likelihood:** [Low/Medium/High]
  **Mitigation:** [Concrete action]

## Implementation Notes

### Key Files Affected
- `path/to/file.ext` -- [What changes]

### Code Examples
[Show the pattern, not just describe it]

### Migration Required
[Steps to migrate existing code, or "None"]

## Verification

### How to Verify
[Commands, checks, or criteria to confirm this decision is followed]

### What Breaks If Violated
[Concrete consequences of ignoring this decision]

## Related Decisions

- **Depends on:** ADR-XXX
- **Related to:** ADR-XXX
- **Supersedes:** ADR-XXX (if applicable)

## References

- [Links to docs, specs, benchmarks, discussions]
```

---

## Naming Convention

```
Format: ADR-XXX-short-descriptive-title.md
Location: docs/adr/

Examples:
  ADR-001-local-first-sqlite.md
  ADR-002-mcp-first-architecture.md
  ADR-003-tauri-desktop-shell.md

Rules:
  - Zero-padded sequential number (001, 002, 003)
  - Kebab-case title
  - ADR prefix uppercase
  - Never reuse numbers from deprecated/superseded ADRs
  - No gaps in numbering
```

---

## ADR Categories

- **Platform & Runtime** -- Desktop shell, frameworks, language choices
- **Data & Storage** -- Database, schema, indexing, search
- **Protocol & Integration** -- MCP, API design, transport
- **Editor & Writing** -- Text editing, autosave, conflict resolution
- **Publishing & Output** -- Pipelines, channels, deployment
- **UI & Design** -- Component library, design tokens, layout
- **Security & Privacy** -- Local-first, access control, data handling
- **Search & Discovery** -- Full-text, semantic, hybrid strategies
- **Build & Development** -- Tooling, CI/CD, testing

---

## Workflow

### Before Making Architectural Changes

1. Review existing ADRs in `docs/adr/README.md`
2. Search for related decisions
3. Check if change conflicts with existing ADRs
4. Determine if new ADR needed (check triggers above)
5. Check anti-rationalization table -- are you skipping this step?

### During Implementation

1. Create ADR with Status: **Proposed**
2. Get next sequential number from `docs/adr/`
3. Write comprehensive ADR using the template
4. Run all 4 verification gates
5. Reference ADR in code where the pattern is implemented

### After Implementation

1. Update Status: Proposed -> **Accepted**
2. Add implementation date
3. Link to PR/commit
4. Update `docs/adr/README.md` index
5. Verify code examples match actual implementation

### Superseding an ADR

1. Create new ADR explaining the change
2. Reference original ADR and explain why it's being replaced
3. Update old ADR status to "Superseded by ADR-XXX"
4. **Never modify** the original decision or context
5. Update README index for both ADRs

---

## Initial Codebase Analysis

### First-Time Use

On first use in an existing codebase, perform architectural analysis to identify undocumented decisions.

**Step 1: Identify Patterns**
Scan the codebase for architectural choices in each category (platform, data, protocol, UI, etc.)

**Step 2: Ask Critical Questions**
For each pattern:
- WHY was this approach chosen? (context, constraints)
- WHAT alternatives exist? (at least 2-3 viable options)
- WHY were alternatives rejected? (specific technical reasons)
- WHAT are the consequences? (benefits, costs, risks)
- HOW is this implemented? (code examples, key files)

**Step 3: Generate ADRs**
For each undocumented decision:
1. Use explore agent to understand the pattern
2. Review code, comments, git history for context
3. Research alternatives
4. Create ADR with Status: Accepted (since already implemented)
5. Link to actual implementation

**Step 4: Prioritize**
Start with foundational decisions that affect multiple components, constrain future choices, or are non-obvious.

---

## Code Review Integration

### Automatic Checks During Review

1. Do changes violate any existing ADRs?
2. Do changes require a new ADR?
3. Are ADR references in code accurate?

### Review Comment Patterns

```
VIOLATION: "This change violates ADR-004 (Static Buffer Allocation).
           See docs/adr/ADR-004-static-buffer-allocation.md"

ALIGNED:   "This follows ADR-002 (MCP-First Architecture).
           Good use of tool-based interface."

MISSING:   "This introduces a new architectural pattern (vector search).
           Please create an ADR documenting the decision."
```

### PR Checklist

```markdown
## ADR Compliance

- [ ] Changes reviewed against existing ADRs
- [ ] No violations of architectural decisions
- [ ] New ADR created if needed
- [ ] ADR status updated if implementing existing ADR
- [ ] docs/adr/README.md updated if new ADR added
```

---

## Human Decision Documentation

When a user explicitly makes an architectural choice, mark it clearly:

```markdown
**Decision Maker:** User: [Name]

## Decision
**User Decision:** [What the user chose]

The user explicitly chose [X] over [Y] because [stated reason].

## Alternatives Considered
### Alternative 1: [What was presented]
**User Feedback:** "[Direct quote or paraphrase of reasoning]"
```

This preserves the human reasoning chain. Never modify a human decision ADR without the user's explicit approval.

---

## ADR Index (docs/adr/README.md)

Maintain an index as the navigation hub for all ADRs.

**Required sections:**
1. What are ADRs (brief explanation for new readers)
2. Quick Navigation by category with counts
3. Full categorized ADR index
4. When to create an ADR (link to triggers)
5. Architectural dependencies (which ADRs depend on which)

**Update process:** When adding a new ADR, always update the index, category count, and cross-references in related ADRs.

---

## Quick Reference

### Creation Checklist

```
- [ ] Next sequential number assigned
- [ ] Filename: ADR-XXX-kebab-case-title.md
- [ ] Status, Date, Decision Maker present
- [ ] Context explains the problem clearly
- [ ] At least 2 alternatives documented
- [ ] Pros/cons for each alternative
- [ ] "Why Not Chosen" for each rejected alternative
- [ ] Consequences: positive AND negative
- [ ] Risks with mitigations
- [ ] Code examples included
- [ ] Related ADRs referenced
- [ ] Added to docs/adr/README.md
- [ ] All 4 verification gates passed
```

### Common Mistakes

```
- Writing "We should use X" without explaining why
- Skipping alternatives ("This is the only way")
- No code examples for technical decisions
- Vague consequences ("It will be better")
- Hiding negative consequences
- Modifying accepted ADRs instead of superseding
- Not updating the README index
- Using jargon without defining it
- Skipping measurements ("faster" vs "68.5% reduction")
```

---

## Resources

- [ADR Best Practices](https://adr.github.io/)
- [Michael Nygard's Original Post](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [MADR Template](https://github.com/adr/madr)
- [Joel Parker Henderson Collection](https://github.com/joelparkerhenderson/architecture-decision-record)

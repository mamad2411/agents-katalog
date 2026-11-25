---
name: architectural-discovery
description: Guides users through software design decisions by asking targeted questions about scalability, complexity, and infrastructure. Use when a user asks for architectural patterns, system design advice, or project planning.
---

# Architectural Discovery & Design Strategy

Use this skill to help users choose between patterns like Microservices, Monoliths, Event-Driven Architecture, CQRS, or Hexagonal Design.

**Important:** Always refer to `REFERENCE.md` in this directory for detailed technical descriptions of these patterns when providing explanations to the user.

## Discovery Workflow
Ask the following targeted questions to narrow down the best approach. Do not ask all at once; choose the 2-3 most relevant to the user's current project stage.

### 1. Scalability & Load
- **Question:** "What is the expected user load? Is this an internal tool for 50 people or a global app for millions?"
- **Logic:** High load → *Microservices*; Low load → *Layered/Monolith*.

### 2. Business Complexity
- **Question:** "Is the logic mostly CRUD (save/retrieve), or are there complex, interdependent business rules?"
- **Logic:** High complexity → *Domain-Driven Design (DDD)*; Simple → *Layered*.

### 3. Data & Consistency
- **Question:** "Does data need to be consistent instantly, or is eventual consistency acceptable?"
- **Logic:** Reactive/Async → *Event-Driven (EDA)*; Strict → *Monolith*.

### 4. Read/Write Asymmetry & Auditing
- **Question:** "Is your system read-heavy with complex queries, or do you need a strict, immutable audit trail of all state changes?"
- **Logic:** High read/write disparity or strict audit needs → *CQRS & Event Sourcing*.

### 5. Team Size and Developer Skillset
- **Question:** "How large is your engineering team, and what is their experience level with distributed systems?"
- **Logic:** Small team (1-5 devs) or lack of DevOps experience → *Strongly* weight towards Monolith or Layered. Very large/distributed team → *Microservices*.

### 6. Time-to-Market vs. Long-term Polish
- **Question:** "Are you trying to validate an MVP quickly (weeks/months) or are you rewriting a legacy system for long-term scalability?"
- **Logic:** Fast MVP → *Layered (Monolith)*. Long-term rebuild → *Microservices* or *Event-Driven*.

### 7. Deployment Constraints & Infrastructure
- **Question:** "Will this system be deployed heavily on public Cloud providers (AWS, Azure) or does regulatory compliance restrict you to on-premises hardware?"
- **Logic:** Public cloud embraced → Consider *Serverless Architecture*. On-premises restricted → *Layered* or *Event-Driven* on VMs/bare-metal.

## Recommended Patterns Reference
- **Microservices:** Best for independent scaling and large teams.
- **Event-Driven:** Best for high-throughput, reactive systems like Fintech.
- **CQRS & Event Sourcing:** Best for high-performance read/write separation and audit trails.
- **Hexagonal:** Best for systems with many third-party integrations.
- **Serverless:** Best for highly scalable, zero-ops applications on public cloud.

## Signal Assessment
Before outputting a recommendation, assess how clearly the answers point to a single pattern:

- **Clear signal** — answers consistently align with one pattern (e.g. small team + simple CRUD + fast MVP all point to Layered Monolith)
- **Mixed/unclear signal** — answers are ambiguous, contradictory, or span multiple patterns (e.g. high load but small team, or complex rules but tight deadline)

If the signal is unclear and fewer than 3 questions have been asked, prefer asking one more targeted clarifying question rather than jumping to multiple options.

## Output Format

### Mode A — Clear signal: single recommendation
1. **The "Why":** Connect the pattern back to the user's specific answers.
2. **The Trade-off:** Mention at least one complexity cost (e.g., "Microservices increase operational overhead").

### Mode B — Mixed/unclear signal: top 3 options
Open with a brief note explaining why multiple options are being shown (e.g. "Your answers suggest competing priorities — here are the top 3 patterns that fit your context, ranked by fit").

Then present a ranked list:

1. **[Primary recommendation]** — best overall fit given the signals
   - *Aligns with:* which of the user's answers support this
   - *Key trade-off:* the main cost or risk

2. **[Strong alternative]** — best fit if [specific condition from their answers]
   - *Aligns with:* which answers support this
   - *Key trade-off:* the main cost or risk

3. **[Worth considering]** — fits if [specific condition from their answers]
   - *Aligns with:* which answers support this
   - *Key trade-off:* the main cost or risk

Close with a single follow-up question that, if answered, would narrow it to one recommendation.

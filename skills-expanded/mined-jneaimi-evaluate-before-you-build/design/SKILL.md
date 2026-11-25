---
name: design
description: >
  Solution design skill based on Bloom's AI Collaboration model. Use when the
  user says /design, wants to design a solution, compare architectural options,
  evaluate tradeoffs, or produce a solution design document before building.
  Also trigger on phrases like "design the solution", "how should we architect
  this", "system design", "architecture review", "choose between approaches",
  "evaluate tradeoffs", "NFRs", or "solution shape". Produces an ADR-style
  document — not code.
---

# Solution Design Checkpoint (/design)

A solution architect's checkpoint. Before code gets written, shape the
solution: boundaries, components, data flow, tradeoffs, failure modes. The
deliverable is a solution design document, not working code.

**Core principle:** Options without honest tradeoffs are just preferences.
Never produce a "chosen approach" until two or more real alternatives have
been written down and compared against named non-functional requirements.

**Interaction model:** Scan-first like `/prebuild` (context matters for
architecture), then evaluate with `AskUserQuestion` options like `/think`.
This is the bridge skill: it sits between strategy (`/think`), planning
(`/plan`), and implementation (`/prebuild`).

## How It Differs from the Others

| | /design | /think | /plan | /prebuild |
|---|---------|--------|-------|-----------|
| **Focus** | Solution shape / architecture | Strategic decision | Delivery / timeline | Code generation |
| **Output** | ADR / design doc | Domain-adapted doc | Phased plan | Working code |
| **Key work** | Options + tradeoffs + NFRs | Evaluate + research | Sequence + own | Scan + build |
| **Scans code?** | Yes (context for options) | Sometimes | Sometimes | Yes |

Use `/design` after `/think` has confirmed *why*, and before `/prebuild`
generates code. On small features, skip straight to `/prebuild`. On
anything non-trivial or multi-component, design first.

## Framework Reference

```
┌─────────────────────────────────────────┐
│  Level 5: Evaluate     HUMAN → AI      │  Problem, NFRs, chosen option
│  Level 4: Analyze      HUMAN ↔ AI      │  Options + tradeoffs (core)
├─────────────────────────────────────────┤
│  Level 3: Apply        AI → HUMAN      │  Produce design doc
│  Level 2: Understand   AI → HUMAN      │  Walk through the design
│  Level 1: Remember     AI alone        │  Save as ADR
└─────────────────────────────────────────┘
```

## Commands

### /design [topic] — Start design session
Begin a new solution design for the described problem.

### /design compare [A] vs [B] — Fast option compare
Skip to Level 4. Two named options, generate tradeoff matrix.

### /design review [file] — Review existing design
Evaluate an existing design doc against the framework. Flag missing NFRs,
unexamined alternatives, hand-wavy tradeoffs.

---

## Step 1: Scan the Context (Silent)

Before asking questions, understand what already exists. Use Glob, Grep,
Read for 1–2 minutes:

- **Existing architecture**: relevant services, modules, interfaces
- **Tech stack**: framework, data stores, infra primitives already in use
- **Prior decisions**: existing ADRs, design docs, CLAUDE.md notes
- **Integration points**: what this solution will touch

Output a brief scan summary:

> **Context scan:**
> - Stack: [detected]
> - Existing components this touches: [list]
> - Relevant prior decisions: [ADR / doc reference if found]
> - Natural extension points: [if any]

---

## Step 2: Level 5 — Evaluate (6 Design Questions)

Split into two rounds of 3 questions each.

### Round 1: Problem, NFRs, Boundaries

```
AskUserQuestion (3 questions):

Question 1 — PROBLEM (header: "Problem")
  "What's the actual problem being solved, in one sentence?"
  Options — propose framings based on user's request:
    - "Capability gap — [specific capability] doesn't exist today"
    - "Quality gap — [capability] exists but fails on [axis]"
    - "Cost/complexity gap — [capability] works but is too [expensive/slow/fragile]"
    - "Integration gap — [system A] and [system B] don't talk"

Question 2 — NFRs (header: "Must hold")
  "Which non-functional requirements are load-bearing?"
  multiSelect: true
  Options — propose based on problem type:
    - "Latency (user-facing responsiveness)"
    - "Throughput (volume / concurrency)"
    - "Availability / uptime SLO"
    - "Security / tenant isolation"
    - "Data consistency (strong vs eventual)"
    - "Cost ceiling"
    - "Compliance / audit"
    - "Operability (observability, debuggability)"

Question 3 — BOUNDARIES (header: "Scope")
  "How broad is this design?"
  Options — propose scope shapes:
    - "Single component — one service/module, internal shape" (Recommended if narrow)
    - "Feature slice — multiple components end-to-end for one capability"
    - "Subsystem — reshape a domain area"
    - "Cross-cutting — changes that ripple across the system"
```

### Round 2: Options, Risks, Reversibility

```
AskUserQuestion (3 questions):

Question 4 — OPTIONS (header: "Candidates")
  "Which candidate approaches are on the table?"
  multiSelect: true
  Options — propose from scan + domain knowledge:
    - "Option A: [scan-informed approach A]" (Recommended)
      preview: one-paragraph sketch of the shape
    - "Option B: [scan-informed approach B — meaningfully different]"
      preview: one-paragraph sketch
    - "Option C: [third alternative, often the 'do nothing' or 'buy not build']"
      preview: one-paragraph sketch
    - "None of these — let's brainstorm"

Question 5 — FAILURE MODES (header: "Fails when")
  "Where is this design most likely to fail?"
  multiSelect: true
  Options — propose based on problem + NFRs:
    - "Under load spike"
    - "On partial failure of a dependency"
    - "On data skew / unexpected input shape"
    - "On operator error / misconfiguration"
    - "On scale boundaries (volume, users, tenants)"
    - "On security boundary violation"

Question 6 — REVERSIBILITY (header: "Reversibility")
  "How reversible is this decision?"
  Options:
    - "Easily reversible — swap later without disruption"
    - "Hard to reverse — becomes load-bearing infra"
    - "One-way door — committing means living with it"
```

### Domain-adapted option examples

**Capability gap (new feature/system):**
- Options: "Build inline in existing service" / "New dedicated service" / "Vendor/SaaS" / "Library in a shared module"

**Quality gap (performance, reliability):**
- Options: "Cache layer" / "Rewrite hot path" / "Horizontal scale" / "Redesign data model"

**Integration gap:**
- Options: "Direct sync API" / "Event bus" / "Shared database read" / "Batch ETL"

**Data consistency:**
- Options: "Single-writer with queue" / "Two-phase commit" / "Event sourcing" / "Eventual with reconciliation"

---

## Step 3: Level 4 — Analyze (The Core Work)

This is the heart of `/design`. Produce an options matrix. For each option
the human selected in Q4, analyze against the NFRs from Q2 and failure
modes from Q5.

### Options matrix

```
| Dimension        | Option A            | Option B            | Option C            |
|------------------|---------------------|---------------------|---------------------|
| Shape            | [1-line description] | [1-line]            | [1-line]            |
| [NFR 1 from Q2]  | [honest assessment] | [honest assessment] | [honest assessment] |
| [NFR 2 from Q2]  | ...                 | ...                 | ...                 |
| Failure under... | ...                 | ...                 | ...                 |
| Operational cost | ...                 | ...                 | ...                 |
| Reversibility    | ...                 | ...                 | ...                 |
| Effort estimate  | S / M / L / XL      | S / M / L / XL      | S / M / L / XL      |
```

**Rules for honest tradeoffs:**
- Every option has downsides. If an option has no cons in your matrix,
  you haven't thought hard enough.
- Prefer concrete assertions ("~50ms p99 read latency", "requires a new
  message queue") over vague ones ("fast", "simple").
- If tradeoffs are unknowable without a spike, say so — don't bluff.

### Flag new decisions

If the options matrix reveals a decision the human hasn't made (e.g., "Option
A requires choosing between Redis and Memcached"), LOOP BACK to Level 5:

```
AskUserQuestion (1 question):

Question: "[New sub-decision surfaced by the options analysis]"
Header: "New decision"
Options:
  - "[Choice A — with implication]"
  - "[Choice B — with implication]"
```

Then continue Level 4 with the new constraint in place.

### Chosen approach

After the matrix is complete, use `AskUserQuestion` once more:

```
AskUserQuestion (1 question):

Question: "Which option do we commit to?"
Header: "Decision"
Options (populate with the specific options analyzed):
  - "Option A — [one-line rationale the matrix supports]" (Recommended based on NFRs)
  - "Option B — [one-line rationale]"
  - "Option C — [one-line rationale]"
  - "Need more investigation — spike first, decide after"
```

Do NOT mark an option "recommended" unless the matrix genuinely supports it.
If tradeoffs are close, say so and let the human choose.

---

## Step 4: Level 3 — Produce the Design Doc

Produce an ADR-style solution design document:

```markdown
# Solution Design: [Title]

## Context
[Why this is being designed now — tie to prior decisions if any.
Reference scan findings: existing components, prior ADRs, constraints.]

## Problem
[One-sentence problem statement from Q1.]

## Non-functional requirements
[NFRs from Q2 with specific targets where possible — e.g.,
"p95 latency < 200ms", "99.9% availability", "PCI-DSS scope excluded".]

## Scope
**In:** [from Q3]
**Out:** [explicit exclusions — prevent scope creep]

## Options considered

### Option A — [name]
[1–2 paragraphs: shape, key components, data flow]

### Option B — [name]
[1–2 paragraphs]

### Option C — [name]
[1–2 paragraphs]

## Tradeoff matrix
[The matrix from Level 4]

## Decision
**Chosen:** Option [X]

**Rationale:**
[Why this option best balances the NFRs and constraints. Reference the matrix.]

**Rejected alternatives and why:**
- Option [Y]: [honest reason]
- Option [Z]: [honest reason]

## Consequences
**Positive:**
- [consequence]

**Negative (accepted):**
- [consequence we're choosing to live with]

**Neutral / watch:**
- [thing to monitor or revisit]

## Failure modes & responses
| Failure mode (from Q5) | Detection | Response |
|-----------------------|-----------|----------|
| [mode]                | [signal]  | [action] |

## Components & data flow
[Bullet list or sketch in text. If a diagram would help, note:
"→ render with /diagram after approval".]

## Open questions
- [Question that needs answering before build]
- [Question that can wait until later phase]

## Reversibility
[From Q6 — note explicit exit criteria if reversible,
or "one-way door — confirm before building" if not.]

## Next steps
- [ ] [Spike or validation if needed]
- [ ] Handoff to /plan for sequencing, or /prebuild for implementation
```

---

## Step 5: Level 2 — Walk Through the Design

After producing the doc, explain:
- Why the chosen option wins (reference specific cells in the matrix)
- What the biggest accepted downside is, and why we accept it
- Which failure mode we're most exposed to, and what the mitigation is
- What still needs to be decided (open questions) before building

Tailor depth:
- **Senior engineer / architect:** Highlights of non-obvious tradeoff choices only
- **Implementer who will build it:** Component-by-component walkthrough
- **Non-technical stakeholder:** Problem → decision → consequences, skip internals

---

## Step 6: Level 1 — Save as ADR

Use `AskUserQuestion` for destination:

```
AskUserQuestion (1 question):

Question: "Where should we save this design?"
Header: "Save to"
Options:
  - "Vault: ~/SecondBrain/04-knowledge/decisions/YYYY-MM-DD-[slug].md" (Recommended)
  - "Project repo: docs/adr/NNNN-[slug].md"
  - "Both vault and repo"
  - "Don't save — this was a thought exercise"
```

Always include:
- Frontmatter: `type: adr`, `status: proposed | accepted | superseded`,
  `date: YYYY-MM-DD`, `decides: [one-line]`, `supersedes: [prior ADR if any]`
- Stable slug (kebab-case)
- Cross-links to related ADRs, the `/think` or `/plan` session that led
  here, and the `/prebuild` session that will implement it

---

## Integration with Other Skills

`/design` is the bridge between strategy and code:

```
/think  ──►  /design  ──►  /plan   ──►  /prebuild
(why?)       (what      (when/who?)    (build it)
              shape?)
```

You don't always need all four. Common flows:
- **New system:** /think → /design → /plan → /prebuild
- **Known feature, non-trivial shape:** /design → /prebuild
- **Small feature:** /prebuild alone
- **Strategic choice:** /think alone (may or may not lead to code)

---

## When NOT to Use

- **Problem is trivial** — one component, one obvious approach → /prebuild
- **Decision already documented** — an ADR exists → follow it
- **Still deciding whether to do the thing** — use /think first
- **Just need to sequence known work** — use /plan

---

## Rules

1. **NEVER skip the options matrix.** A design doc with one option is a
   preference, not a design. Minimum two real alternatives analyzed.
2. **NEVER mark an option "recommended" without matrix support.** If the
   tradeoffs are close, say so.
3. **NFRs must be specific.** "Fast" is not an NFR. "p95 < 200ms under
   1000 concurrent users" is.
4. **Every option has cons.** If your matrix shows none, you're flattering
   the preferred option. Try again.
5. **Loop back to Level 5** when the options matrix reveals a new decision.
   Don't fold assumptions into the chosen option silently.
6. **Honor reversibility (Q6).** For one-way doors, require explicit human
   confirmation before marking the ADR `accepted`.
7. **Scan before asking.** Generic options without codebase context are
   guesses. Read the code first.
8. **Handoff cleanly.** End by naming the next skill in the chain (`/plan`
   or `/prebuild`) with the design doc as input.

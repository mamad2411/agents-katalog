---
name: plan-interviewer
description: "This skill should be invoked when the user has a vague or underspecified idea and needs to think it through before building. Triggers include 'I need a plan', 'I have an idea but...', 'help me think this through', 'let's scope this', 'spec this out', 'write a PRD', 'product requirements', 'what am I missing', 'I'm building an MVP', 'am I overcomplicating this', or 'I'm not sure what to build' -- even if they just describe a feature in one sentence with no spec or written requirements yet, or say 'is this feature feasible' or 'I keep changing my mind about what to build.' Not for breaking an existing spec into tasks (use task-breakdown), designing technical architecture (use system-architecture), marketing plans (use imc-plan), or documenting existing features (use technical-writer)."
license: MIT
metadata:
  author: hungv47
  version: "1.1.1"
---

# Plan Interviewer

*Productivity — Standalone skill. Transform shallow feature requests into well-specified plans through multi-round interviews.*

**Core Question:** "What haven't we thought of yet?"

## Inputs Required
- A feature request, problem description, or existing plan/spec file to refine
- Access to AskUserQuestion tool for multi-round interviews

## Output
- Spec file at user-designated path (default: `.agents/spec.md`)

## Quality Gate
Before delivering, verify:
- [ ] All 5 interview dimensions explored (Technical, UX, Business Logic, Architecture, Security)
- [ ] Spec contains concrete decisions, not open-ended options
- [ ] Edge cases documented with explicit handling strategies
- [ ] Open questions list is empty or explicitly deferred with rationale

## Chain Position
Previous: none | Next: `task-breakdown` or `system-architecture`

### Skill Deference
- **Have a FEATURE or PRODUCT to specify?** → Use this skill.
- **Have a declining METRIC to diagnose** (X is at Y, should be Z)? → Use `problem-analysis` (from strategy-skills) instead — it structures metric diagnosis with hypothesis testing, not feature specification.

**Re-run triggers:** When requirements change significantly, when new technical constraints emerge, or when a previous spec leads to implementation blockers.

---

## Before Starting

### Step 0: Product Context
Check for `.agents/product-context.md`. If available, read for product and audience context before interviewing — it prevents asking questions already answered. If missing, this is fine — plan-interviewer can work standalone.

If `.agents/product-context.md` has a `date` field older than 30 days, recommend re-running `icp-research` (from comms-skills) to refresh it.

### Optional Artifacts
| Artifact | Source | Benefit |
|----------|--------|---------|
| `.agents/product-context.md` | icp-research (from `hungv47/comms-skills`) | Product context prevents redundant interview questions |
| `.agents/problem-analysis.md` | problem-analysis (from `hungv47/strategy-skills`) | Root cause context when the feature being spec'd is a solution to a diagnosed problem |

---

## Core Process

### Phase 0: Problem Validation

Before diving into details, challenge the premise. Detailed specs for the wrong feature waste more time than vague specs for the right one.

1. **Right problem?** — Is this the most direct path to the user/business outcome, or are we solving a proxy problem? Restate the actual outcome in one sentence.
2. **What if we did nothing?** — Is there real, measurable pain today, or is this hypothetical? If nobody is complaining, probe why this surfaced now.
3. **What already exists?** — Does existing code, tooling, or process already partially solve this? Map each sub-problem to what's already in place before designing net-new solutions.

If any answer reveals the request is misdirected, recommend the right framing before continuing. If the user confirms they want to proceed anyway, note the concern in the artifact and continue — don't block. One round of "are we building the right thing?" saves multiple rounds of detailed spec work on the wrong thing.

### Phase 1: Context Gathering

1. **Read existing artifacts**: If a plan file or spec file exists (or is mentioned), read it first to understand current state
2. **Identify the domain**: Determine whether this is frontend, backend, full-stack, infrastructure, data, etc.
3. **Assess complexity**: Estimate how many rounds of questioning are needed

### Phase 2: Multi-Round Interview

Conduct interviews using **AskUserQuestion** tool. Each round explores a different dimension. Avoid obvious questions like "what framework?" or "what language?" when context already provides this — they waste interview rounds and erode trust.

**Interview Dimensions (cycle through these):**

#### Technical Implementation
- Data flow edge cases (What happens when X fails mid-operation?)
- State management boundaries (Where does this state live? Who owns it?)
- Concurrency considerations (What if two users do this simultaneously?)
- Migration paths (How do we get from current state to this without breaking things?)
- Performance cliffs (At what scale does this approach break down?)

#### UX & Interaction Design
- Error recovery flows (User does X wrong—then what?)
- Loading/empty/error states (What does the user see during transitions?)
- Undo/redo expectations (Should this be reversible? How far back?)
- Accessibility edge cases (How does a screen reader announce this state change?)
- Mobile-first considerations (Does this gesture conflict with system gestures?)

#### Business Logic & Domain
- Edge case ownership (Who decides what happens when rules conflict?)
- Audit/compliance needs (Does this action need to be logged? For how long?)
- Multi-tenancy implications (How does this behave across different accounts/orgs?)
- Internationalization (Does this text expand 40% in German? RTL support?)

#### Architecture & Tradeoffs
- Consistency vs availability (What's acceptable during network partition?)
- Coupling concerns (Does this create a dependency we'll regret?)
- Testability (How do we verify this works without manual testing?)
- Observability (How do we know this is broken in production?)
- Implementation foresight (What decisions will need to be made mid-build that should be resolved now? What will surprise the implementer? Example: "If enrichment APIs partially fail, do we degrade gracefully or block the whole flow?" — resolve this now, not at 2am during implementation.)

#### Security & Privacy
- Trust boundaries (What if this input comes from an attacker?)
- Data exposure (What PII touches this flow? Who can see it?)
- Rate limiting (What happens if someone calls this 10,000 times?)

### Phase 3: Synthesis & Specification

After sufficient interview rounds (typically 3-7 depending on complexity):

1. **Summarize findings**: Recap the key decisions made during interview
2. **Write specification**: Create or update the spec/plan file with:
   - Clear problem statement
   - Decided approach with rationale
   - Edge cases and their handling
   - Open questions (if any remain)
   - Implementation notes

## Interview Technique Guidelines

### Question Quality Rules

**Avoid obvious questions — they waste rounds and erode credibility:**
- "What tech stack?" (look at the codebase)
- "What should the button say?" (context usually provides this)
- "Should we use TypeScript?" (check existing code)

**Ask revealing questions:**
- "If the webhook fails after the database write succeeds, should we retry, rollback, or alert?"
- "When the cache is stale but the origin is down, do we serve stale or error?"
- "If a user is mid-edit and their session expires, do we save their work or lose it?"

### Question Framing

Frame questions to surface hidden assumptions:
- "What's the worst thing that could happen if..."
- "When you say X, do you mean A or B? Because they have different implications for..."
- "I notice the current system does Y—should we preserve that behavior or is this a chance to fix it?"
- "Who's the angriest user for this feature and what would make them happy?"

### Pacing

- Ask 2-4 questions per round maximum
- Group related questions together
- After each round, briefly acknowledge answers before next questions
- Stop when answers start repeating or user indicates completion

## AskUserQuestion Tool Usage

Structure questions for maximum clarity:

```
Use AskUserQuestion with:
- 2-4 questions per invocation
- Each question has 2-4 concrete options
- Options should represent real tradeoffs, not obvious choices
- Include brief description explaining implications of each option
```

**Example question structure:**
```
Question: "When a background sync fails, how should we handle it?"
Options:
1. Silent retry (3x with backoff) - User unaware, but may see stale data
2. Toast notification - User informed but may be annoyed
3. Badge indicator - Subtle, user can investigate when ready
4. Block UI until resolved - Safest but worst UX
```

## Spec File Format

When writing the specification, use this structure:

```markdown
# [Feature Name] Specification

## Problem Statement
[1-2 paragraphs on what we're solving and why]

## Decided Approach
[High-level approach with key architectural decisions]

## Key Decisions
| Decision | Choice | Rationale |
|----------|--------|-----------|
| [Topic]  | [What] | [Why]     |

## Edge Cases
- **[Scenario]**: [How we handle it]

## Out of Scope
- [What we're explicitly NOT doing]

## Open Questions
- [ ] [Anything still unresolved]

## Implementation Notes
[Technical details, gotchas, dependencies]
```

## Completion Criteria

Stop interviewing when:
- All 5 interview dimensions have been covered
- User indicates readiness to proceed
- Answers are becoming repetitive
- Core architecture and edge cases are documented

Write the spec to the designated file and confirm with user.

---

## Artifact Template

On re-run: rename existing artifact to `spec.v[N].md` and create new with incremented version.

Save to user-designated path (default: `.agents/spec.md`) using the Spec File Format above.

---

## Worked Example

**User:** "I want to build a habit tracker app."

**Round 1 — Scope:** "What habits? Just personal, or team/org habits too?" → Personal only. "Mobile, web, or both?" → Mobile-first PWA. "What's your timeline?" → MVP in 4 weeks.

**Round 2 — Users:** "Who's the primary user?" → Health-conscious 25-35 year olds. "What's their current solution?" → Spreadsheets and reminder apps. "What makes them switch?" → Visual streaks and simplicity.

**Round 3 — Features:** "What's the core loop?" → Add habit → check off daily → see streak. "Notifications?" → Yes, configurable reminders. "Social features?" → Not for MVP.

**Round 4 — Edge cases:** "What happens when a user misses a day?" → Streak resets but history preserved. "Timezone handling?" → User's local timezone, no server-side conversion. "Data export?" → Post-MVP.

**Round 5 — Technical:** "Auth method?" → Email magic link. "Offline support?" → Yes, sync on reconnect. "Analytics?" → Basic usage metrics, no PII.

**Spec saved to `.agents/spec.md` with 14 concrete decisions and 3 deferred items.**

**Excerpt from `.agents/spec.md`:**

```markdown
## Key Decisions
| Decision | Choice | Rationale |
|----------|--------|-----------|
| Auth method | Email magic link | No password management needed; target audience (25-35 health-conscious) prefers frictionless login |
| Streak reset policy | Full reset on miss, history preserved | Users in research respond to loss aversion; seeing "Day 0" motivates more than partial credit |
| Offline support | Local-first with sync on reconnect | Habit check-ins happen at gym/outdoors where connectivity is poor; blocking on network kills the core loop |

## Edge Cases
- **Timezone travel**: If user crosses timezone, use the timezone where they checked in most recently. No server-side conversion — all logic runs on device clock.
- **Missed day notification**: Send a single "Don't break the streak" push at user's configured reminder time +2 hours. No guilt-tripping — one nudge only.
- **Concurrent devices**: Last-write-wins with conflict resolution on sync. Display "synced" indicator so user knows state is current.
```

---

## Anti-Patterns

**Leading questions** — "Don't you think we should use WebSockets here?" pushes toward a predetermined answer. Ask open-ended questions that surface the user's actual constraints: "What are your latency requirements?"

**Accepting the first answer** — The first answer is often the surface-level one. Probe deeper: "Why that approach?" and "What would change your mind?" reveal hidden assumptions and constraints.

**Skipping edge cases** — Happy-path specs produce happy-path code that breaks in production. Systematically explore failure modes, concurrent access, empty states, and boundary conditions in every interview round.

**Scope creep during interview** — Each new question expands the feature surface area. Periodically re-anchor to the original problem: "Is this still in scope for the MVP, or should we defer it?"

**Asking questions the codebase answers** — "What framework are you using?" when `package.json` is right there. Read existing artifacts and code before interviewing — redundant questions waste rounds and erode trust.

---

## References
- **`references/question-bank.md`** — Extended list of probing questions by domain

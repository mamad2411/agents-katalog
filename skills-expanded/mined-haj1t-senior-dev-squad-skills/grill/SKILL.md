---
name: grill
description: "Relentlessly interviews the user one question at a time to reach shared understanding before any code is written. Use when aligning on requirements, stress-testing a plan, or starting a feature."
---

# Grill

## Overview

Before writing a single line of code, use a structured interview to surface assumptions, resolve terminology, and confirm that everyone involved shares the same mental model of what is being built and why. Misaligned understanding is the leading cause of rework; this skill front-loads the alignment cost so implementation is cheap and correct.

The process is deliberately slow and deliberate: one question at a time, each answered before the next is asked, with your own recommended answer offered alongside every question. You are not interrogating the user — you are thinking out loud together, walking the design tree branch by branch until no unresolved fork remains.

**Core principle:** NO BUILDING BEFORE ALIGNMENT. Shared understanding is the deliverable of this phase.

## The Iron Law

```
ONE QUESTION AT A TIME — NEVER ASK TWO THINGS IN THE SAME MESSAGE
```

Every question you ask must be fully answered before you ask the next. Bundling questions is a red flag that you are rushing toward implementation.

## When to Use

**Use this when:**
- A new feature, product area, or integration is requested
- Requirements are stated in vague or overloaded terms ("make it smart", "handle edge cases", "be flexible")
- The user has a plan they want to stress-test before committing to it
- You are uncertain which of two reasonable interpretations the user intends
- The project is entering a phase with hard-to-reverse decisions (data model, public API contract, auth strategy)

**Use this ESPECIALLY when:**
- Someone says "let's just start and figure it out" — the interview costs minutes; course-correction costs days
- The feature has been described differently in different conversations
- Multiple stakeholders are involved and you have only heard from one
- You notice that key terms are used inconsistently (e.g., "user", "account", "workspace" all meaning different things)

**Don't skip when:**
- Under time pressure (a 10-minute alignment session beats a 3-day rewrite)
- The feature seems small (small features still have forks in the design tree)

## Interview Protocol

### Starting the Session

Open by stating the topic and asking the single most load-bearing question first — the one whose answer constrains the most other answers. Do not list all the questions you intend to ask. Do not explain your process at length. Ask one question and wait.

Format every question like this:

> **Question:** [The question, stated simply and precisely]
>
> **My recommended answer:** [Your honest recommendation with brief rationale]

This makes it easy for the user to confirm your recommendation or correct it, without requiring them to construct an answer from scratch.

### Walking the Design Tree

After each answer, do one of three things before asking the next question:

1. **Confirm understanding** — restate what was just decided in one sentence so the user can catch misinterpretation immediately.
2. **Note a dependency unlocked** — if the answer resolves a downstream question, say so before moving on.
3. **Probe further** — if the answer reveals a new ambiguity, ask about that next rather than moving down your original list.

This is not a linear checklist. It is depth-first traversal of the decision tree, guided by what you learn at each node.

### Reading the Codebase First

Before asking the user any question that the codebase can answer, read the relevant files. If you can resolve "how is authentication currently handled?" by reading the code, do that — do not ask. Questions should cover decisions that have not yet been made, not facts that already exist. Demonstrating that you read the code before asking builds trust and saves time.

### Resolving Terminology

When a term is used in a way that could mean two different things — or when the same concept has been called different names in different messages — pause and challenge it directly:

> **Term under review:** "session"
>
> I notice this word has been used to mean both (a) a browser authentication session and (b) a collaborative editing session. These are different concepts that will need different data structures and lifecycle rules. I propose we call them **auth-session** and **collab-session** going forward.
>
> **Question:** Does that distinction match your mental model, or should we draw the boundary differently?

Once agreed, record the canonical term and its definition in `CONTEXT.md` at the project root (or `docs/CONTEXT.md` if a `docs/` directory exists). This is the project's ubiquitous language. Every subsequent conversation, spec, and ADR should use only these canonical terms.

### Stress-Testing with Edge Cases

After the core design is understood, introduce concrete edge-case scenarios to probe the plan:

- "What happens if the user submits the form twice in rapid succession?"
- "What should the system do if the third-party payment provider returns a 500?"
- "What is the expected behavior if two users edit the same record simultaneously?"

These are not adversarial — they are gifts. A scenario that breaks the plan before code is written is far more valuable than one that breaks it in production. When a scenario reveals a gap, treat it as a new question and walk it through the protocol.

Also cross-check stated plans against the actual codebase. If the user says "we already handle retries in the API client", verify that claim by reading the relevant file before accepting it as a constraint.

### Recording Hard Decisions as ADRs

When the interview produces a decision that is hard to reverse — a data model choice, a public contract, a dependency on a specific vendor, an authentication strategy — record it as an Architecture Decision Record. Point to `docs/adr/` for the file location and `templates/ADR-FORMAT.md` for the required format. Do not write the ADR yourself during the interview; flag that the decision warrants one and confirm the user will create it before implementation begins.

> **ADR warranted:** Choosing to store audit logs in a separate PostgreSQL schema rather than a separate service is a deployment-topology decision that will be expensive to undo. This should be captured as an ADR before we proceed.

### Stop Condition

The interview is complete when:

1. Every question in the design tree has been answered or explicitly deferred with a written rationale.
2. All key terms used in the spec are recorded in `CONTEXT.md`.
3. Any ADR-worthy decisions have been flagged and queued.
4. Open questions that cannot be resolved yet are captured in a numbered list, not left implicit.

Summarize the session: list what was decided, what was deferred, and what ADRs are needed. Then explicitly hand off to the next skill (typically `spec-first-development` or `architecture-planner`).

## Question Taxonomy

The design tree has predictable categories. Use this map to ensure no category is skipped before declaring the interview complete.

| Category | What to expose | Example probing questions |
|---|---|---|
| **Scope boundary** | What is explicitly in vs. out | "Does this feature need to work for users who are not logged in?" / "Are mobile push notifications in scope for this iteration or a later one?" |
| **Success criteria** | How anyone will know it is done | "What does success look like in six weeks — what number moves, and in which direction?" / "What would make a stakeholder demo this and say 'not quite'?" |
| **Constraints** | Non-negotiable limits | "Are there latency SLAs we must not break?" / "Does this have to work on the existing data model, or can we migrate?" |
| **Edge cases** | Rare-but-real scenarios | "What should happen if two users trigger this simultaneously?" / "What is the expected behavior when the upstream service is degraded?" |
| **Non-goals** | Things explicitly excluded | "Is bulk export in scope or should we call that out as a non-goal to prevent scope creep?" |
| **Assumptions** | Beliefs the plan depends on | "This plan assumes users have completed onboarding — is that guaranteed, or do we need to handle the partial-onboarding state?" |
| **Dependencies** | Upstream services, teams, data | "Does this depend on a feature another team is building that isn't shipped yet?" / "Which external APIs must be reachable for the happy path?" |
| **Failure modes** | What breaks and what the response is | "If the background job fails halfway through, is the result corrupted or safely idempotent?" / "Who gets paged and what does the retry policy look like?" |

Not every category needs exhaustive drilling — some answers will be obvious from context or codebase reads. The purpose of the taxonomy is to guarantee you do not skip a whole category by accident.

## Decision Tree

Use this to decide whether to keep grilling or close the interview.

```
START: Is there at least one unanswered question in any taxonomy category?
├── YES → Ask the single most load-bearing open question. (Return to START after answer.)
└── NO → Are all key terms defined in CONTEXT.md?
    ├── NO → Resolve undefined terms before stopping.
    └── YES → Are any hard decisions (data model, public contract, vendor) flagged for ADRs?
        ├── NO → Are open questions that cannot be resolved captured in a numbered list?
        │   ├── NO → Capture them now.
        │   └── YES → STOP. Produce session summary. Hand off.
        └── YES (not yet flagged) → Flag them now. Then check open-questions list. (Return to that branch.)
```

**Keep grilling when:** any taxonomy category has an unexamined fork, any term is still ambiguous, or a hard decision was made orally but not written down.

**Stop when:** you can produce a session summary — decisions made, terms defined, ADRs flagged, open questions listed — and it contains no implicit "TBD" items.

The worst stopping error is stopping because the *conversation* feels done, not because the *decision tree* is actually exhausted.

## Worked Example

The following is a condensed but realistic transcript. The feature request arrives vague; the interviewer asks exactly one question per turn.

---

**User:** We should add notifications to the app.

**Interviewer:**
> **Question:** When you say "notifications" — are you thinking in-app alerts (a bell icon the user polls), push notifications to a mobile device, transactional emails, or some combination?
>
> **My recommended answer:** Start with in-app only. Email and push can follow once we know which events actually drive re-engagement.

**User:** In-app for now, but designed so email can be added later.

**Interviewer:** Understood — in-app notifications, extensible architecture. What event should trigger the first notification? I want to make sure we nail the most important one before designing the system around it.

> **Question:** Which single event, if it never triggered a notification, would generate the most complaints from users?
>
> **My recommended answer:** Based on what I can see in the codebase, the most common action is a comment being posted on a task someone owns. I'd start there.

**User:** Yes — comment on a task I'm assigned to.

**Interviewer:** Good. One thing I need to check: should a user be notified when they comment on their own task, or only when someone else does?

> **Question:** Self-comment: notify or suppress?
>
> **My recommended answer:** Suppress. Notifying someone about their own action is noise by default.

**User:** Suppress, agreed.

**Interviewer:** That's now a term that needs a home in CONTEXT.md. I'll note: "notification" = an in-app alert surfaced by the bell icon, triggered by other-user actions on records the recipient owns or watches. Does that definition match your model?

**User:** Add "watches" — we have a watch list feature.

**Interviewer:**
> **Question:** A user can own a task (assignee) and also watch it independently. Should the notification rules be identical for both relationships, or should watchers get a subset of events — for example, no notifications for status changes, only for comments?
>
> **My recommended answer:** Watchers get comments only; assignees get comments + status changes. Keeps the volume manageable.

**User:** Let's do that.

**Interviewer:** One more category before we close: failure behavior.

> **Question:** If the notification write fails (DB down, constraint violation), should we silently swallow the error and let the primary action succeed, or should the entire operation roll back?
>
> **My recommended answer:** Swallow and log. A failed notification should never block a user from saving a comment. We can replay from the event log.

**User:** Agreed — best-effort delivery.

**Interviewer:** I have enough to close. Here is the session summary:

**Decisions made:**
- In-app only (v1). Email/push are explicitly non-goals for this iteration.
- Trigger: comment posted by another user on a task the recipient owns or watches.
- Self-comment → suppressed.
- Assignees: comments + status changes. Watchers: comments only.
- Delivery is best-effort; notification write failure does not roll back the parent transaction.

**Terms added to CONTEXT.md:**
- `notification` — in-app alert surfaced by the bell icon, triggered by other-user actions on records the recipient owns or watches.
- `watch` — a voluntary subscription to a record that grants comment notifications but not status-change notifications.

**ADR warranted:** The best-effort delivery + event-log replay pattern is a significant reliability decision. An ADR should be created before implementation begins.

**Open questions:**
1. Read state: is a notification marked read on click, on view, or manually? Needs a follow-up decision before the UI is specced.

---

The resulting CONTEXT.md snippet and ADR stub are now ready inputs for `spec-first-development`.

## Red Flags — STOP and Follow Process

If you catch yourself doing any of the following, stop and return to the protocol:

- **Asking two questions in the same message** — bundling is always a sign you are rushing. Split them. Ask the most load-bearing one first.
- **Asking a leading question** — "You probably want the standard OAuth flow, right?" is not a question; it is an answer wearing a question mark. State your recommendation separately and ask an open question.
- **Accepting a vague answer without pushing back** — "flexible", "scalable", "it depends", "probably fine" are not answers. Restate the question more concretely and ask again.
- **Stopping because the conversation feels complete** — feelings are not evidence. Check the taxonomy and decision tree before declaring done.
- **Offering implementation suggestions before the interview is complete** — even helpful suggestions ("we could use Redis for this") anchor the design before constraints are known. Hold them until after closure.
- **Using a term that has not been defined in `CONTEXT.md`** as if its meaning is obvious. If it is not in the glossary, challenge it.
- **Moving to the next question without confirming the previous answer** — restate what was just decided before advancing.
- **Skipping the codebase read** and asking a question the code already answers. Reading first is cheaper and more credible.
- **Treating the interview as a formality** — if you already know the answers and are just going through motions, the questions will be low-quality and the user will notice.
- **Writing any code, schema, or config during the interview phase** — any artifact produced before closure is premature and biases the remaining questions.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I already understand what they want, the interview is a waste of time" | You understand your interpretation of what they said. Those are different things. Run the interview. |
| "We can align as we go during implementation" | Mid-implementation corrections are 5-10x more expensive than pre-implementation ones. Align first. |
| "The feature is simple enough that we don't need this" | Simple features have forks too. A five-minute interview on a simple feature costs almost nothing. |
| "They seem confident in their plan, I shouldn't challenge it" | Stress-testing a confident plan is a service, not a criticism. Unchallenged plans have unchallenged blind spots. |
| "I'll just note the ambiguity and handle it later" | Ambiguity deferred is a decision made by accident. Make it on purpose, now, in writing. |
| "I asked one question and got a long answer, that's good enough" | A long answer often contains multiple sub-decisions, each of which needs a dedicated question. Parse the answer; don't accept it wholesale. |
| "The user is in a hurry, I'll ask fewer questions" | A hurried user is exactly who needs the interview most. Their urgency is the source of risk, not a reason to skip coverage. |

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**

- "That's not what I meant" — You moved on from an answer without confirming your interpretation.
- "Can we back up?" — You went too far down one branch before resolving a higher-level fork.
- "Why are you asking that?" — Your question is not load-bearing; you are asking out of habit, not because the answer matters.
- "Just build it, I'll tell you when it's wrong" — The user has lost confidence in the interview process, likely because previous questions felt redundant or low-value. Return to the highest-priority open question and make the value of that question explicit.
- "You already asked that" — You forgot to record the answer. Update `CONTEXT.md` and continue.
- "You're overthinking it" — Your recommended answer for a question was more complex than the situation warrants. Simplify and re-ask.

**When you see these:** STOP. Name what you observed, acknowledge it, and correct course.

## Requirements Elicitation & User Stories

Grill now absorbs two previously separate skills. When the context calls for it, extend the session with either or both modes — full details in [`REFERENCE.md`](REFERENCE.md).

- **Structured project discovery (Part 1):** when a project or feature arrives with little context, run the 8-step question flow (Project Identity → Technical Direction → Data & Storage → Features & Scope → Architecture → Operations → Scale → Meta) and the adaptive questioning matrix *before* the main interview loop. The answers seed your first grill question.
- **INVEST user-story refinement (Part 2):** after grilling surfaces what is wanted, transform raw ideas into production-ready stories — INVEST validation, Given/When/Then acceptance criteria, edge-case enumeration, and SPIDR story-splitting patterns.

## Related Skills

- **spec-first-development** — the natural successor; run after alignment is complete to turn decisions into formal acceptance criteria
- **architecture-planner** — use after grilling when the decisions made warrant a formal architecture design pass
- **setup-senior-dev-squad** — use when onboarding to a new project before any feature work begins
- **tech-stack-advisor** — invoke from the discovery flow (Part 1) when the user needs help choosing a stack

## Verification

- [ ] Every question was asked one at a time with your recommended answer provided
- [ ] No implementation suggestions were made before the interview concluded
- [ ] All vague or overloaded terms have been challenged and resolved
- [ ] Canonical terms are recorded in `CONTEXT.md` with definitions
- [ ] At least one concrete edge-case scenario was used to stress-test the plan
- [ ] Codebase was read before asking any question the code could have answered
- [ ] All hard/irreversible decisions have been flagged for ADR creation
- [ ] Open questions that could not be resolved are captured in a numbered list
- [ ] A session summary was produced: decisions made, deferred items, ADRs needed
- [ ] Handoff to the next skill (spec-first-development or architecture-planner) was explicit

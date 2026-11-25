---
name: brainstorming
description: Design discovery process that scales with task size and user tier. Prevents wasted work on wrong assumptions while staying out of the way for small tasks. Enforces design-before-code discipline with architecture-aware constraints.
invoke_when: Use when building something new, adding a significant feature, or redesigning existing functionality. First determine task size and user tier, then follow the appropriate mode.
---

# Brainstorming

## Task Size Classification

Before doing anything, classify the task:

| Size | Examples | Signal Words |
|------|----------|-------------|
| **Quick Fix** | Add a health endpoint, fix a typo, change button color, update copy, add an env var, tweak spacing | "add", "fix", "change", "update", "tweak", "rename" on a single small concern |
| **Feature** | Build user authentication, add Stripe payments, create a dashboard page, implement file upload | "build", "create", "implement", "add" for a user-facing capability |
| **Project** | Design a microservice architecture, rebuild the data layer, migrate databases, redesign the app | "design", "architect", "rebuild", "migrate", "redesign" spanning multiple systems |

When in doubt, start small. You can always escalate if complexity reveals itself.

## User Tier Detection

- **Builder tier**: Non-technical or semi-technical user. Wants things built. Dislikes process talk. Cares about outcomes, not methodology. Signs: asks "can you build X", doesn't mention tech stack specifics, uses product language not engineering language.
- **Engineer tier**: Technical user. Appreciates rigor. Wants to understand tradeoffs. Signs: mentions specific technologies, asks about architecture, uses engineering terminology, requests design docs.

If uncertain, default to Builder tier. Nobody ever complained that you moved too fast; plenty have complained about being lectured on process.

---

## Lite Mode

**Use when:** Quick Fix tasks (any tier) OR Feature tasks with Builder-tier users.

Collapses the full process into 3 steps. Fast, focused, no ceremony.

### Step 1: Understand
- What needs to happen?
- Who is this for?
- Any constraints? (existing code patterns, architecture.md rules, performance needs)
- Read relevant existing code quickly to avoid breaking things

### Step 2: Recommend
- Propose ONE approach. Not three. One.
- Briefly explain why this is the right call
- For Builder-tier: "Here's what I'll do" not "Here are your options"
- For Quick Fixes: this step can be a single sentence

### Step 3: Confirm and Build
- Let me make sure I understand what you want before I start building
- For Quick Fixes with obvious intent: proceed immediately, confirm as you deliver
- For Features: brief confirmation, then build
- Ensure a spec exists in `.shipworthy/specs/` — if `intent-to-spec` already created one, reference it. If not (e.g., came here directly), save a lightweight spec now with intent, deliverables, and acceptance criteria
- Transition directly to implementation (invoke `writing-plans` only if the feature has 3+ moving parts)

**Example — Quick Fix (Lite Mode):**
> User: "Add a health endpoint"
> AI: "I'll add a GET /health endpoint that returns 200 with a JSON status. It'll follow the existing route pattern in your app." [proceeds to build]

**Example — Feature, Builder tier (Lite Mode):**
> User: "I need user authentication"
> AI: "I'll set up NextAuth with email/password and Google sign-in, using your Supabase database for user storage. This gives you login, signup, and session management. Let me make sure I understand what you want — do you need social logins beyond Google, or is email + Google enough?"

---

## Full Mode (9 Steps)

**Use when:** Feature tasks with Engineer-tier users OR Project tasks with any user.

This is the complete design discovery process. It exists because big decisions made on wrong assumptions waste days, not minutes.

### Step 1: Explore Context
- Read relevant existing code, configs, and architecture.md
- Understand what exists, what patterns are established, what constraints apply
- If architecture.md exists, all proposals MUST comply with its Mandatory Rules

### Step 2: Understand the Problem
- What problem is being solved? (Not "what feature to build" — what PROBLEM)
- Who is affected?
- What happens if this isn't solved?

### Step 3: Ask Clarifying Questions
- What's unclear about the requirements?
- What are the edge cases?
- What are the constraints (performance, security, compatibility)?
- Ask these questions NOW, not after implementing the wrong thing

### Step 4: Propose Alternatives
- Present at least 2-3 approaches
- For each: brief description, pros, cons, estimated complexity
- Include a "simplest possible" option — sometimes it's the right one

### Step 5: Recommend an Approach
- State which approach you recommend and why
- Reference architecture.md constraints that influenced the recommendation
- Identify risks and mitigations

### Step 6: Write a Design Spec
- Save to `.shipworthy/specs/[feature-name].md`
- Include: problem, approach, data model changes, API changes, UI changes, testing approach
- Keep it concise — a spec is not a novel

### Step 7: Self-Review
- Does this violate any Mandatory Rules from architecture.md?
- Does this introduce circular dependencies?
- Does this increase complexity proportional to the value it delivers?
- Is there a simpler way?

### Step 8: Present for Approval
- Show the user the design spec
- Ask for explicit approval before proceeding
- "Does this approach make sense? Should I proceed with writing the implementation plan?"

<HARD-GATE>
DO NOT proceed to Step 9 (Transition to Planning) until your human partner has explicitly approved the design.
Acceptable approval signals: "looks good", "approved", "go ahead", "yes", "proceed", "ship it", or similar affirmative.
NOT acceptable: silence, "hmm", "interesting", or ambiguous responses. If unclear, ASK: "Should I proceed with this approach?"
</HARD-GATE>

### Step 9: Transition to Planning
- Once approved, invoke the `writing-plans` skill
- Pass the approved design spec as context

---

## Anti-Pattern Warnings

These apply at every size, but proportionally:

**For Quick Fixes:** If you're writing a design doc for adding a health endpoint, you've lost the plot. Ship it.

**For Features:** If you catch yourself writing implementation code before understanding what the user actually wants, pause. A 2-minute conversation saves 2 hours of rework. But don't turn that 2-minute conversation into a 20-minute interrogation.

**For Projects:** If you catch yourself writing implementation code before completing at least steps 1-5, STOP. Go back to step 1. The 30 minutes you spend brainstorming saves days of rework on the wrong architecture.

**For all sizes:**
- Don't ask questions you can answer by reading the code
- Don't propose alternatives when there's one obviously correct answer
- Don't write a spec when a comment would do
- Don't block progress with process — process serves progress, not the other way around

---

## Rationalization Pressure Test

These are excuses you might generate to skip brainstorming. Each one is wrong.

| Rationalization | Why It's Wrong | What To Do Instead |
|----------------|---------------|-------------------|
| "This is too simple for brainstorming" | Simple projects are where unexamined assumptions cause the most wasted work | Use Lite Mode — it takes 30 seconds |
| "I already know the answer" | If you already know, writing it down costs nothing. If you're wrong, it saves hours | Write it down. You'll be surprised how often "obvious" answers have gaps |
| "The user seems impatient" | A broken result wastes more time than a 2-minute brainstorm | Use Lite Mode for speed. Never skip entirely |
| "I'll figure it out as I code" | This is how scope creep, rework, and architectural mistakes happen | Even a 1-minute mental model prevents 1-hour rewrites |
| "The user didn't ask for brainstorming" | They asked for working software. Brainstorming is how you deliver that | The skill is invisible to Builder-tier. Just do it |
| "This is just a refactor" | Refactors without understanding the full picture break things | At minimum, read the code and understand dependencies first |

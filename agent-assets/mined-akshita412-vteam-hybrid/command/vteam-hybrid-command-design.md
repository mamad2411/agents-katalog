<!-- agent-notes: { ctx: "sacrificial concept design exploration", deps: [docs/methodology/personas.md, .claude/agents/dani.md], state: active, last: "dani@2026-02-12" } -->
Run a design exploration with sacrificial concepts for: $ARGUMENTS

This follows Dani's approach (see `docs/methodology/personas.md`). The goal is to explore the design space before committing to an implementation.

---

## Step 1: Clarify the Design Question

Before generating options, make sure the problem is well-framed:

- What exactly are we designing? (A feature, a flow, a component, an API shape?)
- What are the constraints? (Technical, UX, timeline, existing patterns?)
- Who is this for? What do they need?
- What would "good" look like? What would "bad" look like?

---

## Step 2: Generate Sacrificial Concepts

Create 2-3 intentionally different approaches. These are **sacrificial** — meant to provoke reactions and learning, not to be implemented directly.

- Vary on key dimensions: complexity, user model, technical approach, level of abstraction.
- Label each concept explicitly: "This is a sacrificial concept — meant to be torn apart."
- For each concept, describe:
  - How it works (the user/developer experience)
  - Key trade-offs (what you gain, what you give up)
  - When this approach shines vs. when it breaks down

---

## Step 3: Elicit Reactions

Don't ask "which is best?" Instead:

- "Which do you hate least, and why?"
- "What elements from different concepts would you combine?"
- "What's missing from all of these?"
- "Which one would you be most embarrassed to ship? Why?"

---

## Step 4: Converge

Synthesize the feedback into a single direction:

- Pull the best elements from across concepts.
- Validate the converged direction with the human: "Here's what I'm hearing — does this capture it?"
- Identify any remaining open questions.

---

## Step 5: Connect Forward

- If the design has architectural implications, flag them for Archie / create an ADR with `/adr`.
- If acceptance criteria need updating, note what changed for Pat.
- If the design needs user validation, suggest a prototype or mockup approach.

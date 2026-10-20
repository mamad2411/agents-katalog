<!-- agent-notes: { ctx: "guided human review session", deps: [docs/methodology/personas.md, .claude/agents/cam.md], state: active, last: "cam@2026-02-12" } -->
Run a guided review session for completed work.

This follows Coach Cam's post-build mode (see `docs/methodology/personas.md`). The goal is to help the human evaluate what was built and turn their reactions into actionable next steps.

---

## Step 1: Orient

Summarize what was built and why:

- Reference the original acceptance criteria, plan, or user story.
- Briefly describe the key changes — what's new, what changed, what was removed.
- Set context so the human knows what they're looking at.

---

## Step 2: Prioritize

Identify the 2-3 most important things for the human to evaluate. Don't dump everything at once.

- Focus on areas where human judgment matters most (UX decisions, business logic, naming, flow).
- Deprioritize things that are well-covered by tests or automated checks.
- Frame each area with a specific question or lens: "Does this flow match what you envisioned for a first-time user?"

---

## Step 3: Walk Through

For each priority area:

- Show the relevant code, UI, or behavior.
- Ask targeted questions: "Does this match what you envisioned? What surprises you? What feels off?"
- Listen for emotional reactions — hesitation, enthusiasm, confusion — and probe them.

---

## Step 4: Translate

When feedback is vague, dig deeper:

- "You said 'something feels off' — is it the layout, the flow, the data shown, or something else?"
- "When you say 'simpler,' do you mean fewer steps, less information on screen, or a different mental model?"
- "Is this a 'must fix before shipping' or a 'nice to have for later'?"

Don't accept "it's fine" at face value — ask "what would make it better than fine?"

---

## Step 5: Actionize

Convert all feedback into concrete items:

- Each item gets clear acceptance criteria — not "make it better" but "reduce the checkout flow from 4 steps to 2."
- Prioritize with the human: what's blocking, what's next, what's backlog.
- If any items need design exploration, flag them for `/design`.
- Summarize the action items and confirm with the human before ending.

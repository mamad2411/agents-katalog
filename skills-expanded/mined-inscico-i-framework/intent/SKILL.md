---
name: intent
description: Stage 1 of the I-Framework. Run a guided interview to capture a founder's intent — the problem, the target user, why-now and why-us, and evidence of real pain — then write Product/intent.md. Start here when defining a new startup or product idea.
allowed-tools: Read, Write, Edit, Glob, AskUserQuestion
---

# /intent — Stage 1: capture the "why"

You retire **founder–problem risk** before any solution talk. Run a guided interview, one question at a time. Stay on the *problem*, not the solution — if the founder jumps to features, gently redirect to the pain.

## Procedure

### 1. Set up
Create the `Product/` folder if it doesn't exist. If `Product/intent.md` already exists, read it and offer to refine rather than overwrite.

### 2. Interview (one question at a time)
Draw out, and challenge thin answers on:
- **The problem** — in plain language, the pain not the product. ("What's broken today?")
- **The target user** — who has this most acutely? Push back on "everyone"; get to a specific persona.
- **Why now** — what changed? The tailwind/shift that makes today the moment.
- **Why you** — founder–problem fit: lived experience, unfair insight, access. What will keep you in the fight when it's hard?
- **Status quo** — what does the user do about this today? (The real competitor is usually a workaround or "nothing.")
- **Evidence of pain** — the cheapest test: who have you actually talked to, and what did they say? Aim for 5–10 people in genuine pain. Accept "it's still a hunch" honestly — but name it.

Use AskUserQuestion for genuine forks; use open prompts for narrative answers. Don't fill silence with invented facts — ask.

### 3. Synthesize `Product/intent.md`
Write it using the structure from the plugin's `templates/intent.md`. Read the draft back to the founder for confirmation/correction before finalizing.

### 4. Evaluate the gate
Set frontmatter `gate: passed` when all three hold: (1) a crisp problem statement, (2) a named target user, (3) at least one piece of real pain evidence. Otherwise `gate: open` and clearly list what's missing — but never block the founder from moving on.

### 5. Hand off
Point to `/ideate` as the next step (and `/iflow` if they want the orchestrator to route them).

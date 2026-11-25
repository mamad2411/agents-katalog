---
name: ideate
description: Stage 2 of the I-Framework. Diverge into many candidate solutions to the captured intent (fanning out across subagents for independent angles), then converge to 1-3 bets with a demand hypothesis, and write Product/ideation.md. Use after /intent.
allowed-tools: Read, Write, Edit, Glob, AskUserQuestion, Task
---

# /ideate — Stage 2: diverge, then converge

You retire **solution & demand risk**. First go wide (escape the first-idea trap), then narrow to a small number of bets with an explicit, testable demand hypothesis.

## Procedure

### 1. Load context & check the gate (soft)
Read `Product/intent.md`. If it's missing, suggest `/intent` first. If its `gate: open`, warn that you're ideating on an unvalidated problem but proceed if the founder wants.

### 2. Diverge — fan out for breadth
Spawn a handful of subagents in parallel via the Task tool, **each with a different lens**, so the option space isn't anchored on one mindset. Suggested lenses (pick 4–6):
- **Cheapest MVP** — the scrappiest thing that could work.
- **10x technology** — what becomes possible with the best available tech.
- **Different business model** — subscription, marketplace, services, usage-based, free+data.
- **Adjacent analog** — how an unrelated industry solved a structurally similar problem.
- **Do-it-for-them** — a concierge/service version before any product.
- **Platform / ecosystem** — enabling others to solve it.

Give each subagent the intent (problem, user, status quo) and ask for a short list of distinct candidate solutions with a one-line description each. Then **dedupe and cluster** the returned candidates yourself.

> If the bet is tightly scoped or the user prefers, skip the fan-out and brainstorm a single broad pass inline.

### 3. Converge — score and narrow
Score each candidate on **desirability** (fit-to-intent / demand signal), **feasibility**, and **differentiation potential** (H/M/L). Narrow to **1–3 bets**. Interview the founder to confirm the choice — their conviction and constraints matter as much as the scores.

### 4. Demand hypothesis & cheapest test
For the chosen bet(s), force a falsifiable demand hypothesis ("We believe <persona> will <behavior> because <reason>") and the smallest experiment that would confirm or kill it **before building**.

### 5. Write `Product/ideation.md`
Use the structure from the plugin's `templates/ideation.md`: the full option space (keep the killed ones and why), the chosen bet(s) and rationale, the demand hypothesis, and the cheapest test.

### 6. Gate & hand off
Set `gate: passed` when there's a chosen bet, a demand hypothesis, and a cheapest-test plan. Point to `/innovate` next.

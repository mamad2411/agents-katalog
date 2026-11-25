---
name: premortem
version: 1.0.1
description: "Stress-test a concrete plan or decision by assuming failure and reasoning backward. Use for a premortem, blind-spot review, or failure analysis of a launch, hire, pricing change, strategy, or commitment. Produces failure scenarios, hidden assumptions, warning signs, and plan changes. Skip vague ideas, factual questions, and irreversible decisions."
---

# Premortem

A premortem is the inverse of a postmortem: assume the plan has already failed, then reason backward to explain why. The method is Gary Klein's (HBR, 2007). Kahneman cited it as one of his most valuable decision tools. Wharton/Cornell research calls the underlying mechanism *prospective hindsight* — when people assume an outcome has occurred, they generate substantially more specific and honest causal explanations than when asked to forecast risks.

The reason it matters here: Claude defaults to validating plans. "Is this good?" gets agreement. "This already died — why?" forces the model into narrative explanation mode and produces specific, grounded failure stories instead of hedged risk-assessment language.

---

## When NOT to run it

- Vague ideas with no concrete plan — help the user shape the plan first.
- Questions with a single correct answer — just answer them.
- Editing or feedback on a draft — that's editing, not a premortem.
- Decisions that can no longer change — there's nothing to act on.

---

## Phase 1 — Context

Failure scenarios are only as good as the input. Before running, you need three things:

1. **What is it?** A one-sentence description you can repeat back.
2. **Who does it affect?** Audience, customer, team, stakeholders.
3. **What does success look like?** Failure is the inversion of this.

**First, scan what's already available** — the current conversation, attached files, and relevant project instructions or saved project memory exposed by the user's workspace. Project instructions and memory are optional external context, not files bundled with this skill; do not assume they exist or search unrelated projects. Don't spend more than ~30 seconds. If you can infer an answer, don't ask.

**Then ask only for what's missing**, one question at a time. Stop asking the moment the threshold is met.

You also need a **decision horizon** — when would failure become evident? Pick the timeframe that fits the decision (a pricing change might fail in 4 weeks; a strategic pivot in 12–18 months). Default to asking the user; don't hardcode "6 months."

---

## Phase 2 — Frame and generate

State the frame explicitly:

> "It is [horizon] from now. [The plan] has failed. We're looking back to understand why."

Then generate every genuine failure reason. Be specific to *this* plan — not generic risk-management advice. Stop when you've exhausted real ones, not at a number. Some plans have 3 real failure modes; others have 9.

Each reason should be:
- Specific to the plan's actual details
- A genuine threat (not a minor inconvenience or extreme edge case)
- Stated in 1–2 sentences

---

## Phase 3 — Depth (conditional)

For each failure mode, you can optionally go deeper: a short narrative of how it played out, the underlying assumption that made it possible, and 1–2 observable early-warning signs.

**When to fan out to parallel sub-agents:** high-stakes decision (significant money, reputation, or irreversibility), 5+ failure modes, user explicitly asks for depth. Each sub-agent takes one failure reason with the full plan context and produces failure story + assumption + warning signs.

**When to stay inline:** smaller decisions, fewer failure modes, time-sensitive sessions. Write the depth analysis directly. The synthesis is what matters — fan-out is a tool, not a default.

If you fan out, spawn all agents in a single message so they run in parallel.

---

## Phase 4 — Synthesis (always)

This is the product. Produce:

1. **Most likely failure** — which scenario is most probable, and why.
2. **Most dangerous failure** — which would cause the most damage if it hit, even if less likely.
3. **The hidden assumption** — the single biggest thing the user is taking for granted that they probably haven't questioned. This is usually where the real value lives.
4. **Revised plan** — concrete changes, each mapped to a specific failure scenario. Not "consider your pricing" but "test pricing at $X with N people before committing publicly."
5. **Pre-launch checklist** — 3–5 things to verify, test, or put in place before executing. Each one prevents or detects a specific failure mode.

Deliver the synthesis in chat. Keep it specific, direct, and free of hedging. Don't sugarcoat — the entire point is to surface what the user doesn't want to hear before reality does.

---

## Phase 5 — Optional artifacts

By default, the synthesis lives in chat. Offer artifacts only when warranted:

- **HTML report** — only if the user wants something to share, revisit, or present. Ask first. Keep styling minimal unless they specify.
- **Markdown transcript** — only if the user asks to keep a record.

Don't write files by default. A premortem of a hire decision over coffee shouldn't drop two artifacts on the user.

---

## Phase 6 — Memory

A premortem produces exactly the kind of insight worth keeping: a hidden assumption the user was making, or a validated decision-making pattern. At the end:

- If the host exposes an existing auto-memory or project-memory location for the current project, offer to save the hidden assumption there as a `feedback` or `project` memory — whichever fits. This is an optional user-workspace destination, not a bundled resource; do not invent a path or create a memory store.
- Don't save reflexively. Ask. The user knows whether the assumption generalizes beyond this one decision.

---

## Operating notes

- **Set the failure frame explicitly every time.** "This already failed" is the load-bearing mechanism. Without it, the analysis collapses into polite risk assessment.
- **Be honest, not exhaustive.** Don't pad to hit a number. Don't truncate to be tidy.
- **The revised plan must be actionable this week.** If it's not, it's a wish.
- **Ground every failure mode in actual plan details.** If a failure reason would apply to any plan, it's not specific enough.
- **Respect the context threshold.** A premortem on insufficient context produces generic failures and wastes the user's time. Ask the missing question.

---
name: brainstorming
version: 1.0.0
description: >
  Brainstorm, offer ideas, and explore options or weigh alternatives before a decision ("let's brainstorm", "what are my options", "pros and cons of"). Runs the session, tracks every option's strengths, weaknesses and status, and at the end offers, but never writes unasked, a recap report.
tags: [brainstorming, ideation, decision-making, productivity]
---

# Brainstorming Skill

Runs a brainstorming session with the user: understands the problem, generates a wide range of options, evaluates them honestly, and helps the user decide. Throughout, it keeps an accurate account of every option raised and what became of it, so that the session can end with a recap report — **but only if the user asks for one**.

---

## Core Principles

1. **The user decides.** You propose, challenge and evaluate; the user accepts or rejects. Never mark an option accepted or rejected unless the user said so.
2. **Breadth before judgement.** Generate first, evaluate after. Criticizing ideas while they are still being produced shuts down the unusual ones, which are often the useful ones.
3. **Honest evaluation.** Every option gets real strengths *and* real weaknesses, including the user's favourite and your own suggestions. An option with no stated weakness hasn't been evaluated.
4. **Keep track.** Every option raised — by you or by the user — is remembered with its status and the reason behind it, so nothing is lost and the recap is accurate.
5. **No report without asking.** Never write the recap on your own initiative. Ask whether the user wants one, and write it only on a yes.

---

## Step 1 — Frame the Problem

Before generating anything, make sure you understand:

- **The goal**: what the user is trying to achieve, in one sentence.
- **Constraints**: budget, time, technology, people, rules — what any option must respect.
- **Success criteria**: how the user will judge an option (cost, speed, risk, user impact, effort). These become the evaluation criteria in Step 3.
- **What has already been tried or ruled out**, so you don't propose it again.

Ask at most 2–3 focused questions. If the user wants to jump straight in, start generating and pick up the missing context as it comes. Restate the problem in one or two sentences and check it before moving on.

---

## Step 2 — Explore (Diverge)

Generate a genuinely varied set of options, typically 5–8 to start:

- **Mix safe and bold**: the obvious approach, an incremental one, a radical one, a "do nothing / defer" option, and a combination.
- **Vary the angle**: change the constraint ("what if budget weren't the issue?"), invert the problem ("how would we make this worse?"), borrow from another domain, split the problem into parts.
- **Invite the user's ideas** and build on them ("yes, and…") rather than replacing them.
- Give each option a **short, memorable name** and a one-line description, so it can be referred to later ("Option C — the phased rollout").
- Hold back detailed criticism in this phase. A brief "worth noting: X" is fine; the full evaluation comes next.

Offer another round if the set feels thin or the user isn't excited by any of it.

---

## Step 3 — Evaluate (Converge)

For the options the user wants to pursue (or all of them, if there are few), assess each against the success criteria from Step 1:

| Aspect | What to cover |
|---|---|
| **Strengths** | what it does well, and for whom; which criteria it satisfies |
| **Weaknesses** | where it falls short; which criteria it fails or strains |
| **Risks** | what could go wrong, and how likely or severe |
| **Effort / cost** | rough size: small / medium / large, and what drives it |
| **Unknowns** | what would have to be found out before committing |

- Be specific to this problem — "risky" is not an evaluation; "depends on the vendor API staying free" is.
- Compare options against each other where it helps: a small table with the options as rows and the criteria as columns makes trade-offs visible at a glance.
- Look for **combinations**: the strengths of two options often cover each other's weaknesses.
- If one option clearly dominates, say so and why — but leave the decision to the user.

---

## Step 4 — Decide

- Ask the user which options they want to **accept**, **reject**, or **keep open** for later.
- For every decision, capture the **reason** — in the user's words where possible ("rejected: too expensive for this quarter").
- An option the user never explicitly decided on stays **open**. Do not infer a rejection from silence or an acceptance from enthusiasm.
- If the user changes their mind, update the status and keep the history ("rejected, then reconsidered and accepted after the cost estimate").

---

## Keeping Track During the Session

The recap is only as good as your account of the session, and long conversations lose detail. So:

- Keep a mental ledger of every option: **name**, **one-line description**, **proposed by** (you or the user), **strengths**, **weaknesses**, **status** (open / accepted / rejected) and **reason**.
- At each natural transition (end of a generation round, after an evaluation, after decisions) give a **short status line** of the options in play, e.g.:

  > In play: A — phased rollout (accepted), C — vendor partnership (open), E — build in-house (rejected: no team capacity).

  This keeps the options visible to the user and in the conversation, so none is lost later.
- Options the user dismisses quickly still count: record them as rejected, with the reason.

---

## Offering the Recap

**Never produce the recap report directly.** When the session reaches a natural end, **ask** whether the user wants one.

A natural end is when:
- the user has made the key decisions, or
- the user signals wrapping up ("ok, that's enough", "thanks, that helps", "let's go with X"), or
- the conversation is about to move to a different topic.

Ask once, briefly, for example:

> Would you like a recap of this brainstorming — the options we explored, their strengths and weaknesses, and which ones you accepted or rejected?

- **If the user says yes**, write the report (next section).
- **If the user says no**, or doesn't answer, don't write it and don't ask again unless the session continues and reaches another natural end.
- Don't ask at every turn, and don't ask in the middle of the session.
- If the user asks for a recap at any point themselves, that counts as a yes.

---

## The Recap Report

Write it as a Markdown file, by default `brainstorms/<topic>-<YYYY-MM-DD>.md` in the working directory (a different location if the user gives one; add a suffix rather than overwrite an existing file). Give the user the path, and a two-sentence summary in chat. If you cannot write files, put the report in the chat instead.

The report is a faithful record of the session — **not** a place for new ideas or new analysis. Every option, strength, weakness and decision in it must have come up in the conversation. If something was never evaluated, say so rather than filling it in now.

```markdown
# Brainstorming: [Topic]

**Date:** YYYY-MM-DD
**Goal:** [the problem, in one or two sentences]
**Constraints:** [the constraints that shaped the options]
**Success criteria:** [how options were judged]

### Outcome
[2–4 sentences: what was decided, and what is still open.]

| Option | Status | Reason |
|---|---|---|
| A — [name] | ✅ Accepted | [reason] |
| B — [name] | ❌ Rejected | [reason] |
| C — [name] | ⏸ Open | [what is needed to decide] |

### Options Explored

#### A — [Name] · ✅ Accepted
**Idea:** [one or two sentences]
**Proposed by:** user / assistant
**Strengths:**
- [...]
**Weaknesses:**
- [...]
**Risks and unknowns:** [if discussed]
**Decision:** Accepted — [reason, in the user's words where possible]

#### B — [Name] · ❌ Rejected
...

### Combinations and Variants
[Options merged or refined during the session, and how they relate to the ones above. Omit if none.]

### Open Questions and Next Steps
- [Unknowns to resolve, open options awaiting a decision, actions the user mentioned]
```

- Order options by status — accepted first, then open, then rejected — so the outcome is read first.
- Keep each option short: a few bullets per list. The reader should be able to scan the whole report in two minutes.
- If an option's status changed during the session, note it in **Decision** ("rejected, then accepted after …").

---

## Interaction Style

- Be an active partner, not a list generator: react to the user's ideas, build on them, and push back when an idea has a real problem.
- Keep turns short enough to discuss — a wall of 20 options is harder to react to than 6 good ones.
- Ask one question at a time when you need input.
- Don't steer toward your own suggestions; evaluate them as critically as the user's.
- Use the options' short names consistently, so both of you can refer to them easily.

---

## Quality Checklist

Before offering the recap, and again before writing it:

- [ ] The goal, constraints and success criteria were stated and confirmed
- [ ] The options were genuinely varied (not five versions of the same idea)
- [ ] Every evaluated option has both strengths and weaknesses, specific to this problem
- [ ] Every status (accepted / rejected / open) comes from the user, with a reason
- [ ] The recap was offered, not written unasked
- [ ] The report contains only what came up in the session, with nothing new added

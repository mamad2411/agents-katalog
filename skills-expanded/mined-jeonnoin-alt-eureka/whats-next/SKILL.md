---
name: whats-next
description: Use when a researcher is stuck, unsure of the next step, feels lost in the middle of a project, or asks any variant of "what should I do next?", "where am I?", "what now?", "I'm stuck" — diagnoses research state and recommends which Eureka skill to invoke next
---

# What's Next?

## Overview

Researchers get stuck. Not because they're lazy or incompetent — because the research lifecycle has many branches, every project has different state, and "what should I do now?" is a hard question even for experienced PIs.

This skill diagnoses **where you are in the research lifecycle**, then recommends the next Eureka skill to invoke. It does NOT do the work itself. It is a router — it figures out which specialist to call.

**Core principle:** When stuck, the answer is almost never "try harder at what you're doing." The answer is usually "you're in a different phase than you think — switch tools."

## Modes

This skill has two modes:

### Diagnostic mode (default)

User doesn't know where they are in the research lifecycle, or needs help picking the next skill. Scan state → diagnose phase → recommend specialist skill. This is the existing workflow (Steps 1-6 below).

### Resume mode (NEW in v1.10.0)

User returns after a break and wants to continue where they left off. Trigger phrases: "resume", "continue", "last session", "where was I", "어디서부터", "이어서".

**Resume workflow:**

1. Read the most recent entry in `docs/eureka/journal/` (sort by filename `YYYY-MM-DD.md`). If no journal entry exists, fall back to Diagnostic mode.
2. Read the last 20 commits of `git log --oneline -20` for context on what was worked on.
3. Scan `docs/eureka/` subdirectories for most-recently-modified artifacts:
   - `designs/` — any new design docs?
   - `registrations/` — any new or amended registrations? (check `INDEX.md`)
   - `plans/` — any experiment plans in progress?
   - `audits/` — recent claims-audit runs?
   - `reviews/` — recent research-reviewer runs?
   - `novelty-audits/` — recent novelty audits?
   - `verifications/` — recent verification runs?
4. Synthesize: "Last session ended at [phase] based on [evidence]. Expected next step is [skill]. Context in 3 sentences: [...]. Proceed with [skill]?"
5. Wait for user confirmation, then hand off to the recommended skill.

**Decision rule**: if the journal entry clearly identifies the current phase AND there are no stale artifacts suggesting the state has drifted, use resume mode. If the journal entry is ambiguous or more than 2 weeks old, fall through to diagnostic mode.

---

## When to Use

**Use this skill when:**
- The user says any variant of "what now?", "what should I do next?", "I'm stuck", "어디서부터 손대야 하지", "어디쯤이지"
- The user describes ambiguous progress without a clear next step
- The user has been spinning on the same task for an unusually long time
- The user asks for general advice rather than a specific operation
- The user just finished a phase but doesn't say what they're moving to

**Do NOT use this skill when:**
- The user has a specific request — go to the matching specialist skill directly
- The user is in active execution and just needs to keep going
- The user is asking for help with a single concrete task (use the relevant specific skill)

## Core Principle: Diagnose, Don't Solve

This skill **never executes the actual research work**. It always ends with a recommendation to invoke another Eureka skill. If you find yourself starting to brainstorm a hypothesis, troubleshoot a result, or write a manuscript while in this skill — STOP. You skipped the handoff.

The job of `whats-next` is to answer one question: **"Which Eureka skill should I invoke right now?"**

## Checklist

You MUST create a task for each of these and complete them in order:

1. **Scan project state** — read project files to determine objective state
2. **Identify most recent activity** — what was the last thing the user finished or attempted?
3. **Ask diagnostic questions** — one at a time, as needed to disambiguate
4. **Map to research lifecycle phase** — name the phase the user is currently in
5. **Recommend 2-3 next actions** — each linked to a specific Eureka skill
6. **Hand off** — user picks one, then invoke that skill

## Step 1: Scan Project State

Before asking anything, scan the project files to gather objective evidence:

| Look for | What it tells you |
|---|---|
| `docs/eureka/designs/*.md` | A research design exists → past brainstorming phase |
| `docs/eureka/registrations/*.md` | Hypothesis is registered → past hypothesis-first phase |
| `docs/eureka/plans/*.md` | Experiment plan exists → past experiment-design phase |
| `results/` directory with files | Experiments have been run |
| `docs/eureka/records/experiment-log.md` | Structured experiment tracking exists |
| `docs/eureka/audits/*.md` | Claims have been audited |
| `docs/eureka/journal/*.md` (most recent) | Narrative context from last session — decisions, failures, blockers, and the "Next session starts with" hint. This is your strongest continuity signal. |
| Recent `git log` (last 5–10 commits) | What the user actually did most recently |
| `*.tex`, `manuscript/`, `paper/` | Manuscript writing is in progress |
| `notes/` or other free-form files | Additional free-form thinking that may reveal context |

If the project does not use Eureka conventions yet (no `docs/eureka/` structure), the user is likely at the very beginning. That is its own diagnosis — the answer will probably be `eureka:research-brainstorming`.

## Step 2: Identify Most Recent Activity

Look at the latest commits, the newest files in `results/`, the most recently modified document. State what you found:

> "I see your most recent activity: 3 baseline experiment results in `results/run_20260411_*/`, last commit was `Run baseline model` from 2 days ago. The design doc exists but no review report yet."

This is not an interpretation — it is a factual report. The user can correct it if you read the state wrong.

**If `docs/eureka/journal/` exists**, read the most recent entry (latest date file, last `##` session block within it). The `Next session starts with` field is your strongest single signal for what to recommend — it is a message from past-user to future-user specifically about the next action. Quote it back to the user:

> "Your last journal entry (2026-03-22, 18:00 session) says next session starts with: 'Re-run Model A with per-subject normalization'. Is that still the right starting point, or has anything changed since?"

The journal also surfaces `Blockers` and `Failed attempts` from prior sessions, which tell you what to avoid recommending.

## Step 3: Ask Diagnostic Questions

Ask **one at a time**. Stop as soon as you have enough information to recommend.

The four core questions (skip any that are already answered by Step 1 or by the conversation):

1. **What was the most recent thing you finished or attempted?**
2. **What was the outcome?** (multiple choice: success / partial success / failure / unclear / haven't checked yet)
3. **What is blocking you from moving forward?** (multiple choice if possible: missing information / unclear interpretation / decision paralysis / waiting on external / lost confidence in approach / other)
4. **If a senior collaborator walked in right now, what would you ask them?**

Optional follow-ups when needed:
- "Are these results aligned with what your registered hypothesis predicted, or different?"
- "Have you written down what you expect the next experiment to show?"
- "Is the issue technical (something broke) or interpretive (you don't know what the result means)?"

## Step 4: Map to Research Lifecycle Phase

Based on Steps 1–3, identify which phase the user is in. Use this map:

| State | Phase | Recommend |
|---|---|---|
| No design doc, **no research question at all** — only keywords, a dataset, or vague interest (e.g., "something with EEG") | **Pre-ideation** | `eureka:research-ideation` |
| No design doc, **has a research question** but it needs refinement (e.g., "Does X cause Y?") | **Pre-design** | `eureka:research-brainstorming` |
| Design exists, no registration, no analysis | **Pre-registration** | `eureka:hypothesis-first` |
| Hypothesis registered, no experiment plan | **Pre-execution planning** | `eureka:experiment-design` |
| Experiment plan exists, no results | **Execution** | Just run the experiments — no skill needed yet |
| Some results, but mixed/unclear/unexpected | **Investigation** | `eureka:systematic-troubleshooting` (if technical) OR `eureka:requesting-research-review` (if interpretive) |
| Results complete, not yet evaluated | **Phase review** | `eureka:requesting-research-review` |
| Review passed, starting to write | **Manuscript drafting** | `eureka:claims-audit` (use during writing, not just at the end) |
| Manuscript drafted | **Pre-publication audit** | `eureka:claims-audit` then `eureka:verification-before-publication` |
| Verification passed | **Submission decision** | `eureka:submission-readiness` |
| Pivoting / lost direction | **Re-design** | `eureka:research-brainstorming` (start over with new question) |

If the user's state spans multiple phases, pick the **earliest unfinished one**. You cannot skip Phase N to get to Phase N+1.

**Discriminating rule for Pre-ideation vs Pre-design:** If the user can state the question as "Does/Is/Can [X] [verb] [Y]?", they have a formed question → Pre-design. If they cannot, they are in Pre-ideation.

## Step 5: Recommend 2-3 Next Actions

Present the recommendations in this format:

```
You are currently in: [phase name]

Most likely next actions:

1. [Recommended] Invoke `eureka:[skill-name]` — [one-sentence rationale]
2. Alternative: Invoke `eureka:[other-skill]` — [when this is the better choice]
3. Optional: [non-skill action, e.g., "wait for collaborator response"]

Which one?
```

Lead with **one** clear recommendation. The alternatives exist for cases where the user has context you don't.

## Step 6: Hand Off

After the user picks, invoke the chosen skill via the `Skill` tool. Do NOT try to do that skill's job inside `whats-next`.

If the user picks the recommended skill, just invoke it. If they pick an alternative, invoke that one — they have context you don't.

After the hand-off, gently remind the user:

> "At the end of this session, `eureka:research-journal` can capture today's decisions and what to start with next time."

This is a soft reminder, not a requirement. The user decides whether to journal at session end.

## Output Format

Total response length: **short**. This is a triage skill, not a coaching session. Aim for:

- 2–3 sentences of state report
- 1 question (if any are needed)
- 2–3 line recommendation
- Hand off

Long outputs defeat the purpose. The user is stuck. They need a direction, not a lecture.

## Anti-Patterns

| What you might do wrong | What to do instead |
|---|---|
| Start brainstorming the next experiment | Stop. Recommend `eureka:research-brainstorming` and hand off. |
| Diagnose technical bugs in the data | Stop. Recommend `eureka:systematic-troubleshooting` and hand off. |
| Critique the user's research direction | Stop. The right skill for evaluation is `eureka:requesting-research-review`. |
| Write a long motivational/coaching response | Triage is fast and factual. Save the empathy for a different conversation. |
| Recommend more than 3 actions | Decision paralysis is part of the problem. Narrow it down. |
| Skip the project state scan | Without scanning, your recommendation is a guess. Always scan first. |
| Recommend a skill the user has clearly already done | Read the project state. If they registered a hypothesis already, do not tell them to register one. |
| Treat this as a brainstorming session | This skill is a router. The brainstorming happens in `eureka:research-brainstorming`. |

## Red Flags

These thoughts mean STOP — you're slipping out of triage mode:

- "Let me just suggest one quick experiment" → No. Recommend the skill.
- "I'll explain why their result is unexpected" → No. Recommend `systematic-troubleshooting`.
- "Let me draft the manuscript section for them" → No. Recommend `claims-audit`.
- "I should give them a deeper analysis of their situation" → No. Triage is short.
- "They probably know all this — let me just tell them what to do" → Scan first. You may be wrong.

## Common Stuck States

These are the most frequent stuck states researchers experience and the typical correct routing:

| Stuck state | Likely phase | Skill to recommend |
|---|---|---|
| "Baseline done, results are mixed" | Phase review | `requesting-research-review` to evaluate rigor before drawing conclusions |
| "I have an idea but don't know how to test it" | Pre-design | `research-brainstorming` |
| "Experiment crashed and I don't know why" | Execution → Investigation | `systematic-troubleshooting` |
| "The numbers look right but feel wrong" | Investigation | `systematic-troubleshooting` (Phase 1: investigate) |
| "Reviewer said X, not sure how to respond" | Post-review | `receiving-research-review` |
| "I think I'm done but not sure" | Pre-publication | `verification-before-publication` |
| "Should I keep going or pivot?" | Decision | `submission-readiness` (the four-option gate) |
| "I have results but no plan to write them up" | Drafting | Start writing, then `claims-audit` |
| "I haven't touched this in weeks, where was I?" | Any | Scan state, recommend the next gate |
| "I keep going in circles on the same analysis" | Investigation OR re-design | `systematic-troubleshooting` first; if 3+ attempts failed, escalate to `research-brainstorming` |
| "I have data but don't know what to study" | Pre-ideation | `research-ideation` |
| "What interesting questions are there in this field?" | Pre-ideation | `research-ideation` |
| "The figure looks wrong / won't pass journal review" | Writing / submission prep | `figure-design` |
| "I need to make a figure for Results" | Writing | `figure-design` (after results are finalized) |
| "Results are technically fine but the paper feels flat" | Writing / pre-submission | `manuscript-writing` narrative-arc lock step (Discovery-Adjusted Framing) with `docs/references/narrative-guide.md` section **"Discovery-Adjusted Framing"** |
| "Not sure if this is Nature-level or specialty-journal-level" | Submission prep | `submission-readiness` venue-framing check with `narrative-guide.md` section **"Venue-specific altitude tuning"** |
| "The paper is rigorous but I'm not sure it's still novel" / "worried about preemption" | Pre-submission | `novelty-competitive-audit` (blocks `submission-readiness` until PASS) |
| "Reviewer/editor surfaced a preempt paper; what do I do?" | Pre-revision / pre-resubmission | `novelty-competitive-audit` first, then `manuscript-writing` narrative-arc lock re-fire if altitude needs adjustment |

## Integration

- **Called by:** `eureka:using-eureka` when the user expresses being stuck or asks "what next?"
- **Invokes:** Any other Eureka skill (this is a dispatcher)
- **Pairs with:** Every other Eureka skill — this is the front door when the user can't pick one themselves
- **Does NOT replace:** Any specific skill. It always hands off.

## Skill Type

**FLEXIBLE** — The diagnostic conversation adapts to context. The order and depth of questions can change based on what the project state already reveals. The constant is the structure: scan → identify → diagnose → map → recommend → hand off.

This is a router skill. Routers do not solve problems — they make sure the right specialist gets called. Discipline here means resisting the urge to "just help" inside the router itself.

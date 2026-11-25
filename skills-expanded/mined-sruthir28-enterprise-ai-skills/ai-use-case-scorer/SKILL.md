---
name: ai-use-case-scorer
description: Score and prioritize AI use cases for your own job. Given a list of candidate use cases (or a description of your workflow), evaluates each on Value × Feasibility × Safety and tiers them — Do Now / Do This Quarter / Park / Avoid. Use when you've heard "we should use AI more" and need to figure out what to actually build first. Built for the individual IC, not org-wide rollout.
---

# AI Use-Case Scorer

Turns "I should be using AI more" into "here are the 3 things I'm building this week, here's why, and here's what I'm explicitly NOT doing." Built for the individual IC trying to figure out where to deploy AI in their own work.

---

## Why this exists

Most AI-use-case lists are theater — pages of "potential" use cases that never get built. This skill compresses the call: of the use cases on your list, which 2–3 actually pay off this month, and which to ignore.

**Built for the IC.** If you're rolling AI out to a 50-person team, this is the wrong framework — that's change management, not personal scoring.

---

## Scoring framework: V × F × S

Each use case scored on three axes (1–5 scale).

### Value — what's the upside?
| Score | Time saved | Quality lift | Strategic fit |
|-------|------------|--------------|---------------|
| 5 | >5 hrs/wk | Visibly better output | Hits a top-3 personal goal |
| 3 | 1–5 hrs/wk | Modest improvement | Adjacent to a goal |
| 1 | <1 hr/wk | Marginal | Not connected to goals |

**Value score** = round(avg of three sub-scores)

### Feasibility — can you actually do it?
| Score | Tool maturity | Your skill / time |
|-------|---------------|-------------------|
| 5 | Mature off-the-shelf skill or tool exists | Ship in one sitting |
| 3 | Tools exist but need glue | A weekend project |
| 1 | Requires custom dev / new infra | Multi-week build |

**Feasibility score** = round(avg of two sub-scores)

### Safety — what could go wrong? (Inverted: higher = safer)
| Score | Quality risk | Data risk | Trust risk |
|-------|--------------|-----------|------------|
| 5 | Errors easy to catch | No sensitive data | Team comfortable with AI |
| 3 | Errors land in internal docs | Some PII / internal data | Mixed signals from team |
| 1 | Errors land in customer / exec face | Confidential / regulated | Active resistance |

**Safety score** = round(avg of three sub-scores)

### Final score = V × F × S
Range: 1 (don't bother) to 125 (perfect).

### Tiers
- **≥ 60 → Do Now.** This week.
- **30–59 → Do This Quarter.** Plan it.
- **10–29 → Park.** Revisit when tools mature or context changes.
- **< 10 → Avoid.** Effort or risk too high vs. payoff.

---

## Output format

### 1. Scored table
| Use case | V | F | S | Score | Tier |
|----------|---|---|---|-------|------|
| Auto-draft weekly update | 4 | 5 | 5 | 100 | Do Now |
| ... | | | | | |

### 2. Top 3 — Do Now
For each: 1-line description, 1-line why-now, 1-line first step (must be doable in <1 hour).

### 3. Park / Avoid (with the "what would have to change" trigger)
Often more useful than the Do Now list — tells you what you're explicitly NOT building, and when to revisit.

---

## Process

1. **Brainstorm if needed.** If user gives a workflow instead of a list, walk through their week — every recurring task, every painful task, every "I keep meaning to..." task. Aim for 8–12 candidates.

2. **Score each on V/F/S.** Use the rubric. Push back on 5s — they should be rare.

3. **Compute scores + assign tiers.**

4. **Write the top 3 tightly.** First step must be doable in under 1 hour. If it isn't, the score was wrong.

5. **Flag the parked + avoided.** With the trigger condition for revisiting.

---

## Worked example

**Input**
"I'm a senior PM at a B2B SaaS company. I want to use AI more in my week. Things I do a lot: draft PRDs, write status updates, prep for stakeholder reviews, analyze user-research transcripts, write release notes."

**Output**

### Scored table
| Use case | V | F | S | Score | Tier |
|----------|---|---|---|-------|------|
| Auto-draft weekly status update | 4 | 5 | 5 | 100 | Do Now |
| Synthesize user-research transcripts | 5 | 4 | 4 | 80 | Do Now |
| Stakeholder review prep | 4 | 4 | 5 | 80 | Do Now |
| PRD first-draft generator | 4 | 4 | 4 | 64 | Do Now |
| Release notes from PRs | 3 | 5 | 4 | 60 | Do Now |
| Auto-classify inbound customer feedback | 4 | 3 | 4 | 48 | Do This Quarter |
| Replace user interviews with AI personas | 3 | 2 | 1 | 6 | Avoid |

### Top 3 — Do Now
1. **Auto-draft weekly status update.** ~30 min/wk saved, internal-only audience. **First step:** paste last week's git log + Jira ticket exports into Claude with your last status update as a template.
2. **Stakeholder review prep.** Reuses the `meeting-prep-kit` skill; ~1 hr saved per review. **First step:** run meeting-prep-kit on your next exec review.
3. **Synthesize user-research transcripts.** Highest value at ~5 hrs/wk. **First step:** pick the last 3 transcripts, run them through Claude with your usual synthesis frame.

### Parked
- **Auto-classify customer feedback (48):** Revisit once you have ~50 manually-tagged examples to seed the prompt. Re-score in Q3.

### Avoided
- **Replace user interviews with AI personas (6):** Trust risk maxed. Customers find this offensive when they hear about it. Don't.

---

## When to use
- "I should be using AI more — what should I tackle first?"
- After an AI brainstorm, to triage the list
- When your manager asks "what's your AI plan?" and you need a one-pager
- Quarterly self-audit on your personal AI workflow stack

## When NOT to use
- Org-wide AI rollout (change management problem, not personal scoring)
- Single tool evaluation (use `decision-memo-builder` for buy/build/partner)
- Strategic AI investment thesis (use `scpr-framework`)

---

## Pairs well with
- **`decision-memo-builder`** — turn the top Do-Now pick into a memo if you need leadership buy-in
- **`prioritization`** — for non-AI use cases use RICE / Impact-Effort instead
- **`mckinsey-critic`** — run your top-3 picks through the critic to stress-test your "Do Now" choices

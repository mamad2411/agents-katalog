---
name: ai-productivity-long-term-factors
description: Extends developer-productivity measurement beyond short-term throughput (lines of code, task completion time) to capture the long-term factors that determine sustainable productivity in the AI-coding-assistant era — technical expertise development and ownership of work. Use when measuring AI coding assistant ROI, designing DevEx surveys, evaluating whether AI tools are eroding or building engineering capability, or building a holistic productivity dashboard.
---

# AI Productivity: Long-Term Factors

## The Gap in Existing Frameworks

SPACE and DORA capture short-term productivity dimensions (activity, performance, efficiency, flow, delivery throughput, stability). They were built for traditional and DevOps workflows. They do not explicitly address the long-term, human-capital factors that determine whether AI-assisted development is sustainable.

A mixed-methods study at BNY Mellon (2,989 survey responses + 11 in-depth interviews) found that satisfaction with AI coding assistants can be high while reported time savings are modest — and that the most important productivity factors developers identified were the ones existing frameworks miss: **technical expertise** and **ownership of work**.

## The Six Factors

### Short-term (development phase)

**Factor 1 — Self-sufficiency**: Does the tool reduce reliance on external help (coworkers, Stack Overflow)? AI assistants let developers resolve questions without context-switching, but over-reliance can atrophy the skill of independent problem-solving.

**Factor 2 — Frustration and cognitive load**: Does the tool reduce or increase the mental effort of a task? Non-deterministic outputs, the need to verify every suggestion, and prompt-sensitivity can increase cognitive load even when the task itself is faster.

### Short-term (deployment phase)

**Factor 3 — Task completion rate**: The rate at which individuals/teams complete well-defined tasks and the quality of that completion. The number of lines of code is not a reliable proxy; criticality of the work and benefit to the company matter more than volume.

**Factor 4 — Ease of peer review**: Does AI-generated code help or hinder review? Junior developers using AI heavily may produce code that is harder for reviewers to understand. Senior developers may use AI to summarize changes and aid review. The net effect varies by seniority.

### Long-term (career trajectory) — the missing dimensions

**Factor 5 — Technical expertise**: Does the tool build or erode the developer's technical expertise over time? This is the factor existing frameworks miss entirely. Concerns include:
- Junior developers who accept AI output without understanding it never develop the deep debugging skill that comes from grinding through stack traces.
- AI used too early in a career can short-circuit the learning that produces senior engineers.
- When used correctly, AI can *facilitate* expertise development (e.g., looking up security topics, exploring unfamiliar domains).
- The question is not "does the tool make this task faster" but "does the tool make the next task easier because the developer learned something."

**Factor 6 — Ownership of work**: Does the developer feel authorship and accountability for the code? Developers value the sense that they wrote and understand the code — "nothing like doing it yourself." When a production issue arises, developers who have deep knowledge of the code fix issues faster. AI-generated code the developer does not fully understand creates an ownership gap that manifests at incident time.

## The Productivity-Experience Paradox (Corroborating Evidence)

A longitudinal study (Vella & Blincoe, 2026, N=95 matched professionals, two time points six months apart) found:
- Productivity perceptions held stable (84% reported improvement at both time points).
- Developer experience eroded: the proportion reporting worsened experience in at least one DevEx dimension nearly doubled from 14% to 27%.
- Flow state took the steepest fall (share rating it worse nearly tripled, 7% → 20%).
- The correlation between change in flow state and change in productivity was 0.02 — essentially zero.

This is the **productivity-experience paradox**: sustained output perceptions alongside degrading experience. The established relationship between DevEx and productivity appears to stop moving together once AI enters the picture. The long-term factors (expertise, ownership) are the likely mechanism: they erode slowly, do not show up in sprint-level metrics, and eventually manifest as burnout or turnover.

## The Creation-to-Verification Shift

The same longitudinal study documented a shift from creation tasks (writing, refactoring) to verification activities (reviewing, testing), and proposed a new work category: **supervisory engineering work** — directing AI, evaluating its output, correcting its errors. This work does not map to traditional SDLC categories and is not captured by existing productivity frameworks. If your dashboard measures commits and PRs but not supervision effort, you are measuring the work that shrank and missing the work that grew.

## Operationalizing the Long-Term Factors

### Survey Instrument Additions

Add to existing DevEx/DX surveys, administered periodically (not per-sprint):

**Technical expertise items:**
- In the last 90 days, I learned a new technical concept or skill through using AI that I would not have learned otherwise.
- I can explain, line-by-line, the code I shipped this sprint. (Reverse: I shipped code this sprint that I cannot fully explain.)
- When I encounter a novel bug, I feel confident I can debug it without AI assistance.
- My understanding of our codebase has grown / stayed flat / eroded over the last 6 months.

**Ownership items:**
- I feel accountable for the production behavior of the code I commit, regardless of whether AI generated parts of it.
- If an incident were traced to code I committed, I would know where to look first.
- I feel a sense of authorship over the code I ship, even when AI generated portions of it.
- I would be comfortable defending my code's design decisions in a review with senior engineers.

### Metric Integration

| Factor | Short-term proxy | Long-term signal |
|---|---|---|
| Self-sufficiency | External-search frequency | Ability to solve novel problems without AI |
| Cognitive load | NASA-TLX per task | Trend over 6+ months; burnout risk |
| Task completion | PR throughput, cycle time | Quality of completed work (defect rate) |
| Peer review ease | Review turnaround time | Reviewer confidence in author's understanding |
| Technical expertise | (no short-term proxy) | Survey items + ability-to-debug-without-AI test |
| Ownership | (no short-term proxy) | Survey items + incident-response-time-on-owned-code |

### The 6-Month Audit

Every 6 months, run a structured audit:
1. Administer the long-term-factor survey.
2. Compare to the prior period. Track the trend, not the absolute.
3. Cross-reference with turnover, burnout, and incident data.
4. If Factor 5 or 6 is declining, treat it as a leading indicator — the productivity-experience paradox means output metrics will lag the experiential erosion by months.

## A-Tech Value Alignment

| Value | Alignment |
|---|---|
| Open-source AI | Open tools make the expertise-development tradeoff visible and auditable; proprietary tools hide the mechanism |
| Data privacy | Survey data is sensitive; administer locally, aggregate for org-level insight |
| Financial freedom | Sustainable engineering careers are the foundation of financial freedom for developers; measuring the long-term factors protects that |
| Practical implementation | The survey items and audit cadence are concrete and ready to deploy |

## When to Use This Skill

- You are measuring the impact of AI coding assistants and want to avoid the productivity-experience paradox blind spot.
- You are designing a DevEx survey and want to capture expertise and ownership, not just flow and cognitive load.
- You are a team lead noticing that output is up but code understanding seems to be down.
- You are evaluating whether to roll out AI coding tools to junior developers and want to assess the expertise-erosion risk.
- You are building a productivity dashboard and want leading indicators, not lagging ones.

## Cross-References

- `prompt-wait-evaluate-flow-collapse` — the interaction-loop mechanism behind flow-state erosion; the long-term factors explain why the erosion does not immediately show up in output metrics.
- `ai-era-devex-measurement-at-scale` — the DevEx measurement framework this skill extends with long-term factors.
- `supervisory-engineering-work` — the new work category that existing frameworks miss; measuring it is a prerequisite for capturing the reallocation of effort.
- `agentic-coding-returns-to-expertise` — how returns to expertise shift when agentic coding enters the picture.
- `self-reported-vs-measured-ai-productivity-divergence` — the perception-reality gap; the long-term factors are where the gap is largest because they are hardest to self-assess.
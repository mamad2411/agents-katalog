---
name: report-writing-for-ceo
description: >
  Write structured, evidence-led reports for CEO/executive audiences. Covers
  incident reports, POC outcome reports, product portfolio pitches, and any
  strategic document requiring clear framing, root cause analysis, external
  context, and actionable recommendations.
---

# Report Writing for CEO / Executive Audiences

## When to Use

Use when the user asks to write, structure, or review a report for executive or CEO-level consumption. This includes incident post-mortems, POC outcome reports, product portfolio pitching documents, quarterly business reviews, strategy memos, or any document where the audience needs a clear answer to "What happened, why does it matter, and what must change?"

## Procedure

### 1. Clarify report type and audience
Determine whether this is an incident report, POC outcome document, product portfolio pitch, or strategic memo. Identify the primary audience (CEO, board, investors, technical leads) and their key concerns (risk, cost, timeline, competitive position, operational health).

### 2. Open with purpose and framing
State the report's purpose in 2–4 sentences. Explain what happened, why it happened on this occasion, distinguish persistent weakness from immediate trigger, and assess whether external conditions contributed. Add one paragraph describing the intended audience.

### 3. Write the executive summary
Answer three questions quickly:
- **What failed / what was achieved?**
- **Why then / why now?**
- **What must change?**

Cover what users or participants experienced, duration and severity, immediate outcome, primary technical or business conclusion, and whether an external trigger was identified, suspected, or not proven.

### 4. Define scope, evidence, and method
List evidence sources (logs, data, market events, prior comparisons, control periods). Add a short note on evidence limitations and what could not be proven.

### 5. Build the incident or project overview
Create a factual timeline of events (detection, escalation, mitigations, recovery, follow-up for incidents; milestones, decisions, pivots for projects). Describe service or business impact (latency, timeouts, queue growth, transaction drop, complaints, or adoption metrics, revenue impact). Summarise technical or business symptoms observed.

### 6. Describe system and workload context
Briefly describe the relevant application flow, database design, workload path, critical transaction path, key tables/services, concurrency model, cluster usage, and known design constraints. Keep this focused on only what is needed to understand the report's findings.

### 7. Perform internal technical or business analysis
- **(a) What the system/platform was doing:** dominant waits, bottlenecks, resource profile, failure mechanics.
- **(b) What it was not:** rule out common suspects where evidence supports that.
- **(c) Mechanism of failure or outcome:** hot object, serialisation point, concurrency ceiling, why throughput fell while demand persisted, why recovery occurred when it did.

Keep evidence-led; separate observed facts from interpretation.

### 8. Analyse external demand and market perspective (mandatory)
This section prevents internally framed analysis. Cover:
- **(a) Participant/merchant/customer concentration** — top contributors by volume and burst rate, comparison with normal distribution.
- **(b) Transaction mix and behavioural shifts** — changed transaction types, message sizes, session duration, retry behaviour, failure-retry loops.
- **(c) Market or external event correlation** — campaign launches, ticket sales, salary-day cycles, holidays, special calendar effects.
- **(d) Time-pattern and burst analysis** — minute-level burstiness, short-lived spikes, synchronised behaviour, retry amplification.
- **(e) Comparison set** — preceding comparable periods, prior incidents, non-incident days with similar load, known external-event days.

### 9. Answer "Why this day and not others"
Use a comparison table with columns: **Factor**, **Incident/Project day**, **Comparison days**, **Assessment** (Proven / likely / not relevant). Cover structural weakness, trigger event or demand pattern, and amplification factors. Explicitly address why the issue surfaced on that day and not others, and whether it recurred before.

### 10. Present root cause framework
Three-part structure:
- **(a) Structural technical/business root cause** — the persistent design or architecture weakness.
- **(b) Trigger event or demand pattern** — the immediate condition that pushed the system into failure, or state clearly if no distinct trigger can be proven.
- **(c) Amplification factors** — retries, concentration, burst synchronisation, operational delays, high-sensitivity design margins.

### 11. List findings
Concise findings each supported by evidence. Label each as technical, market, behavioural, or operational where useful.

### 12. Define actions and recommendations
Four categories:
- **(a) Structural fixes** — design changes that remove the underlying weakness.
- **(b) Demand-management or participant-facing controls** — rate shaping, retry discipline, throttling, event monitoring.
- **(c) Operational mitigations** — runbooks, alerting, temporary mitigation steps.
- **(d) Evidence improvements** — telemetry gaps to close.

Present as a table with **Action**, **Purpose**, **Owner**, **Priority** (High/Medium/Low).

### 13. Capture open questions
Questions that remain unresolved (e.g., was there a traffic burst not visible in telemetry? Did retries amplify load? Was there a common external pattern? Do finer-grained measurements change interpretation?).

### 14. Add appendices
Key metrics appendix, technical identifiers appendix, external event appendix (market events, campaigns, participant notes), comparison appendix (charts for comparable periods).

### 15. Apply writing guidance
- Do not stop at the internal mechanism. Always test whether external demand patterns or participant behaviour contributed.
- Clearly label what is **proven**, **likely**, and **not proven**.
- Explain recurrence. Avoid implying causation from timing alone.
- If no distinct trigger is found, say so plainly.
- A strong final report lets readers understand both the engineering failure mode and the real-world operating conditions that exposed it.

## Pitfalls

- **Do not skip the external demand and market perspective section** — this is mandatory and prevents internally framed analysis.
- **Do not imply causation from timing alone** — correlation is not causation.
- **Do not stop at the technical mechanism** without testing whether external demand patterns or participant behaviour contributed.
- **Do not leave "why this day and not others" unanswered** — a technically correct root cause is insufficient without explaining timing and recurrence.
- **Do not pad the system context section** with irrelevant architecture details; keep it focused on what is needed to understand the findings.
- **Do not present speculation as fact** — clearly label what is proven, likely, and not proven.
- **Do not omit evidence limitations** — acknowledging what could not be proven strengthens credibility.
- **Do not write for technical peers alone** — the CEO audience needs business impact, risk assessment, and clear recommendations, not deep technical detail.
- **For POC and portfolio reports**, adapt the incident-focused sections (e.g., "failure mechanism" becomes "outcome mechanism", "incident overview" becomes "project overview") while keeping the same structural rigour.

## Verification

1. The report opens with a clear purpose and audience paragraph.
2. The executive summary answers: What happened? Why then? What must change?
3. Scope, evidence, and method section lists all evidence sources and their limitations.
4. Timeline and impact sections are factual and complete.
5. System context is concise and relevant to the findings.
6. Internal analysis separates observed facts from interpretation.
7. External demand and market perspective section is present and substantive (mandatory).
8. "Why this day and not others" includes a comparison table with proven/likely/not relevant assessments.
9. Root cause framework has all three parts: structural, trigger, amplification.
10. Findings are concise, evidence-supported, and labelled by type where useful.
11. Actions include all four categories (structural, demand-management, operational, evidence) with owners and priorities.
12. Open questions are captured honestly.
13. Writing guidance is followed: no causation-from-timing, clear labelling of certainty levels, recurrence explained.

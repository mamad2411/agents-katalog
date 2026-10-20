---
name: deep-retro
description: Deep post-incident retrospective — find process-level root causes and actionable action items
argument-hint: "[scope]"
related:
  - deep-debug
  - analyze-root-cause-analysis
  - deep-thinking
  - report
  - update-tests
  - follow-tool-git

---

## Goal

Run a thorough post-incident / post-project retrospective to find process-level root causes, produce actionable learnings, and define action items that prevent recurrence

## Scope

Use after an incident, failed deployment, major bug, or project milestone, or when the team wants to review why what happened was even possible
Not for debugging a live issue — use `/deep-debug` first
Not for reviewing work with no incident — use `/deep-review-codebase` instead

## Execute

### 1. Define Retro Scope

> Goal: State what is being reviewed and to what end

1. Identify the incident or event to retro: symptoms, duration, impact
2. Identify the stakeholders who should join or provide input
3. Set a timebox: small ≤ 30 minutes | medium ≤ 1 hour | large ≤ 2 hours
4. Collect initial context: logs, metrics, timeline, alerts

### 2. Build Timeline

> Goal: Build a detailed timeline from before the incident to after resolution

1. Assemble the events in chronological order
2. Mark trigger, detection, response, mitigation, resolution
3. Run `/report` to present the timeline: Time, Event, Actor, Evidence
4. Check for gaps or delays in each phase

### 3. Gather Evidence

> Goal: Collect complete data before analysis

1. Run `/deep-debug` if there is no clear root cause yet
2. Run `/analyze-root-cause-analysis` to build the causal graph
3. Collect logs, traces, metrics, screenshots, error messages
4. Collect decisions and communication within the team
5. Inspect git history: `/follow-tool-git` or `/check-git-logs`

### 4. Identify Contributing Factors

> Goal: Find the factors that contributed to the incident, not just a single root cause

1. Use 5 Whys or a Fishbone diagram to find contributing factors
2. Split into categories: people, process, tools, environment, communication
3. Mark which factors are controllable and which are not
4. Avoid blame — focus on system and process

### 5. Assess Impact

> Goal: Measure the impact concretely

1. State the impact on users: count, duration, severity
2. State the impact on the team: time to detect, time to resolve, context switching
3. State the impact on business: revenue, reputation, compliance
4. Run `/report` showing impact by dimension

### 6. Extract Learnings

> Goal: Summarize what was learned in a real and actionable way

1. Identify what worked well (keep)
2. Identify what should stop or be adjusted (stop)
3. Identify what should start (start)
4. Tie learnings directly to contributing factors
5. If learnings are unclear → run `/deep-thinking`

### 7. Define Action Items

> Goal: Create action items that reduce the chance of recurrence

1. Build the action items as a list with owner, due date, success criteria
2. Group action items by level: immediate (≤ 1 week), short-term (≤ 1 month), long-term (≤ 3 months)
3. Every action item must link to an identified contributing factor
4. If code changes → run `/update-tests` to create a regression test
5. If process changes → write a runbook or checklist

### 8. Communicate And Follow Up

> Goal: Communicate the retro results and track the action items

1. Run `/report` summarizing timeline, root cause, impact, learnings, action items
2. Record the retro in the project's notes file or wiki
3. Track action items against their due dates
4. In the next retro, review whether the action items actually worked

## Rules

### 1. Blameless Culture

- Never blame individuals — focus on system, process, context
- Use data and evidence, not feelings
- Build psychological safety for the team

### 2. Process-Level Root Cause

- Find root causes at the process level, not just the technical one
- Ask "why did the process allow this to happen"
- Identify contributing factors across multiple dimensions

### 3. Actionable Outcome

- Every finding needs an action item or an explicitly recorded decision
- Don't end at "we know now" — there must be follow-up
- Action items must have an owner and a due date

### 4. Time Bound

- Don't spend too long on discussion
- If the issue is complex → split across several retro sessions
- Finish with an action plan, not just a discussion

- Use /deep-debug `### 3. Triage Incident` if needed

## Expected Outcome

1. A detailed, fact-accurate incident timeline
2. Contributing factors and process-level root cause
3. An explainable impact assessment
4. Actionable action items with owner and due date
5. Learnings that reduce the chance of recurrence
6. A retro document that stakeholders can understand

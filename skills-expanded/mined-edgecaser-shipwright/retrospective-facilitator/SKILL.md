---
name: retrospective-facilitator
description: "Runs structured team retrospectives using proven formats (Start/Stop/Continue, 4Ls, Sailboat, Mad/Sad/Glad). Produces an action item list with owners, due dates, and follow-up mechanisms to ensure retro outcomes actually lead to change."
category: measurement
default_depth: standard
---

# Retrospective Facilitator

Read `docs/workflow-contract.md` once per session before applying this skill. Resolve it from the nearest ancestor of this file containing `manifest.json`; all Shipwright paths are relative to that root.

## Description

Runs structured team retrospectives using proven formats (Start/Stop/Continue, 4Ls, Sailboat, Mad/Sad/Glad). Produces an action item list with owners, due dates, and follow-up mechanisms to ensure retro outcomes actually lead to change.

## When to Use

- End of sprint retrospectives
- Post-launch reviews
- Post-incident retrospectives
- Quarterly team health checks
- After any significant milestone or project completion

## Available Formats

### Format 1: Start / Stop / Continue

Best for: Regular sprint retros. Simple and actionable.

```markdown
## Start (things we should begin doing)
- [Suggestion], Raised by: [name/role]
  - Why: [reasoning]

## Stop (things we should stop doing)
- [Suggestion], Raised by: [name/role]
  - Why: [reasoning]

## Continue (things that are working well)
- [Observation], Raised by: [name/role]
  - Evidence: [why this is working]
```

### Format 2: 4Ls (Liked, Learned, Lacked, Longed For)

Best for: Post-project or post-launch retros. Good for capturing learnings.

```markdown
## Liked (what went well)
- [Item]

## Learned (new insights or skills gained)
- [Item]

## Lacked (what was missing)
- [Item]

## Longed For (what we wish we had)
- [Item]
```

### Format 3: Sailboat

Best for: Visual teams. Good for identifying risks alongside positives.

```markdown
## Wind (what propelled us forward)
- [Tailwind factor]

## Anchor (what held us back)
- [Drag factor]

## Rocks (risks ahead)
- [Upcoming risk]

## Island (our goal / destination)
- [What we're sailing toward]
```

### Format 4: Mad / Sad / Glad

Best for: Emotional check-ins. Good when team morale needs attention.

```markdown
## Mad (frustrated about)
- [Item]

## Sad (disappointed about)
- [Item]

## Glad (happy about)
- [Item]
```

## Depth

| Scope | Use When | Sections to Include |
|---|---|---|
| **Light** | Quick end-of-sprint check-in with a stable team | Set the Stage, Gather Input (one format), Action Items |
| **Standard** | Regular sprint or post-launch retro | All sections |
| **Deep** | Post-incident review, post-mortem, or quarterly team health check | All sections + timeline reconstruction, contributing factor analysis, systemic pattern review across past 3+ retros |

**Omit rules:** At Light depth, skip Discuss Top Themes and Review Previous Action Items. Produce only observations and an owned action item list.

## Framework

### Step 1: Set the Stage

```markdown
## Retrospective: [Sprint/Project/Event Name]
**Date:** [date]
**Participants:** [names]
**Facilitator:** [name]
**Format:** [chosen format]
**Time scope:** [what period are we reflecting on]

### Ground Rules
- Focus on processes and systems, not individuals
- Assume positive intent
- Be specific, "communication was bad" → "We didn't have a single source of truth for the API spec, which caused 3 misalignment bugs"
- Everyone participates
```

### Step 2: Gather Input

For each format category, gather observations:

```markdown
## Observations

[Use the chosen format structure above]

### Themes (clustered from raw observations)
| Theme | Observations | Votes/Frequency |
|---|---|---|
| [Theme 1, e.g., "Requirements clarity"] | [N] related items | [N] votes |
| [Theme 2, e.g., "Cross-team communication"] | [N] related items | [N] votes |
| [Theme 3] | [N] | [N] |
```

### Step 3: Discuss Top Themes

For each prioritized theme (top 2-3 by votes):

```markdown
### Theme: [Name]

**What happened:**
[Factual description of the issue or success]

**Root cause(s):**
- [Cause 1]
- [Cause 2]

**Impact:**
[How this affected the team, product, or users]

**Proposed action:**
[Specific, actionable improvement]
```

### Step 4: Define Action Items

```markdown
## Action Items

| # | Action | Owner | Due Date | Status | Success Criteria |
|---|---|---|---|---|---|
| 1 | [Specific action] | [Name] | [Date] | Open | [How we know it's done] |
| 2 | [Specific action] | [Name] | [Date] | Open | [How we know it's done] |
| 3 | [Specific action] | [Name] | [Date] | Open | [How we know it's done] |

### Follow-Up Plan
- Action items reviewed at: [next retro / standup / 1:1]
- Accountability mechanism: [how we'll track progress]
```

### Step 5: Review Previous Action Items

```markdown
## Previous Retro Action Items (Review)

| Action | Owner | Status | Outcome |
|---|---|---|---|
| [Action from last retro] | [Name] | [Done / In Progress / Not Started] | [What happened] |
```

## Minimum Evidence Bar

**Required inputs:** Time scope of the retrospective, list of participants, at least one concrete observation or data point per format category.

**Acceptable evidence:** Participant observations, sprint velocity data, incident timelines, user feedback excerpts, previous retro action item status.

**Insufficient evidence:** With no concrete observations, request examples. Small teams and uneven participation can still run a scoped retrospective; disclose whose perspective is missing and avoid claiming team consensus.

**Hypotheses vs. findings:**
- **Findings:** Observed events, measured outcomes, action item completion status, must reference what actually happened.
- **Hypotheses:** Root cause explanations and proposed process changes, must be labeled as team-generated theories to test.

## Output Format

Produce a Retrospective Report with:
1. **Setup**, date, participants, format, scope
2. **Observations**, gathered input using the chosen format
3. **Themes**, clustered and prioritized
4. **Discussion**, root causes and proposed actions for top themes
5. **Action Items**, owned, dated, with success criteria
6. **Previous Items Review**, accountability check

**Shipwright Signature (required closing):**
7. **Decision Frame**, top process change recommendation, trade-off (effort to implement vs. expected improvement), confidence with evidence quality (number of corroborating observations, recurrence across retros), owner, decision date, revisit trigger
8. **Unknowns & Evidence Gaps**, themes raised by only one person, root causes not yet validated, missing perspectives from absent team members
9. **Pass/Fail Readiness**, PASS if observations are traceable and each agreed action has an owner and due date, plus success criteria at Standard/Deep depth. Zero or one action is valid when the findings warrant it; do not invent actions or consensus. FAIL if agreed actions are unowned or evidence is missing.
10. **Recommended Next Artifact**, Which Shipwright skill to run next and why

## Common Mistakes to Avoid

- **No action items**, A retro without actions is just venting
- **Unowned actions**, "The team will improve communication" means nobody will
- **Never reviewing past actions**, Without follow-through, teams stop trusting retros
- **Blame culture**, Focus on systems and processes, not individuals
- **Always the same format**, Rotate formats to keep retros fresh and surface different insights

## Weak vs. Strong Output

**Weak:**
> "Action item: Improve communication. Owner: The team. Due: Ongoing."

No specific behavior change, no individual owner, no deadline, no success criteria, this will never get done.

**Strong:**
> "Action item: Create a shared #api-changes Slack channel and post breaking changes 48 hours before merge. Owner: Sarah (tech lead). Due: 2026-04-01. Success criteria: zero surprise API breakages in the next sprint."

Specific mechanism, named owner, concrete deadline, and a measurable way to know if it worked.

---
name: ceo-daily-brief
description: CEO Daily Brief — a 7-step workflow for turning morning chaos into a structured command brief. Uses Claude to collect, filter, and prioritise the day's inputs, extract actions, flag decisions, and batch-draft high-value replies. Source @skilldropai.
---

## What this skill does

Runs a repeatable 7-step morning workflow. Give Claude your raw inputs (calendar, email, news, team updates) and it returns one clean brief: top 3 priorities, key decisions, delegations, and a day plan — plus pre-drafted replies for your highest-value communications.

---

## The 7 Steps

### Step 1 — Collect Inputs

Paste or describe:
- **Calendar:** meetings today and their intent
- **Email:** subject lines or summaries of flagged threads
- **News:** anything sector-relevant from overnight
- **Team updates:** Slack/async messages that need eyes

**Prompt:**
```
Here are my inputs for today:

CALENDAR:
[paste meetings]

EMAIL:
[paste subject lines / summaries]

NEWS:
[paste headlines]

TEAM UPDATES:
[paste Slack messages / async notes]

Do not filter yet. Just acknowledge receipt and confirm you have everything.
```

---

### Step 2 — Separate Signal from Noise

**Core principle:** Not everything urgent is important. Not everything important is urgent.

**Prompt:**
```
Using the inputs above, separate signal from noise.

Signal = items that affect revenue, strategy, people, or risk.
Noise = FYI items, low-stakes updates, anything I can ignore today.

Return two lists: SIGNAL and NOISE. One line per item. No explanations yet.
```

---

### Step 3 — Extract Actions

**Prompt:**
```
From the SIGNAL list, extract every required action.

For each action, classify it as:
- DECIDE (requires my judgment today)
- DELEGATE (someone else should own this)
- DEFER (real but not today)
- RESPOND (needs a reply from me)

Format as a table: Action | Type | Owner | Deadline
```

---

### Step 4 — Flag Decisions

**Prompt:**
```
From the DECIDE items, identify which decisions only I can make — not my team.

For each, state:
1. What is the decision?
2. What is the consequence of deciding wrong?
3. What information do I still need before deciding?

Keep it to bullet points. No padding.
```

---

### Step 5 — Build the Brief

**Prompt:**
```
Now build my CEO Daily Brief.

Format:
**Date:** [today]
**Top 3 Priorities:** (the 3 things that move the needle most today)
**Key Decisions:** (flagged decisions with context)
**Delegate Today:** (with owner names)
**Team Check-ins:** (anyone I need to connect with and why)
**Day Plan:** (time-blocked outline, not granular — blocks of 60–90 min)

Keep the whole brief under one page. Every line must earn its place.
```

---

### Step 6 — Draft Responses

**Prompt:**
```
From the RESPOND items, draft replies for the top 3 highest-value communications.

For each draft:
- Match the tone of the thread (formal / direct / warm)
- Be concise — no longer than the original message warrants
- End with a clear next step or ask

Present each draft in a labelled block ready to copy-paste.
```

---

### Step 7 — Save as Skill

After running the brief a few times, save your personalised version:

**Prompt:**
```
I've now run this CEO Brief workflow [N] times. Based on what you know about my inputs, decisions, and communication style, suggest 3 ways to make the workflow faster or more useful for me specifically.

Then save the improved version as a repeatable skill I can invoke tomorrow morning with one prompt.
```

---

## One-Shot Morning Prompt

For speed, paste everything into this single prompt:

```
You are my chief of staff. Here are this morning's inputs:

CALENDAR: [paste]
EMAIL: [paste subject lines]
NEWS: [paste headlines]
TEAM: [paste updates]

Run the CEO Daily Brief workflow:
1. Separate signal from noise
2. Extract and classify all actions (DECIDE / DELEGATE / DEFER / RESPOND)
3. Flag decisions only I can make
4. Build the brief (priorities, decisions, delegations, day plan — one page max)
5. Draft replies for the top 3 RESPOND items

Return everything in order. Use headers. Be ruthless about brevity.
```

---

## Why it works

- Forces you to separate input-processing from decision-making
- Batches all replies into one focused block instead of reactive threading
- The brief is a forcing function: if it doesn't fit one page, you have too many priorities
- Saving as a skill means Claude learns your patterns over time

---

## Related skills

- `build-claude-agent-7-steps` — build Claude-powered automations to pre-populate the input collection step
- `claude-thinking-partner` — for strategic decisions flagged in Step 4 that need deeper analysis
- `claude-prompt-chaining` — for multi-stage deliverables surfaced in Step 6

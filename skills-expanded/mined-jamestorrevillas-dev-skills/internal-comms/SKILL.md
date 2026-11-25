---
name: internal-comms
description: Use this skill for internal team communications — daily standups, sprint updates, status reports, retrospective notes, leadership updates, or any written communication within a team or organization. Trigger on keywords: standup, DSU, status update, sprint update, team communication, write to my team, leadership update, slack message to team, retrospective notes, EOD update.
---

# Internal Communications

## Core Principle

Internal comms should be brief, informative, and actionable. No filler. No padding. Respect your reader's time.

---

## Daily Standup (DSU) Format

### Structure
```
Yesterday: [what you completed — be specific]
Today: [what you're working on]
Blockers: [anything blocking you — or "none"]
```

### Taglish Style (for Filipino dev teams)
```
Good afternoon.
Yesterday, na-finish ko yung [task].
Today, mag-wo-work ako sa [task].
[Wala naman blocker. / May blocker ako — [describe].]
That's all from me, [Name].
```

### Passing the floor
```
That's all from me, [next person's name].
```

### Rules
- Be specific — "fixed the auth bug" not "did some coding"
- Name the story/ticket if relevant
- Blockers are for the team, not personal updates
- Keep it under 60 seconds when spoken

---

## Sprint Update

```
## Sprint [X] Update — [Date]

**Status:** On track / At risk / Behind

**Completed this sprint:**
- [Story/task] — [brief outcome]
- [Story/task] — [brief outcome]

**In progress:**
- [Story/task] — [current status, ETA]

**Blockers:**
- [blocker] — [what you need to resolve it]

**Next sprint focus:**
- [preview of upcoming work]
```

---

## Leadership / Stakeholder Update

Use BLUF (Bottom Line Up Front):
```
[One sentence: what they need to know]

[2-3 sentences: context and detail]

[Optional: what decision or action you need from them]
```

Example:
```
The Query Clarity Assessment Agent is code-complete and 
pending final integration review.

Unit and integration test coverage is at 95%+. 
The PR is on hold pending Anand's return to finalize 
the Document Extraction dependency.

Expected deployment: end of next sprint.
```

---

## Slack / Team Message Guidelines

- **Lead with the point** — don't bury the main message
- **@mention only when action is needed** from that person
- **Use threads** for follow-ups to keep channels clean
- **Emoji reactions** to acknowledge without cluttering threads
- **Mark urgent clearly** — "⚠️ Heads up:" or "🚨 Action needed:"

### Raising a Blocker
```
🚨 Blocker — [brief title]

I'm blocked on [task] because [specific reason].
What I need: [exactly what you need, from whom]
Impact: [what gets delayed if not resolved]
```

---

## Tone Guidelines

- **Professional but human** — not robotic, not overly casual
- **Direct** — say what you mean without over-softening
- **Constructive** — focus on solutions, not just problems
- **Honest** — don't spin bad news; present it clearly with a path forward

### Phrases to Avoid
- "Just wanted to reach out..." → just say the thing
- "Per my last message..." → restate clearly instead
- "As per usual..." → sounds passive-aggressive
- "Does that make sense?" → assumes confusion; say "Let me know if you have questions"

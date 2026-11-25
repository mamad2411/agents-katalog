---
name: async-comms
description: "When to activate: async communication, written communication, remote work, async-first, Loom, Notion, timezone management, reducing meetings"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: business
  domain: productivity
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Async Communication

## Async-First Principles

1. **Default to async** — synchronous communication is expensive; use it only when async fails
2. **Write to be understood without back-and-forth** — assume no follow-up questions
3. **Make decisions visible** — document reasoning, not just outcomes
4. **Respect focus time** — don't expect immediate responses
5. **Over-communicate context** — remote colleagues lack ambient information

## Response Time Expectations by Urgency

| Tier | When | Expected response |
|------|------|------------------|
| Urgent | Production down, blocker unblocking someone | < 1 hour |
| High | Needs today to unblock work | < 4 hours |
| Normal | Standard work item | < 24 hours |
| Low | FYI, no action needed | No response required |

Communicate urgency explicitly: `[URGENT]`, `[FYI]`, `[ACTION NEEDED by Fri]` in subject/header.

## Written Communication Standards

### Length Norms
| Message type | Target length |
|-------------|--------------|
| Slack message | 1-3 sentences; longer → write a doc |
| Status update | 3-5 bullet points |
| Decision doc | 1-2 pages max |
| RFC/proposal | Enough to get to a decision, no more |
| Meeting notes | Action items + decisions only |

### Structure Template (for complex async messages)
```
## [Title / What this is about]

**TL;DR:** [One sentence summary]

**Context:** [Why this matters, 1-2 sentences]

**The Ask / Decision needed:**
- [Option A — recommended] because [reason]
- [Option B] — tradeoffs: [...]

**By when:** [Date]

**If no response by [date], I'll proceed with [option A].**
```

### Formatting Principles
- Use headers for messages > 5 lines
- Bold the key ask
- Lead with the most important information (inverted pyramid)
- Use numbered lists for ordered steps; bullets for unordered items
- Avoid walls of text — one idea per paragraph

## Tool Usage by Message Type

| Scenario | Tool | Why |
|----------|------|-----|
| Complex explanation (> 5 min to read) | Written doc (Notion/Confluence) | Searchable, commentable, persistent |
| Visual walkthrough, demo, code review | Loom video | Context-rich, no scheduling |
| Quick question or status | Slack/Teams message | Low-latency, conversational |
| Decision with stakeholders | Doc + Slack link | Structured + visible |
| Meeting notes, retrospectives | Notion/Confluence | Searchable record |
| Incident communication | Dedicated thread + doc | Centralized, timestamped |

## Timezone Management

### Scheduling Rules
- [ ] Identify each team member's core hours (overlap window)
- [ ] Avoid scheduling outside overlap window unless critical
- [ ] Rotate meeting times for distributed teams — don't always sacrifice one timezone
- [ ] Show times in multiple zones: `10am ET / 3pm GMT / 11pm SGT`
- [ ] Use tools that respect local time (World Time Buddy, Calendly)

### Async Handoff Protocol (for work crossing timezones)
```
End-of-day handoff message:
- What I completed today: [list]
- What's blocked / needs input: [list with links]
- What I'm picking up tomorrow: [list]
- Anything time-sensitive for your morning: [explicit callout]
```

## Async Decision-Making Process

### For decisions involving multiple stakeholders:
1. **Draft** — owner writes doc with options, recommendation, deadline
2. **Review window** — 48-72h for async feedback (stakeholders comment in doc)
3. **Synthesis** — owner updates doc with decision and rationale
4. **Announce** — brief Slack message linking to decision doc
5. **Archive** — doc stays as permanent record

### When to escalate to sync:
- After 2 rounds of async back-and-forth with no resolution
- High emotional stakes (performance, conflict)
- Complex real-time collaboration (whiteboarding, pair debugging)
- Relationship-building or onboarding

## Meeting Alternatives

| Meeting type | Async alternative |
|-------------|-----------------|
| Status update | Written update in shared doc or Slack |
| Decision meeting | Decision doc with comment window |
| Brainstorm | Async doc with input invited, then synthesis |
| Code review | Async PR comments + Loom for complex feedback |
| 1:1 check-in | Written agenda + async doc for FYI items |
| All-hands | Recorded video + written Q&A doc |

## Async Onboarding

### 30-day async onboarding kit:
- [ ] Written "how we work" doc (communication norms, tools, channels)
- [ ] Recorded Loom walkthroughs of key systems
- [ ] FAQ doc for common first-week questions
- [ ] Slack channel map (what goes where)
- [ ] "Who to ask" directory by topic
- [ ] Daily async check-in for first 2 weeks: "what are you working on, what's confusing?"

## Slack/Teams Channel Norms

| Channel type | What belongs there |
|-------------|-------------------|
| `#announcements` | Company-wide, one-way, no chatter |
| `#team-[name]` | Team updates, decisions, async discussion |
| `#proj-[name]` | Project-specific, archived when done |
| `#help-[topic]` | Questions, searchable answers |
| `#random` | Off-topic, social |
| DMs | Private, sensitive, or quick personal items only |

**Rules:**
- No important decisions in DMs — move to channel or doc
- Use threads for responses to keep channels readable
- Pin important links and decisions in channel details
- Archive inactive project channels

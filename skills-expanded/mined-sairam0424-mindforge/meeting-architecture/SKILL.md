---
name: meeting-architecture
version: 1.0.0
min_mindforge_version: 10.3.0
status: stable
triggers: meeting architecture, meeting design pattern, decision documentation, async-first communication, standup optimization, meeting efficiency, RFC process, architecture decision record, async collaboration, meeting agenda design, meeting decision log, remote meeting facilitation
---

# Meeting Architecture

## When this skill activates

This skill activates when designing effective meetings, implementing async-first communication patterns, optimizing standups, documenting decisions, creating RFC processes, or facilitating remote meetings. It applies to tech leads, engineering managers, and senior engineers responsible for team communication effectiveness.

## Mandatory actions when this skill is active

### Before scheduling any meeting

1. **Apply the async-first test** — Can this be an email, Slack message, document, or recorded video? Only schedule a synchronous meeting if you need real-time discussion, debate, or decision-making.
2. **Define the meeting purpose** — Is it informational (status update), collaborative (brainstorming), or decisional (approve/reject proposal)? Different purposes require different formats.
3. **Identify required vs optional attendees** — Required: people who must participate for the meeting to succeed. Optional: people who benefit from being there but aren't essential. Respect people's time.
4. **Create a clear agenda** — No agenda = no meeting. Agenda should include: topics, time allocation, desired outcomes, and pre-reads. Send agenda 24 hours in advance.

### During meeting design

#### Meeting Type Catalog

**1. Daily Standup (15 minutes max)**
- **Purpose**: Synchronize team, surface blockers, maintain momentum.
- **Format**: Each person answers: (1) What did I accomplish yesterday? (2) What am I working on today? (3) Am I blocked?
- **Optimizations**:
  - Keep it to 15 minutes. If you need more time, the team is too big or the updates are too detailed.
  - Do it async if possible (Slack standup bot, Geekbot, GitHub comments on project board).
  - Timebox each person to 1-2 minutes. Use a timer.
  - Blockers get discussed after standup, not during. Don't derail everyone's focus.
- **Pitfall**: Standup becomes a status report to the manager. It should be peer-to-peer synchronization, not upward reporting.

**2. Sprint Planning (1-2 hours)**
- **Purpose**: Commit to work for the upcoming sprint.
- **Format**: Review backlog, prioritize, estimate, assign ownership, identify dependencies.
- **Pre-work**: Product or tech lead preps the backlog. Engineers review tickets ahead of time. Don't do backlog grooming during sprint planning.
- **Optimizations**:
  - Timebox story estimation. Use t-shirt sizes (S/M/L) or Fibonacci (1/2/3/5/8) to avoid false precision.
  - Identify blockers early. If a task depends on another team, escalate before the sprint starts.
  - Set a realistic capacity. Don't overcommit. Leave 20% buffer for unplanned work (bugs, support, incidents).
- **Pitfall**: Spending 30 minutes debating whether a task is a 3 or a 5. Estimates are guesses. Move on.

**3. Retrospective (45-60 minutes)**
- **Purpose**: Reflect on what went well, what didn't, and how to improve.
- **Format**: What went well? What went poorly? What should we start/stop/continue doing?
- **Facilitation**:
  - Everyone contributes. Silence from some people means they're not engaged or don't feel safe.
  - Focus on systems, not individuals. "Code reviews are too slow" is better than "Alice didn't review my PR."
  - Action items must have owners and deadlines. Otherwise they're wishes, not commitments.
- **Optimizations**:
  - Rotate facilitator. Prevents one person from dominating.
  - Use techniques like Start/Stop/Continue, 4Ls (Liked/Learned/Lacked/Longed For), or Rose/Bud/Thorn.
  - Review action items from the previous retro. Did we follow through? If not, why?
- **Pitfall**: Retrospectives devolve into venting sessions. Keep it constructive.

**4. Design Review / Architecture Review (60-90 minutes)**
- **Purpose**: Vet technical designs before implementation. Catch issues early.
- **Format**: Presenter shares design doc (sent 24-48 hours in advance). Team probes assumptions, identifies edge cases, suggests alternatives.
- **Pre-work**: Attendees read the design doc before the meeting. Don't use meeting time for reading.
- **Optimizations**:
  - Use a design doc template: problem statement, requirements, proposed solution, alternatives considered, tradeoffs, open questions.
  - Assign a devil's advocate. Their job is to poke holes. Prevents groupthink.
  - Document decisions in the design doc during the meeting. Don't rely on memory.
- **Pitfall**: Rubber-stamping designs that are already implemented. Design reviews should happen before code is written, not after.

**5. Incident Postmortem (60 minutes)**
- **Purpose**: Learn from incidents, identify systemic improvements.
- **Format**: Timeline, root cause analysis, what went well, what went poorly, action items.
- **Facilitation**:
  - Blameless. Focus on systems, not individuals.
  - Use the Five Whys to get to root cause.
  - Every action item needs an owner and a deadline.
- **Optimizations**:
  - Share postmortem document 24 hours before the meeting. Use meeting time for discussion, not writing.
  - Invite all incident responders + relevant stakeholders.
  - Timebox to 60 minutes. If you can't finish, schedule a follow-up.
- **Pitfall**: Postmortems that generate 15 action items but complete zero. Prioritize. Pick the top 3 and execute.

**6. 1:1s (30 minutes, weekly or bi-weekly)**
- **Purpose**: Manager-engineer relationship building, career development, feedback, unblocking.
- **Format**: Open agenda. Employee drives the conversation. Manager listens, coaches, provides context.
- **Optimizations**:
  - Don't use 1:1s for status updates. That's what standups and project boards are for.
  - Ask open-ended questions: "What's on your mind?" "What's frustrating you?" "What do you need from me?"
  - Take notes. Reference previous 1:1s. Show that you remember and care.
  - Cancel other meetings, not 1:1s. 1:1s are sacred.
- **Pitfall**: Manager dominates the conversation. The 1:1 is for the employee, not the manager.

**7. RFC (Request for Comments) Review (Async + Optional Sync Meeting)**
- **Purpose**: Propose architectural changes, gather feedback, build consensus.
- **Format**: Author writes RFC document (problem, proposal, alternatives, tradeoffs). Team comments asynchronously. Optional sync meeting to resolve open questions.
- **Optimizations**:
  - Set a comment deadline (e.g., 5 business days). After deadline, author addresses feedback and makes a decision.
  - Use a template. Consistency reduces cognitive load.
  - Distinguish between blocking concerns (correctness, security) and non-blocking suggestions (style, minor optimizations).
- **Pitfall**: RFCs that linger for weeks with no decision. Set a decision deadline and stick to it.

#### Async-First Communication Patterns

- **Default to async** — Status updates, announcements, design proposals, and decisions should be written and shared asynchronously. Reserve sync meetings for real-time collaboration.
- **Use threads, not channels** — In Slack or Teams, use threads for discussions. Keeps channels scannable. Main channel is for announcements, threads are for details.
- **Document decisions publicly** — Every significant decision (architectural choice, roadmap change, policy update) gets written down in a shared doc or wiki. Don't let decisions live only in someone's head or in a Slack thread.
- **Record meetings** — For all-hands, demos, or important discussions, record the meeting and share the link. Accommodates different time zones and allows people to catch up asynchronously.
- **Set response time expectations** — Async doesn't mean "respond whenever." Set norms: Slack messages within 4 hours during work hours, emails within 24 hours, RFCs within 5 days.

#### Decision Documentation

- **Use Architecture Decision Records (ADRs)** — Every significant architectural decision gets a lightweight ADR:
  - **Title**: Short description (e.g., "Use Postgres for primary datastore")
  - **Context**: What's the situation?
  - **Decision**: What did we decide?
  - **Consequences**: What are the tradeoffs?
  - **Alternatives Considered**: What else did we evaluate?
- **Maintain a decision log** — Store ADRs in the repo (`docs/adr/`) or wiki. Version control ensures decisions are traceable.
- **Link decisions to code** — In PRs, reference the ADR. Future engineers will thank you.

#### Remote Meeting Facilitation

- **Video on by default** — Encourages engagement. People are less likely to multitask when video is on.
- **Use collaborative tools** — Miro, Figma, Google Docs for real-time collaboration. Screen sharing alone is passive.
- **Timebox discussions** — Use a timer. When time's up, move on. Prevents bikeshedding.
- **Mute when not speaking** — Reduces background noise. Unmute to contribute.
- **Use breakout rooms for large meetings** — If you have >8 people, break into smaller groups for brainstorming. Reconvene to share findings.

### After meetings

- **Publish meeting notes within 2 hours** — Key decisions, action items, owners, deadlines. Share in the team channel or wiki.
- **Track action items to completion** — Review action items in the next meeting. If they're not getting done, either they weren't important or there's a resourcing issue.
- **Measure meeting effectiveness** — Periodically survey the team: "Are meetings productive? Too many? Too few?" Course-correct based on feedback.
- **Cancel recurring meetings that lost their purpose** — If a meeting becomes a status update or no one has updates, cancel it. Don't let zombie meetings linger.

## Self-check before task completion

- [ ] Meeting passes the async-first test (can't be an email or doc)
- [ ] Agenda is created and shared 24 hours in advance with topics, time allocation, and desired outcomes
- [ ] Required vs optional attendees are explicitly identified
- [ ] Meeting type is appropriate for the goal (standup, planning, retro, design review, 1:1)
- [ ] Design reviews and RFC reviews require pre-reading; meeting time is for discussion, not reading
- [ ] Decisions are documented using ADRs or decision logs and shared publicly
- [ ] Meeting notes with action items, owners, and deadlines are published within 2 hours
- [ ] Recurring meetings are reviewed quarterly and canceled if they've lost their purpose

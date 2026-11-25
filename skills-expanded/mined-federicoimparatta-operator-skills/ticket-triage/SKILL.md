---
name: ticket-triage
description: Use this skill when the user asks to triage a backlog of tickets in Linear, Jira, GitHub Issues, Shortcut, or any similar tool, or to decide what a team should do, defer, and decline. Trigger phrases include "triage this backlog", "review my Linear inbox", "what do we pick up next", "clean the backlog", "triage de tickets", "revisar la cola", "decidir qué hacemos". Produces a triage session with a disposition for every ticket, ranked by impact, and a decline message for the ones the team will not do.
---

# ticket-triage

> **Anchor:** A triage session is a decision about what the team will not do.

## When to use

Use this skill when the user needs to process a queue of tickets and decide what happens to each one. Works for:

- A weekly team triage of the incoming queue.
- A backlog grooming pass before planning.
- A fresh owner inheriting a product area with an overgrown backlog.
- An incident tail: the tickets opened during and after a major incident.

Do not use when:

- The user is writing a single bug or feature ticket. That is a ticket-writing task, not triage.
- The user is building a roadmap. Use `roadmap-from-data`.
- The user is running a post-mortem. Use `post-mortem`.

## Voice rules (apply to all outputs)

- No buzzwords: leverage, empower, synergy, resonate, tapestry, delve, elevate, captivate, explore, dynamic, testament.
- No em dashes.
- No filler openings.
- Decision-oriented over descriptive.
- High-context, no overexplaining.
- Standard sentence case for formal outputs.
- ES outputs match the register of the handbook: direct, self-aware, no reverence for process, comfortable naming failure.
- EN outputs use direct US business register. Do not soften bluntness into corporate-speak.
- Language switches based on audience, not author.

## Bilingual handling

- **ES.** Rioplatense register. Vos over tú. Keep standard terms in English: ticket, backlog, triage, bug, feature request, duplicate, assignee, priority, severity, SLA, reporter.
- **EN.** Direct US business register.
- Decline messages keep the register of the tool they will be posted in. A polite product follows its polite tone. A technical Linear thread does not need to apologize.

## Method

### Step 1. Freeze the queue

Pick the window that will be triaged. The queue is everything created or reopened within that window. Anything outside is out of scope for this session.

If the queue is larger than the session can handle, split by area or by creation date. Do not skim.

### Step 2. Classify each ticket

Every ticket gets exactly one classification:

- **Bug.** Something is broken against intended behavior.
- **Feature.** Someone wants new or changed behavior.
- **Noise.** Not actionable: vague complaint, misunderstanding, wrong surface.
- **Duplicate.** The same issue is tracked elsewhere.
- **Already fixed.** Work landed, ticket is stale.
- **Not our problem.** The issue belongs to a different team or a vendor.

Classification is not severity. A classified noise ticket is closed, not deprioritized.

### Step 3. For real tickets, score impact, certainty, and cost

Only bugs and features get scored. Everything else is disposed of.

- **Impact.** How much value a fix creates. Users affected, revenue, retention, support load.
- **Certainty.** How sure the team is about impact. Three levels: confirmed, likely, guess.
- **Cost.** Effort to fix. Three levels: small, medium, large.

A small-cost, confirmed-certainty, high-impact bug skips ahead of a large-cost guess.

### Step 4. Decide the disposition

Every real ticket gets one of:

- **Take now.** Scheduled into the current window.
- **Take next.** Scheduled into the next window.
- **Park.** Not scheduled. Kept open with a clear "what would change this" note.
- **Decline.** Closed as won't-do, with a message to the reporter.
- **Reassign.** Moved to a different team.

Park is not a polite decline. Park is for tickets that may become worth doing if context changes. If context is unlikely to change, close with decline.

### Step 5. Write decline messages that do not burn trust

A decline is a product decision, not an excuse. Good decline messages have:

- **Direct statement.** We are not going to do this.
- **Reason.** One sentence, honest. "It serves too narrow an audience." "The workaround is acceptable." "This is on another team's scope."
- **What could change this.** One sentence. A future condition that might reopen consideration. If there is none, say so.
- **Alternative if any.** A workaround, an existing feature, a different request that would be considered.

Do not write "thanks for your feedback, we will consider it". That is both dishonest and the phrase reporters trust least.

### Step 6. Communicate the session output

A triage session is wasted if the team and reporters do not see the output.

- Team gets the sequenced list by owner.
- Reporters get individualized responses on their tickets, not a group email.
- Stakeholders who track specific asks get a direct note.

### Step 7. Keep the register honest

Tickets that consistently end up in noise or decline are signals. Note the patterns:

- A surface that generates many misclassified tickets suggests a UX problem.
- A reporter whose tickets are mostly declined suggests a relationship that needs a separate conversation.
- A category of request that keeps coming back suggests a strategic miss, not a set of tickets.

These observations belong in the triage output, not in a private note.

## Templates

- `templates/en/triage-session.md`: full triage session output.
- `templates/en/decline-message.md`: decline message template.
- `templates/es/triage-session.md`: output completo de la sesión de triage.
- `templates/es/decline-message.md`: template de mensaje de decline.

## Related skills

- `roadmap-from-data`: move to it when the queue is feeding a planning cycle, not a triage pass.
- `post-mortem`: use it when the tickets are an incident tail that needs a retro, not just dispositions.
- `ux-audit`: use it when a surface keeps generating misclassified tickets and the cause is UX.

## Anti-patterns

This skill must never produce:

- A triage output without a disposition for every ticket.
- A classification that doubles as a severity.
- Decline messages that use "we will consider it".
- A park bucket used as a polite decline.
- A session whose output is not communicated to reporters.
- A classification scheme with more than six categories.
- A ticket marked "won't fix" without a reason the reporter can read.

## Checklist before delivery

- [ ] Window is named and queue is frozen.
- [ ] Every ticket has exactly one classification.
- [ ] Every bug and feature has impact, certainty, cost.
- [ ] Every real ticket has a disposition.
- [ ] Decline messages are written, not templated placeholders.
- [ ] Team-facing and reporter-facing outputs both exist.
- [ ] Pattern observations are included.
- [ ] No buzzwords from the voice rules appear.

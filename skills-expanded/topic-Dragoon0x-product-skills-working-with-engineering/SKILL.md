---
name: working-with-engineering
description: "Partner with engineering as a collaborator, not a ticket-writer. Covers communication norms, technical empathy, scope negotiation, and building mutual trust. Use when PM-engineering relationships feel transactional, technical decisions are made without product input, or scope conversations become adversarial."
---

# Working with Engineering

Partner with engineers as collaborators, not requesters.

## How to use

- `/working-with-engineering` Apply engineering collaboration constraints to this conversation.
- `/working-with-engineering <situation>` Navigate a specific PM-engineering dynamic.

## Constraints

### Communication
- MUST communicate the why behind every requirement. Engineers make better decisions with context.
- MUST speak in terms of user problems and outcomes, not implementation instructions
- SHOULD learn enough technical vocabulary to have productive conversations without faking it
- NEVER tell engineers how to build. Define what and why. They own the how.
- MUST be available for questions during implementation — disappearing after the PRD kills trust

### Scope Negotiation
- MUST involve engineering in scoping before committing to timelines
- SHOULD ask "what's the simplest version that solves the user problem?" before "what's the full version?"
- MUST treat estimates as ranges, not commitments. Push for "1-3 weeks" not "exactly 10 days."
- NEVER negotiate against engineering estimates publicly — discuss concerns 1:1
- SHOULD be willing to cut scope to protect quality and team health

### Technical Empathy
- MUST respect tech debt as real work that prevents future problems
- SHOULD understand infrastructure and platform constraints that affect product decisions
- MUST factor engineering maintenance burden into feature prioritization
- NEVER treat "it works" as sufficient — performance, reliability, and maintainability matter
- SHOULD attend design reviews and architecture discussions to stay informed

### Trust Building
- MUST follow through on commitments. If you say you'll get an answer, get it.
- SHOULD protect engineering time from unnecessary meetings and context switches
- MUST advocate for engineering priorities (debt, tooling, performance) in roadmap discussions
- SHOULD celebrate engineering wins publicly, not just product launches
- NEVER throw engineering under the bus when something ships late or buggy

### Anti-Patterns
- The Ticket Machine: writing JIRA tickets and waiting for output without collaboration
- The Solution PM: specifying implementation details instead of defining problems
- The Scopecreep: adding "one more thing" after engineering has already committed
- The Meeting Hog: filling engineering calendars with syncs that could be Slack messages
- Ignoring Tech Debt: always prioritizing features and wondering why velocity drops

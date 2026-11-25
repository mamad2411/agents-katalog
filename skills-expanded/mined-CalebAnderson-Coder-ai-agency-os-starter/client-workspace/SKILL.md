---
name: client-workspace
description: Create and maintain an isolated workspace per client, with a client CLAUDE.md holding brand voice, rules, banned claims, contacts, access map, and logs. Use when adding a client, switching clients, or when Claude must "act as" a specific client.
---

# Client Workspace

Every client lives in its own folder so voice, rules and context never leak between clients.

## Layout
```
clients/
  _template/                 copy this for each new client
  <client-slug>/
    CLAUDE.md                client rules (loaded when you work inside this folder)
    brand/voice.md           tone, vocabulary, 3-5 approved writing samples
    brand/claims.md          approved claims + sources; banned claims
    BRIEF.md                 goals, KPIs, scope (from client-onboarding)
    SCOPE.md                 contracted deliverables (from proposal-sow)
    LOG.md                   dated log of work + decisions
    CHANGES.md               change requests (from scope-guard)
    reports/  drafts/  meetings/  assets/
```
## Client CLAUDE.md template
```markdown
# Client: [Client Name]  (slug: [slug])
- Industry / ICP:
- Voice: (3 adjectives) — see brand/voice.md. Never: (words/phrases)
- Approved claims only from brand/claims.md. No invented stats or testimonials.
- Contacts: decision-maker [role], day-to-day [role] (names live in your CRM, not here)
- Access: where each credential lives (password manager entry names). NEVER store secrets here.
- Approval rules: what needs client sign-off (copy, spend, deploy, publishing)
- Reporting: cadence, KPIs, data sources (GA4 property, Search Console site, ad accounts as env var names)
- Out of scope: see SCOPE.md
```
## Rules
1. Start every client task with `cd clients/<slug>` (or open Claude Code there) so the client CLAUDE.md loads on top of the agency CLAUDE.md.
2. Never reuse one client's copy, data or assets for another. When asked to "reuse", genericize first.
3. Append a line to LOG.md after each work session: date, what, decisions, next step.
4. `/client-switch <slug>`: summarize the client's CLAUDE.md, last 5 LOG entries and open CHANGES before doing anything.

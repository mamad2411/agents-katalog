---
name: pith-arch
description: >
  One-shot architecture decision format. Use for technology choices, design decisions, system design questions.
  Format: Decision / Options table / Choice / Risks / Next. Does not persist.
---

Architecture decision format. Structured. No narrative.

**Decision:** [what is being decided — one line]

| Option | Pro | Con | Complexity |
|--------|-----|-----|------------|
| A      | ... | ... | low/med/high |
| B      | ... | ... | low/med/high |
| C      | ... | ... | low/med/high |

**Choice:** [option name] — [single sentence reason]

**Risks:**
- [risk]
- [risk]

**Next:** [immediate first action]

## Rules

- Table rows: 2–5 options. If more, group similar ones.
- Pro/Con: one phrase each. Not full sentences.
- Choice: lead with option name. One sentence reason. No hedging.
- Risks: 2–4 real blockers. Not generic "might take longer."
- Next: one concrete action, not a plan.
- If exploratory question (no decision needed): show table only, omit Choice/Risks/Next.

## Example

**Decision:** session storage strategy for auth

| Option     | Pro                         | Con                       | Complexity |
|------------|-----------------------------|---------------------------|------------|
| JWT        | stateless, no DB reads      | can't revoke, large cookie | low       |
| Redis      | revocable, small cookie     | infra dependency          | medium     |
| DB session | simple, no new infra        | DB read every request     | low        |

**Choice:** Redis — revocability is required (security team req), team already operates Redis for cache

**Risks:**
- Redis downtime = full auth outage (add fallback or circuit breaker)
- Session data size can grow if not careful — set explicit TTLs

**Next:** Add `ioredis` to package.json, write `src/lib/session.ts`

One-shot. Does not persist.

---
name: client-intake
description: Use when starting work on a new client site, business website, or rank-and-rent project; when asked to write customer-facing copy and no FACTS.md exists in the project root; or when the user corrects a business fact (pricing, experience, services, stats) mid-session.
---

# Client Intake → FACTS.md

## Overview

Every business project gets a `FACTS.md` in its project root — the single source of truth for every factual claim in customer-facing copy. **No customer-facing copy is written until FACTS.md exists.** Copy that contains a fact not in FACTS.md is a bug.

## When to Use

- New client/site/rank-and-rent project kickoff → run the intake, create FACTS.md
- Asked for copy and no FACTS.md exists → stop, run intake first
- User corrects any business fact mid-session → update FACTS.md immediately, before continuing
- Dispatching a sub-agent that writes copy → paste FACTS.md contents into its prompt

## The Iron Rules

1. **No FACTS.md, no copy.** If the user is in a hurry, the intake takes 2 minutes — do it anyway. Placeholder copy marked `[FACT NEEDED: x]` is acceptable; invented facts are not.
2. **Exact numbers, never rounded or inflated.** "26 enquiries" is not "28". "25+ years" is not "20 years". If unverified, leave it out.
3. **The Discontinued list is a blocklist.** Anything on it must never appear in copy, even if old pages mention it.
4. **Corrections propagate.** When the user corrects a fact: (a) update FACTS.md in the same turn, (b) grep existing pages for the stale fact and fix them, (c) include the corrected FACTS.md in every subsequent sub-agent prompt. Sub-agents cannot see the conversation.
5. **Copy speaks as the owner** (first person, warm, direct, conservative — no hype), unless FACTS.md says otherwise.

## Intake Interview

Ask only for what's missing — check the user's messages, existing site, and project AGENTS.md first. Ask in one batch, not one-by-one:

1. Business/trading name, phone, email, address (exact NAP format)
2. Domain + repo path + deploy target
3. Registrations/accreditations with numbers (Gas Safe, NICEIC, etc.)
4. Years of experience (exact)
5. Services offered — and explicitly NOT offered
6. Current pricing; anything discontinued
7. Service area towns
8. Verified stats usable in copy (exact numbers only)
9. Sibling sites (for duplicate-content checks) and SOURCE design site if cloning
10. Voice notes (first person as whom? tone constraints?)

## FACTS.md Template

```markdown
# FACTS.md — [Business name]
Last verified: [date]

## Identity
- Trading name:
- Phone / Email / Address (NAP, exact):
- Domain / Repo / Deploy:

## Credentials
- Registrations (with numbers):
- Years of experience (exact):

## Offering
- Services offered:
- Services NOT offered:
- Pricing (current):
- DISCONTINUED — never mention:

## Reach
- Service area towns:
- Sibling sites:
- SOURCE design site:

## Copy rules
- Voice:
- Verified stats (exact numbers):
- Claims to avoid:
```

## Common Mistakes

| Mistake | Fix |
|---|---|
| "It's obvious, I'll just write plausible copy" | Plausible = fabricated. `[FACT NEEDED]` placeholder instead. |
| Rounding numbers to sound better | Exact or absent. Customers with a keen eye notice. |
| Fixing a fact in chat but not in FACTS.md | The next session/sub-agent reintroduces the stale fact. Update the file first. |
| Copying facts from a sibling site | Siblings share design, never facts or copy. |
| Sub-agent prompt without FACTS.md contents | Sub-agents fabricate. Paste the file in. |

---
name: knock-product-messaging-strategy
description: Design a cross-channel product messaging system that drives activation, engagement, and retention while controlling fatigue. Use when planning lifecycle messaging, auditing notification strategy, prioritizing workflows, or turning product moments into Knock workflows, guides, preferences, and measurement.
---

# Product messaging strategy skill

Turn a product into a coordinated messaging system — not a pile of one-off notifications. This skill operationalizes [The product leader's guide to effective messaging](https://knock.app/manuals/product-leaders-guide-to-effective-notifications/the-product-leaders-guide-to-effective-notifications) into agent steps that produce Knock-ready plans and resources.

Complementary manuals:

- [In-app messaging best practices](https://knock.app/manuals/in-app-messaging/best-practices-for-in-app-messaging)
- [Transactional email](https://knock.app/manuals/transactional-email)
- [Notification infrastructure](https://knock.app/manuals/notification-infrastructure)

## Output contract (hard)

Write the full plan to **`knock-plan.md`** (repo root). Keep chat **minimal** — status + confirmation only. Follow `rules/knock-plan-file.md`.

Do **not** paste full recommendation briefs, taxonomies, or checklists into chat. Rely on the plan file as the source of truth for context and for handoff to `knock-setup`.

## Overview

Work through these rule files in order when designing or auditing a messaging system. Put detailed findings in `knock-plan.md` as you go; do not narrate them in chat.

1. **Data foundation and triggers** — meaningful product moments and event payloads
2. **Recipients and ownership** — who should get the message and why
3. **Delivery strategy** — channels, escalation, timing, stop conditions
4. **Volume and batching** — frequency controls and digests
5. **Relevance and preferences** — personalization and preference taxonomy
6. **Measurement and review** — outcomes, fatigue signals, launch checklist
7. **Apply in Knock** — map the plan to workflows, guides, audiences, and preferences

## How to use this skill

### Designing a messaging system for a product

1. Learn the product (codebase, events, roles, lifecycle). Ask at most 3 clarifying questions if needed.
2. Follow `rules/data-foundation-and-triggers.md` to list meaningful moments and required event data — write them into `knock-plan.md`.
3. For each high-value moment, complete recipient, delivery, volume, and preference decisions using the next rule files — update the plan file, not chat.
4. Prioritize by growth outcome: activation, retention, revenue recovery, then nice-to-have alerts.
5. Run every candidate through `rules/measurement-and-review.md` before marking build-ready in the plan.
6. Use `rules/apply-in-knock.md` to enrich Knock shapes in the plan (or create resources only if the user explicitly asks). Prefer Knock MCP / CLI when connected.
7. In chat: one status line pointing at `knock-plan.md`, then ask which items to build. Confirmation question last, bolded.

### Auditing an existing notification program

1. Inventory current workflows, guides, channels, and preference categories into `knock-plan.md` (Audit section).
2. Score each against the review checklist in `rules/measurement-and-review.md`.
3. Flag missing stop conditions, broad recipient rules, channel spam, and preference gaps in the file.
4. Chat: one status line + ask which Fix/Merge/Kill items to act on next.

### Handing off into setup or implementation

- For greenfield Knock setup after strategy is approved, continue with `knock-setup`.
- For copy and channel formatting, use `knock-notification-best-practices`.
- For in-app guides UI, use `knock-in-app-ui`.
- For local resource management, use `knock-cli`.

When handing off to `knock-setup`, update **Setup handoff** in `knock-plan.md` and pass the same lists in chat (no re-ranking unless the user asks):

```markdown
### Setup handoff
- **plan.** knock-plan.md
- **confirmed.** [names or indexes]
- **skipped.** [names or indexes]
- **deferred / blocked.** [names + reason]
```

`knock-setup` must treat `confirmed` as authoritative, read detail from `knock-plan.md`, and skip rediscovery.

## Rule files reference

- `rules/knock-plan-file.md` — plan file path, structure, and chat brevity rules
- `rules/data-foundation-and-triggers.md` — events, payloads, and moment types
- `rules/recipients-and-ownership.md` — recipient selection and escalation
- `rules/delivery-strategy.md` — channel progression and timing
- `rules/volume-and-batching.md` — frequency, cooldowns, digests
- `rules/relevance-and-preferences.md` — context, personalization, prefs
- `rules/measurement-and-review.md` — outcomes, fatigue, launch standard
- `rules/apply-in-knock.md` — map decisions onto Knock primitives

## Quick reference

### Four moment types

1. **User-requested outcomes** — export done, payment submitted (usually immediate)
2. **Collaborative activity** — mention, assignment, approval (immediate or batched)
3. **Product or account state changes** — integration down, usage limit, payment failed
4. **Time-based conditions** — trial ending, incomplete onboarding, overdue approval

### Non-negotiables before building

- Trigger represents a meaningful state change, not a vague inactivity heuristic alone
- Recipient is the person responsible for the next action
- Primary channel + escalation path defined
- Stop / cancel condition defined and re-checked after delays
- Preference category assigned (or explicitly marked transactional/service-critical)
- Success metric is a product outcome, not only an open rate

### Growth priority order

1. Activation / time-to-value
2. Core loop engagement (collaboration, habit)
3. Revenue protection (failed payment, trial, limits)
4. Re-engagement / win-back with precise state
5. Announcements and education (lowest interrupt)

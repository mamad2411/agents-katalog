---
name: business-model-validator
description: Use when a prospect, new customer, or existing operator wants to know whether Zooza fits their business, or which Zooza features map to how they operate. No Zooza account required — works as a pure knowledge interview.
---

# Business Model Validator

> **No Zooza account required.** Pure knowledge interview. Works for:
> - Prospects — "Does Zooza fit our studio?"
> - New customers — "We just signed up, where do we start?"
> - Existing operators — "Are we using Zooza the right way?"

## When to use

- "Does Zooza fit us / our school / our studio?"
- "We're thinking about Zooza — what can it do?"
- "We run [type of business] — can Zooza handle this?"
- "We just signed up, how do we set this up?"
- "Are we using Zooza correctly?"

## Interview flow

Run **one question per message**. Match the user's language (Slovak, Czech, English, Hungarian, Romanian, German).

### Phase 1 — What do you do?

1. "What kind of activities do you run — group classes, individual lessons, camps, one-off events, or a mix?"
2. "Who are your clients? Adults, children (with parents paying), corporate groups, or a mix?"
3. "Do you operate from one location or multiple? One brand, or franchise/licensed locations?"

### Phase 2 — How do you sell?

4. "How do clients typically pay — per session, per term, monthly subscription, punch card, drop-in?"
5. **If children's group activities:** "Do parents pay once per term (lump sum), or monthly?" — this determines which Zooza model to use.
6. "Do you sell anything alongside classes — products, vouchers, gift cards, equipment?"

### Phase 3 — Edge cases (only when relevant signals appear)

- "Do you offer free trial or intro sessions that convert to paid enrolment?"
- "Can clients attend a session from a different group if they miss their own?"
- "Is any part of your offering online or hybrid?" — if yes, treat as delivery layer on top of another model.
- "Do your locations operate independently with their own clients and revenue?"

---

## Phase 4 — Match and output

Map answers to the capability map below. Output one of three verdicts:

**✅ Full fit:**
> "Zooza is built for this. Here's how it maps:
> - [User's thing] → [Zooza mechanism]
> - ...
> Want me to walk you through setting up your first class?"

**🟡 Partial fit:**
> "Zooza handles most of this well. One area to be aware of:
> - [Limitation + honest workaround]
> Overall still a strong fit. Shall I show you the setup path?"

**❌ Poor fit:**
> "Zooza might not be the right tool for [specific aspect]. Here's why:
> - [Specific gap, not generic]
> It would work for [what fits], but [what doesn't] would need [workaround / external tool]."

**Output rules:** Name the user's specific business type. List 3+ concrete mappings. For partial/poor: name the exact gap.

---

## Phase 5 — Next step

After verdict, offer one concrete next step:
- Ready to set up → "Want me to help you create your first class?" (use the `class-management` skill)
- Wants docs → return matching URLs from the guide table below
- Poor fit → "If [fitting subset] is the main use case, Zooza still makes sense for that part — want to explore?"

---

## Capability map

### Activity types

| What they run | Zooza mechanism |
|---|---|
| Recurring group classes (weekly/biweekly/monthly) | Programme → Class → Sessions with recurrence blocks |
| Open/drop-in classes (no fixed cohort) | Open class type + punch cards (permanentka) — must use pay-as-you-go, not block |
| Fixed-term courses (semester, block, camp) | Programme + billing period + count-mode sessions |
| Single events & workshops | One-off session or event-type programme |
| Camps (day, week, holiday) | Programme with date range + capacity — all-or-nothing booking, no individual days, no make-ups |
| 1-to-1 / individual lessons | Programme with `target_audience=individual` — each client = own private Class |
| Online & hybrid classes | Delivery modifier (not standalone) — add to any base model via online flag + meeting link |
| Trial classes → auto-convert to paid | Trial class type + auto-enrolment rule |

### Pricing & selling

| What they do | Zooza mechanism |
|---|---|
| Fixed price per class/term | Standard price on Programme |
| Monthly subscription | Billing period + auto-renewal |
| Punch card / package | Open class + punch card product |
| Pay-as-you-go / drop-in | Open class, pay per session |
| Vouchers & gift cards | Digital product type |
| Upsell products with classes | Service/product catalogue + class attachment |
| Tiered pricing (early bird, member) | Payment schedule templates |

### Client & enrolment

| What they need | Zooza mechanism |
|---|---|
| Direct client self-registration (B2C) | Online registration, public class page |
| Corporate clients / B2B | Corporate client account type |
| Child activities (parent pays, child attends) | Parent account + child profile |
| Make-up sessions for missed classes | Náhradky — credit system |
| Waitlists | Capacity limit + waitlist enabled |

### Multi-location & franchise

| Structure | Zooza mechanism |
|---|---|
| Single location | Single company account |
| Multiple venues, one brand | One company, multiple places |
| Franchise / chain (each location independent) | Network — each franchise = separate company; HQ consolidates reporting |
| Revenue tracking per location | Network reporting |

---

## Business model guides

| Business type | URL |
|---|---|
| Adult language school | https://help.zooza.online/programmes/adult-language-school/ |
| Children's group — block/term | https://help.zooza.online/programmes/childrens-group-activities-block-term/ |
| Children's group — monthly subscription | https://help.zooza.online/programmes/childrens-group-activities-monthly-subscription/ |
| Camps | https://help.zooza.online/programmes/camps/ |
| Individual lessons (1-to-1) | https://help.zooza.online/programmes/individual-lessons/ |
| Online and hybrid classes | https://help.zooza.online/programmes/online-hybrid/ |
| Open classes / drop-in | https://help.zooza.online/programmes/open-classes-drop-in/ |
| Franchise / network | https://help.zooza.online/settings/franchise-network/ |

---

## Known gaps — flag proactively

- **Global timezone management:** Zooza is for local/regional operators — no multi-timezone scheduling.
- **Async / on-demand LMS content:** Zooza handles live sessions, not video module delivery.
- **Complex membership access control:** Billing periods and price tiers exist, but not a full access-control engine.
- **Teacher marketplace with revenue splits:** Not natively supported.
- **Camps with individual day booking:** All-or-nothing. Workaround: multiple short-block programmes.
- **Monthly subscription auto-pause for holidays:** Not supported — requires cancel + re-enrol.
- **Corporate language school per-employee invoicing:** Use one Programme per course level, not one per corporate client.
